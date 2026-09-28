"""``python -m psl ...`` == ``psl ...`` (useful when the script is not on PATH)."""

from psl.finder.cli import main

raise SystemExit(main())
