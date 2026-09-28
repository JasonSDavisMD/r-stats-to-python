#!/usr/bin/env bash
# post-create.sh -- runs once when a Codespace / dev container is created.
# Installs uv, builds workbench/.venv from uv.lock (core libraries + JupyterLab),
# and runs the environment check. Optional add-ons are NOT installed here, to
# keep Codespaces fast: add them with  uv sync --extra deep  (or --all-extras).
# It only touches workbench/, and a failure here leaves the container usable:
# rerun this script, or run `uv sync --group lab` in workbench/ by hand.
set -euo pipefail

WORKBENCH="$(cd "$(dirname "${BASH_SOURCE[0]}")/../workbench" && pwd)"

if ! command -v uv >/dev/null 2>&1; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi
export PATH="$HOME/.local/bin:$PATH"

cd "$WORKBENCH"
uv sync --frozen --group lab     # exact versions from uv.lock, into ./.venv
uv run --no-sync python -m statsbench.envcheck

# Activate .venv in every new bash terminal (VS Code, JupyterLab, SSH), so
# `stats find ...` and `python` always mean the workbench environment.
ACTIVATE="source $WORKBENCH/.venv/bin/activate"
grep -qxF "$ACTIVATE" "$HOME/.bashrc" 2>/dev/null || echo "$ACTIVATE" >> "$HOME/.bashrc"

echo
echo "Workbench ready. JupyterLab starts automatically: Ports tab -> 8888 -> Open in Browser."
echo "Search the toolbox from a NEW terminal (Ctrl+Shift+\`):  stats find \"inverse logit\""
