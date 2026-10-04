"""Step 1 on the three startups, animated (Plotly frames): slide one constant gamma across the profits. Left: the
profits, the line at gamma and the gaps to it. Right: the total loss 1/2 * sum (y - gamma)^2 against gamma.
The lowest loss is at the mean, 142.41.
Run: python best_constant.py  -> best_constant.gif, best_constant_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
BLUE, RED, GREY = "#4C78A8", "#E45756", "#6B6B6B"
y = pd.read_csv(HERE.parent / "data" / "startups3.csv").profit.to_numpy()
loss = lambda g: 0.5 * np.sum((y - g) ** 2)
G = np.linspace(60, 220, 401)
L = np.array([loss(g) for g in G])
best = y.mean()
assert np.isclose(best, 142.41, atol=0.005) and abs(G[L.argmin()] - best) < 0.5
GAMMAS = list(np.arange(60, 221, 10)) + list(np.arange(210, 142, -10)) + [best]


def frame(g):
    fig = make_subplots(1, 2, horizontal_spacing=0.12, column_widths=[0.45, 0.55],
                        subplot_titles=["profits and the constant γ", "total loss ½ Σ (y − γ)²"])
    xs = [1, 2, 3]
    for x, yi in zip(xs, y):
        fig.add_trace(go.Scatter(x=[x, x], y=[yi, g], mode="lines", line=dict(color=RED, width=4), showlegend=False), 1, 1)
    fig.add_trace(go.Scatter(x=xs, y=y, mode="markers+text", marker=dict(color=BLUE, size=18), showlegend=False,
                             text=[f"{v:.2f}" for v in y], textposition="middle right", textfont=dict(size=20)), 1, 1)
    fig.add_hline(y=g, line=dict(color="black", width=3), row=1, col=1)
    fig.add_trace(go.Scatter(x=G, y=L, mode="lines", line=dict(color=GREY, width=3), showlegend=False), 1, 2)
    fig.add_trace(go.Scatter(x=[g], y=[loss(g)], mode="markers", marker=dict(color="black", size=16),
                             showlegend=False), 1, 2)
    done = np.isclose(g, best)
    if done:
        fig.add_annotation(x=best, y=loss(best), text="lowest: γ = 142.41, the mean", ay=-80, ax=0, arrowhead=2,
                           font=dict(size=22, color=RED), row=1, col=2)
    fig.update_xaxes(tickvals=xs, ticktext=["startup 1", "startup 2", "startup 3"], range=[0.6, 3.8], row=1, col=1)
    fig.update_yaxes(title_text="profit (thousands)", range=[50, 230], row=1, col=1)
    fig.update_xaxes(title_text="γ", range=[60, 220], row=1, col=2)
    fig.update_yaxes(range=[0, 16000], row=1, col=2)
    fig.update_annotations(font_size=24)
    fig.update_layout(template="simple_white", width=1200, height=560, font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text=f"γ = {g:.2f},  loss = {loss(g):,.0f}", x=0.5, y=0.97, font_size=26),
                      margin=dict(l=80, r=30, t=110, b=60))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".best_constant_frames"
    tmp.mkdir(exist_ok=True)
    for i, g in enumerate(GAMMAS):
        frame(g).write_image(tmp / f"{i:03d}.png")
    last = len(GAMMAS) - 1
    for i in range(last + 1, last + 8):
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "4", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=800:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "best_constant.gif")], check=True)
    keys = [Image.open(tmp / f"{GAMMAS.index(g):03d}.png").convert("RGB") for g in (60, 120, 220)]
    keys.append(Image.open(tmp / f"{last:03d}.png").convert("RGB"))
    keys[-1].save(HERE / "best_constant_frames.png")                # the PDF shows the last frame: a 2x2 grid was too small
    shutil.rmtree(tmp)
