#!/usr/bin/env bash
# start-lab.sh -- start JupyterLab in the background unless it is already running.
# Called on every Codespace start (postStartCommand), so after "Stop" and
# "Resume" JupyterLab is simply there again: open the Ports tab -> 8888.
#
#   Usage: bash start-lab.sh [project_dir]   (default: the folder above .devcontainer)
#   Log:   /tmp/jupyterlab.log
#
# Security: the server listens on 127.0.0.1 only. Inside GitHub Codespaces the
# token prompt is turned off, because Codespaces already requires your GitHub
# login to reach a forwarded port while its visibility is Private (the default).
# Never make port 8888 Public. Outside Codespaces the normal token stays on.
set -u

PROJECT_DIR="${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
PORT="${JUPYTERLAB_PORT:-8888}"
JUPYTER="$PROJECT_DIR/.venv/bin/jupyter"

if [ ! -x "$JUPYTER" ]; then
    echo "JupyterLab is not installed in $PROJECT_DIR/.venv; run: uv sync --group lab"
    exit 0   # never fail the Codespace start over this
fi
if curl -s -o /dev/null "http://127.0.0.1:$PORT/api"; then
    echo "JupyterLab already running on port $PORT"
    exit 0
fi

ARGS=(lab --no-browser --ip=127.0.0.1 --port="$PORT" --ServerApp.root_dir="$PROJECT_DIR")
if [ "${CODESPACES:-}" = "true" ]; then
    ARGS+=(--IdentityProvider.token=)
fi
if [ "$(id -u)" = "0" ]; then
    ARGS+=(--allow-root)   # some containers run as root; Jupyter refuses by default
fi

cd "$PROJECT_DIR"
nohup "$JUPYTER" "${ARGS[@]}" > /tmp/jupyterlab.log 2>&1 &
echo "JupyterLab starting on port $PORT (Ports tab -> 8888 -> Open in Browser)."
