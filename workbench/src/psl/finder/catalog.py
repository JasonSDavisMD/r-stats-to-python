"""Catalog loader: reads ``catalog/*.toml`` into validated ``Entry`` objects.

Each TOML file is one course topic and holds ``[[entry]]`` tables. Loading
is fault-isolated: a file that fails to parse, or an entry that fails
validation, is skipped and reported in ``Catalog.problems``. The remaining
topics still load, so one bad edit cannot take down search.
"""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

# The operation kinds the workbench teaches. See docs/operation-kinds.md.
KINDS = {
    "fit": "estimate unknown parameters from observed data (X, y)",
    "evaluate": "apply a known function or already-known parameters to inputs",
    "optimize": "search numerically for a minimizer or root",
    "solve": "solve symbolically for an unknown symbol, boundary or region",
    "compute": "reshape, summarize or transform data; no model involved",
    "visualize": "draw a picture of data or of an already-computed result",
}

REQUIRED = ("id", "title", "kind", "library", "import", "call", "example", "docs")
LISTS = ("aliases", "r", "caveats", "see_also")
OPTIONAL_TEXT = ("inputs", "returns", "recipe")


@dataclass(frozen=True)
class Entry:
    """One task-to-function mapping. Field meanings: docs/adding-a-topic.md."""

    id: str
    topic: str
    title: str
    kind: str
    library: str
    import_line: str
    call: str
    example: str
    docs: str
    aliases: tuple[str, ...] = ()
    r: tuple[str, ...] = ()
    caveats: tuple[str, ...] = ()
    see_also: tuple[str, ...] = ()
    inputs: str = ""
    returns: str = ""
    recipe: str = ""


@dataclass
class Catalog:
    """All entries that loaded cleanly, plus human-readable load problems."""

    entries: list[Entry] = field(default_factory=list)
    problems: list[str] = field(default_factory=list)
    directory: Path | None = None

    def get(self, entry_id: str) -> Entry | None:
        for entry in self.entries:
            if entry.id == entry_id:
                return entry
        return None


def default_catalog_dir() -> Path:
    """Locate ``catalog/``: $PSL_CATALOG_DIR, else walk up to the workbench root."""
    override = os.environ.get("PSL_CATALOG_DIR")
    if override:
        return Path(override)
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "catalog"
        if candidate.is_dir() and (parent / "pyproject.toml").is_file():
            return candidate
    raise FileNotFoundError(
        "Could not find the workbench 'catalog/' folder. Install the project "
        "editable (`uv sync`) or set PSL_CATALOG_DIR."
    )


def workbench_root() -> Path:
    """The folder containing pyproject.toml and catalog/."""
    return default_catalog_dir().parent


def _entry_from_table(table: dict, topic: str) -> Entry:
    missing = [key for key in REQUIRED if not str(table.get(key, "")).strip()]
    if missing:
        raise ValueError(f"missing required field(s): {', '.join(missing)}")
    if table["kind"] not in KINDS:
        raise ValueError(f"kind '{table['kind']}' is not one of {sorted(KINDS)}")
    if not str(table["docs"]).startswith("https://"):
        raise ValueError("docs must be an https:// URL")
    for key in LISTS:
        value = table.get(key, [])
        if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
            raise ValueError(f"'{key}' must be a list of strings")
    return Entry(
        id=table["id"],
        topic=topic,
        title=table["title"],
        kind=table["kind"],
        library=table["library"],
        import_line=table["import"].strip(),
        call=table["call"].strip(),
        example=table["example"].strip("\n"),
        docs=table["docs"],
        aliases=tuple(table.get("aliases", [])),
        r=tuple(table.get("r", [])),
        caveats=tuple(table.get("caveats", [])),
        see_also=tuple(table.get("see_also", [])),
        **{key: str(table.get(key, "")).strip() for key in OPTIONAL_TEXT},
    )


def load_catalog(directory: Path | str | None = None) -> Catalog:
    """Load every ``*.toml`` topic file; never raises for bad content."""
    directory = Path(directory) if directory else default_catalog_dir()
    catalog = Catalog(directory=directory)
    seen: set[str] = set()

    for path in sorted(directory.glob("*.toml")):
        topic = path.stem
        try:
            with path.open("rb") as handle:
                tables = tomllib.load(handle).get("entry", [])
        except (tomllib.TOMLDecodeError, OSError) as error:
            catalog.problems.append(f"{path.name}: skipped file ({error})")
            continue

        for position, table in enumerate(tables, start=1):
            label = f"{path.name} entry #{position} ({table.get('id', '?')})"
            try:
                entry = _entry_from_table(table, topic)
            except (ValueError, KeyError, TypeError) as error:
                catalog.problems.append(f"{label}: skipped ({error})")
                continue
            if entry.id in seen:
                catalog.problems.append(f"{label}: skipped (duplicate id)")
                continue
            seen.add(entry.id)
            catalog.entries.append(entry)

    return catalog
