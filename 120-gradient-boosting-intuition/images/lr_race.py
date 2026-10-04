"""Learning rate against number of trees (section 12): gradient boosting with learning rates 1, 0.5 and 0.1 (8 leaves
per tree) grows tree by tree. Top: the model on the curve data of the app. Bottom: test error averaged over 20 fresh
datasets of the same recipe, 5,000 test points each (the Notebook's experiment).
Run: python lr_race.py  -> lr_race.gif, lr_race_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots
from sklearn.ensemble import GradientBoostingRegressor

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import GRID, X, boost, mse, predict, y  # noqa: E402  the curve data and the boosting loop of the app

LRS = {1.0: "#E45756", 0.5: "#F58518", 0.1: "#4C78A8"}
N = 200
fits = {lr: boost(N, lr, 8) for lr in LRS}
test = {lr: [] for lr in LRS}
for s in range(20):                                   # the Notebook's averaging, cell for cell
    r = np.random.RandomState(s)
    Xs = r.rand(100, 1) - 0.5
    ys = 3 * Xs[:, 0] ** 2 + 0.05 * r.randn(100)
    Xt = r.rand(5000, 1) - 0.5
    yt = 3 * Xt[:, 0] ** 2 + 0.05 * r.randn(5000)
    for lr in LRS:
        gbr = GradientBoostingRegressor(n_estimators=N, learning_rate=lr, max_leaf_nodes=8, max_depth=None,
                                        random_state=0).fit(Xs, ys)
        test[lr].append([mse(yt, p) for p in gbr.staged_predict(Xt)])
test = {lr: np.mean(v, axis=0) for lr, v in test.items()}
best = {lr: (v.min(), int(v.argmin()) + 1) for lr, v in test.items()}
assert [b[1] for b in best.values()] == [4, 6, 35], best          # section 12's table
print({lr: (round(b[0], 5), b[1], round(test[lr][-1], 5)) for lr, b in best.items()})
KS = [0, 1, 2, 3, 4, 6, 10, 15, 25, 35, 50, 75, 100, 150, 200]


def frame(m):
    fig = make_subplots(2, 3, specs=[[{}, {}, {}], [{"colspan": 3}, None, None]], row_heights=[0.5, 0.5],
                        vertical_spacing=0.14, horizontal_spacing=0.04,
                        subplot_titles=[f"learning rate {lr:g}" for lr in LRS] + ["test error, average of 20 datasets"])
    for i, (lr, c) in enumerate(LRS.items(), start=1):
        f0, trees = fits[lr]
        fig.add_trace(go.Scatter(x=X[:, 0], y=y, mode="markers", marker=dict(color="#B8B8B8", size=5)), 1, i)
        fig.add_trace(go.Scatter(x=GRID[:, 0], y=predict(f0, trees[:m], lr, GRID), mode="lines",
                                 line=dict(color=c, width=3)), 1, i)
        if m:
            fig.add_trace(go.Scatter(x=np.arange(1, m + 1), y=test[lr][:m], mode="lines", line=dict(color=c, width=3),
                                     name=f"learning rate {lr:g}", showlegend=True), 2, 1)
            fig.add_trace(go.Scatter(x=[m], y=[test[lr][m - 1]], mode="markers", marker=dict(color=c, size=10)), 2, 1)
            b, at = best[lr]
            if m >= at:
                fig.add_trace(go.Scatter(x=[at], y=[b], mode="markers", marker=dict(symbol="star", size=16, color=c,
                                                                                    line=dict(color="black", width=1))), 2, 1)
    fig.add_trace(go.Scatter(x=[0, 205], y=[0.0025, 0.0025], mode="lines", line=dict(color="#6B6B6B", dash="dot")), 2, 1)
    fig.add_annotation(x=200, y=0.0025, xref="x4", yref="y4", text="noise floor 0.0025", showarrow=False,
                       xanchor="right", yanchor="bottom", font=dict(size=18, color="#6B6B6B"))
    fig.update_xaxes(showticklabels=False, ticks="", row=1)
    fig.update_yaxes(range=[-0.2, 0.9], showticklabels=False, ticks="", row=1)
    fig.update_xaxes(range=[0, 205], title_text="number of trees", row=2, col=1)
    fig.update_yaxes(range=[0.0, 0.01], title_text="test MSE", row=2, col=1)
    fig.update_annotations(font_size=24)
    fig.update_layout(template="simple_white", width=1300, height=900, showlegend=True, legend=dict(x=0.45, y=0.37, yanchor="top", font_size=22),
                      font=dict(family="Latin Modern Roman", size=20), margin=dict(l=80, r=20, t=110, b=60),
                      title=dict(text=f"{m} tree{'s' * (m != 1)}  (★ = lowest test error)", x=0.5, y=0.97, font_size=30))
    fig.for_each_trace(lambda t: t.update(showlegend=bool(t.name and t.name.startswith("learning rate"))))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".lr_frames"
    tmp.mkdir(exist_ok=True)
    for i, m in enumerate(KS):
        frame(m).write_image(tmp / f"{i:03d}.png")
    for i in range(len(KS), len(KS) + 5):                   # hold the last frame
        shutil.copy(tmp / f"{len(KS) - 1:03d}.png", tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1.2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "lr_race.gif")], check=True)
    keys = [Image.open(tmp / f"{KS.index(m):03d}.png").convert("RGB") for m in (1, 6, 35, 200)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "lr_race_frames.png")
    shutil.rmtree(tmp)
