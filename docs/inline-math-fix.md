# Task: one step per line, nothing rolled into sentences (NOTE-RULES §15 and its addendum)

The user, quoting a section of MA-063 as it showed on the site: "Again so much math inline. Each step in new line. It looks too cluttered to follow and read. Across all files." Read `docs/NOTE-RULES.md` in full first, especially §11, §14 and §15 with its addendum.

## For every Note on your list
1. Run `/home/anshu/miniforge3/envs/campusx/bin/python tools/find_inline_calc.py <Note>.md`. It lists:
   - `prose`: a calculation inside a sentence (inline `$...$` with "=", a number and an operation);
   - `wide`: a one-line `$$...$$` over about 40 visible characters (too wide for a phone).
2. Fix each one:
   - **prose:** rewrite the sentence in words, then put the calculation on display lines, one operation per line, each on its own line `$$ ... $$` (inside a list item, indent the `$$` lines to the item's text). Example:
     before: `The angle grows from $\pi/6 = 0.524$ to $0.524 + 0.6 = 1.124$; the radius stays 2.`
     after:
     ```
     The angle grows by $h = 0.6$; the radius stays 2.
     $$\theta = \pi/6 = 0.524$$
     $$\theta + h = 0.524 + 0.6$$
     $$\theta + h = 1.124$$
     ```
   - **wide:** split at the "=" signs into several lines, one step each; two results side by side (`\qquad`, `,`) go on separate lines; a long sum is built up in two or three lines (first products, then the total). A single matrix that cannot be split stays as it is.
   - Keep inline maths only for naming one symbol or one value (`$h$`, `$h = 0.6$`).
3. Also read each section once as a beginner on a phone: if a paragraph still reads as a wall of symbols, break it into short sentences and display lines (§15). Do not add new content, caveats or depth (§14); keep every number, fact and Extra.
4. Rerun the finder: the Note must print "0 found" (or only lines you deliberately kept, e.g. one unsplittable matrix: list those in your report).

## Checks
`tools/build.sh <Note folder>` prints Built; `python tools/github_math.py --check <Note>.md` is clean; `grep -nP "[\t\x08\x0c\r]" <Note>.md` is empty (edit with the Edit tool or raw strings: a Python `\t` eats `\times`). If `tools/check_pdf.py` complains about display maths inside a list item, put a blank line before and after each `$$` line (indented to the item) rather than turning the steps back into inline maths.

## Do not touch
git, `glossary.md`, `course_map/`, `tools/`, `docs/`, `site/`, figures, notebooks, and any Note not on your list. No background agents.

## Report (as text)
Per Note: the count before and after, and any line kept with the reason. Nothing else.
