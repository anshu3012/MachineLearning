# Task: visual upgrades for a block of Notes

The user has ADHD and learns visually: "the whole project depends on animations and figures". In every Note, figures and animations are the main teaching channel; the text supports them. The gold standard is 3Blue1Brown-style intuition: an idea you can watch move.

## Read first
1. `docs/NOTE-RULES.md`: every rule, especially evidence and "right data, right results".
2. `docs/visual-audit.md`: the summary, the top 30, and the proposal for each of your Notes in section 4.
3. Your Notes' `note.md`, their current `images/` scripts and their notebooks.
4. Model animations to match in quality and convention:
   - `603-hessian-and-multivariate-taylor/images/optimizer_race.py` (Plotly frames → ffmpeg GIF plus a `_frames.png` grid for the PDF);
   - `1056-rnn-forward-propagation/images/rnn_unroll.py`;
   - `1075-self-attention-geometric-intuition/images/attention_2d.py`.

## What to build
- **For each Note in your list:** build the proposed visual, or a better one if you find it. Priorities:
  1. animate the Note's core process;
  2. give every key-point section a visual.
  One strong animation per core idea beats many small plots.
- **Tools:** Manim Community 0.20 for geometric or vector motion; Plotly frames for data and curves changing; TikZ for still structure. Never matplotlib. Name the tool and the reason in your report.
- **Data:** use the Note's own real data or model where possible, and show the principle the Note teaches. If the visual's data contradicts the lesson, redesign; never pick a lucky seed.
- **Output:** each animation as `images/<name>.gif` (in `note.md`) plus `images/<name>_frames.png`, a grid of the key frames that the PDF build swaps in (`tools/media-swap.lua`). Keep each GIF under about 3 MB: about 10–15 fps, sensible size.
- **Labels:** readable at phone width: large fonts and few words per frame. One idea per frame; build up step by step; hold the final frame.
- **Credits:** when the idea comes from 3Blue1Brown, StatQuest or another visual explainer, recreate it with our own data and code (never copy frames) and credit the intuition in the text and the Sources, e.g. Sanderson, G. (3Blue1Brown), "<title>", 3blue1brown.com/lessons/<slug>. **Open every source before crediting it:** for a web page, fetch it; for a video, check its title and what it actually shows (captions, or stills); for a book, check the section in the PDF. Credit only what the source really shows. If our animation is our own design, say so and credit nothing. A check on 2026-10-03 found 4 credits that claimed pictures their sources never draw.
- **Text:** add or adjust only the text that introduces each new figure: a numbered figure caption, and one sentence before or after saying what to watch for. Keep the voice and house rules: we-voice; no video, teacher, course, CampusX or YouTube; GitHub-safe maths (`tools/github_math.py` runs in the build). Do not rewrite unrelated text.
- **Heavy renders:** Manim and long Plotly frame runs go to topgro, `tools/remote_run.sh <folder> "<command>"`, which has the same `campusx` environment. The laptop is shared and loaded.

## Checks
- `tools/build.sh <folder>` prints "Built".
- Look at every new GIF (several frames) and the `_frames.png` yourself.
- Look at the PDF page where each figure sits.
- Fix overlaps, clipped labels and unreadable text before moving on.

## Do not touch
Notes outside your list, the glossary, `course_map/`, `docs/` (except your report section), `tools/` and git. Notes 1055–1085 belong to other agents unless they are in your list.

## Report
- Per Note: the visuals added (file, tool, why), what each shows, the data used, and any text changed.
- Anything skipped, and why.
- The audit score you would now give.
