# Round 2: visuals for every key-point section

The user has ADHD and learns visually: "the whole project depends on animations and figures". Round 1 gave each Note one strong animation of its core idea. Round 2 finishes the job. Every section that teaches something gets a visual that teaches it.

## Read first
- `PROMPT.md` in this folder: all of its rules still apply (tools, real data, output format, credits, checks, heavy renders on topgro, do-not-touch list).
- Your batch in `round2.md`.
- Each Note's `note.md` and its existing `images/`.

## Target per Note
- **Strong:** at most about 400 words of text per visual, and at least 60% of the numbered sections with a figure. Leave out Summary, Prerequisites, Sources and Key terms.

## What to add, in order of teaching value
1. **Any process still not animated:** an algorithm step, a value changing with a parameter, data flowing, an iteration. Animate it (Plotly frames, or Manim for geometry).
2. **Worked examples, drawn:** turn the Note's own numbers into a step-by-step picture or a short animation, such as a table filling in, a computation building up, or a split being chosen.
3. **Comparisons as pictures:** A vs B side by side on the same data, such as two methods, before and after, or two settings.
4. **Definitions and structure:** a small labelled diagram (TikZ) where a section introduces a structure or a set of parts.
5. **Code sections:** show what the code's output looks like (the plot or table it produces), not a picture of code.

## Rules
- **Every visual must teach** the section's key point. No decoration, no stock images, no repeating a figure that already exists.
- **Use the Note's own data and numbers.** Assert them in the script, so the picture cannot drift from the text.
- **Change only the text that frames each new figure:** a caption, and one "what to watch for" sentence. If a figure shows the text is wrong, fix the text, say so in your report, and back the fix with the data.
- **Keep GIFs under about 3 MB,** and give each one a `_frames.png` grid for the PDF. A frame grid too small to read in the PDF can show the last frame alone.
- **Rebuild every Note** with `tools/build.sh <folder>`; it must print "Built". Look at every new PNG and frame grid, and at the PDF page where each figure sits.
- **Cross-agent tips:**
  - After copying a remote render back, run `touch images/.built_<name>` before building.
  - Run Keras training on the laptop CPU (`CUDA_VISIBLE_DEVICES=`) when the Note's numbers must reproduce exactly; topgro's GPU can change them.
  - `tools/remote_run.sh` warns if a run changed `data/`.

## Report
- For each Note: the visuals added (file, tool, what it teaches), its words per visual and figure share before and after, and any text fixed.
- Anything skipped, and why.
