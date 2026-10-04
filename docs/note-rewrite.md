# Task: rewrite ML and DL Notes along their teaching paths

Follow `docs/maths-rewrite.md` in full. Every rule there applies. Only these points differ:
- **Your Note's map** is its block in `docs/teaching-paths/` (`ML-001-067.md`, `ML-068-134.md` or `DL-1001-1090.md`), not `docs/maths-sources.md`. Use all six parts of the block: Sources, Teaching path, What the Note lacks, Animation ideas, CampusX vs the others, Contradictions.
- **Transcripts:** `transcripts/teaching-video/<number>-*.txt` (timestamped), `transcripts/NNN.*.txt` (ML) and `dl_map/transcripts/` (DL). Check every beat you use against the transcript text.
- **CampusX is the main path** for these Notes (NOTE-RULES §13). An outside video leads only where the map shows it is clearer; a CampusX angle is never dropped.
- **Fixed depth, no nitpicking (NOTE-RULES §14):** read §14 first. Stay at the beginner depth of the CampusX video. Skip every map finding that is a date, a rounding, an edge case, a convention or a slip in a video the Note does not repeat. Add no new caveats or Extra boxes for such things.
- **Fix only what passes the §14 test** from what the map flags ("What the Note lacks", "Contradictions", and the summary at the top of the map file). Each fix needs evidence under NOTE-RULES §3: a source you opened, the Note's own data, or a derivation. If nothing grounds a claim, remove it and report it.
- **Build the map's animation ideas** for your Notes, unless an existing figure already shows the same thing. Say which in your report.
- **A Note with no outside video** still gets the full pass: the §11 ladder in every section, the standard terms with glossary IDs (§10), and a visual for every key idea and process.

## Notes that just had the visuals pass (lists in `docs/rewrite-lists/`)
These Notes were upgraded hours ago by another pass: new figures and animations, glossary IDs, the §11 ladder. Do not redo or undo that work. Your job is only what that pass did not do:
- compare the Note with its teaching-path block and add the beats, worked examples and visuals that are still missing;
- do the CampusX comparison (§13), using `transcripts/NNN.whisper-en.txt` when it exists;
- apply the §14 test to anything the map flags;
- convert any figure script that still imports matplotlib or seaborn to Plotly, keeping the same data and message.
If a Note already covers its teaching path, say so and move on. A short report line is the right outcome for such a Note.
