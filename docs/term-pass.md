# Task: every technical term explained before use, glossed per section, linked to its explanation (NOTE-RULES §20 addendum)

The user's decision, after asking "what's the difference between our repo and a book?": the repo differs in **order and support**, not in avoiding terms. Read `docs/NOTE-RULES.md` in full, especially §11, §17, §19, §20 and the §20 addendum.

## The rule, for every technical term in every section of the Note
1. **Explained before used.** A term may appear only after the reader has met its explanation: in this Note (earlier), or in another Note that the first use links to.
2. **Where this Note explains it:** plain words first, then the term in bold with its glossary ID ("a list of numbers like (2, 3) is a **vector** (G-2081)").
3. **First use in each later section:** the term with its plain meaning beside it ("a vector (a list of numbers)", "the gradient (the list of slopes, one per input)"). After that, within the same section, the term alone.
4. **Explained in another Note:** at the first use in this Note, link the term to the exact section that explains it, with the plain meaning beside it. Look up the section in `docs/term-owners.tsv` (columns id, term, owner, anchor, link; run `tools/term_owners.py <G-id>` for one row). If the owner or anchor there is wrong (the section does not actually explain the term), find the section that does with `tools/section_links.py --headings <Note.md>` and link that; list the wrong row in your report.
5. **A plain stand-in that lingers** after the term was introduced ("the spread" for standard deviation, "the guess" for prediction, "a list of numbers" alone where "vector" was already taught in this section) becomes the term. A plain description used as the first introduction, before the term, is correct and stays.
6. **Wrong plain words** for the object ("one number" for a vector) are errors (§20): fix them.

A "technical term" is any word with a glossary ID, any word a textbook or library doc would use as a name (vector, gradient, epoch, hyperparameter, logit, residual, variance…), and any abbreviation. When unsure whether a word is technical, gloss it once.

## Keep
Every fact, number, figure, Extra and gotcha (§14). Do not change maths or figures. Do not touch the generated "Where this fits" block. No filler or puffery edits.

## Checks per Note
`tools/build.sh <Note folder>` prints Built; `python tools/github_math.py --check <Note>.md` clean; `grep -nP "[\t\x08\x0c\r]" <Note>.md` empty (use the Edit tool); `tools/section_links.py --check <Note>.md` reports 0 broken.

## Do not touch
git, `glossary.md` (read only), `course_map/`, `tools/`, `docs/`, `site/`, images, notebooks, and any Note not on your list. No background agents. Helper scripts go in `/home/anshu/.claude/jobs/8c1c0992/tmp/<your-group>/`.

## Report (as text)
Per Note: number of terms glossed per section, terms newly linked to their explaining section, lingering stand-ins replaced, wrong plain words fixed (one line each), and any wrong rows in `docs/term-owners.tsv`.
