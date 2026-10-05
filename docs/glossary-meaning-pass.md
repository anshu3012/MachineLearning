# Task: make every glossary meaning say what the term is and what it does (NOTE-RULES §23)

Read `docs/NOTE-RULES.md` §3, §10, §11, §14, §18, §20, §21 and §23 first.

You get a range of rows of `glossary.md` (by G-ID list in a file). For each row:
1. Find where the term is explained: `grep -rn "(G-N)" MA ML DL --include=*.md` (also `G-N;` / `G-N,` inside brackets). Read that part of the Note (the "First explained" Note first; if it only mentions the term and another Note actually explains it, use that one).
2. Judge the meaning. It is fine if a reader who taps it learns **what the thing is** and **what it does / why it is used**. It fails if it only says where it sits ("the step after…"), only gives a formula or symbol, only gives a synonym, or is so terse a beginner cannot tell what it is.
3. If it fails, write a new meaning: one or two short plain sentences, simple words first, standard words after; a formula only after the plain meaning. It must agree with the Note (§21) and add no claim the Note or a checked source does not support (§3). Keep `$...$` maths valid; no `|` characters (it is a table cell); no newlines.
4. Also give the section that explains the term: `<Note path from repo root>#<anchor>`, where the anchor is the heading slug computed by `python3 -c "import sys; sys.path.insert(0,'tools'); from section_links import slug; print(slug('5.2 Add and norm'))"`. Give it for **every** row in your range, failing or not.

Do not edit any file except your output file. Do not touch git.

Output: write a JSON file (path given) mapping each G-ID to an object: `{"where": "DL/.../DL-081-....md#52-add-and-norm", "meaning": "<new meaning>"}`; leave out `"meaning"` when the old one is fine. Validate it with `python3 -m json.tool`. Report: counts (rows, rewritten), and any row where the term is explained nowhere (list them).
