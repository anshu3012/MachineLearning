"""Plain gradient descent near a saddle point (section 5.5). Loss L = w1^2 - w2^2: it rises along w1 and falls along
w2, and the gradient (2 w1, -2 w2) is zero at the centre. Gradient descent starts at (1.5, 0.001), almost on the
ridge, with learning rate 0.1, 40 steps. Left: the surface with the path. Right: the length of each step on a log
scale. The steps shrink about 40-fold near the flat centre before the path slides off along w2.
Plotly frames (3D surface + line) -> ffmpeg GIF + a grid of key frames for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots

from common import BLUE, RED

HERE = Path(__file__).parent
ETA, STEPS = 0.1, 40
P = [np.array([1.5, 0.001])]
for _ in range(STEPS):
    a, b = P[-1]
    P.append(P[-1] - ETA * np.array([2 * a, -2 * b]))
P = np.array(P)
L = P[:, 0] ** 2 - P[:, 1] ** 2
step = np.linalg.norm(np.diff(P, axis=0), axis=1)          # step[k] = length of step k + 1
SLOW = int(step.argmin()) + 1
assert round(step[0], 2) == 0.30 and round(step.min(), 3) == 0.008 and SLOW == 19, (step[0], step.min(), SLOW)
SMALL = int((step < 0.03).sum())                           # steps shorter than a tenth of the first one
g = np.linspace(-1.6, 1.6, 61)
GX, GY = np.meshgrid(g, g)


def frame(k):
    fig = make_subplots(1, 2, column_widths=[0.58, 0.42], horizontal_spacing=0.08,
                        specs=[[{"type": "scene"}, {"type": "xy"}]])
    fig.add_trace(go.Surface(x=g, y=g, z=GX ** 2 - GY ** 2, colorscale="RdBu", reversescale=True, showscale=False,
                             opacity=0.75), 1, 1)
    fig.add_trace(go.Scatter3d(x=P[:k + 1, 0], y=P[:k + 1, 1], z=L[:k + 1] + 0.04, mode="lines+markers",
                               line=dict(color="black", width=6), marker=dict(size=4, color="black"),
                               showlegend=False), 1, 1)
    fig.add_trace(go.Scatter3d(x=[P[k, 0]], y=[P[k, 1]], z=[L[k] + 0.04], mode="markers",
                               marker=dict(size=9, color=RED), showlegend=False), 1, 1)
    fig.add_scatter(x=np.arange(1, k + 1), y=step[:k], mode="lines+markers", line=dict(color=BLUE, width=3),
                    marker=dict(size=8), showlegend=False, row=1, col=2)
    fig.update_xaxes(title_text="step", range=[0, STEPS + 1], row=1, col=2)
    fig.update_yaxes(title_text="length of the step (log scale)", type="log", range=[-2.4, 0], dtick=1, row=1, col=2)
    where = "sliding down towards the flat centre" if k < 12 else ("crawling on the plateau" if k < 30 else "sliding off along w₂")
    fig.update_layout(template="simple_white", width=1300, height=640, font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text=f"Gradient descent on the saddle L = w₁² − w₂², step {k}: {where}", x=0.5,
                                 font=dict(size=24)),
                      scene=dict(xaxis=dict(title="w₁", nticks=4, tickfont=dict(size=13)),
                                 yaxis=dict(title="w₂", nticks=4, tickfont=dict(size=13)),
                                 zaxis=dict(title="L", range=[-2.6, 2.6], nticks=5, tickfont=dict(size=13)),
                                 camera=dict(eye=dict(x=1.5, y=-1.5, z=0.9)), aspectmode="cube"),
                      margin=dict(l=10, r=20, t=70, b=70))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".saddle_frames"
    tmp.mkdir(exist_ok=True)
    for k in range(STEPS + 1):
        frame(k).write_image(tmp / f"{k:03d}.png")
    for k in range(STEPS + 1, STEPS + 9):
        shutil.copy(tmp / f"{STEPS:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "5", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "saddle_gd.gif")], check=True)
    ims = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (5, SLOW, 32, STEPS)]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "saddle_gd_frames.png")
    shutil.rmtree(tmp)
    print("first step", step[0].round(3), "shortest", step.min().round(4), "at step", SLOW, "steps under 0.03:", SMALL,
          "end", P[-1].round(3), "loss", L[[0, SLOW, STEPS]].round(3))
