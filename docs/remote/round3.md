# Task (topgro): Round 3 visuals and style, for the Notes in docs/visual-audit/round3_N.txt (N is given in your prompt)

You work in `~/campusx` on topgro, a copy of the project. **No git.** **Do not start background agents.** This headless session ends when you reply. Do every Note in your list yourself, Note by Note, and reply only when all are done.

Follow `docs/visual-audit/ROUND3.md` exactly, with these topgro specifics:
- **Build:** `CAMPUSX_ENV=~/miniforge3/envs/campusx tools/build.sh <folder>`. For Plotly image export, set `BROWSER_PATH` to Chrome, as in `docs/remote/cnn-practice-report.md`, if needed.
- **Keras runs:** use `CUDA_VISIBLE_DEVICES=` when the Note's existing numbers must reproduce exactly. The GPU is fine for new experiments.
- **Glossary:** do **not** run `tools/merge_glossary.py` and do not edit `glossary.md`. List any new Key terms in your report; they are merged on the other machine. You may *look up* IDs with `python3 tools/merge_glossary.py --id "<term>"`.
- Three other sessions run at the same time on other lists. Touch only your Notes.
- Write the report to `docs/remote/round3-N-report.md`.
