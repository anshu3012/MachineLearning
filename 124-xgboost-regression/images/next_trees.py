"""The boosting loop on the four students, tree after tree (eta = 0.3, lambda = 0, depth 2, exact greedy):
each stage grows an XGBoost tree on the current residuals and adds 0.3 times its output.
Left: the model's prediction (a staircase in CGPA) closing in on the students. Right: each student's residual,
stage by stage, shrinking towards 0.
Run: python next_trees.py  -> next_trees.gif, next_trees_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, PURPLE, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"
x = np.array([6.7, 9.0, 7.5, 5.0])
y = np.array([4.5, 11.0, 6.0, 8.0])
ETA, STAGES = 0.3, 12


def grow(idx, r, depth):
    """XGBoost tree (lambda = 0): split on the largest gain S_L + S_R - S_parent, leaf output = mean residual."""
    S = lambda m: r[m].sum() ** 2 / len(m)
    xs = np.unique(x[idx])
    best = None
    if depth > 0 and len(xs) > 1:
        for t in (xs[:-1] + xs[1:]) / 2:
            L, R = idx[x[idx] < t], idx[x[idx] >= t]
            g = S(L) + S(R) - S(idx)
            if best is None or g > best[0] + 1e-12:
                best = (g, t, L, R)
    if best is None:
        return ("leaf", r[idx].mean())
    return ("split", best[1], grow(best[2], r, depth - 1), grow(best[3], r, depth - 1))


def predict(tree, v):
    if tree[0] == "leaf":
        return np.full_like(v, tree[1], dtype=float)
    return np.where(v < tree[1], predict(tree[2], v), predict(tree[3], v))


grid = np.linspace(4.6, 9.4, 600)
pred, pgrid = np.full(4, y.mean()), np.full_like(grid, y.mean())
hist_pred, hist_grid, trees = [pred.copy()], [pgrid.copy()], []
for m in range(STAGES):
    tree = grow(np.arange(4), y - pred, 2)
    trees.append(tree)
    pred = pred + ETA * predict(tree, x)
    pgrid = pgrid + ETA * predict(tree, grid)
    hist_pred.append(pred.copy()); hist_grid.append(pgrid.copy())
res = [y - p for p in hist_pred]
# the Note's numbers: tree 1 and tree 2 outputs, residuals after stages 2 and 3
assert np.allclose(predict(trees[0], np.array([5.0, 6.7, 9.0])), [0.625, -2.125, 3.625])
assert np.allclose(predict(trees[1], np.array([5.0, 6.7, 9.0])), [0.4375, -1.4875, 2.5375])
assert np.allclose(res[1], [-2.2375, 2.5375, -0.7375, 0.4375])
assert np.allclose(res[2], [-1.79, 1.78, -0.29, 0.31], atol=0.006)
print("residuals after the last stage:", res[-1].round(3))

COLS = [BLUE, ORANGE, GREEN, PURPLE]


def frame(k):
    fig = make_subplots(1, 2, column_widths=[0.55, 0.45], horizontal_spacing=0.1,
                        subplot_titles=["prediction after each tree", "residual of each student"])
    fig.add_trace(go.Scatter(x=grid, y=hist_grid[k], mode="lines", line=dict(color=RED, width=4, shape="hv"),
                             showlegend=False), 1, 1)
    for i in range(4):
        fig.add_trace(go.Scatter(x=[x[i], x[i]], y=[y[i], hist_pred[k][i]], mode="lines", showlegend=False,
                                 line=dict(color=GREY, width=2, dash="dot")), 1, 1)
        fig.add_trace(go.Scatter(x=[x[i]], y=[y[i]], mode="markers", marker=dict(color=COLS[i], size=16),
                                 showlegend=False), 1, 1)
        fig.add_trace(go.Scatter(x=list(range(k + 1)), y=[r[i] for r in res[:k + 1]], mode="lines+markers",
                                 line=dict(color=COLS[i], width=3), marker=dict(size=9),
                                 name=f"student {i + 1}"), 1, 2)
    fig.add_hline(y=0, line=dict(color="black", width=1), row=1, col=2)
    sse = (res[k] ** 2).sum()
    title = "stage 1 (the mean 7.375)" if k == 0 else f"after {k} tree{'s' if k > 1 else ''}"
    fig.update_xaxes(title_text="CGPA", range=[4.6, 9.4], row=1, col=1)
    fig.update_yaxes(title_text="package (LPA)", range=[3.5, 12], row=1, col=1)
    fig.update_xaxes(title_text="trees added", range=[-0.4, STAGES + 0.4], dtick=2, row=1, col=2)
    fig.update_yaxes(range=[-3.2, 4], row=1, col=2)
    fig.update_annotations(font=dict(family="Latin Modern Roman", size=24))
    fig.update_layout(template="simple_white", width=1200, height=640, font=dict(family="Latin Modern Roman", size=22),
                      title=dict(text=f"{title}: sum of squared residuals {sse:.2f}", x=0.5, y=0.97),
                      margin=dict(l=80, r=20, t=110, b=120), legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".next_frames"
    tmp.mkdir(exist_ok=True)
    holds = [8] + [4] * (STAGES - 1) + [14]                  # linger on the start and the end
    n = 0
    for k in range(STAGES + 1):
        frame(k).write_image(tmp / "src.png")
        for _ in range(holds[k] if k < len(holds) else 14):
            shutil.copy(tmp / "src.png", tmp / f"{n:03d}.png"); n += 1
        if k in (0, 1, 2, STAGES):
            shutil.copy(tmp / "src.png", tmp / f"key{k}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "5", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "next_trees.gif")], check=True)
    ims = [Image.open(tmp / f"key{k}.png").convert("RGB") for k in (1, STAGES)]
    w, h = ims[0].size
    sheet = Image.new("RGB", (w, len(ims) * h + 16 * (len(ims) - 1)), "white")   # stacked: readable in the PDF
    for i, im in enumerate(ims):
        sheet.paste(im, (0, i * (h + 16)))
    sheet.save(HERE / "next_trees_frames.png")
    shutil.rmtree(tmp)
