# Brief for a subagent writing one Note

You are writing Notes for a study-notes project built from CampusX playlists: "100 Days of Machine Learning" (Notes ML-001–ML-128),
the maths playlists (Notes MA-003+, see `docs/maths-plan.md`) and "100 Days of Deep Learning" (Notes DL-001–DL-085 = 1000 + Video,
see `dl_map/PLAN.md`).
The reader is a beginner with ADHD and a visual learner. A reviewer (the main agent) checks your work before the user sees it.

Project root: `/home/anshu/campusx`. Read these first, fully:
- `README.md` (all rules: Note structure, writing style, layout for focus, visuals, building)
- `CONTEXT.md` (the project's vocabulary)
- One finished Note as the model to copy: `13-toy-project/note.md` (code-heavy) and its `notebook.ipynb`, `images/`

## Inputs
- Transcript: Whisper English translation, `transcripts/NNN.whisper-en.txt` (ML), `transcripts/Mnn.whisper-en.txt` or
  `Mnn.captions-en.txt` (maths), `transcripts/DNNN.whisper-en.txt` (DL). Some also have a cleaner `*.timestamped.txt`;
  prefer it. Whisper can loop on a phrase or hallucinate counted numbers: rebuild such passages from context and say so.
  Older auto-Hindi captions (`NNN.hi-orig.txt`, `dl_map/transcripts/`) are a last resort.
- The teacher's code and data: `reference/campusx-code/` (folders named by "day", NOT equal to video numbers; match by topic).
  If the data you need is not there, search the teacher's other repos (GitHub API `users/campusx-official/repos`, paginated,
  235 repos) and file contents before concluding it is missing. Never invent a dataset if the real one exists.

## What to produce, in your folder only (e.g. `15-working-with-csv/`)
1. `note.md`, following every rule in README: title only in front matter; numbered sections named after topics;
   every section opens with a `> **Key point:**` box; paragraphs max 3 sentences, split never cut; "we" voice;
   NEVER mention the video, the teacher, "he", timestamps or the course itself (no "Video N" or "(Video N, coming)" either:
   refer to other Notes by topic, linking only to Notes that exist); bold only a term where first defined;
   `> **Extra:**` boxes for anything not in the video; `> **Python:**` boxes for code (short lines, comments on their own
   line if long); formulas in 3 steps (words, display maths `$$...$$`, worked numbers); figures numbered via captions
   and referred to as "Figure N"; ends with `## Summary` then `## Key terms` table. No ₹ sign (write "rupees").
   Leave space for the "Where this fits" box: the main agent generates it, do not write one.
2. `images/`: every figure. No matplotlib. Tools: TikZ (`\input{../../tools/tikz-style.tex}`, still concept diagrams),
   Manim (step-by-step processes; render MP4 + GIF + `_frames.png` 2x2 key frames, copy the pattern from
   `13-toy-project` or `11-tensors/images/tensor_buildup.py`), Plotly (interactive or chart; also write a `.pdf`),
   Seaborn objects interface only (still statistical charts), Dash (apps that rerun Python, in the Notebook).
   Never call matplotlib directly, not even to tweak a Seaborn figure (e.g. `._figure`, rotating labels): if Seaborn
   objects cannot do it, use Plotly.
   All text in Latin Modern ("Latin Modern Roman" in Python, the TikZ style already sets it). Same colours as existing figures.
   For EVERY figure, look at the rendered PNG yourself (Read tool) and fix overlaps, clipping, unreadable text.
3. `notebook.ipynb` if the Video has code: rebuild the teacher's code for current library versions (never copy his
   notebook), one comment per step for a beginner. Run it end to end with
   `$PY -m nbconvert --to notebook --execute` (output to the project-root `.logs/`, never a `.logs/` inside your folder)
   and make sure it works. Data files go in `data/`. Keep `data/` under about 1 MB: trim big files to a sample that still
   shows the same behaviour, and say in the Note where the full file comes from.
   If the Video calls a live website or API, save one real reply in `data/` and let the Notebook fall back to it.
4. Build: `tools/build.sh <folder>` must print `Built pdf/<folder>.pdf` (it also checks no text went missing).
   Look at every PDF page (pdftoppm, then Read) and fix layout problems.

Python: `export PYTHONNOUSERSITE=1` first, then `/home/anshu/miniforge3/envs/campusx/bin/python`; run Jupyter as `$PY -m nbconvert --to notebook --execute ...` (never plain `jupyter`: a stray copy in ~/.local/bin is not the env's). LaTeX: `export PATH=$HOME/.local/bin:$PATH`.
Missing LaTeX package: `tlmgr install <name>`.

## No duplication
Each concept is taught in ONE Note. Before explaining any concept, check whether a written Note already teaches it:
- `course_map/concepts.yaml`: find the Concept; its `videos:` list and the `notes:` map at the top tell which Notes cover it.
- `grep -ril "<term>" [0-9]*/note.md` and `glossary.md` for terms that are not Concepts.
If it is already taught: give a one-line recap and a link (e.g. "Standardization (see the [standardization Note](../ML/03-feature-engineering/ML-023-standardization/ML-023-standardization.md)) puts every column on mean 0, std 1."),
then teach only what is NEW in this Video. Do not re-derive, re-draw or re-define it. Reuse the glossary's wording for terms
already defined. If this Video teaches the same thing in more depth or from a new angle, keep only the new part.
The same holds between Notes you write in one batch: teach a concept in the first Note that needs it, link from the later ones.

## Do NOT touch
`README.md`, `CONTEXT.md`, `glossary.md`, `course_map/`, other Notes' folders, `tools/`, git. The main agent merges.

## Report back (your final message)
1. Folder, page count, figure list with the tool used for each and one line on why that tool.
2. **Concept list from the transcript and code** ("transcript first, map second"): every concept taught, each with
   its pipeline step (0-13, see README) and any Links to other Concepts (types: needs, is a kind of, fixes,
   compared with, used in). Compare with the draft entries for your Video in `course_map/concepts.yaml` and say what
   to add, change or remove. Do not edit the YAML.
3. Key terms (term + one-line meaning) for the glossary.
4. Anything you corrected from the teacher (facts, outdated APIs) and anything you were unsure about.
5. Linked instead of repeated: each concept you only recapped, with the Note you linked to.
