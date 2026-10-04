# Rules for every Note (writing and review)

These rules collect everything the user has decided. They apply to every Note, every figure and every experiment.

## 1. Purpose
The project exists so that a beginner can **learn**, building intuition from basic to advanced. Every rule below serves that purpose.

## 2. Voice and style
- **Voice:** a professional textbook in the "we" voice. Never mention a video, the teacher (including by name in examples, such as "Nitish"), "he", the course, CampusX, YouTube, or "Video N" in the body text. The one exception is the **Built from** list in Sources (section 8), which credits the source videos by channel, title and link. No narration about a lecture, and no fluff.
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

## 7. Maths that renders on GitHub

GitHub drops the backslash from `\,` `\;` `\!` `\{` `\}` `\|` `\\` `\%` `\_` `\&` `\#` inside maths. Write `\thinspace`, `\thickspace`, `\negthinspace`, `\lbrace`, `\rbrace`, `\Vert` and `\cr` (row break) instead; `tools/build.sh` converts the first seven automatically. Keep `%`, `_`, `&` and `#` out of maths: write "percent" in words, and put code names such as `max_depth` in code text outside the formula.

## 8. Sources: credit what the Note was built from (user, 2026-10-03)

Every Note's Sources section starts with a **Built from** list: every source the Note was actually built from.
- **Each playlist video:** channel, title, year if known, and its link (https://www.youtube.com/watch?v=ID). Credit the channel ("CampusX"), not the teacher by name.
- **Each 3Blue1Brown, StatQuest or DeepMind/UCL lecture used:** the same format.
- **Each book chapter and paper the Note rests on.**

The **Built from** list is followed by the other references. This is the one place a video or channel is named; the body text still never narrates a video, the teacher, or the course. Why: crediting the origin makes every Note traceable and lets anyone check it against its source.

Format:

    **Built from**
    - CampusX, "<video title>", YouTube, https://www.youtube.com/watch?v=<ID>
    - Sanderson, G. (3Blue1Brown), "<lesson title>", <year>, 3blue1brown.com/lessons/<slug>

    **Other references**
    - <the remaining books, papers and docs>

The **Other references** label is needed: without it, pandoc merges the two lists into one.

## 9. Lists, not list-paragraphs (user, 2026-10-03)

When a paragraph names three or more parallel items, write it as a bulleted or numbered list. That covers a Note's contents, the steps of a method, reasons, options and cases. The commonest case is the Overview sentence "This Note explains X (section 3), Y (section 4), Z (section 5)…": it becomes a short lead-in plus one bullet per item, each with its section link. Use a numbered list when order matters. Keep explanation and argument as normal short paragraphs; don't break real reasoning into fragments. Why: the reader has ADHD, and lists can be scanned.

## 10. Simple words, standard terms, pictures that illustrate (user, 2026-10-03)

The user said: "boundary? What boundary. So unprofessional… the student will never learn official terms or be able to convey it in interviews", "be more professional and still keep it simple", and "using pictures to explain words is helpful". When I wrote that a picture "carries the explanation", the user corrected it: "No it does not. The words explain the picture."
1. **The words explain.** The flow is in simple language, as a person would explain it. Every explanation gives the mechanism step by step. A sentence that only sounds like an explanation is not allowed, for example "a thousand neurons have the capacity to combine a thousand lines".
2. **Attach the standard term where the idea appears,** with its glossary shorthand. For example: "The gradient takes small steps towards the minimum. These steps are the **learning rate** (G-118)." Use that term every time after that. Never let an informal stand-in, such as "the boundary", "draw a line", "pieces" or "knobs", be the only wording.
3. **Pictures illustrate the words:** each key idea or term gets a figure or animation that makes the words concrete. The text points to it ("in Figure 2, the dashed lines are the neurons' hyperplanes").
4. **The glossary holds the precise definition.** Every new term goes into Key terms and `glossary.md`.

## 11. Simple first, then technical (user, 2026-10-03)

The user wants "simple-language explanations leading up to advanced technical". Every section climbs the same ladder:
1. **The idea in plain words,** with a picture or animation that illustrates it.
2. **The standard term,** attached where the idea appears (§10).
3. **The mechanism, step by step,** on a small worked example with the Note's own numbers.
4. **The formal version:** the formula, the derivation or the exact definition, with every symbol named.
5. **Extra** (optional): the deeper or advanced point.

Never open a section with the formula or the jargon. Never stop at the plain words when the topic has a formal version that a practitioner must know.

## 12. A named example is a rule for every Note (user, 2026-10-04)

When the user points at one Note or one topic (the Hessian, EM, Note DL-026), that is an example of a kind of problem, not the only case. The user said: "I don't have the time to go over 100 of files and tell you each and every single instance." Every fix applies to every Note (ML, maths and DL): check each Note for the whole kind of problem. Standing kinds, from the user's examples so far:
- hard to read: no plain-words start, jargon without a term and glossary ID, no step-by-step mechanism (§10, §11);
- missing visuals: a process with no animation, a key term with no figure;
- not following the best beginner teaching path: the order, analogies, worked examples and visuals of the source videos (CampusX, 3Blue1Brown, StatQuest, Khan Academy) are not used.

## 13. CampusX is the baseline; other sources must agree with it (user, 2026-10-04)

The user said: "make sure none of it clashes with campus x explanations. And also check if campus x intuition or explanation clearer or if campus x adds a new angle". For every concept that both the CampusX video and an outside source (3Blue1Brown, StatQuest, Khan Academy, a book) explain:
1. **No clash.** The Note never teaches two explanations that contradict each other. If CampusX and the other source disagree, check a cited source, keep the correct one, and correct the other in the text only with that citation. List every such case in the report.
2. **Pick the clearer explanation for the main path.** Compare them for a beginner: which one gives the mechanism step by step with a concrete example and a picture? Use that one as the main explanation. Never drop the CampusX explanation just because an outside source exists.
3. **Keep a new angle.** If CampusX adds an angle the other source lacks (a different analogy, an Indian everyday example, a code-first view, a practical caveat), keep it as a second short view, such as "Another way to see it", with its own picture where it helps. The same applies the other way round.
CampusX transcripts: ML `transcripts/NNN.*.txt`, DL `dl_map/transcripts/`, maths `transcripts/Mxx.whisper-en.txt`.

## 14. Fixed depth, no nitpicking (user, 2026-10-04)

The user said: "Don't nitpick" (example: "neural networks date from the 1960s" against 1943/1958) and "you have to decide on the depth… each time you go over something you go deeper into the topic and find something that's wrong, something which might be a niche obscure or some edge case".

**The depth is the beginner level of the source video.** A Note teaches what its CampusX video teaches, as clearly as possible, with pictures. A new pass over a Note never goes deeper than that.

**Fix an error only if it passes this test:** would a beginner end up with the wrong core idea, a wrong answer to a standard interview question, or code and numbers that don't work? If yes, fix it with a source. If no, leave the Note as it is.

**Not worth a fix, a caveat or a report line:**
- approximate dates, round figures, loose everyday wording, a rounded number;
- edge cases, rare conditions and exceptions a beginner will not meet;
- different conventions between sources;
- slips in a source video that the Note does not repeat;
- "technically" corrections that make the sentence harder to read.

**No depth creep.** Do not add caveats, proofs or citations whose only job is to defend a simple, right-way explanation against a niche objection (§3: intuitions that point the right way stay). A review pass checks the Note against these rules; it is not a hunt for more errors.

**Never remove real content** (user, 2026-10-04: "make sure we don't remove any gotchas or something advanced or any building blocks"). This rule is about trivia, not about how far a Note goes. Always keep, and keep adding where the sources teach them:
- **gotchas:** practical pitfalls a learner will actually hit, such as data leakage, scaling before the split, the dummy-variable trap, a wrong default, a common interview trap;
- **advanced material:** the formal version, derivations and Extra boxes that take the topic further (§11 still climbs to the formal version);
- **building blocks:** any idea, term or step that a later Note or a later section depends on.

When unsure whether something is trivia or a gotcha, keep it.
