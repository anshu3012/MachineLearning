# Claims audit: instructions for each audit agent

You are auditing study Notes in /home/anshu/campusx. These are beginner ML, maths and DL Notes. Each `<ID>-<topic>/note.md` was written from a lecture transcript.

Transcripts:
- ML Note N: `transcripts/NNN.*.txt` (three digits).
- Maths session Mnn: `transcripts/Mnn.*.txt`. The Note's ID is 200 + 10 × session + part. See `docs/maths-plan.md`; the book-based gap Notes 600–622 cite the MML book.
- DL Note 10NN: `transcripts/DNN.whisper-en.txt` or `dl_map/transcripts/0NN.*.txt`.

## The rule (from the user; it is not negotiable)
Every statement in a Note must rest on one of these:
- **TRANSCRIPT**: the lecture says it.
- **SOURCE**: a real textbook, paper or official doc that you have verified exists and says this. Check it with WebSearch or WebFetch, or with a local copy in `reference/`. A citation that names a work which does not say this, or a work that does not exist, counts as a failure.
- **DATA**: output of the Note's own notebook or figure script, from an experiment that actually tests the claim.
- **MATH**: a derivation or standard definition shown in the Note.

An explanation that rests on the writer's reasoning alone ("this is probably because…", "Adam rescales… so…") is **UNSUPPORTED**, even if it sounds right.

## What to check
Check every Extra box (`> **Extra:**`), every sentence that goes beyond the transcript, every causal explanation of a result ("because", "this is why", "so"), every hedge ("probably", "likely", "seems", "perhaps") and every citation or number attributed to someone else.

## What to do with each UNSUPPORTED or wrongly cited claim
The goal is not just to show the data. The Note must also say what the data **means**, and that meaning must be grounded. Work in this order:
1. **Find the explanation in a real source** (textbook, paper, official docs) and cite it: author, title, year, section or page. Then tie it to the Note's own numbers, as in "this matches X: …".
2. **Or derive it with maths.** Show the derivation in the Note (for example, write out the update rule and show what it does to a weight).
3. **Then test it with data.** Design the experiment so it can confirm or refute the explanation; one that merely repeats the observation does not count. For example, if the claimed cause is the optimizer, change only the optimizer and compare. Run it on CPU only (`CUDA_VISIBLE_DEVICES=""`, conda env `/home/anshu/miniforge3/envs/campusx/bin/python`, `PYTHONNOUSERSITE=1`). Write the result and what it means into the Note.
4. **Last resort:** if no source, derivation or test grounds it, take the claim **out of the Note entirely**. Do not leave open questions or "the cause is unclear" in a Note. List the removed text under "UNRESOLVED (removed from Note)" in your report so the user sees it.

Never replace one unsupported explanation with another. Do not change anything that is already backed.

## Scope and limits
- Edit only the `note.md` files (and, only if an experiment needs it, the notebook and figures) of the folders in your list.
- After editing a folder, rebuild it with `tools/build.sh <folder>` and make sure it prints "Built".
- Do not touch git, the glossary, `course_map`, other folders or the tools.
- Keep the house style: "we" voice; never mention the video, the teacher, the course or YouTube; plain simple English; "rupees", not the rupee sign.

## Report
Write `docs/audit/report-<k>.md`. It needs one row per finding:

Note | quote (short) | verdict (UNSUPPORTED / WRONG CITATION / WRONG FACT) | action (sourced: <ref> / tested: <result> / reworded / unresolved)

Also give the counts per Note, including the Notes that had no problems.

Return a short summary: the number of Notes checked, the findings by verdict, the 3 worst findings, and any Note you could not fix.

## Learning comes first (from the user)
The project exists so that a beginner can learn. Evidence keeps the teaching correct, but it must not crowd it out.
- **Explain first, in plain words.** Say what the result means and why, simply. Put the evidence behind it, not in front of it.
- **Short citation in the text, full reference at the end.** In the text, use a short tag such as "(Grinstead and Snell, Thm 6.2)" or "(ESL §15.2)". List each full reference once, under a `## Sources` heading at the end of the Note, just before the Key terms. Never put a full title, edition and year mid-sentence.
- **Keep long proofs and experiments out of the main text.** Put a long derivation or an experiment's details in an Extra box or the notebook, and give a one-line takeaway in the main text.
- **Don't add material only to show evidence.** If an unsupported side remark is not needed for learning, removing it is better than building a heavy defence of it.
- The Note must not get harder to read. After editing, re-read the section as a beginner would.

## Intuitions are welcome (from the user)
"Even if an intuition is slightly off from theory, it's okay. As long as the intuition is right and it gets its point across."
- **Keep simplified intuitions, analogies and pictures** that point the right way, even if they are not exact. Examples: "large and small values tend to cancel" for the CLT, or "a company where no employee can rely on one colleague" for dropout. Do not remove them or bury them under caveats. Label one "the intuition:" if that helps.
- **Remove or fix an intuition only if it points the wrong way**, that is, if it would leave the learner believing something false.
- **The evidence rule still applies to facts and to explanations of results:** numbers, history, "X happens because Y", and claims about what an experiment shows.
- Do not remove true, well-known background either (for example, that Gosset was a chemist at Guinness). Give it a short citation instead.

## Right data, right results (from the user)
"Just having true data is not enough. Having the right data is the key and the right results."

Every experiment in a Note must **demonstrate the principle the Note teaches**, as the textbooks state it. If the Note's data contradicts the textbook principle, do not write the contradiction into the Note. Examples of contradictions: a regularizer that does not help, early stopping "only luck", pairing that "gains nothing", tuning no better than the default.

Instead, **redesign the experiment** so it sits in the conditions where the book says the principle holds. Change the dataset, the size, the noise, the model capacity or the settings, and average over several seeds. Then:
1. state those conditions plainly in the Note;
2. tie the result to the book;
3. re-run the notebook and update every number, figure and table.

Teach an exception only if a cited book or paper teaches it, label it clearly, and never make it the main result. Never fake or hand-pick a lucky number: choose honest conditions and use enough seeds.

If you already reworded a Note to "the data shows the principle fails here", redo that experiment this way.

## Keep it simple (from the user)
"In making it right, don't lose the simplicity. The key idea of this project is to build intuition and learning, from basic to advanced."

A redesigned experiment must be both **correct and simple**:
- **One clear picture or table that shows the lesson at a glance.** **Prefer a real dataset** (for example Titanic, Iris, MNIST, California housing, or a dataset an earlier Note already uses) whenever one shows the principle clearly. Build a toy dataset (for example with sklearn's `make_*` generators) only when no real dataset shows the principle cleanly.
- **Change one thing at a time.** Use a few lines of code and a short description.
- **Average over seeds quietly.** Do it in the notebook and give one averaged number in the Note. Put no "30 splits" tables in the main text; mention the averaging in one short clause.
- **Basic to advanced.** Use only ideas the learner has already met in earlier Notes. If an experiment needs a newer idea, such as selection bias or correlation between trees, either link to the Note that teaches it or choose a simpler experiment. Do not teach a new advanced idea inside a side experiment.
- **The intuition first.** The main text gives the idea in plain words, then the picture or number that confirms it. Caveats, conditions and extra statistics go in one short Extra box, or are left out.
- **Real data first, toy data as the fallback.**
- **When in doubt, simpler.** A clean small demo of the true principle beats a thorough but confusing one.

## Evidence is welcome; the presentation must be simple (from the user)
"Having too much evidence is not a problem, but presenting that evidence in a non-simple way or a non-intuitive way is the problem."

Do not cut evidence to make a Note simpler. Present it simply instead:
- **Layer it.** Lead with the idea in one plain sentence (the Key point), then the picture or number that shows it, then the details for readers who want them.
- **Show before you tell.** A figure, a small table or a worked example with real numbers is better than a paragraph of statistics.
- **Use everyday language and an analogy for the "why"**, then give the source tag.
- **Use one idea per paragraph.** Use short sentences, and define each new term before using it.
- **Use extra evidence well.** A second experiment or a supporting table is welcome when it makes the idea clearer. Place it after the main idea, never before it.
- **Example (Note 99):** a section on selection bias can stay if it opens with a plain picture. For example: "If we try 90 settings and keep the best score, that score is a little lucky, like picking the tallest of 90 random people." Then come the numbers and the source.
