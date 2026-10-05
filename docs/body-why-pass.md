# Task: find and fill missing "why"s in the whole Note (NOTE-RULES §3, §14, §22)

The user asked for an audit "for more missing why's, and not just in the summary section". This is **one pass, find and fix together**, over every section of each Note on your list. Read `docs/NOTE-RULES.md` first (all of it; §3, §11, §14, §15, §17, §20, §22 matter most).

## What counts as a missing why
A place in the body where the Note tells the reader **what** to do, choose or expect, and a beginner would ask "why?", but the Note never answers. Examples:
- a step or rule with no reason: "scale the features before KNN", "fit the scaler on the training set only", "drop one dummy column", "use `stratify=y`";
- a choice with no reason: "we use cross-entropy, not MSE", "ReLU in the hidden layers", "learning rate 0.001", "k = 5";
- a result stated with no explanation of what it means or why it happened: "the test score drops", "the tree overfits", "the curve flattens";
- a formula or step whose purpose is never said: "we take the log", "we square the errors", "divide by $n-1$".

Not a missing why (leave alone):
- the reason is already given anywhere in the Note, or in a section the Note links to;
- trivia, edge cases, conventions, history (§14). No depth creep: the reason a beginner needs, at the video's depth;
- arbitrary demo values that the Note does not present as a choice (a `random_state=42`).

## How to fill one
1. Find the reason in this order:
   a. the Note's own content (another section, a figure, a derivation, its notebook output): then just connect it in a plain clause;
   b. a short maths step (§15: one step per line);
   c. a **real source you open and check** says it: textbook, paper, official docs (scikit-learn, PyTorch, Keras), or a reputable tutorial (user, 2026-10-05: "why can't you use a book as a source or a tutorial as a source? ... As long as it's correct"). Free online books are fine: ISLR, ESL, Deep Learning (Goodfellow et al.), d2l.ai, Boyd's Convex Optimization, Penn State STAT courses, scikit-learn user guide, etc.
2. Write it as one or two plain sentences next to the claim ("…, because …" / "…, so …"). Simple words first (§11), the standard term after. Short citation tag in the text, e.g. "(ISLR §2.2)", full reference added to `## N. Sources` (do not renumber sections; add to the existing list).
3. If the summary repeats this point, make its clause agree.
4. Never invent a reason, never cite a page you did not open. "Could not source" is not an answer: search harder. If truly nothing says it, the claim is wrong (§3): correct it to what the sources say, or remove it, and report it. Never delete a true claim, gotcha or building block (§14).
5. CampusX is the baseline (§13): a source must agree with the video's teaching, not overturn it.

## Keep
- Do not change headings (anchors), figures, notebooks, code, or numbers.
- No puffery, no filler, no "it is important to note" (§18). Plain, short.
- Fix only core gaps: the reader would otherwise follow a rule blindly or misread a result. Typically 0–5 per Note; zero is a fine answer.

## Checks per edited Note
`python tools/github_math.py --check <Note.md>` clean; `grep -nP "[\t\x08\x0c\r]" <Note.md>` empty; `python tools/find_inline_calc.py <Note.md>` 0; `python tools/section_links.py --check <Note.md>` 0 broken; `python tools/find_puffery.py <Note.md>` nothing new.

## Do not touch
git, `glossary.md`, `course_map/`, `tools/`, `docs/`, `site/`, Notes not on your list. No background agents.

## Report (short, as text)
Per Note with changes: one line per added why ("§4: why fit the scaler on train only — sklearn common pitfalls"). Then a list of whys you could not source (Note, point). Nothing else.
