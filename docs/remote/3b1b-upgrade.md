# Task (topgro): upgrade the transformer Notes 1067–1085 with 3Blue1Brown's intuitions and animations

You are working in `~/campusx` on topgro, a copy of the project. **No git.** Your folders are copied back and reviewed on another machine. **Do not start background agents.** This headless session ends when you reply, and anything still running would be lost. Do the work yourself and reply only when everything is done.

## Read first
- `docs/NOTE-RULES.md`
- `docs/visual-audit/PROMPT.md`: the visual standards. Animations are the backbone. Use Manim CE or Plotly frames, output as a GIF plus `_frames.png`; never matplotlib.
- `docs/3b1b-transformers.md` in full. The transcripts are in `transcripts/3b1b/`.
- The proposals for Notes 1067–1085 in `docs/visual-audit.md` §4.

The user considers 3Blue1Brown the gold standard for transformers:
- "His animation and intuition is way too good."
- "the whole project depends on animations and figures since I have ADHD".

**Rules for using his work:**
- Recreate his intuitions with our own code and real data. Never copy his frames.
- Read the transcript around each timestamp before you recreate it.
- Credit the intuition in the text and in the Sources as: Sanderson, G. (3Blue1Brown), "title", year, 3blue1brown.com/lessons/slug.

## Do, in this order

### 1. The five intuition upgrades
1. **1075 §6–7 and 1080 §5.2:** the attention output as a change *added* to the word's vector, linked to the residual connection. Make a Manim animation of a word vector being nudged.
2. **1077 §5.3:** concatenating the heads and multiplying by W_O equals summing one change per head. Add the low-rank value map (value down, value up) as a new §5.4.
3. **1072 §3:** replace "each number is one meaning" with "each direction is one meaning". Link `../1086-meaning-as-direction/note.md`, a new Note being written elsewhere.
4. **1073 §7:** add the adjective–noun query/key example, and redraw Fig 2 as a grid of dots sized by weight.
5. **1080 §5.3 / §7.2:** add a short box: W₁ rows are questions, W₂ columns are what gets written. Link `../1089-mlp-stores-facts/note.md`, also being written elsewhere.

### 2. The highest-ranked animations for existing Notes
Take these from the doc's §3:
- the attention dot grid with causal masking, built from the trained model of 1081/1084;
- **the capstone animation for 1085:** one sentence flowing through embeddings → blocks → next word.

### 3. Changes to Note 1067
- Add the chatbot prompt format and compute-in-years from the doc.
- Fix "117M": the GPT-2 paper reports 117M parameters, while the released GPT-2 small weights have 124.4M. Say both, with sources.

### 4. The remaining proposals
Do the visual-audit proposals for 1067–1085 not already covered.

## Standards
- Every claim must be backed by a paper you opened, our data, or maths. Nothing unresolved stays in a Note.
- Keep each Note's structure and house rules. Change only the text around new figures, plus the upgrades listed above.
- Rebuild with `CAMPUSX_ENV=~/miniforge3/envs/campusx tools/build.sh <folder>`; it must print "Built".
- Check every new frame grid and PDF page yourself.
- Plotly image export needs Chrome. If needed, set `BROWSER_PATH` as the earlier topgro session did.

## Do not touch
Other Notes, the glossary, `course_map`, `tools`, or git. Never send personal data to any outside service.

## Report
Write the report to `docs/remote/3b1b-upgrade-report.md`. For each Note, give:
- what changed;
- the animations (tool, data, what to watch for);
- the sources opened;
- anything removed.
