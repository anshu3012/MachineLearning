"""Additive modelling, animated (Plotly frames). Left: the line y = x, then the wave sin(x) is added bit by bit until the
sum is y = x + sin(x). Right: gradient boosting builds the same curve from a constant plus small trees (4 leaves each,
learning rate 0.5), one tree per frame; 200 noise-free points of y = x + sin(x).
Run: python additive_build.py  -> additive_build.gif, additive_build_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots
from sklearn.ensemble import GradientBoostingRegressor

HERE = Path(__file__).parent
GREEN, ORANGE, RED, GREY = "#54A24B", "#F58518", "#E45756", "#B0B0B0"
x = np.linspace(-10, 10, 200)
y = x + np.sin(x)
gbr = GradientBoostingRegressor(n_estimators=60, learning_rate=0.5, max_leaf_nodes=4, max_depth=None,
                                random_state=0).fit(x[:, None], y)
staged = [np.full_like(y, y.mean())] + list(gbr.staged_predict(x[:, None]))
mse = [float(np.mean((y - p) ** 2)) for p in staged]
assert all(b <= a + 1e-12 for a, b in zip(mse, mse[1:]))  # the training error never rises from one stage to the next
TREES = [0, 1, 2, 3, 4, 5, 6, 8, 10, 15, 20, 30, 45, 60]


def frame(a, m):
    """a: share of the wave already added (left). m: number of trees in the boosted model (right), None = not started."""
    fig = make_subplots(1, 2, horizontal_spacing=0.08, subplot_titles=[
        "a line plus a wave" if a < 1 else "y = x + sin(x): the sum",
        "a constant plus small trees" if m is None else f"constant + {m} tree" + ("" if m == 1 else "s")])
    fig.add_trace(go.Scatter(x=x, y=x, mode="lines", line=dict(color=GREEN, width=2, dash="dot"), name="y = x"), 1, 1)
    fig.add_trace(go.Scatter(x=x, y=np.sin(x), mode="lines", line=dict(color=ORANGE, width=2), name="y = sin(x)"), 1, 1)
    fig.add_trace(go.Scatter(x=x, y=x + a * np.sin(x), mode="lines", line=dict(color=RED, width=4),
                             name="the sum so far"), 1, 1)
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(color=GREY, width=6), name="y = x + sin(x)",
                             showlegend=False), 1, 2)
    if m is not None:
        fig.add_trace(go.Scatter(x=x, y=staged[m], mode="lines", line=dict(color=RED, width=3, shape="hv"),
                                 showlegend=False), 1, 2)
        fig.add_annotation(x=-4, y=9, text=f"squared error {mse[m]:.2f}", showarrow=False, font_size=22, row=1, col=2)
    fig.update_yaxes(range=[-11, 11])
    fig.update_xaxes(title_text="x")
    fig.update_annotations(font_size=24)
    fig.update_layout(template="simple_white", width=1300, height=600, font=dict(family="Latin Modern Roman", size=20),
                      margin=dict(l=50, r=20, t=70, b=90), legend=dict(orientation="h", x=0.0, y=-0.16))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".additive_build_frames"
    tmp.mkdir(exist_ok=True)
    plan = [(0, None, 4)] + [(a, None, 1) for a in np.linspace(0.1, 0.9, 9)] + [(1, None, 5)]
    plan += [(1, m, 2 if m < 6 else 1) for m in TREES[:-1]] + [(1, 60, 8)]
    n, keys = 0, []
    for a, m, rep in plan:
        frame(a, m).write_image(tmp / f"{n:03d}.png")
        if (a == 1 and m is None) or m in (1, 5, 60):
            keys.append(Image.open(tmp / f"{n:03d}.png").convert("RGB"))
        for k in range(1, rep):
            shutil.copy(tmp / f"{n:03d}.png", tmp / f"{n + k:03d}.png")
        n += rep
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "4", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=860:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "additive_build.gif")], check=True)
    w, h = keys[0].size
    grid = Image.new("RGB", (2 * w, 2 * h), "white")
    for i, im in enumerate(keys):
        grid.paste(im, ((i % 2) * w, (i // 2) * h))
    grid.save(HERE / "additive_build_frames.png")
    shutil.rmtree(tmp)
