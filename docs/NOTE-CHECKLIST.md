# Note checklist: a Note passes only when every answer is yes

Every agent that writes, edits or reviews a Note answers these 21 questions for each of its Notes. The detail is in `docs/NOTE-RULES.md` (§ numbers). Answer each with **yes**, **fixed** (what changed) or **no** (why it could not be fixed here). Any **no** means the Note does not pass.

1. **Tools clean?** `find_inline_calc.py` prints 0 found; every `find_puffery.py` hit is read; `section_links.py --check` shows 0 broken; `build.sh` prints Built when figures or maths changed (§6, §15, §17, §18).
2. **One story?** Each section opens from the previous section's gap and ends by handing over to the next; one running example carries through; reading only each section's first and last line tells the whole story (§27).
3. **Tied to the opening problem?** The Overview says what works so far, what still breaks and what this Note adds; each section names its part of the problem; the Summary answers it with the opening's numbers and ends with what is still missing, which is the next Note (§25).
4. **Why before what?** Each idea opens with the problem it solves, on numbers; each step says why it holds; a question is answered right away, with its figure (§24, §26).
5. **Climbs to the formal version?** Each section goes plain words → standard term → mechanism on the Note's numbers → formal version; never opens with a formula, never stops at plain words (§11).
6. **Standard terms?** Plain words first, then the term in bold with its glossary ID, then only the term; no invented stand-ins; each term explained or linked before use (§10, §20).
7. **Right object, right type word?** Each statement names what it is about (the function or its derivative, a sample or the population) with the right type word (number, vector, matrix, function, distribution) (§20).
8. **Definitions say what and why?** Each glossary and Key terms row says what the thing is and what it does; every new term is in both (§10, §23).
9. **Step by step?** Symbols defined with values; one step per line; display lines fit a phone (about 40 characters); no maths inside sentences; every abstract statement has a concrete example (§15).
10. **Figures explained?** Each key idea has a figure or animation; the text says what to look at and what to conclude; unfamiliar visual codes are built up first; detail stays next to its figure; figure text matches the body (§16, §19, §21).
11. **True?** Every claim rests on the transcript, a checked source, the Note's own data or a derivation; no "open question" wording (§3).
12. **Consistent?** Numbers match the notebook; the running example keeps its numbers; a symbol and a unit keep one meaning; nothing points at content that is not there (§21, §26).
13. **Key point right?** One or two sentences; it agrees with the Note's own examples, conditions included (§21).
14. **Experiments show the principle?** Real data where possible, conditions stated, one change at a time, numbers from the executed notebook (§4).
15. **No clash with CampusX?** The two explanations never contradict; the clearer one leads; a new angle from either is kept (§13).
16. **Summary says why?** Each Summary point says what and why ("so …" or "because …") (§22).
17. **Only what is needed?** No orphan subtopics; no proof above the beginner level when a figure already shows the answer; no trivia or depth creep; a building block for a later Note lives in that Note (§14, §26, §27).
18. **Nothing real removed?** Gotchas, advanced material and building blocks stay (§14).
19. **Links right?** One owner per concept, others recap in one line and link; links go to a section anchor; link text is the idea, never the word "Note" (§2, §17).
20. **Voice and Sources clean?** Textbook "we" voice; no video, teacher or course narration; no puffery or filler; lists for three or more items; full subject names; Sources start with **Built from**, then **Other references** (§2, §8, §9, §18).
21. **Symbols listed?** Before the formula that first uses them in a section, each symbol has its own bullet with what it is, its unit and its value; a section or Key point that reuses a symbol from earlier says again what it is or links its list (§28).

## Report format
Per Note, 20 numbered lines: `6 fixed: 14 "bell" → "Gaussian"`, `10 no: Figure 3 image says "bell" (needs a figure rebuild)`. End with **PASS** or **NOT PASS**.
