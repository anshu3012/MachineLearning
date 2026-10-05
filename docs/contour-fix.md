# Task: show the surface before every contour map (NOTE-RULES §16)

The user, on the chain-rule figure of MA-063 (`images/chain_path.gif`): "contour map of f=xy², but the user doesn't know how it looks like, in the image you just made contours, it's confusing." Read `docs/NOTE-RULES.md` in full first, especially §10, §11, §15 and §16, and `docs/visual-audit/PROMPT.md` (figure conventions).

## For every Note on your list
1. Find every figure that is a contour map, a filled contour, a heat map of a function of two inputs, or level sets (grep the Note's `images/*.py` and `*.tex` for `Contour`, `contours`, `Heatmap`, `contour`; then read the Note around each figure).
2. Decide what it is:
   - **A contour map of a surface** (a loss over two weights, a function f(x, y), a probability density over two inputs): it needs the surface first.
   - **A classifier's decision regions** (coloured areas for predicted classes): not a surface. Only make sure a plain sentence says what the colours and the boundary mean. No 3D needed.
3. For each contour map of a surface:
   - Show that function's own surface in 3D **before** the contour map: best is a short animation (Plotly frames → GIF + `_frames.png`) where the camera tilts from a side view down to the top view and ends on exactly the contour map used next, with contour lines drawn on the surface and dropped to the floor. A still 3D surface beside the contour map (two panels) is acceptable when an animation would add nothing.
   - Same colour scale, same axes, and the same marked point, path or minimum on both.
   - Write the function as an equation with one value first (§15), e.g. "f(x, y) = x·y², so f(2, 2) = 8".
   - In the text: what the surface looks like in plain words (a bowl, a saddle, a ridge, a valley), then "the contour map is this surface seen from above; each line joins points at the same height", then what to read off it (lines close together = steep; the centre ring = the lowest point).
   - If the same surface was already shown earlier in the Note, point back to that figure by number and add the one reading line. If another Note owns the surface (e.g. the optimizer Notes share one loss surface), give a one-line recap with a link and still put a small surface panel beside the contour map.
   - Link "contour map" at its first use in the Note to MA-062 (the owner of how to read a contour map), unless the Note is MA-062.
4. Keep every existing figure, fact and number (§14). Renumber figures and in-text references if you insert figures.

## Visuals
Our own code; Plotly for surfaces and camera tilts (`go.Surface` with `contours_z=dict(show=True, project_z=True)`, frames changing `scene.camera.eye`), exported with the repo's existing GIF helper (`gifkit.py` in many images folders; copy one if needed). Manim only if a Plotly version cannot show it. Never matplotlib or seaborn. Look at the `_frames.png` grid and the PDF page of every new figure; fix clipped labels and overlaps.

## Machines and checks
Python: `/home/anshu/miniforge3/envs/campusx/bin/python` with `PYTHONNOUSERSITE=1`. `tools/build.sh <Note folder>` prints Built; `python tools/github_math.py --check <Note>.md` is clean; `grep -nP "[\t\x08\x0c\r]" <Note>.md` is empty. Keras notebooks whose numbers a Note quotes re-run on the laptop CPU only.

## Do not touch
git, `glossary.md`, `course_map/`, `tools/`, `docs/`, `site/`, and any Note not on your list. No background agents.

## Report (as text)
Per Note: each contour figure found, its kind (surface or decision regions), what you added (file, tool, what it shows), and any figure left alone with the reason.
