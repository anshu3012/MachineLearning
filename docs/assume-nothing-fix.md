# Task: make every Note pass "assume nothing" (NOTE-RULES §19 and the rules under it)

The user has given many single examples and said each time: "this is just an example... I'm sure many more similar issues and bugs exist in the same umbrella." Your job is the umbrella, not the examples. Read `docs/NOTE-RULES.md` in full first; §10, §11, §15 (with both addenda), §16, §17, §18, §19 and §20 (with its addendum) drive this task.

## The umbrella
Never assume the reader already knows something, and never teach them something false or vague. A beginner with ADHD reads each Note on a phone, one line at a time. At every point ask: what does the reader need to know to follow this line, and have we shown it yet, correctly, with the real term?

## What to check, section by section, in every Note on your list
1. **Figures (§16, §19).** What kind of picture it is; what each axis, colour, line, arrow and panel means; the familiar thing it is built from (a surface before its contour map, a grid before it bends, a table before its heat map); what to look at and what to conclude. Any visual code the reader has not been taught gets built up first, in this Note or with a link to the section that teaches it plus a one-line recap.
2. **Symbols and functions (§15).** Each is written as an equation with a value at first use; notation (ℝ^D, ∈, Σ, ∂, ᵀ, subscripts) explained with an instance.
3. **Terms (§11, §20 addendum).** Plain words introduce an idea once, the standard term is attached with its glossary ID, and from then on the Note uses the term. Replace plain stand-ins that linger after the term exists ("list of numbers" → vector, "single number" → scalar, "table of numbers" → matrix, "the spread" → variance or standard deviation, "the guess" → prediction, "the setting" → hyperparameter, "the shift" → bias or intercept, "the bend" → curvature); these are examples, find the rest.
4. **Statements say what they are about (§20).** Each names its object when two are on show (function or its derivative, input or output, loss or gradient, probability or its log, sample or population, prediction or score); the type word is right (scalar, vector, matrix, function, distribution); shapes and counts match what is shown; hidden conditions are stated. A sentence a beginner can reasonably read as false is an error.
5. **Abstract statements get an instance (§15 addendum 2)** in the same sentence or the next.
6. **Steps (§15).** One operation per display line; no calculation inside a sentence. Run `tools/find_inline_calc.py` on the Note; it must print "0 found" (or only unsplittable matrices).
7. **Links (§17).** Every link to another Note points at the section that teaches the idea (`tools/section_links.py --headings <target.md>` lists anchors) and its text is the idea, not "the X Note". Rewrite the sentence so it reads naturally. Run `tools/section_links.py --check <Note.md>`: 0 broken, 0 without a section, 0 with "Note" in the text.
8. **Filler (§18, filler only).** Cut filler words that add nothing ("note that", "in fact", "actually", "essentially", "it is worth noting", "let us", trailing ", highlighting…" clauses). Keep the word when it does work ("clearly the same digit" = visibly; "the part we actually measure" = in contrast to the population). **Leave puffery as it is** (the user chose this). `tools/find_puffery.py` lists candidates; judge each.

## Keep
Every correct fact, number, experiment, gotcha, Extra box and building block (§14). No new depth, caveats or trivia. Numbers must still match the executed notebook.

## Figures you add or change
Our own code; Plotly frames → GIF + `_frames.png`, Manim for geometric motion (long renders on topgro via `tools/remote_run.sh`), TikZ for still structure; never matplotlib or seaborn. Look at the frames grid and the PDF page of every new figure.

## Checks per Note
`tools/build.sh <Note folder>` prints Built; `python tools/github_math.py --check <Note>.md` clean; `grep -nP "[\t\x08\x0c\r]" <Note>.md` empty (edit with the Edit tool; a Python `\t` eats `\times`); `tools/find_inline_calc.py` and `tools/section_links.py --check` as above. Keras notebooks whose numbers a Note quotes re-run on the laptop CPU only.

## Do not touch
git, `glossary.md` (read only; list new terms in your report), `course_map/`, `tools/`, `docs/`, `site/`, and any Note not on your list. No background agents.

## Report (as text)
Per Note, a short list: issues found by kind (figure, symbol, term, statement, example, step, link, filler) with one line each on the fix. Then anything left and why, and any new glossary terms needed.
