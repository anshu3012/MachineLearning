"""Momentum's oscillations for three decay factors (section 3). The bowl L(w) = w^2/2 of Figure 5 (gradient w), from
w = -10 with learning rate 0.1: plain gradient descent and momentum with beta = 0.9, 0.8 and 0.5. The weight is traced
step by step. A larger beta arrives sooner, overshoots further and takes longer to settle.
Plotly frames -> ffmpeg GIF + a grid of key frames for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image

from common import BLUE, GREEN, GREY, ORANGE, RED

HERE = Path(__file__).parent
ETA, STEPS = 0.1, 100


def run(beta):
    w, v, P = -10.0, 0.0, [-10.0]
    for _ in range(STEPS):
        v = beta * v + ETA * w
        w = w - v
        P.append(w)
    return np.array(P)


RUNS = [("gradient descent", 0.0, GREY), ("momentum, β = 0.5", 0.5, GREEN), ("momentum, β = 0.8", 0.8, BLUE),
        ("momentum, β = 0.9", 0.9, ORANGE)]
PATH = {name: run(b) for name, b, _ in RUNS}
first = {n: int(np.argmax(np.abs(p) < 1)) for n, p in PATH.items()}                      # first step within 1 of the minimum
over = {n: float(p.max()) for n, p in PATH.items()}                                      # furthest past the minimum
settle = {n: int(np.max(np.nonzero(np.abs(p) >= 0.1)[0])) + 1 for n, p in PATH.items()}  # within 0.1 from this step on
assert settle["momentum, β = 0.9"] == 81 and round(over["momentum, β = 0.9"], 2) == 6.04   # the numbers of section 6
assert settle["momentum, β = 0.5"] < settle["momentum, β = 0.8"] < settle["gradient descent"] < settle["momentum, β = 0.9"]


def frame(k):
    fig = go.Figure()
    fig.add_hline(y=0, line=dict(color=RED, width=1.5, dash="dot"))
    for name, _, c in RUNS:
        label = f"{name}: settled at step {settle[name]}" if k >= settle[name] else name
        fig.add_scatter(x=np.arange(k + 1), y=PATH[name][:k + 1], mode="lines", name=label, line=dict(color=c, width=4))
        fig.add_scatter(x=[k], y=[PATH[name][k]], mode="markers", marker=dict(size=13, color=c), showlegend=False)
    fig.update_layout(template="simple_white", width=1050, height=620, font=dict(family="Latin Modern Roman", size=21),
                      title=dict(text=f"step {k} (dotted line: the minimum, w = 0)", x=0.5),
                      xaxis=dict(title="step", range=[0, STEPS]), yaxis=dict(title="weight w", range=[-10.5, 7]),
                      legend=dict(x=0.42, y=0.03, bgcolor="rgba(255,255,255,0.85)"), margin=dict(l=75, r=20, t=60, b=65))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".beta_frames"
    tmp.mkdir(exist_ok=True)
    SHOW = list(range(0, 30)) + list(range(30, STEPS + 1, 2))
    made = {}
    for k in SHOW:
        made[k] = tmp / f"k{k}.png"
        frame(k).write_image(made[k])
    seq = SHOW + [STEPS] * 10
    for i, k in enumerate(seq):
        shutil.copy(made[k], tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "8", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=800:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "beta_sweep.gif")], check=True)
    ims = [Image.open(made[k]).convert("RGB") for k in (5, 15, 40, STEPS)]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "beta_sweep_frames.png")
    shutil.rmtree(tmp)
    for n in PATH:
        print(n, "| within 1 at step", first[n], "| furthest past", round(over[n], 2), "| settled from step", settle[n])
