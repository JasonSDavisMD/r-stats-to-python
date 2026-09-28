"""Command-line front end for the catalog: ``stats find | show | r | list | kinds``.

Run from any terminal with the project environment active, from the
"stats: find" VS Code task, or as ``python -m statsbench ...``. Output is plain
ASCII so it renders in Windows PowerShell and cmd.exe.
"""

from __future__ import annotations

import argparse
import difflib
import sys
import textwrap

from .catalog import KINDS, Catalog, Entry, load_catalog
from .search import Index

WIDTH = 88


def _wrap(text: str, indent: str = "   ") -> str:
    return textwrap.fill(text, WIDTH, initial_indent=indent, subsequent_indent=indent)


def _brief(rank: int, entry: Entry) -> str:
    lines = [
        f"{rank}. {entry.id}  [{entry.library} | {entry.kind}]  {entry.title}",
        textwrap.indent(entry.import_line, "   "),
        f"   {entry.call}",
    ]
    extras = []
    if entry.extra:
        extras.append(f"needs add-on: {entry.extra}")
    if entry.r:
        extras.append("R: " + ", ".join(entry.r))
    if entry.recipe:
        extras.append("recipe: " + entry.recipe)
    if extras:
        lines.append("   " + "   ".join(extras))
    lines.append(f"   docs: {entry.docs}")
    return "\n".join(lines)


def _full(entry: Entry) -> str:
    rule = "-" * WIDTH
    parts = [
        rule,
        f"{entry.id}  [{entry.library} | {entry.kind}: {KINDS[entry.kind]}]",
        entry.title,
        rule,
        "IMPORT   " + entry.import_line.replace("\n", "\n         "),
        "CALL     " + entry.call,
    ]
    if entry.inputs:
        parts.append("INPUTS   " + entry.inputs)
    if entry.returns:
        parts.append("RETURNS  " + entry.returns)
    if entry.r:
        parts.append("R        " + ", ".join(entry.r))
    if entry.aliases:
        parts.append("ALSO     " + ", ".join(entry.aliases))
    parts += ["", "EXAMPLE (copy into a cell; runs on its own):", textwrap.indent(entry.example, "    ")]
    if entry.caveats:
        parts.append("")
        parts.append("CAVEATS")
        parts += [_wrap("- " + c, "  ") for c in entry.caveats]
    if entry.see_also:
        parts.append("")
        parts.append("SEE ALSO " + ", ".join(entry.see_also) + "   (stats show <id>)")
    if entry.recipe:
        parts.append("RECIPE   " + entry.recipe)
    if entry.extra:
        missing = entry.missing_modules()
        state = "NOT installed here" if missing else "installed"
        parts.append(
            f"ADD-ON   {entry.extra} ({state}): uv sync --extra {entry.extra}"
            f"   or   pip install \"statsbench[{entry.extra}]\""
        )
    parts.append("DOCS     " + entry.docs)
    return "\n".join(parts)


def _report_problems(catalog: Catalog) -> None:
    for problem in catalog.problems:
        print(f"warning: {problem}", file=sys.stderr)


def cmd_find(catalog: Catalog, args: argparse.Namespace) -> int:
    query = " ".join(args.query)
    hits = Index(catalog).search(query, limit=args.limit, kind=args.kind)
    if not hits:
        print(f'No match for "{query}". Try fewer words, an R name, or `stats list`.')
        return 1
    print("\n\n".join(_brief(i, h.entry) for i, h in enumerate(hits, start=1)))
    print(f"\nDetails and runnable example: stats show {hits[0].entry.id}")
    return 0


def cmd_show(catalog: Catalog, args: argparse.Namespace) -> int:
    entry = catalog.get(args.id)
    if entry is None:
        ids = [e.id for e in catalog.entries]
        close = difflib.get_close_matches(args.id, ids, n=3)
        hint = f" Did you mean: {', '.join(close)}?" if close else " Try `stats find`."
        print(f"No entry with id '{args.id}'.{hint}")
        return 1
    print(entry.example if args.code else _full(entry))
    return 0


def cmd_r(catalog: Catalog, args: argparse.Namespace) -> int:
    rows = [(r_name, e) for e in catalog.entries for r_name in e.r]
    if args.name:
        wanted = args.name.lower()
        rows = [(n, e) for n, e in rows if wanted in n.lower()]
        if not rows:
            print(f"No R mapping for '{args.name}'. Try `stats find {args.name}`.")
            return 1
    rows.sort(key=lambda row: row[0].lower())
    width = min(max(len(n) for n, _ in rows), 34)
    for r_name, entry in rows:
        print(f"{r_name:<{width}}  ->  {entry.call:<44}  ({entry.id})")
    return 0


def cmd_list(catalog: Catalog, args: argparse.Namespace) -> int:
    current_topic = None
    for entry in sorted(catalog.entries, key=lambda e: (e.topic, e.id)):
        if args.topic and entry.topic != args.topic:
            continue
        if args.kind and entry.kind != args.kind:
            continue
        if entry.topic != current_topic:
            current_topic = entry.topic
            print(f"\n[{current_topic}]")
        print(f"  {entry.id:<30} {entry.kind:<9} {entry.title}")
    return 0


def cmd_kinds(catalog: Catalog, args: argparse.Namespace) -> int:
    for kind, meaning in KINDS.items():
        count = sum(1 for e in catalog.entries if e.kind == kind)
        print(f"{kind:<9} {meaning}  ({count} entries)")
    print("\nFilter any search: stats find \"logistic\" --kind evaluate")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="stats",
        description="Find the right Python library call for a statistics task.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("find", help='search tasks, e.g. stats find "inverse logit"')
    p.add_argument("query", nargs="+")
    p.add_argument("-n", "--limit", type=int, default=5)
    p.add_argument("-k", "--kind", choices=sorted(KINDS))
    p.set_defaults(handler=cmd_find)

    p = sub.add_parser("show", help="full entry with runnable example")
    p.add_argument("id")
    p.add_argument("--code", action="store_true", help="print only the example code")
    p.set_defaults(handler=cmd_show)

    p = sub.add_parser("r", help="R -> Python lookup; no name lists everything")
    p.add_argument("name", nargs="?")
    p.set_defaults(handler=cmd_r)

    p = sub.add_parser("list", help="list entries by topic")
    p.add_argument("-t", "--topic")
    p.add_argument("-k", "--kind", choices=sorted(KINDS))
    p.set_defaults(handler=cmd_list)

    p = sub.add_parser("kinds", help="explain fit / evaluate / optimize / solve ...")
    p.set_defaults(handler=cmd_kinds)
    return parser


def main(argv: list[str] | None = None) -> int:
    # Never crash on a console that cannot encode a character (Windows cp1252).
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")
    args = build_parser().parse_args(argv)
    catalog = load_catalog()
    _report_problems(catalog)
    return args.handler(catalog, args)


if __name__ == "__main__":
    raise SystemExit(main())
