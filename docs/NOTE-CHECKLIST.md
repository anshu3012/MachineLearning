# Note checklist: a Note passes only when every item is yes

Every agent that writes, edits or reviews a Note checks every item below for each of its Notes. Each item is one rule; the detail is in `docs/NOTE-RULES.md` (§ numbers). Answer each with **yes**, **fixed** (what changed) or **no** (why it could not be fixed here). Any **no** means the Note does not pass. A new rule becomes a new item; it is never folded into an existing one.

## Tools
1. `find_inline_calc.py` prints 0 found (§15).
2. Every `find_puffery.py` hit is read (§18).
3. `section_links.py --check` shows 0 broken (§17).
4. `github_math.py --check` is clean (§7).
5. `build.sh` prints Built when figures or maths changed (§6).
6. The notebook runs end to end, seeded, and the Note's numbers match its output (§4).

## One story
7. The Overview says what works so far, what still breaks (on the shared example) and what this Note adds (§25).
8. The opening names the problem in concrete words with numbers (§25).
9. Each section's first line names its part of that problem, in the opening's words (§25).
10. When a result fixes a part, the text says so with the opening's numbers (§25).
11. Each section opens from where the last one stopped (§27).
12. Each section ends by handing over: what it solved, what is still missing (§27).
13. One running example carries through; a new example gets one line of why (§25, §27).
14. A result reused from an earlier section is named and linked, not explained again (§27).
15. Every subtopic earns its place, or is moved or cut (§27).
16. Reading only the first and last line of every section tells the whole story (§27).
17. The Summary's first bullet answers the opening question with its numbers (§25).
18. The Summary ends with what is now possible and what is still missing, which is the next Note (§25).

## Why before what
19. Each idea opens with the problem it solves, shown on numbers (§24).
20. Each formula or step says why it holds: derivation, mechanism, or a check at easy values (§24).
21. A question is answered right away, with its figure (§26).
22. Names, definitions and comparisons come after the answer (§26).

## Simple first, then technical
23. Each section climbs: plain words with a picture, the standard term, the mechanism on the Note's numbers, the formal version, then an optional Extra (§11).
24. No section opens with a formula or jargon (§11).
25. No section stops at plain words when a formal version exists (§11).
26. A beginner can read up to the formula and already know what it will say (§11).
27. The teaching path follows the best beginner source, not the textbook's order (§11).
28. Formal steps and claims are tied to the textbook with citations (§11).
29. Evidence is layered: Key point, then the picture or worked example, then details (§5).
30. Show before telling, with an everyday analogy for the why (§5).

## Terms
31. Plain words first, then the **term** with its G-ID, then only the term (§10, §20).
32. No invented stand-ins such as "the boundary" or "knobs" (§10).
33. First use in each later section: the term with its plain meaning (§20).
34. A term appears only after it is explained here, or linked to where it is explained (§20).
35. Every new term is in Key terms and `glossary.md` (§10).
36. A definition says what the thing is and what it does, in one or two sentences (§23).
37. Each statement names its object: the function or its derivative, a sample or the population (§20).
38. The right type word: number, vector, matrix, function, distribution, set (§20).
39. Shapes and counts match what is shown (§20).
40. No hidden conditions: a claim true only in one case names the case (§20).
41. No sentence starts with a vague "It", "This" or "That" (§2).
42. "Feature", "target" and "observation" are used; "column" and "row" only for a table (§2).

## Step by step
43. A symbol is defined before use, with a value: "f(2, 3) = 13" (§15).
44. Set and space symbols (ℝ², ∈, ∑) are explained with a small instance (§15).
45. One step per line; calculations are display lines or tables (§15).
46. No maths inside sentences; inline maths only names one symbol already defined (§15).
47. Display lines fit a phone: about 40 characters, split at "=" (§15).
48. Every abstract statement has a concrete example right where it appears (§15).
49. Before the formula that first uses them, each symbol has its own bullet: what it is, its unit, its value (§28).
50. A section or Key point that reuses a symbol says again what it is, or links its list (§28).
51. A symbol in a caption, heading or Key point is defined right next to it (§28).
52. Derivations are plain maths: numbers first, paired with the same steps in symbols, one move per line, no narration (§15).
53. Maths renders on GitHub: `\thinspace`, `\lbrace` and the like; no `%`, `_`, `&` or `#` inside maths (§7).

## Figures and animations
54. Each key idea or term has a figure or animation (§10).
55. The text says what to look at and what to conclude (§15, §19).
56. An unfamiliar visual code is built up first, such as the surface before its contour map (§16, §19).
57. Detail stays next to its figure (§21).
58. Text inside a figure or animation matches the body; every `_frames.png` is read (§21).
59. Hidden scaling is stated (§21).
60. Each figure number points at the right figure (§21).
61. The text points into an animation by stage or frame name, never by grid position (§21).
62. Anything that happens over time, in steps, in a loop or in a sequence is an animation, not a still (§29).
63. Each animation sits next to its text, uses the Note's numbers, holds its last frame and has a frames grid (§29).
64. Figures use Plotly, TikZ or Manim, never matplotlib, with the tool picked per figure (§2).

## True
65. Every claim rests on the transcript, a checked source, the Note's own data or a derivation (§3).
66. No "open question", "unclear" or "could not source": search harder, or fix the claim (§3).
67. Short citation tags in the text, full references in Sources (§3).
68. Intuitions may simplify but point the right way (§3).
69. Experiments show the principle as the books state it, with the conditions stated (§4).
70. Real data where possible; toy data only when no real dataset works (§4).
71. One change at a time; seeds averaged; no number faked or cherry-picked (§4).
72. Exceptions only when a cited book teaches them, labelled (§4).

## Consistent
73. The running example keeps its numbers; a change is stated (§21).
74. A fact stated twice agrees (§21).
75. A symbol keeps one meaning; a unit keeps one meaning (§21).
76. A number agrees with the section it links to (§21).
77. Text and figure report the same run (§21).
78. Paired numbers name each side; every display line names its quantity (§21).
79. Rounded numbers reproduce the arithmetic shown: 6.26 / 0.029 is 216, not 215, so write 0.0291 (§21).
80. Nothing points at content that is not there (§26).
81. Every file the Note names exists; a named statistic is the one computed (§21).
82. Code examples give the output the text says (§21).
83. A reason given for a result matches the model's internals (§21).
84. The Key point is one or two sentences, agrees with the Note's examples and keeps its conditions (§21).

## CampusX
85. CampusX and other sources never contradict (§13).
86. The clearer explanation leads; the CampusX one is never dropped (§13).
87. A new angle from either side is kept as "another way to see it" (§13).
88. Where CampusX is wrong on a point that matters, the Note teaches the correct version without narrating the video (§21).

## Scope
89. Each Summary point says what and why ("so …" or "because …") (§22).
90. The depth is the beginner level of the source video (§14).
91. Only errors that would mislead a beginner on the core idea are fixed; no nitpicks (§14).
92. No caveats or proofs added only to defend against niche objections (§14).
93. No proof above beginner level when a figure already shows the answer (§26).
94. Tables and summaries use only ideas the Note explains (§26).
95. Gotchas, advanced material and building blocks are kept (§14).

## Links
96. One owner per concept; other Notes recap in one line and link (§2).
97. Links go to a section anchor (§17).
98. Link text is the idea, never "Note" (§17).
99. Link text does not change what the sentence says (§21).
100. Ownership points the right way: a later Note is never named as the definer (§21).

## Voice and Sources
101. Textbook "we" voice; no video, teacher or course narration (§2).
102. Plain English, short sentences, one idea per paragraph; "rupees", never ₹ (§2).
103. No puffery, filler or vague sources (§18).
104. A list for three or more parallel items (§9).
105. Full subject names: "Maths (MA)", "Machine Learning (ML)" (§2).
106. Sources start with **Built from**, then **Other references** (§8).
107. Simple words in a professional register: precise standard terms and textbook sentences, never chatty or colloquial phrasing ("try holding", "is short", "the two meet", "the ramp's damage"); simple is not casual (§2).

## Report format
Per Note, one numbered line per item: `31 fixed: 14 "bell" → "Gaussian"`, `58 no: Figure 3 image says "bell" (needs a figure rebuild)`. End with **PASS** or **NOT PASS**.
