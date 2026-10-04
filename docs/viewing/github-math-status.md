# GitHub maths status (for the viewer decision, after all Notes are done)

Checked on 2026-10-03 through GitHub's Markdown API. This checks only whether the **website** recognises each formula as maths; it does not check MathJax errors. The GitHub **mobile app** renders no maths at all.

- Formulas recognised: 16,285 of about 16,680.
- Not recognised: about 400 spots in 55 Notes. Most are matrices inside quoted "Extra" boxes, formulas right after a quote mark, and `_` after a brace.
- `\sb{...}` (TeX subscript) works on GitHub and avoids the `_`-after-brace problem.
- In a list item, a block `$$` works only when `$$` stands on its own lines.

Detail: the job tmp gh_a.txt and gh_b.txt (not kept). Decide the phone viewer first; see the viewing-and-math memory.
