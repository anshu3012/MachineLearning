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
- "Could not source" is never a final answer (user, 2026-10-05: "Couldn't find source for? That's not true or even possible. If it's not on the Internet and it's just in our note then it's clearly wrong"). Search harder: free books, lecture notes, official docs, papers, reputable tutorials. If nothing anywhere says it, the claim is wrong: correct it to what the sources say, or remove it, and list it in your report. Never leave "open question" or "unclear" wording in a Note.

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

**Textbook-based Notes are not exempt (user, 2026-10-04).** The user read the Gaussian mixture Note and said: "do you really think it's friendly for a beginner? … There is no intuition no nothing, just directly math." When no StatQuest, Khan Academy, 3Blue1Brown or CampusX video exists for a topic, the fallback is NOT to teach from the textbook's order. Find the next most beginner-friendly explainer for the intuition and the teaching path: a video (Luis Serrano Academy, StatQuest-style channels, a lecture that builds the idea from a picture), a good Medium article, or a GitHub repository's explanation (user, 2026-10-04: these "are also acceptable before moving to textbook"). Open it, follow its build-up, credit it in Built from. The textbook is still essential: every Note ties its formal step and its claims to the textbook with citations ("tying to textbook in the note essential"). A Note whose sections lead with definitions and formulas fails this rule, however correct it is. Test for every section: a beginner must be able to read up to the formula and already know what it will say.

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

## 15. Every step shown, every symbol defined where it first appears (user, 2026-10-04)
The user read the chain-rule section of a maths Note: "In words: the value of f changes because x changes and because y changes. Add the two effects… This is very confusing. You have not defined f and the inline math does not help. These are two products added, but you have not shown the products and then the addition. You cannot roll things into text like that. Show by either math (step by step) or images or animations. All notes need to be step and step and no inline math." And on another section: "4.3 One picture of every shape makes no sense at all. Explanation is poor." And: "You cannot list notation without showing what it is… what is f, you just said with words. You never said f = something… you keep using R^D but you don't explain the notation." These are examples; apply to every Note.
- **Define before use.** The first time a function, variable or symbol appears, write what it is with a concrete value: "f(x, y) = x² + y², so f(2, 3) = 13", not "a function f". Every set or space symbol (ℝ, ℝ^D, ∈, ∑) is explained on first use in plain words with a small instance ("ℝ² means pairs of numbers such as (2, 3)").
- **One step per line, shown.** A calculation is a stack of display lines or a table: each product on its own line with its numbers, then the sum on the next line. Never "add the two products" in a sentence. A process is shown by a figure or animation, with the text pointing at it.
- **No maths rolled into prose.** Formulas and numbers live in display lines or tables, not inside sentences. Inline maths is only for naming a single symbol already defined (for example "the slope m").
- **Explain every picture's point.** A section titled "one picture of every shape" is not an explanation: say what the reader should see, why, and what to conclude, in plain steps next to the figure.
- Run this check on every section of every Note: could a beginner with ADHD follow it one line at a time without guessing what any symbol means?

## 16. A contour map comes after the surface it flattens (user, 2026-10-04)
The user, on the chain-rule figure of MA-063: "contour map of f=xy², but the user doesn't know how it looks like, in the image you just made contours, it's confusing." This is an example (§12): it applies to every contour map, heat map of a function, or level-set picture in every Note.
- **Not only contours** (user: "Countours was just an example"): any figure that uses a visual code the reader has not been taught (contour map, heat map of a function, vector field, a bent grid such as the polar map, log axes, dendrogram, attention heat map, confusion matrix, ROC curve) is built up first: show the familiar thing, then how it becomes the picture, then how to read it.
- **Owner:** MA-062 owns "how to read a contour map": an animation of a surface being sliced at several heights, each slice's outline dropping to the floor, and the camera tilting from a side view to the top view, so the reader sees the contour lines *are* the surface seen from above.
- **Every other contour figure:** first show that function's own surface in 3D (a still or, better, a short tilt from side view to top view ending on the exact contour map used next), with the same colours and the same point or path marked on both. Then the contour map. Then one line saying what to read off it ("lines close together = steep; the centre ring = the lowest point").
- If the surface was already shown earlier in the same Note, point back to that figure by number; if another Note owns it, give a one-line recap with a link and still show a small surface beside the contour map.
- Decision-region plots (a classifier's coloured regions) are not contour maps of a surface; they need only a plain sentence saying what the colours mean. A probability surface drawn as contours *is* a contour map and follows this rule.

### 15 addendum: phone width and sums in sentences (user, 2026-10-04)
The user, quoting MA-063 §4.1 as it showed on the site: "Again so much math inline. Each step in new line. It looks too cluttered to follow and read. Across all files."
- No calculation inside a sentence. "The angle grows from π/6 = 0.524 to 0.524 + 0.6 = 1.124" becomes a sentence in words ("the angle grows by h = 0.6") followed by display lines, one operation each. Inline maths may only name a symbol or a single value ("with $h = 0.6$").
- A display line must fit a phone: at most about 40 visible characters. Split a long line at its "=" signs, one step per line; put two matrices or two results on separate lines, not side by side with `\qquad`.
- `python tools/find_inline_calc.py <Note>.md` lists both problems; a fixed Note prints "0 found".

## 17. Links go to the section, and the link text is the idea (user, 2026-10-04)
The user: "Instead of linking the note, link the direct section and click would take us to the section" and "if you're hyperlinking them remove the 'Note'".
- A link to another Note points at the section that teaches the idea: `[tangent line](../MA-061-.../MA-061-....md#41-from-secant-to-tangent)`. `python tools/section_links.py --headings <Note.md>` lists the anchors; `--check` verifies them. Avoid headings with maths in them (unreliable anchors); link the nearest plain heading.
- The link text is the idea itself, not "the X Note": "This linearisation is the [tangent line](…#41-…) in several dimensions", not "the tangent line of the [derivatives of one variable Note](…)". Rewrite the sentence so it reads naturally without the word "Note".

## 18. No puffery, no filler, no vague sources (user, 2026-10-04)
The user agreed to cut "puffery, filler, vague sources", "especially the puffery and fillers".
- **Puffery:** words that praise instead of inform ("powerful", "elegant", "beautiful", "crucial", "remarkable", "the heart of", "unlocks"). Replace with what the text means ("gives good results on many kinds of data") or delete.
- **Filler:** words that add nothing ("clearly", "actually", "in fact", "note that", "essentially", "it is worth noting", "let us", trailing "-ing" clauses such as ", highlighting…").
- **Vague sources:** "experts say", "studies show": name the source or delete.
- Keep technical uses ("robust to outliers", RobustScaler, "powerful" as in statistical power) and words inside quoted example sentences. Keep every fact and number.
- `python tools/find_puffery.py <Note.md>` lists candidates; it is a prompt to look, not a list to delete blindly. Also read for filler sentences it cannot catch.

### 15 addendum 2: an example right where the abstract idea appears (user, 2026-10-04)
The user, on "For a function with several outputs, the derivative is a matrix": "For a function with several outputs (eg: ?????) the derivative." Every abstract statement (a kind of function, object or situation) gets a concrete instance in the same sentence or the next: "For a function with several outputs, such as the polar map f(r, θ) = (r cos θ, r sin θ), the derivative is a matrix."

## 19. Assume nothing: show it before using it (user, 2026-10-04)
The user, after the contour-map feedback was turned into a contour-only rule: "the contour is just an example of the issues that I gave you... anything that I send you for feedback is just one general example because there are hundreds of documents to go through." The single idea behind §15, §16 and §17 and every other piece of feedback: **never assume the reader already knows something.** Anything the reader meets is shown, at their level, at the point they meet it, before it is used:
- a **figure**: what kind of picture it is, what each axis, colour, line, arrow and panel means, the familiar thing it is built from (a surface before its contour map, a grid before it bends, a table before its heat map), then what to look at and what to conclude;
- a **function or symbol**: written as an equation with a value (§15);
- a **term or idea from another Note**: a one-line plain recap here, plus a link to the exact section (§17);
- an **abstract statement**: a concrete instance in the same sentence (§15 addendum 2);
- a **step**: shown, one per line, never "it follows that" (§15).
When the user names one case, apply this to every kind of thing in every Note, not just to that kind of thing.

## 20. Every statement says what it is about, with the right word for it (user, 2026-10-04)
The user, on MA-063 §4.3 ("Case 2: several numbers in, one number out", followed by ∇f(2, 3) = [4, 6]): "Is this really one number out? I don't think that's a number... You are teaching the reader something wrong. Again, this is just an example... Find issues like this." The label described the function f (two numbers in, one number out: 13), but it sat on top of the derivative (two numbers), so a beginner learns that [4, 6] is "one number". A statement that a beginner can reasonably read as false is an error, even if an expert can find a reading that is true.
- **Name the object.** Each statement says which thing it describes when two are on show: the function or its derivative, the input or the output, the loss or its gradient, a probability or its log, a sample or the population, a prediction or a score.
- **Use the right type word.** number (one value), vector / row / column (a list), matrix (a table), function, distribution, set. Never "a number" for a vector, "the value" for a whole curve.
- **Shapes and counts match what is shown:** "1 × 2" only for a row of two; "three features" only if three are listed.
- **No hidden conditions.** If it is only true in a case (a convex loss, independent features, a balanced dataset), say the case.
This is one example of the §19 idea; check every statement in every Note against it.

### 20 addendum: teach the technical term, keep its plain meaning beside it (user, 2026-10-04)
The user asked "why use incorrect terms like numbers? The correct term is a vector... teach the user to be technical and build up", then: "that's going against the ethos of this repo if you keep using technical terms... what's the difference between a reader reading our repo versus going to a book?" Agreed answer (user chose it): the repo differs from a book in **order and support**, not in avoiding terms. Picture, plain words and the Note's own numbers come first; the term is the destination.
- **Introduce once, where it is explained:** plain words, then the term with its glossary ID ("a list of numbers like (2, 3) is a **vector** (G-2081)").
- **First use in each later section: term + plain meaning**, e.g. "f takes a vector (a list of numbers) and gives a scalar (one number)". Within the same section after that, the term alone ("vector in, scalar out").
- **Explained before used, and linked:** a term may appear only after it is explained, in this Note or another. If another Note explains it, its first use in this Note links to the exact section that explains it (`docs/term-owners.tsv`, made by `tools/term_owners.py`), with the plain meaning beside it. If no Note explains it yet, explain it here.
- Never a wrong plain word in place of the term ("one number" for a vector), and never the term alone where the reader has not met it in this section.

## 21. The Note agrees with itself, its figures and its links (independent audit, 2026-10-04)
An independent reader, not shown the user's examples, found these in randomly chosen Notes after the §15–§20 sweep. All are errors under §19/§20.
- **Internal consistency:** a fact stated twice must agree (row vs column of the same matrix; a table and the summary on whether a layer is tied; "the same drop" in one paragraph and "no drop" in the next). A running example keeps its numbers; if they change, the text says so and why.
- **Text inside a figure or animation** (titles, labels, baked-in sentences) must agree with the body. Read the `_frames.png` of every GIF, not only the body text.
- **A number must agree with the section it links to.** "Two thirds of the parameters" linked to a count where it is 46% is false for that link. Name the case the number belongs to.
- **Ownership points the right way:** the Note that teaches a term says it is defined here; a later Note is never named as the definer of something taught earlier.
- **Conditions stay attached to claims** (approximately, for large n, when the variance is finite, for GPT-3 not GPT-2), in the Key point and Key terms too, not only in the Extra.
- **Link text must not change what the sentence says:** the linked words read as part of the sentence's meaning; never make a link title the grammatical subject.
- **Key point boxes stay short:** one or two plain sentences.
- **Display lines wider than about 40 visible characters** are split even when the finder misses them (it under-counts some LaTeX).
- **A Key point never contradicts the Note's own worked example** (audit: a voting Key point said the vote beats every model; the Note's own 0.7/0.6/0.55 example votes to 0.673). Test each Key point against the examples below it.
- **Text and figure report the same run.** If a figure's panel shows numbers from one run (splits, trees, seed), the text quotes that run or says plainly which run each comes from.
- **Words for how one figure relates to another are exact** ("mirrored" is not a half turn).
- **Every file a Note names exists** (the notebook is `<Note>.ipynb`, not `notebook.ipynb`).
- **The statistic named is the one computed** (a "median" column must hold medians, not means).
- **A shortened excerpt keeps everything the text points at** (if the text says "line 5" or "4 books", the excerpt shows them).
- **When a figure shows a model's output, the text says whether it matches the target** (a prediction "amies" against the target "amis" needs a comment).
- **A rule-of-thumb sentence must allow for the exceptions its own figures show** (if one frame shows the forest wrong, the text cannot say it is always right).
- **Claims about code ("without changing a line") are checked against the notebook.**
- **Each figure number points at the right figure.**
- **A figure's hidden scaling is stated** (bumps drawn already divided by n; values rescaled to 0–1). A real-data value that is impossible on the raw scale (iris sepal width 0.4) says it was rescaled.
- **Paired numbers name each side** ("linear regression 0.31, Ridge 0.30", not "0.31 against 0.30").
- **A running dataset that grows or changes says so where it changes**, and which results the change affects.
- **A figure explanation does not over-generalise** beyond what the Note's own data shows.
- **Point into an animation by stage or frame name, never by grid position** ("top left" exists only on the PDF frame sheet; on the site the GIF plays one frame at a time).
- **Code examples give the output the text says** (run them on the Note's data; e.g. `parse_dates` on integer years silently gives 1970 timestamps).
- **A demonstrated prediction says whether its input was in the training data**; a training row predicted correctly is not evidence.
- **When CampusX itself is wrong on a point that matters** (check first that it really is an error and not a second valid reading: rank looked like one, but an exam rank is a count of candidates ahead, so both the discrete and the ordinal views are kept), the Note teaches the correct version with its reason, without narrating the video (the no-narration rule holds); keep the video's point where it is right. §13 still holds for everything else.
- **Leakage counts as a training-data problem:** features ranked, selected or scaled on the full data before a split or cross-validation let the test data help choose the model.
- **When the text gives a reason for a result, the reason matches the model's own internals** (the filter's weights, the tree's leaves, the code): "the bar left the receptive field" is wrong if it is still inside on the negative side.
- **Every display line names its quantity**, especially when its digits repeat a nearby number (a p-value of 0.47 next to a 0.47 kg gain).
- **A unit keeps one meaning in a Note** (GB as 1024³ bytes, or decimal, not both).
- **A symbol keeps one meaning in a Note**, and each glossary tag (G-N) is the ID of the term actually meant.

## 22. The summary says why, not only what (user, 2026-10-05)
"In summary for each note it says what but not the why." Each summary point states the fact **and** why it matters or why it holds, in one short clause the Note itself supports: "so …" (what it lets the reader do or decide), or "because …" (the reason shown in the Note). Example: "Temperature divides the logits: $T \to 0$ is greedy, large $T$ is close to uniform" becomes "…, so $T$ is the one knob between safe, repetitive text and varied, riskier text."
- The why rests on §3 evidence: the Note's own sections, figures or derivations, **or a checked book, paper, official docs or tutorial**. If the Note never gives the reason, add it to the body (one or two plain sentences, cited, listed under Sources) and then summarise it. Staying at the video's depth never means leaving a reason out (user, 2026-10-05: "why can't you use a book as a source or a tutorial as a source? ... As long as it's correct").
- Summary tables keep their columns; a table whose rows need a why gets a "Why it matters" column or a bullet under it.
- The summary still ends by tying back to the Note's opening question.

## 23. A definition says what the thing is and what it does (user, 2026-10-05)
"It does not explain what it is or what it does, what use is 'next step', this is basically useless" (on G-172 "Add and norm: The step after each transformer sub-layer: LayerNorm(x + Sublayer(x))").
A glossary meaning or Key terms row must let a reader who taps it understand the term without opening the Note:
- **what it is**, in plain words (not only where it sits, a formula, or a synonym);
- **what it does or why it is used**, in one short clause.
Example: "Add and norm: adds a sub-layer's input back to its output (a residual connection) and then layer-normalises the sum, so the signal and gradients pass through deep stacks and the numbers stay on one scale."
A formula or position may follow, never replace, the meaning. One or two short sentences; the Note keeps the details. The meaning must agree with the Note that explains it (§21), and the glossary link points to the section that explains it.
