# Task (topgro): lists and plain-words-with-standard-terms, for the Notes in docs/visual-audit/lists-sweep.txt

You work in `~/campusx` on topgro, a copy of the project. **No git.** **Do not start background agents.** This headless session ends when you reply. Do the work yourself, Note by Note, and reply only when every Note in the list is done.

## Read first
`docs/NOTE-RULES.md`, especially:
- **§9 Lists, not list-paragraphs**;
- **§10 Simple words, standard terms, pictures that illustrate**.

The model passage is §3 of `1026-regularization-in-dl/note.md`. Read it but do not edit it.

## For each Note in `docs/visual-audit/lists-sweep.txt` (172 Notes)
1. **Lists (§9).** Turn every paragraph that names 3 or more parallel items into a lead-in plus a list. That covers contents (especially the Overview sentence "This Note explains X (section 3), Y (section 4)…"), steps, reasons, options and cases. Use a numbered list when order matters. Keep section links. Keep real reasoning as short paragraphs.
2. **Terms (§10).**
   - Where a standard term is used, add its glossary ID after it the **first** time it appears in the Note's body: "**learning rate** (G-1068)". Look the ID up with `python3 tools/merge_glossary.py --id "<term>"`.
   - Replace informal stand-ins with the standard term, glossed in simple words. Examples: "the boundary" → "the decision boundary (G-555)"; "draws a line" → "defines a hyperplane"; "pieces" → "segments"; "knobs" → "parameters" or "hyperparameters".
   - Rewrite any vague sentence that sounds like an explanation into a short step-by-step mechanism, backed by the Note's own data or cited source.
   - Do **not** add new claims or facts. Do **not** change numbers, maths, code, tables, captions, Sources or Key terms. Leave the "> **Key point:**" lines on one line.
3. **Build.** `CAMPUSX_ENV=~/miniforge3/envs/campusx tools/build.sh <folder>` must print "Built"; its PDF text check guards against lost text. If Plotly needs Chrome, use the `BROWSER_PATH` trick from `docs/remote/cnn-practice-report.md`.

Touch only `note.md` files of the listed Notes.

## Report
Write the report to `docs/remote/style-sweep-report.md`, with:
- the Notes changed;
- the counts of paragraphs turned into lists, terms tagged with IDs, and vague passages rewritten (quote 5 before/after examples);
- the build failures.
