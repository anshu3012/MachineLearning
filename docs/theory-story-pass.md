# Task: one read-and-fix pass for (1) agreement with theory and (2) the story of each Note

The user asked for this after the deep pass: "an audit of whether everything matches theory and if it deviates then why" and "review for ordering of things in a note so each note tells a story and connects and clicks." This is a **single pass**: read each Note on your list once, fix what matters, and stop. There is no audit after it. Read `docs/NOTE-RULES.md` in full first (§11, §13, §14, §19, §20, §21 matter most).

## 1. Does every result match theory? If not, does the Note say why?
For every experiment, figure, table and worked result that illustrates an idea, ask what the theory predicts and whether the result agrees:
- examples: a standard error that should shrink as 1/√n; a sample variance that should be unbiased only with n − 1; a CLT histogram that should look normal for large n; train error falling while test error makes a U; bagging lowering variance but not bias; a learning rate above 2/λ diverging; a regularised coefficient shrinking towards 0; an optimizer's path matching its update rule; a derivation's result matching a known formula.
- **If it agrees**, nothing to do (do not add commentary).
- **If it deviates** (a curve not monotone where theory says monotone, a coefficient growing under Ridge, a simulated rate off the formula, a faster model being slower), the Note must say why in one or two plain sentences: finite sample or noise (with the size of the effect), a seed, a library default (name it), a different setting, correlated features, an approximation in the derivation. If the deviation is actually an error in the Note's code or text, fix it.
- **Derivations and stated theory must be right** at the beginner level of the Note: a formula, a condition or an "always" that is wrong in theory is fixed.
- Recompute numbers only where needed to decide a deviation (the deep pass already checked arithmetic).

## 2. Does the Note tell one story that clicks?
Read the Note as a beginner from top to bottom and ask:
- Does it open with the **problem or question** the Note answers (why we need this), then build: intuition and a picture → the mechanism on the running example → the standard terms and the formula → the experiment or code → limits and gotchas → the summary that ties back to the opening question and points to what comes next?
- Does **each section lead to the next**? Is there a one-line bridge where a section changes topic ("We now know X; but Y is still open, so…")? Does anything appear before what it depends on (a result used before it is shown, a figure referred to before its section)?
- Is there **one running example** carried through, or does the Note jump between unrelated examples without saying why?
- Is anything **out of place** (a gotcha in the middle of the intuition, a long Extra that breaks the flow, a summary that introduces new facts)?
**Fix** by adding short bridges, moving a paragraph or section to where it belongs, or tightening the opening question and the closing summary. Moving content is fine; never delete content (§14). Keep the §11 ladder inside each section.

## Headings and links (important)
Other Notes link to this Note's sections by anchor (e.g. `#41-from-secant-to-tangent`). If you rename, renumber or move a heading, **record each change** in `/home/anshu/.claude/jobs/8c1c0992/tmp/anchors/<Note ID>.tsv`, one line per heading: `old-anchor<TAB>new-anchor` (get anchors with `tools/section_links.py --headings <Note.md>` before and after). Do not edit other Notes; the coordinator updates all inbound links at the end. Within your own Note, fix its internal links and "Section N" references yourself.

## Keep
- Fix only what matters to the lesson (§14); no nitpicks, no rounding, no filler or puffery edits (do not remove or replace words like clearly, actually, powerful).
- CampusX is the baseline (§13): before calling a CampusX statement wrong, look for the reading under which it is right; if both hold, keep CampusX's and add the other as "Another way to see it".
- Keep every fact, number, figure, Extra and gotcha. Numbers must still match the notebook.
- Keras notebooks whose numbers a Note quotes re-run on the laptop CPU only.

## Checks per Note
`tools/build.sh <Note folder>` prints Built; `python tools/github_math.py --check <Note.md>` clean; `grep -nP "[\t\x08\x0c\r]" <Note.md>` empty; `tools/find_inline_calc.py <Note.md>` 0 (single matrices aside); `tools/section_links.py --check <Note.md>` 0 broken.

## Do not touch
git, `glossary.md`, `course_map/`, `tools/`, `docs/`, `site/`, other Notes. No background agents. Scratch in `/home/anshu/.claude/jobs/8c1c0992/tmp/<your-batch>/`.

## Report (short, as text)
Per Note: theory deviations found and how each is explained or fixed (one line each); story changes (what moved, bridges added, opening/summary changes); headings changed (count). No list of things that were fine.
