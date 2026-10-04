# Task: hand-designed TikZ mind maps for the Course map

The user rejected auto-laid-out concept graphs as unreadable. Each topic now gets a **hand-designed TikZ mind map**, like the approved example `course_map/mindmaps/dl_training.tex` (look at `course_map/mindmaps/dl_training.png`). Copy its look exactly:
- the shared style `\input{../../tools/tikz-style.tex}`;
- box colours and grey dashed boxes for concepts that belong to another map;
- grouped panels (`fit`, background layer);
- the Note number inside each box as `\nt{N}`;
- a one-line legend at the bottom.

## Rules
1. **Story first.** Pick the layout that tells the topic's story, left to right: for example Problem → Fix → Goal, Raw data → Steps → Ready data, Idea → Method → Variants, or Prerequisite → Concept → Use. Name the columns with `title` nodes.
2. **About 10–15 key concepts per map**, never more than 18, and only the important links. Leave out minor concepts rather than crowd the page.
3. **Links:** every arrow means one relation from `course_map/concepts.yaml`: needs, is a kind of, fixes, used in. Colour each relation consistently and explain it in the legend. Never draw a link that the YAML or the Notes do not support. Read the Notes' Overview and Key points to get the story right.
4. **Connections to other maps:** 1–3 grey dashed boxes for the most important prerequisites or follow-ups in other topics, with their Note numbers.
5. **Readable:** no crossing lines, no text over arrows, no boxes touching, large text (`\large` for box titles). Boxes use plain names from the Notes, with no jargon a beginner has not met yet.
6. **House rules:** never mention a video, the teacher, the course, CampusX or YouTube. Use the "we" voice in any caption.

## For each map
1. Write `course_map/mindmaps/<id>.tex`.
2. Compile it:
   `cd course_map/mindmaps && PATH=$HOME/.local/bin:$PATH pdflatex -halt-on-error -interaction=nonstopmode <id>.tex`
   then convert it:
   `pdftoppm -png -r 110 -singlefile <id>.pdf <id>`.
3. **Look at the PNG yourself** and fix every overlap, crossing or clipped label. Repeat until the map is clean.
4. Delete the `.aux` and `.log` files.

Touch nothing outside `course_map/mindmaps/`. Do not run git.

## Report
Per map, give:
- the id;
- the story layout;
- the concepts shown and the ones left out;
- any link you drew that is not in `concepts.yaml`, with the Note that supports it. Suggest it as a YAML addition; do not edit the YAML.
