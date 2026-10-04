"""One full round of the gradient boosting algorithm on the three startups, animated (Plotly frames), then more rounds.
x-axis: R&D spend (the feature the tree splits on); y-axis: profit. Steps 1, 2(a), 2(b), 2(c), 2(d) appear in turn,
with learning rate 0.1; the last frames repeat the round 5, 20 and 60 times.
Run: python one_round.py  -> one_round.gif, one_round_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from sklearn.ensemble import GradientBoostingRegressor

HERE = Path(__file__).parent
BLUE, RED, GREEN, GREY = "#4C78A8", "#E45756", "#54A24B", "#6B6B6B"
d = pd.read_csv(HERE.parent / "data" / "startups3.csv")
X, y, rd = d[["rd", "admin", "marketing"]].to_numpy(), d.profit.to_numpy(), d.rd.to_numpy()
ETA, CUT = 0.1, (28.66 + 100.67) / 2
F0 = y.mean()
r = y - F0
left = rd <= CUT                                           # region R11: startup 3
gamma = np.where(left, r[left].mean(), r[~left].mean())    # step 2(c) for squared error: the leaf's mean residual
F1 = F0 + ETA * gamma
gbr = GradientBoostingRegressor(n_estimators=60, learning_rate=ETA, max_depth=1).fit(X, y)
staged = list(gbr.staged_predict(X))
assert np.allclose(r, [49.85, 1.85, -51.70], atol=0.005) and np.allclose(gamma, [25.85, 25.85, -51.70], atol=0.005)
assert np.allclose(staged[0], F1) and np.allclose(F1, [144.995, 144.995, 137.24], atol=0.005)


def base(title, pred, regions=False):
    fig = go.Figure()
    if regions:
        fig.add_vrect(x0=0, x1=CUT, fillcolor=BLUE, opacity=0.10, line_width=0)
        fig.add_vrect(x0=CUT, x1=190, fillcolor=GREEN, opacity=0.10, line_width=0)
        fig.add_vline(x=CUT, line=dict(color=GREY, dash="dash", width=2))
        fig.add_annotation(x=CUT / 2, y=222, text="region R<sub>11</sub>", showarrow=False, font_size=22)
        fig.add_annotation(x=(CUT + 190) / 2, y=222, text="region R<sub>21</sub>", showarrow=False, font_size=22)
        fig.add_annotation(x=CUT, y=62, text="R&D spend = 64.67", showarrow=False, font_size=18, xshift=85)
    for x, p in zip(rd, pred):                              # the model's prediction for each startup
        fig.add_trace(go.Scatter(x=[x - 12, x + 12], y=[p, p], mode="lines", line=dict(color="black", width=5),
                                 showlegend=False))
    fig.add_trace(go.Scatter(x=rd, y=y, mode="markers+text", marker=dict(color=BLUE, size=20), showlegend=False,
                             text=[f"startup {i + 1}<br>{v:.2f}" for i, v in enumerate(y)],
                             textposition=["middle left", "top center", "bottom right"], textfont=dict(size=18)))
    fig.update_xaxes(title_text="R&D spend (thousands)", range=[0, 190])
    fig.update_yaxes(title_text="profit (thousands)", range=[50, 232])
    fig.update_layout(template="simple_white", width=1100, height=640, font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text=title, x=0.5, y=0.96, font_size=25), margin=dict(l=80, r=30, t=90, b=70))
    return fig


def gaps(fig, pred, labels=True):
    for x, yi, p in zip(rd, y, pred):
        fig.add_trace(go.Scatter(x=[x, x], y=[p, yi], mode="lines", line=dict(color=RED, width=4), showlegend=False))
        if labels:
            fig.add_annotation(x=x, y=(p + yi) / 2, text=f"r = {yi - p:+.2f}", showarrow=False, xshift=58,
                               yshift=-30 if abs(yi - p) < 10 else 0, font=dict(size=20, color=RED))


def frames():
    out = []                                               # (figure, how many times to repeat it, key frame?)
    flat = np.full(3, F0)
    out.append((base("Step 1: the best constant, F<sub>0</sub> = 142.41 (the mean)", flat), 6, True))
    f = base("Step 2(a): pseudo-residuals r = y − F<sub>0</sub>", flat); gaps(f, flat)
    out.append((f, 7, True))
    f = base("Step 2(b): a tree on the pseudo-residuals makes two terminal regions", flat, True); gaps(f, flat)
    out.append((f, 7, True))
    f = base("Step 2(c): leaf values γ = −51.70 (R<sub>11</sub>) and 25.85 (R<sub>21</sub>)", flat, True)
    gaps(f, flat, False)
    for x0, x1, g in [(0, CUT, gamma[2]), (CUT, 190, gamma[0])]:
        f.add_trace(go.Scatter(x=[x0, x1], y=[F0 + g, F0 + g], mode="lines", line=dict(color=RED, width=3, dash="dot"),
                               showlegend=False))
        f.add_annotation(x=x0 + 0.72 * (x1 - x0) if g < 0 else (x0 + x1) / 2, y=F0 + g, text=f"F<sub>0</sub> + γ = {F0 + g:.2f}", showarrow=False,
                         yshift=-18 if g > 0 else 18, font=dict(size=19, color=RED))
    out.append((f, 7, True))
    for t in np.linspace(0, 1, 6):                         # the update slides in
        out.append((base("Step 2(d): F<sub>1</sub> = F<sub>0</sub> + 0.1 × γ", F0 + t * ETA * gamma, True), 1, False))
    f = base("Step 2(d): F<sub>1</sub> = 144.995, 144.995, 137.24  (a tenth of each γ)", F1, True)
    out.append((f, 7, True))
    for m in list(range(2, 21)) + [25, 30, 40, 50, 60]:    # the loop repeats: new residuals, new tree, new update
        f = base(f"Repeat step 2: after {m} trees", staged[m - 1]); gaps(f, staged[m - 1], False)
        out.append((f, 8 if m == 60 else 1, m in (5, 60)))
    return out


if __name__ == "__main__":
    tmp = HERE / ".one_round_frames"
    tmp.mkdir(exist_ok=True)
    n, keys = 0, []
    for fig, rep, key in frames():
        fig.write_image(tmp / f"{n:03d}.png")
        if key:
            keys.append(Image.open(tmp / f"{n:03d}.png").convert("RGB"))
        for k in range(1, rep):
            shutil.copy(tmp / f"{n:03d}.png", tmp / f"{n + k:03d}.png")
        n += rep
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "4", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=820:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "one_round.gif")], check=True)
    keys = keys[1:4] + keys[4:5] + keys[5:7]               # 2(a), 2(b), 2(c), 2(d), after 5 trees, after 60 trees
    w, h = keys[0].size
    grid = Image.new("RGB", (2 * w, 3 * h), "white")
    for i, im in enumerate(keys):
        grid.paste(im, ((i % 2) * w, (i // 2) * h))
    grid.save(HERE / "one_round_frames.png")
    shutil.rmtree(tmp)
