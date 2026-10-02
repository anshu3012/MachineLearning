# CampusX ML Study Notes

Ground-zero notes for the CampusX playlist
[100 Days of Machine Learning](https://www.youtube.com/playlist?list=PLKnIA16_Rmvbr7zKYQuBfsVkjoLcJgxHH) (134 Videos).
Written for a visual learner with no prior ML or Python knowledge. Terms used here are defined in [CONTEXT.md](CONTEXT.md).

## What each Note is

- **One Note per Video**, in plain English. Complete enough to learn from without watching the Video.
- Follows the **Teacher's flow** (his order, examples, analogies), taken from the Video's subtitles in `transcripts/`.
- **Extra boxes** add what he skips (formulas, common mistakes). Clearly marked as not his.
- **Python boxes** teach just the Python needed at that point.
- Every formula in 3 steps: plain words → formula → worked with small real numbers.
- No practice questions.
- New terms go in [glossary.md](glossary.md), linked to the Note that first explains them.

### Note structure

1. **In one picture**: one diagram of the whole Video
2. **Before you start**: earlier Notes this one builds on
3. **The Teacher's flow**: his sections in his order, each as words → picture → example (Extra and Python boxes inline)
4. **Cheat sheet**: short recap

## Visuals

No matplotlib. Diagram style: clean (few colours, big labels, white background, same colour = same meaning everywhere).
Before making any image, write down which tool fits and why.

| Tool | Used for | Shows up as |
|---|---|---|
| TikZ | Still concept diagrams (sets, flowcharts, neural nets) | PDF (vector) + PNG for Markdown |
| Manim | Ideas that move step by step | GIF in Note, MP4 kept, 3–4 key frames in PDF |
| Plotly | Interactive charts (sliders/buttons) | Live in Notebook, PNG in Note |
| Seaborn | Still statistical charts (pair plots, distributions) | PNG |
| Dash | Demos that must rerun Python (e.g. retrain a model) | Inline in Notebook |

Bokeh is installed but not used: Plotly + Dash cover it.

## Notebooks

Only when a Video has code or a demo worth playing with. We rebuild his code for current library versions; we never copy his notebooks.

## Folder layout

```
campusx/
  01-course-map/        note.md
  02-ai-vs-ml-vs-dl/    note.md  images/  make_images.py (or .tex for TikZ)
  13-toy-project/       note.md  notebook.ipynb  images/  ...
  transcripts/          subtitles for every Video
  pdf/                  generated PDFs
  glossary.md
```

## Setup

- Python: conda env `campusx` (`conda activate campusx`): numpy, pandas, scikit-learn, plotly, kaleido, dash, seaborn, manim, jupyterlab.
- LaTeX: TinyTeX in `~/.local/bin`. Build with `pdflatex -interaction=nonstopmode -halt-on-error` (without `-halt-on-error` a broken file still produces a PDF).
- PDFs: pandoc + TinyTeX.

## Workflow

Write one Note → you review → fix → next. Video 2 first (locks the style), then the Course map (Video 1), then onward.
