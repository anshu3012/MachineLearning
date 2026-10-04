#!/usr/bin/env bash
# Run a Note's notebook (or any command) on the heavy-compute machine, then copy results back.
# Usage: tools/remote_run.sh <folder> [command]     default command: execute notebook.ipynb into .logs/
# The command runs inside the folder on the remote machine, with the campusx env first on PATH.
set -euo pipefail
HOST=${REMOTE_HOST:-topgro-linux-ts}
DIR=${1%/}; shift || true
CMD=${*:-python -m nbconvert --to notebook --execute --ExecutePreprocessor.timeout=7200 --output-dir .logs --output notebook notebook.ipynb}
ROOT=$(cd "$(dirname "$0")/.." && pwd)
RROOT=campusx-remote
ssh -o BatchMode=yes "$HOST" "mkdir -p $RROOT" 2>/dev/null
# send the folder (no PDFs or images built from it) plus shared tools
rsync -az --delete --exclude '.ipynb_checkpoints' "$ROOT/$DIR/" "$HOST:$RROOT/$DIR/" 2> >(grep -v bashrc >&2)
rsync -az "$ROOT/tools/" "$HOST:$RROOT/tools/" 2> >(grep -v bashrc >&2)
ssh -o BatchMode=yes "$HOST" "cd $RROOT/$DIR && mkdir -p .logs && export PATH=\$HOME/miniforge3/envs/campusx/bin:\$PATH PYTHONNOUSERSITE=1 TF_FORCE_GPU_ALLOW_GROWTH=true && $CMD" 2> >(grep -v bashrc >&2)
# bring back what the run produced
for sub in data .logs images; do
  rsync -az "$HOST:$RROOT/$DIR/$sub/" "$ROOT/$DIR/$sub/" 2>/dev/null || true   # folder may not exist
done
echo "remote run done: $DIR on $HOST"
