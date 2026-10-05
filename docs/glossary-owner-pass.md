# Task: point each glossary term at the section that teaches it

The glossary's link ("First explained") was set to the first Note that listed the term in its Key terms. That Note often only mentions the term, while another Note has a section that teaches it (user, 2026-10-05: ML-003 owned PCA although ML-046 teaches it). The site's tap-box says "Explained in: <that section>", so it must be the place a beginner learns the term.

For each candidate line (`G-ID | term | current Note # section | named in: other Notes`):
1. Read the current section, and the sections in the "named in" Notes whose heading or title names the term (grep the Notes for the term and its `(G-N)` code).
2. Decide which section **teaches** the term: it says what it is and how it works or why it is used, as its own topic (a heading named for it, or a paragraph built around it). A passing mention, a code line, or a one-clause gloss on the way to something else does not teach it.
3. If the current section teaches it, keep it (prefer the earlier Note when both teach it properly). Otherwise choose the teaching section.

Output: a JSON file mapping only the G-IDs to move, to `"<Note path from repo root>#<anchor>"` (anchor = `slug(heading)` from `tools/section_links.py`; check it exists). Validate with `python3 -m json.tool`. Edit no other file; no git. Report: number checked, number moved.
