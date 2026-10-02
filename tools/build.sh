#!/usr/bin/env bash
# Build every image and the PDF for one Note.  Usage: tools/build.sh 02-ai-vs-ml-vs-dl
set -euo pipefail
shopt -s nullglob
export PATH=$HOME/.local/bin:$PATH
PY=/home/anshu/miniforge3/envs/campusx/bin/python
root=$(cd "$(dirname "$0")/.." && pwd)
note=${1%/}
cd "$root/$note/images"
for t in *.tex; do
  pdflatex -interaction=nonstopmode -halt-on-error "$t" > /dev/null || { echo "LaTeX failed: $t"; exit 1; }
  pdftoppm -png -r 200 -singlefile "${t%.tex}.pdf" "${t%.tex}"
done
rm -f *.aux *.log
for p in *.py; do "$PY" "$p"; done
cd "$root/$note"
pandoc note.md -o "$root/pdf/$note.pdf" --pdf-engine=pdflatex \
  --lua-filter="$root/tools/media-swap.lua" \
  -V geometry:margin=2cm -V fontsize=11pt -H "$root/tools/pdf-style.tex" -V colorlinks=true -V linkcolor=blue
echo "Built pdf/$note.pdf"
