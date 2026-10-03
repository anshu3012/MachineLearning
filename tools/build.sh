#!/usr/bin/env bash
# Build every image and the PDF for one Note.  Usage: tools/build.sh 02-ai-vs-ml-vs-dl
set -euo pipefail
shopt -s nullglob
export PATH=$HOME/.local/bin:$HOME/bin:$PATH        # TinyTeX
export PYTHONNOUSERSITE=1                           # ignore packages in ~/.local
ENV=${CAMPUSX_ENV:-$(conda info --base)/envs/campusx}
PY=$ENV/bin/python
root=$(cd "$(dirname "$0")/.." && pwd)
note=${1%/}
cd "$root/$note/images"
for t in *.tex; do
  pdflatex -interaction=nonstopmode -halt-on-error "$t" > /dev/null || { echo "LaTeX failed: $t"; exit 1; }
  "$ENV/bin/pdftoppm" -png -r 200 -singlefile "${t%.tex}.pdf" "${t%.tex}"
done
rm -f *.aux *.log
for p in *.py; do "$PY" "$p"; done
cd "$root/$note"
"$ENV/bin/pandoc" note.md -o "$root/pdf/$note.pdf" --pdf-engine=pdflatex --toc --toc-depth=3 -V toc-title=Contents \
  --lua-filter="$root/tools/media-swap.lua" \
  -V geometry:margin=1in -V fontsize=12pt -H "$root/tools/pdf-style.tex" -V colorlinks=true -V linkcolor=blue
"$PY" "$root/tools/check_pdf.py" note.md "$root/pdf/$note.pdf" || { echo "PDF is missing text: $note"; exit 1; }
echo "Built pdf/$note.pdf"
