#!/usr/bin/env bash
# post-create.sh -- runs once when this Codespace is created.
# Installs uv, builds .venv (statsbench from GitHub + JupyterLab), and runs the
# statsbench environment check. A failure leaves the Codespace usable: rerun
# this script, or run `uv sync --group lab` by hand.
set -euo pipefail

PROJECT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! command -v uv >/dev/null 2>&1; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi
export PATH="$HOME/.local/bin:$PATH"

cd "$PROJECT"
uv sync --group lab
uv run --no-sync python -m statsbench.envcheck

# Activate .venv in every new bash terminal (VS Code, JupyterLab, SSH), so
# `stats find ...` and `python` always mean this workspace's environment.
ACTIVATE="source $PROJECT/.venv/bin/activate"
grep -qxF "$ACTIVATE" "$HOME/.bashrc" 2>/dev/null || echo "$ACTIVATE" >> "$HOME/.bashrc"

echo
echo "Ready. JupyterLab starts automatically: Ports tab -> 8888 -> Open in Browser."
