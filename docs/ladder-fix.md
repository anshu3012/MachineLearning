# Task: make a Note climb the beginner ladder (fix for WEAK / FAIL audit results)

The user read a Note built from a textbook and said: "do you really think it's friendly for a beginner? … There is no intuition no nothing, just directly math." An audit (`/home/anshu/.claude/jobs/8c1c0992/tmp/ladder-audit-*.md`) graded every Note against NOTE-RULES §11. Your Notes were graded WEAK or FAIL. Fix every failing section the audit lists, and any other section with the same problem.

## Read first
1. `docs/NOTE-RULES.md`, all of it; §10, §11 (including the last paragraph on sources), §12, §13, §14 drive this task.
2. Your Notes' rows in the audit file: the failing sections and what is missing.
3. `docs/visual-audit/PROMPT.md`: figure conventions (Plotly frames or Manim → GIF + `_frames.png`, fonts, sizes, credits, checks).
4. Your Note's block in `docs/maths-sources.md` (maths) or `docs/teaching-paths/*.md` (ML, DL), and the transcripts it names (`transcripts/`).

## The failure pattern
The "1. In words / 2. Formula / 3. Example" template, where "In words" reads the formula aloud, the example only re-plugs the formula, and the picture (if any) comes after. A Key point that is a formula. A section that opens with a definition, notation or a general form.

## What a fixed section looks like (NOTE-RULES §11)
1. Plain words first: the idea in everyday language, no formula, no undefined term, on something the reader can see (the Note's running example, a picture, a short story).
2. A picture or animation of that idea, in or right next to the opening. Not a plot of the formula's curve: a picture of the *idea* (what happens, what moves, what is compared).
3. The standard term attached where the idea appears, as "**term** (G-NNN)" with the ID from `glossary.md` (read only).
4. A worked example on the Note's own small numbers, step by step, BEFORE the general formula.
5. Then the formal version, every symbol named, and a one-line check that it reproduces the worked numbers.
Reorder the Note as a whole to go concrete → abstract: the running example, analogy or picture comes before the first symbol.

## Sources for the intuition
- Priority: StatQuest, Khan Academy, 3Blue1Brown, CampusX (free videos). Check the Note's source block and the transcripts first.
- If none covers the idea: the next most beginner-friendly explainer, a video (Luis Serrano Academy, ritvikmath, Stats with Brian…), a good Medium article, or a GitHub repository's explanation. Fetch it and read it; credit it under **Built from** (channel or author, exact title, link). Captions: `transcripts/whisper_fetch.py` or `yt-dlp --write-auto-sub`; never cookies, never members-only content.
- The textbook stays essential as the formal grounding: keep every textbook citation, add one for each formula that lacks one.
- §13: compare with CampusX where CampusX covers the idea; no clash; the clearer path leads; the other side's angle is kept as "Another way to see it".

## Also apply NOTE-RULES §15 to every section (define each symbol with a concrete value at first use; one step per display line; no maths in prose; say what each picture shows)

## Keep everything
- Keep every correct fact, number, experiment, gotcha, Extra box and building block. Move content; never drop it (§14, "Never remove real content"). Numbers must still match the executed notebook.
- §14 depth: the beginner level of the source. No new caveats, no trivia.
- No duplication: a concept owned by another Note gets a one-line recap and a link.

## Visuals
Our own version with our own data and code, never copied frames. Manim Community 0.20 for geometric motion; Plotly frames for data and curves changing; TikZ for still structure; never matplotlib or seaborn. Every process idea gets an animation; every key term gets a figure; the text points at each figure.

## Machines
Python: `/home/anshu/miniforge3/envs/campusx/bin/python` with `PYTHONNOUSERSITE=1`. Manim renders and anything over about a minute go to topgro: `tools/remote_run.sh <folder> "<command>"`. Keras notebooks whose numbers a Note quotes re-run on the laptop only.

## Checks
- `tools/build.sh <Note folder>` prints "Built".
- Look at several frames of every new GIF and at each `_frames.png`; look at the PDF page where each figure sits; fix clipped labels, overlaps, unreadable text.
- `python tools/github_math.py --check <Note>.md` is clean.
- Re-read the Note as a beginner: every section now opens in plain words with a picture and reaches the formula after the worked numbers.

## Do not touch
git, `glossary.md`, `course_map/`, `tools/`, `docs/`, `site/`, and any folder not in your list. No background agents.

## Report (as text, not a file)
Per Note: each section fixed and how (what now opens it, which picture, which worked example); sources added; new Key terms; anything skipped and why.
