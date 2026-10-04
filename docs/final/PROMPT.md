# Final pass: instructions for each final-pass agent

You are doing the final quality pass on study Notes in /home/anshu/campusx. The Notes were already audited for unsupported claims; see docs/audit/report-*.md for what changed. Your folder list is `docs/final/list_<k>`.

First read /home/anshu/campusx/docs/NOTE-RULES.md (all the user's rules) and docs/STYLE-naming.md.

## For every Note in your list, check and fix these six things

1. **The lesson matches the data.** Every experiment, table and figure must support the principle the Note teaches, as the books state it. Look for results that contradict the lesson: "no gain", "luck", "chance", "did not help", "worse than expected", a regularizer that does nothing, a better method losing. Redesign any such experiment as NOTE-RULES §4 says: real data first, the right conditions, seeds averaged quietly. Then re-run the notebook, update every number and figure, and state the conditions.

2. **Simple, layered presentation.** Each section must lead with the plain idea (the Key point), then the picture or number, then the details. Find places where evidence crowds out teaching:
   - long statistics in the main text;
   - several caveats before the idea;
   - jargon used before it is defined;
   - an advanced idea that no earlier Note teaches.

   Rewrite them to be layered and intuitive: add an everyday analogy for the "why", and move details into an Extra box. **Do not delete evidence.** Re-present it instead.

3. **Naming rule.**
   - Rewrite sentences that start with a vague "It/This/That" pointing back at an idea, so they name the thing.
   - Where the text means a variable or a record of a dataset, use **feature**, **target** and **observation**, defined in plain words at first use in each Note. Example: "a **feature** (an input variable, one column of the data table)".
   - Keep "column" and "row" when the text is about the table, DataFrame or matrix itself: pandas operations, matrix rows and columns in linear algebra, and so on.
   - Do not change code, code comments or quoted output.

4. **Citations are real.** For every entry under Sources, confirm that the work exists and says what the Note cites it for. Use WebSearch or WebFetch, or local copies in `reference/` (MML text extracts in `reference/maths-sources/`).
   - Replace weak sources with a textbook, paper or official doc: Wikipedia, a blog, an open course text, or anything seen only in a search summary.
   - If no real source can back a claim, remove the claim, and list it in your report.
   - Make sure each citation tag in the text has an entry under Sources.

5. **Sources format.**
   - Every Note that cites anything has a numbered `## N. Sources` section just before `## N+1. Key terms`. Renumber the headings so they run in order.
   - Long URLs must not run off the page: shorten them to the site plus page name, or let them wrap.
   - Notes that cite nothing need no Sources section.

6. **House rules.** Never mention a video, the teacher, "he", the course, CampusX, YouTube or "Video N". This applies inside Sources too: cite StatQuest or 3Blue1Brown by author and site, for example "Starmer, J., StatQuest, statquest.org". Write "rupees", not the rupee sign. Never use matplotlib.

## Mechanics
- Python: `/home/anshu/miniforge3/envs/campusx/bin/python`, with `PYTHONNOUSERSITE=1`.
- Experiments run on CPU (`CUDA_VISIBLE_DEVICES=""`), because other agents share the GPU.
- After editing a folder, rebuild it with `tools/build.sh <folder>`, which must print "Built".
- Edit only folders in your list. Do not touch git, `glossary.md`, `course_map/`, `tools/` or other folders.
- You may fork yourself to split the list. Check every fork's output yourself.

## Report
Return the report as text in your final message; writing under `docs/` may be blocked for subagents. Include:
- per Note: what changed under each of the six checks, or "no change";
- every redesigned experiment: old result → new design → new result, and the book it now matches;
- every citation replaced or removed, and why;
- an UNRESOLVED list: claims removed because nothing backs them;
- totals, and the 3 most important fixes.
