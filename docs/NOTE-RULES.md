# Rules for every Note (writing and review)

These rules collect everything the user has decided. They apply to every Note, every figure and every experiment.

## 1. Purpose
The project exists so that a beginner can **learn**, building intuition from basic to advanced. Every rule below serves that purpose.

## 2. Voice and style
- **Voice:** a professional textbook in the "we" voice. Never mention a video, the teacher (including by name in examples, such as "Nitish"), "he", the course, CampusX, YouTube, or "Video N". No narration about a lecture, and no fluff.
- **Order:** the transcript drives the content and its order, invisibly. Material beyond the transcript is marked as an Extra box, or sourced in the text.
- **Language:** plain, simple English. Short sentences, one idea per paragraph. Write "rupees", never the ₹ sign.
- **Naming** (see `docs/STYLE-naming.md`):
  - No sentence starts with a vague "It", "This" or "That" pointing back at an idea; name the thing instead.
  - Use **feature**, **target** and **observation**, each defined in plain words on first use. Use "column" and "row" only for the table, DataFrame or matrix itself.
- **Figures:** Plotly, TikZ or Manim only, never matplotlib. Pick the tool per figure, for a reason: a chart → Plotly, a still diagram → TikZ, an animation → Plotly frames to a GIF, or Manim.
- **No duplication:** each concept has one owner Note. Other Notes give a one-line recap and a link.

## 3. Evidence
Every fact and every explanation of a result must rest on one of these:
- **the transcript;**
- **a real source** (book, paper or official docs) that you have opened and checked says this;
- **the Note's own data**, from an experiment designed to test the claim;
- **a maths derivation** shown in the Note.

**Explanations:**
- Reasoning alone is never enough, but the Note must still explain what the data **means**, grounded in the sources above.
- If nothing grounds an explanation, remove it from the Note and list it in your report. Never leave "open question" or "unclear" wording in a Note.

**Citations:**
- In the text, use only short tags, such as "(ESL §3.4)".
- List the full references under `## N. Sources`, just before Key terms.
- An invented or unchecked citation is the same failure as no citation.

**Intuitions:**
- Intuitions and analogies are welcome even when slightly simplified, as long as they point the right way.
- Remove or fix one only if it points the wrong way.

## 4. Experiments: right data, right results
- **Show the principle.** Every experiment must demonstrate the principle the Note teaches, as the books state it. If the data contradicts the principle, redesign the experiment so it sits in the conditions where the principle holds: change the dataset, its size, the noise, the model, the settings or the number of seeds. State those conditions plainly.
- **Exceptions:** taught only if a cited book teaches them, labelled clearly, and never as the main result.
- **Data:** use real datasets whenever one shows the principle clearly (Titanic, Iris, MNIST, California housing, Old Faithful, or a dataset an earlier Note uses). Build toy data only when no real dataset works.
- **Simplicity:** change one thing at a time. Average over seeds quietly in the notebook and give one number in the Note. Never fake or cherry-pick a number.
- **Running:** notebooks run end to end, seeded, and the Note's numbers match the executed output.

## 5. Presentation of evidence
- More evidence is fine. A confusing presentation is not.
- **Layer it:**
  1. the idea in one plain sentence (the Key point);
  2. the picture, small table or worked example;
  3. the details, sources and extra experiments, in an Extra box or later section.
- **Show before telling.** Use an everyday analogy for the "why".
- **Basic to advanced:** use only ideas from earlier Notes, or link to the Note that teaches them.

## 6. Mechanics
- **Build:** `tools/build.sh <folder>` must print "Built". Python is `/home/anshu/miniforge3/envs/campusx/bin/python`, with `PYTHONNOUSERSITE=1`.
- **Size:** keep `data/` under about 1 MB.
- **Leave alone:** do not touch git, `glossary.md`, `course_map/`, `tools/` or other Notes' folders unless told to. Do not write a "Where this fits" box; the map tool adds it.
- **Report:** writing under `docs/` may be blocked for subagents, so return your report as text.
