"""How a voting regressor predicts (Plotly frames + ffmpeg): a query point x_q sweeps across the noisy sine data;
at each x_q the three base regressors (linear regression, SVR, depth-5 tree, as in app.py) give a number each, and
the vote is their mean. The vote's curve is traced point by point.
Run: python voting_scan.py -> voting_scan.gif, voting_scan_frames.png"""
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import COLOURS, X_train, y_train, base_models  # noqa: E402
from sklearn.ensemble import VotingRegressor  # noqa: E402

names = ["linear regression", "SVR", "decision tree"]
vr = VotingRegressor(base_models(names)).fit(X_train, y_train)
xs = np.linspace(0.05, 4.95, 36)
P = np.array([m.predict(xs[:, None]) for m in vr.estimators_])          # one row per base model
V = vr.predict(xs[:, None])
assert np.allclose(P.mean(0), V)                                        # the vote is exactly the mean
grid = np.linspace(0, 5, 400)
G = np.array([m.predict(grid[:, None]) for m in vr.estimators_])


def frame(k):
    fig = go.Figure(go.Scatter(x=X_train.ravel(), y=y_train, mode="markers", name="training points",
                               marker=dict(color="#FFD24C", size=9, line=dict(color="black", width=1))))
    for n, g in zip(names, G):
        fig.add_trace(go.Scatter(x=grid, y=g, mode="lines", line=dict(color=COLOURS[n], width=2, dash="dashdot"),
                                 opacity=0.6, name=n))
    fig.add_trace(go.Scatter(x=xs[:k + 1], y=V[:k + 1], mode="lines", line=dict(color="#4C78A8", width=5),
                             name="vote = mean of the three"))
    x = xs[k]
    fig.add_vline(x=x, line=dict(color="black", dash="dot", width=2))
    fig.add_trace(go.Scatter(x=[x] * 3, y=P[:, k], mode="markers", showlegend=False,
                             marker=dict(size=16, color=[COLOURS[n] for n in names], line=dict(color="black", width=1.5))))
    fig.add_trace(go.Scatter(x=[x], y=[V[k]], mode="markers", showlegend=False,
                             marker=dict(size=22, symbol="star", color="#4C78A8", line=dict(color="black", width=1.5))))
    vals = " + ".join(f"{p:.2f}" for p in P[:, k]).replace("+ -", "− ")
    fig.update_layout(template="simple_white", width=1000, height=640, font=dict(family="Latin Modern Roman", size=22),
                      title=dict(text=f"x_q = {x:.2f}:  ({vals}) / 3 = {V[k]:.2f}", x=0.5),
                      xaxis=dict(title="x", range=[0, 5]), yaxis=dict(title="y", range=[-2.6, 2.6]),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2, font_size=19),
                      margin=dict(l=70, r=20, t=70, b=160))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".scan_frames"
    tmp.mkdir(exist_ok=True)
    keys = (4, 14, 24, len(xs) - 1)
    j = 0
    for k in range(len(xs)):
        frame(k).write_image(tmp / "f.png")
        for _ in range(4 if k in keys else 1):
            shutil.copy(tmp / "f.png", tmp / f"{j:03d}.png")
            j += 1
        if k in keys:
            shutil.copy(tmp / "f.png", tmp / f"key_{k}.png")
    for _ in range(8):
        shutil.copy(tmp / f"key_{len(xs) - 1}.png", tmp / f"{j:03d}.png")
        j += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "4", "-i", str(tmp / "%03d.png"), "-vf",
                    "fps=8,scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "voting_scan.gif")], check=True)
    ims = [Image.open(tmp / f"key_{k}.png").convert("RGB") for k in (14, len(xs) - 1)]   # two frames, stacked:
    w, h = ims[0].size                                                                     # readable in the PDF
    sheet = Image.new("RGB", (w, 2 * h + 16), "white")
    for n, im in enumerate(ims):
        sheet.paste(im, (0, n * (h + 16)))
    sheet.save(HERE / "voting_scan_frames.png")
    shutil.rmtree(tmp)
