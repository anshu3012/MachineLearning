# CampusX ML Study Notes

Ground-zero notes for the CampusX playlist
[100 Days of Machine Learning](https://www.youtube.com/playlist?list=PLKnIA16_Rmvbr7zKYQuBfsVkjoLcJgxHH) (134 Videos).
Written for a visual learner with no prior ML or Python knowledge. Terms used here are defined in [CONTEXT.md](CONTEXT.md).

## What each Note is

- **One Note per Video**, in plain English. Complete enough to learn from without watching the Video.
- Follows the **Teacher's flow** (his order, examples, analogies), taken from the Video's subtitles in `transcripts/`, without ever narrating it.
- **Extra boxes** add what he skips (formulas, common mistakes). Clearly marked as not his.
- **Python boxes** teach just the Python needed at that point. Written as a block quote starting `**Python:**` (green bar in the PDF), like `**Key point:**` (blue) and `**Extra:**` (purple).
- Every formula in 3 steps: plain words → formula → worked with small real numbers.
- No practice questions.
- New terms go in [glossary.md](glossary.md), linked to the Note that first explains them.

### Note structure

1. **Overview**: one diagram of the whole topic, plus one or two sentences
2. **Prerequisites**: earlier Notes this one builds on (omit if none)
3. **Numbered sections named after the topic itself**, in the Video's order. Each idea: definition → diagram → example. Extra and Python boxes inline.
4. **Summary**: comparison table + short bullet list

### Writing style

Professional teaching material, written for a reader with ADHD. Every sentence teaches something.
- Voice: "we" (writer and reader working through it together), e.g. "In ML, we select the features ourselves." No scene-setting or filler. Never mention the Video or teacher; his order and examples are used silently.
- Depth: the Video's content plus whatever a beginner needs to fully understand it. Anything added is an **Extra** box.
- Examples: his first; add our own when an idea needs a second angle.
- Headings name a real topic ("Why expert systems fail"), never a bare label ("Limitation", "Example"). Examples live inside sections.
- Figures are numbered with captions, and the text points to them ("Figure 3 shows…").
- Title page: title only. Then the contents.
- Each Note ends with **Key terms** (term + one line), as well as the shared glossary.
- Diagram text follows the same rules: labels and short technical phrases, no chatty captions.

### Layout for focus (ADHD)

- Every section opens with a one-line **Key point** box; the explanation follows.
- Paragraphs: at most 3 sentences. Use a list wherever a paragraph would only enumerate. **Split, never cut**: long ideas become more paragraphs, lists or subsections; no detail is dropped.
- One Note per Video, whatever its length. Notes are never split into parts.
- Bold only a term at the point it is first defined. Key phrases go in Key point boxes.
- Formulas in the 3-step boxes go on their own line as display maths (`$$...$$`), never as tall inline fractions: those collide with the next line in the PDF.
- Text stays black; colour is only used in diagrams.
- Title page: title only (no reading time). No video link anywhere in the Note.

## Visuals

No matplotlib. One font everywhere: Latin Modern (text and every diagram; Plotly/Seaborn/Manim use it as the system font "Latin Modern Roman", linked from TinyTeX into ~/.fonts). Latin Modern has no ₹ sign: write "rupees". Diagram style: clean (few colours, big labels, white background, same colour = same meaning everywhere).
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
- PDFs: pandoc + TinyTeX (xelatex).

## Building a Note

`tools/build.sh 02-ai-vs-ml-vs-dl` builds every image in that Note's `images/` (each `.tex` → PDF + PNG, each `.py` run) and writes `pdf/02-ai-vs-ml-vs-dl.pdf`.
In the PDF, GIFs are swapped for their `_frames.png` key frames and PNGs for a vector `.pdf` of the same name when one exists (`tools/media-swap.lua`).
Shared looks: `tools/tikz-style.tex` (diagrams), `tools/pdf-style.tex` (PDF).
Symbols like ⊃ or → go in Markdown as maths (`$\supset$`, `$\rightarrow$`): the PDF font has no such characters.

## Transcripts

`transcripts/fetch.sh` downloads subtitles for every Video in `transcripts/playlist.txt` as `NNN.<lang>.txt`.
`en-IN` = human English subtitles. `hi-orig` = YouTube's automatic Hindi speech recognition: messy (e.g. "DL" comes out as "डीजल"), so read it for meaning, not word for word.

## Workflow

Write one Note → you review → fix → next. Video 2 first (locks the style), then the Course map (Video 1), then onward.

## Deferred

Videos skipped for now, to come back to later:

- Video 1: Course map (what the course covers, all Videos grouped into modules)
- Video 8: Applications of Machine Learning
- Video 9: Machine Learning Development Life Cycle (MLDLC)
- Video 12: Installing Anaconda / Jupyter / Colab. Do this when the project is done: first pin the exact library versions of the `campusx` environment (e.g. an `environment.yml`), then write the setup Note from that pinned environment.
- Video 14: How to Frame a Machine Learning Problem

## Skipped

Videos we will not make Notes for:

- Video 10: Data Engineer vs Data Analyst vs Data Scientist vs ML Engineer (job roles)
