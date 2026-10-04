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
  00-course-map/00-course-map.md                       the Course map (also its images/)
  MA/<NN-chapter>/MA-001-<slug>/MA-001-<slug>.md       Mathematical foundations
  ML/<NN-chapter>/ML-001-<slug>/ML-001-<slug>.md       Machine learning: each Note folder holds its .md, images/,
  DL/<NN-chapter>/DL-001-<slug>/DL-001-<slug>.md       Deep learning      data/ and <Note>.ipynb when it has code
  ML/06-regression/06-regression.md                    chapter index: the Chapter's Notes in reading order
  pdf/<same layout>/<Note>.pdf                         generated PDFs
  transcripts/                                         subtitles for every Video
  glossary.md
```

## Setup

- Python: conda env `campusx` (`conda activate campusx`): numpy, pandas, scikit-learn, plotly, kaleido, dash, seaborn, manim, jupyterlab.
- LaTeX: TinyTeX in `~/.local/bin`. Build with `pdflatex -interaction=nonstopmode -halt-on-error` (without `-halt-on-error` a broken file still produces a PDF).
- PDFs: pandoc + TinyTeX (xelatex).

## Building a Note

`tools/build.sh ML/01-foundations/ML-002-ai-vs-ml-vs-dl` builds every image in that Note's `images/` (each `.tex` → PDF + PNG, each `.py` run) and writes `pdf/ML/01-foundations/ML-002-ai-vs-ml-vs-dl.pdf`.
In the PDF, GIFs are swapped for their `_frames.png` key frames and PNGs for a vector `.pdf` of the same name when one exists (`tools/media-swap.lua`).
Shared looks: `tools/tikz-style.tex` (diagrams), `tools/pdf-style.tex` (PDF).
Symbols like ⊃ or → go in Markdown as maths (`$\supset$`, `$\rightarrow$`): the PDF font has no such characters.

### Course map build

`python course_map/build_map.py` regenerates the Course map Note (`00-course-map/`) and the *Where this fits* block of every written Note from `course_map/concepts.yaml`; run it before `tools/build.sh`. A name containing a comma must be quoted in the YAML (the script checks). The Algorithm chooser is hand-drawn in `course_map/algorithm_chooser.tex`. Interactive version: `python course_map/app.py`, then open http://127.0.0.1:8050.

## Transcripts

`transcripts/fetch.sh` downloads subtitles for every Video in `transcripts/playlist.txt` as `NNN.<lang>.txt`.
`en-IN` = human English subtitles. `hi-orig` = YouTube's automatic Hindi speech recognition: messy (e.g. "DL" comes out as "डीजल"), so read it for meaning, not word for word.

## Workflow

Videos are grouped as:

| Group | Videos | Status |
|---|---|---|
| A. Foundations | 1-14 | done (10 skipped) |
| B. Prerequisites: getting and understanding data | 15-22 | done |
| C. Feature engineering and preprocessing | 23-45 | done |
| D. Core ML | 46-134 | done |
| E. Maths for ML | Note IDs 210+ (see `docs/maths-plan.md`) | in progress |

Subagents never edit the glossary, README or git; Claude merges those after review.

### Course map

One data file lists every Concept, its Pipeline step and its Links; all four views (Pipeline map, Concept map, Learning path, Algorithm chooser), the PDF, the interactive version (Dash Cytoscape) and every Note's *Where this fits* box are generated from it.

Pipeline steps (the teacher's ML development life cycle, Video 9, split finer): 0 Foundations, 1 Frame the problem, 2 Get data, 3 Understand data, 4 Clean, 5 Engineer features, 6 Reduce dimensions, 7 Split, 8 Model, 9 Evaluate, 10 Tune, 11 Deploy, 12 Test, 13 Monitor and maintain. Understand data comes before Clean (as in the playlist and CRISP-DM), with a loop arrow between them: in practice we go back and forth.

On the map: Video 1 is the Course map and the first lesson; 8 and 12 sit in Foundations; 9 defines the Pipeline map; 14 is Frame the problem.

**Transcript first, map second.** For every Note:
1. List every concept taught in the transcript and the teacher's code, before looking at the draft map.
2. Compare with the draft: add missing Concepts and Links, correct or remove wrong ones.
3. Every Key term must be a Concept or belong to one.
4. Only then mark the Note's Concepts confirmed. Reviews of subagent Notes check this step.


Write one Note → you review → fix → next. Video 2 first (locks the style), then the Course map (Video 1), then onward.

## Deferred

None. The once-deferred Videos are written: Video 1 has two folders, `00-course-map` (the Course map) and `ML/01-foundations/ML-001-what-is-ml` (the lesson); Videos 8, 9, 12 and 14 have their own Notes. Note ML-011 is written from the pinned `environment.yml`.

## Skipped

Videos we will not make Notes for:

- Video 10: Data Engineer vs Data Analyst vs Data Scientist vs ML Engineer (job roles)
