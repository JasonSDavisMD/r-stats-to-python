"""Search: rank catalog entries against a free-text task or R function name.

Plain lexical ranking, no external services or AI, so it works offline and
gives the same answer every time:

1. Text is split into tokens. Code names are split too, so
   ``make_smoothing_spline`` also matches "smoothing" and "spline".
2. Each query token scores against the *best* field it hits in an entry.
   Fields have weights: an exact R name or alias counts more than a word
   buried in a caveat.
3. Tokens are weighted by rarity (inverse document frequency), so a
   distinctive word like "plogis" outweighs a common one like "regression".
4. Whole-phrase matches (e.g. "inverse logit" inside an alias) get a bonus.
   This separates near neighbours such as ``expit`` and ``logit``.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass

from .catalog import KINDS, Catalog, Entry

STOPWORDS = {
    "a", "an", "the", "for", "with", "of", "to", "in", "on", "and", "or", "by",
    "from", "how", "do", "i", "r", "python", "use", "using", "what", "is",
    "my", "me", "get", "into", "at", "as", "it", "this", "that", "via",
}

# Field -> weight. Higher means a hit in that field is stronger evidence.
FIELD_WEIGHTS = {
    "id": 3.0,
    "r": 4.0,
    "aliases": 3.0,
    "title": 2.0,
    "call": 2.0,
    "import": 1.5,
    "kind": 1.2,
    "library": 1.0,
    "topic": 1.0,
    "io": 0.5,
    "caveats": 0.3,
}

# Extra words that make the kind searchable ("estimate" finds kind=fit).
KIND_WORDS = {
    "fit": "fit fitting estimate estimation train learn mle",
    "evaluate": "evaluate evaluation predict prediction known given compute apply",
    "optimize": "optimize optimization minimize maximize numerical root",
    "solve": "solve symbolic exact equation inequality algebra",
    "compute": "compute transform summarize reshape",
    "visualize": "plot visualize draw graph figure",
}


def _stem(token: str) -> str:
    if len(token) > 4 and token.endswith("ies"):
        return token[:-3] + "y"
    if len(token) > 3 and token.endswith("s") and not token.endswith("ss"):
        return token[:-1]
    return token


def tokenize(text: str) -> list[str]:
    """Lowercase, split on anything non-alphanumeric, drop stopwords, stem."""
    raw = re.split(r"[^a-z0-9]+", text.lower())
    return [_stem(t) for t in raw if t and t not in STOPWORDS]


_IDENTIFIER = re.compile(r"[A-Za-z_.][\w.]*")


def _r_base(name: str) -> str:
    """'MASS::lda' -> 'lda', 'glm(family = binomial)' -> 'glm'."""
    match = re.match(r"^\s*(?:\w+::)?([A-Za-z_.][\w.]*)", name)
    return match.group(1).lower() if match else name.lower()


def _phrase(text: str) -> str:
    return " ".join(tokenize(text))


@dataclass(frozen=True)
class Hit:
    entry: Entry
    score: float


class Index:
    """Pre-tokenized view of a catalog; build once, query many times."""

    def __init__(self, catalog: Catalog):
        self.catalog = catalog
        self._fields: list[dict[str, set[str]]] = []
        self._phrases: list[list[str]] = []
        self._r_names: list[set[str]] = []
        document_frequency: dict[str, int] = {}

        for entry in catalog.entries:
            fields = {
                "id": set(tokenize(entry.id)),
                "r": set(tokenize(" ".join(entry.r))),
                "aliases": set(tokenize(" ".join(entry.aliases))),
                "title": set(tokenize(entry.title)),
                "call": set(tokenize(entry.call)),
                "import": set(tokenize(entry.import_line)),
                "kind": set(tokenize(KIND_WORDS.get(entry.kind, entry.kind))),
                "library": set(tokenize(entry.library)),
                "topic": set(tokenize(entry.topic)),
                "io": set(tokenize(entry.inputs + " " + entry.returns)),
                "caveats": set(tokenize(" ".join(entry.caveats))),
            }
            self._fields.append(fields)
            self._phrases.append(
                [_phrase(p) for p in (entry.title, *entry.aliases, *entry.r)]
            )
            for token in set().union(*fields.values()):
                document_frequency[token] = document_frequency.get(token, 0) + 1

        count = max(len(catalog.entries), 1)
        self._idf = {
            token: math.log(1 + count / df) for token, df in document_frequency.items()
        }
        self._default_idf = math.log(1 + count)
        self._r_names = [{_r_base(name) for name in e.r} for e in catalog.entries]

    def _token_score(self, token: str, fields: dict[str, set[str]]) -> float:
        best = 0.0
        for name, tokens in fields.items():
            weight = FIELD_WEIGHTS[name]
            if token in tokens:
                best = max(best, weight)
            elif len(token) >= 4 and any(
                len(t) >= 3 and (t.startswith(token) or token.startswith(t))
                for t in tokens
            ):
                best = max(best, 0.5 * weight)  # prefix match: "valid" ~ "validation"
        return best * self._idf.get(token, self._default_idf)

    def search(self, query: str, limit: int = 5, kind: str | None = None) -> list[Hit]:
        tokens = tokenize(query)
        if not tokens:
            return []
        query_phrase = " ".join(tokens)
        raw_words = {w.lower() for w in _IDENTIFIER.findall(query)}
        hits: list[Hit] = []

        for position, entry in enumerate(self.catalog.entries):
            if kind and entry.kind != kind:
                continue
            fields = self._fields[position]
            per_token = [self._token_score(t, fields) for t in tokens]
            matched = sum(1 for s in per_token if s > 0)
            if matched == 0:
                continue
            score = sum(per_token) * (matched / len(tokens))  # reward coverage
            for phrase in self._phrases[position]:
                if not phrase:
                    continue
                if phrase == query_phrase:
                    score += 12.0
                elif len(phrase.split()) > 1 and f" {phrase} " in f" {query_phrase} ":
                    score += 4.0 * len(phrase.split())
                elif len(tokens) > 1 and f" {query_phrase} " in f" {phrase} ":
                    score += 4.0
            if raw_words & self._r_names[position]:
                score += 10.0  # exact R function name, e.g. "plogis"
            hits.append(Hit(entry, score))

        hits.sort(key=lambda h: (-h.score, h.entry.id))
        if hits:
            floor = 0.25 * hits[0].score  # hide weak tail matches
            hits = [h for h in hits if h.score >= floor]
        return hits[:limit]


def find(query: str, limit: int = 5, kind: str | None = None, catalog: Catalog | None = None):
    """Convenience for notebooks: ``find("inverse logit")`` -> list of Hit."""
    from .catalog import load_catalog

    if kind is not None and kind not in KINDS:
        raise ValueError(f"kind must be one of {sorted(KINDS)}")
    return Index(catalog or load_catalog()).search(query, limit=limit, kind=kind)
