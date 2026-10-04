# Task: final check of a block of Notes

Every Note has just been through several passes (visuals, teaching path, glossary). This is the last, light pass. Read `docs/NOTE-RULES.md` in full first (§13 and §14 matter most). Change as little as possible. No git, no glossary edits, no background agents, no new figures unless a fix needs one. Do not re-run notebooks.

For each Note in your list, do these four checks:

1. **Transcript check (only ML Notes numbered 1–81).** If `transcripts/NNN.whisper-en.txt` exists, read it in full and compare it with the Note. These Notes were first written from garbled Hindi auto-captions, so look for:
   - a core idea the Note states differently from the video (apply the §14 test before changing anything; fix only with a source, the Note's data or a derivation);
   - teaching content the video has and the Note lacks: an analogy, a worked example, a gotcha, a building block, an angle (§13). Add it in the right section, in the Note's voice, briefly.
   Skip trivia. If the file does not exist, say so in the report.
2. **Depth sweep (§14).** Find caveats, Extra boxes and sentences whose only job is a niche correction: a date, a rounding, a convention difference, an obscure edge case, a slip in a video that the Note does not repeat. Remove or shorten those. Never remove gotchas, advanced material, formal versions, derivations or building blocks; when unsure, keep.
3. **Cross-Note references.** For every place the Note cites another Note's "Figure N" or "Section N", open the target Note and check the number still points at the right thing (many Notes were renumbered). Fix wrong numbers. Also check the Note's own "Figure N" references against its figure order.
4. **Build.** If you changed the Note: `tools/build.sh <folder>` prints "Built" and `python tools/github_math.py --check <folder>/note.md` is clean.

Python: `/home/anshu/miniforge3/envs/campusx/bin/python`, `PYTHONNOUSERSITE=1`. Touch only the Notes on your list (you may read any file).

Report as text, short: per Note one line (no change / what changed). Then three lists: content added from transcripts; things removed under §14 (each with one line saying what it was, so the user can object); reference numbers fixed. Notes with no Whisper transcript.
