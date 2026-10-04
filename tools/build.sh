#!/usr/bin/env bash
# Build every image and the PDF for one Note.  Usage: tools/build.sh ML/01-foundations/ML-002-ai-vs-ml-vs-dl
set -euo pipefail
shopt -s nullglob
export PATH=$HOME/.local/bin:$HOME/bin:$PATH        # TinyTeX
export PYTHONNOUSERSITE=1                           # ignore packages in ~/.local
export PYTHONPATH="$(cd "$(dirname "$0")" && pwd)${PYTHONPATH:+:$PYTHONPATH}"   # tools/sitecustomize.py: HTML twin of every Plotly PNG
ENV=${CAMPUSX_ENV:-$(conda info --base)/envs/campusx}
PY=$ENV/bin/python
root=$(cd "$(dirname "$0")/.." && pwd)
note=${1%/}                                         # ML/01-foundations/ML-002-ai-vs-ml-vs-dl
name=$(basename "$note")                            # ML-002-ai-vs-ml-vs-dl: its file name
cd "$root/$note/images"
# Skip figures whose source is older than its last render (FORCE=1 rebuilds all).
for t in *.tex; do
  [ -z "${FORCE:-}" ] && [ "${t%.tex}.png" -nt "$t" ] && continue
  pdflatex -interaction=nonstopmode -halt-on-error "$t" > /dev/null || { echo "LaTeX failed: $t"; exit 1; }
  "$ENV/bin/pdftoppm" -png -r 200 -singlefile "${t%.tex}.pdf" "${t%.tex}"
done
rm -f *.aux *.log
for p in *.py; do
  [ -z "${FORCE:-}" ] && [ ".built_${p%.py}" -nt "$p" ] && continue
  "$PY" "$p"
  touch ".built_${p%.py}"
done
cd "$root/$note"
"$PY" "$root/tools/github_math.py" "$name.md"          # maths GitHub can render (prints any \% to fix by hand)
mkdir -p "$root/pdf/$(dirname "$note")"
"$ENV/bin/pandoc" "$name.md" -o "$root/pdf/$note.pdf" --pdf-engine=pdflatex --toc --toc-depth=3 -V toc-title=Contents \
  --lua-filter="$root/tools/media-swap.lua" \
  -V geometry:margin=1in -V fontsize=12pt -H "$root/tools/pdf-style.tex" -V colorlinks=true -V linkcolor=blue
"$PY" "$root/tools/check_pdf.py" "$name.md" "$root/pdf/$note.pdf" || { echo "PDF is missing text: $note"; exit 1; }
echo "Built pdf/$note.pdf"
