# Task: rewrite maths Notes along the source videos' teaching path

The user finds the maths Notes "hard to read" and short on animations. The fix: rebuild each Note so a beginner follows the same path the best video teacher uses, with that teacher's visuals recreated as our own animations.

User, 2026-10-03: "the primary sources should be stat quest, khan academy, 3b1b, campus x first. If you can't find the math source there only then move to text books" and "what's also important is the images, videos, animations etc they used and the intuition they build. Like I said this is for a beginner."

## Read first
1. `docs/NOTE-RULES.md`: every rule. §10 (simple words, standard term with its glossary ID, pictures illustrate the words) and §11 (the ladder: plain idea + picture → term → step-by-step worked example → formal version) drive this task.
2. `docs/visual-audit/PROMPT.md`: figure conventions (Plotly frames or Manim → GIF + `_frames.png`, fonts, sizes, credits, checks).
3. Your Note's block in `docs/maths-sources.md` (Sources, Teaching path with timestamps, visuals, worked examples).
4. The transcripts it names: `transcripts/maths-video/<N>-*.txt`. Check every beat you use against the transcript itself.
5. Your Note's `note.md`, notebook, `images/` scripts and `data/`.

## What to do, per Note
- **The whole Note, every concept.** The user's examples (the Hessian, EM) only illustrate the problem. Apply every point below to every concept in every Note on your list (NOTE-RULES §12).
- **CampusX first (NOTE-RULES §13):** for every concept, compare the CampusX explanation with the outside source. No clash between them; use the clearer one as the main path; keep a CampusX angle the other lacks (and vice versa). Report each comparison: which was clearer, any angle kept, any clash and how it was resolved.
- **Reorder** the Note to follow the teaching path: the same order of ideas, analogies, build-up and worked examples. Where the Note's current order differs, use the path's order.
- **Keep** every correct fact, number and experiment the Note already has. Move content; don't lose it. Numbers must still match the executed notebook.
- **Every section climbs the §11 ladder.** Attach each standard term where its idea appears, as "**Hessian** (G-NNN)", taking the ID from `glossary.md` (read only). New terms go in Key terms; list them in your report too.
- **Visuals:** for each key visual in the path, build our own version with our own data and code. Never copy frames.
  - Manim Community 0.20 for geometric motion (surfaces, vectors, planes, transformations).
  - Plotly frames for data and curves changing.
  - TikZ for still structure.
  - Never matplotlib or seaborn.
  - Every process idea gets an animation; every key term gets a figure. Text points to each figure ("in Figure 3, watch…").
- **Credits:** the Note's Sources starts with **Built from** (NOTE-RULES §8). List every video you actually used: channel, exact title, link `https://www.youtube.com/watch?v=ID`. Credit a visual idea in the figure caption ("idea after Khan Academy, 'The Hessian matrix'") only if the transcript confirms the video shows it. Textbooks go under Other references, used only for what none of the videos covers. The body text never narrates a video or a teacher.
- **No duplication:** if a concept is owned by another Note, give a one-line recap and a link. Don't re-teach it.

## Machines
- Python: `/home/anshu/miniforge3/envs/campusx/bin/python` with `PYTHONNOUSERSITE=1`.
- The laptop is shared and loaded. Run Manim renders and anything over about a minute on topgro: `tools/remote_run.sh <folder> "<command>"`. It copies back outputs only.
- Remote Claude sessions are editing other Notes on topgro. Touch only your own folders.

## Checks
- `tools/build.sh <folder>` prints "Built".
- Look at several frames of every new GIF and at each `_frames.png`. Look at the PDF page where each figure sits. Fix clipped labels, overlaps and unreadable text.
- `python tools/github_math.py --check <folder>/note.md` is clean.

## Do not touch
git, `glossary.md`, `course_map/`, `tools/`, `docs/`, and any folder not in your list.

## Report (as text, not a file)
For each Note:
- the new section order, and how it maps to the teaching path;
- each visual added: file, tool, what it shows, the data, the credit;
- new Key terms;
- anything skipped, and why.
