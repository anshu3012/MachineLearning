# Task: give every Summary its "why" (NOTE-RULES §22)

The user: "In summary for each note it says what but not the why." This is a **single pass over the Summary section only** of each Note on your list. Read `docs/NOTE-RULES.md` §22 first, then §3, §14, §15, §20.

## What to do, per Note
1. Read the whole Note (the why must come from it), then its `## N. Summary` section.
2. For each summary point (bullet, table row, sentence) that states only *what*, add one short clause saying *why*:
   - **so …**: what the fact lets the reader do, decide or avoid ("…, so scale the features before KNN");
   - **because …**: the reason the Note shows ("…, because each tree sees a different bootstrap sample").
   Pick whichever the Note supports. One clause, plain words, no new facts, no new numbers.
3. A point that already says why is left alone. Do not rewrite for style.
4. Tables: keep the columns. If rows need a why, add a "Why it matters" column (short cells) or a bullet below the table.
5. The summary's last line ties back to the opening question of the Note (§1 Overview); add one plain sentence only if it does not.
6. Maths: one step per display line, no calculation inside a sentence (§15). Plain symbols like $T$ inside a sentence are fine.

## Keep
- Edit **only** the Summary section. Do not touch headings (no anchor changes), other sections, figures, notebooks.
- Never delete a fact or number from the summary; numbers must match the Note.
- No nitpicking (§14), no puffery, no filler words added.

## Checks per Note
`python tools/github_math.py --check <Note.md>` clean; `grep -nP "[\t\x08\x0c\r]" <Note.md>` empty; `python tools/find_inline_calc.py <Note.md>` 0; `python tools/section_links.py --check <Note.md>` 0 broken. (No build needed: only text changed.)

## Do not touch
git, `glossary.md`, `course_map/`, `tools/`, `docs/`, `site/`, other Notes. No background agents.

## Report (short, as text)
Per Note: number of summary points given a why; any point you could not support from the Note (one line). Nothing else.
