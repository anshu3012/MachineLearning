"""Section 7.3: what the warm-up length does to the schedule of Vaswani et al. (2017, eq. 3), d_model = 512. The
warm-up length slides from 1,000 to 8,000 steps: a longer warm-up gives a later and lower peak, and every curve ends
on the same 1/sqrt(step) decay. The paper's 4,000 is marked.
Run: python warmup_slide.py  -> warmup_slide.gif, warmup_slide_frames.png (Plotly frames + ffmpeg: a curve changing)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image

from common import BLUE, FONT, GREY, ORANGE

HERE = Path(__file__).parent
d_model = 512
step = np.unique(np.round(np.geomspace(1, 100_000, 600)).astype(int))
lr = lambda w: d_model ** -0.5 * np.minimum(step ** -0.5, step * w ** -1.5)
peak = lambda w: (d_model * w) ** -0.5
assert abs(peak(4000) * 1e4 - 6.99) < 0.005                                    # the Note's table
WARMUPS = [1000, 1500, 2000, 2500, 3000, 3500, 4000, 5000, 6000, 7000, 8000]
BIG = dict(FONT, size=22)


def frame(w, ghosts=()):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=step, y=lr(4000) * 1e4, mode="lines", line=dict(color=GREY, width=2, dash="dot"),
                             name="the paper: warm-up 4,000"))
    for g in ghosts:
        fig.add_trace(go.Scatter(x=step, y=lr(g) * 1e4, mode="lines", line=dict(color=BLUE, width=2), opacity=0.35,
                                 showlegend=False))
    fig.add_vrect(x0=0, x1=w, fillcolor=ORANGE, opacity=0.12, line_width=0)
    fig.add_trace(go.Scatter(x=step, y=lr(w) * 1e4, mode="lines", line=dict(color=BLUE, width=5),
                             name="this warm-up"))
    fig.add_trace(go.Scatter(x=[w], y=[peak(w) * 1e4], mode="markers", marker=dict(color=ORANGE, size=16),
                             showlegend=False))
    fig.update_layout(template="simple_white", width=1000, height=600, font=BIG, margin=dict(l=90, r=30, t=90, b=70),
                      title=dict(text=f"warm-up {w:,} steps: peak {peak(w) * 1e4:.2f} × 10⁻⁴", x=0.5,
                                 font=dict(size=30)),
                      xaxis=dict(title="training step", tickformat=",", range=[0, 30_000]),
                      yaxis=dict(title="learning rate (× 10⁻⁴)", range=[0, 15]),
                      legend=dict(x=0.55, y=0.98))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".warm_frames"
    tmp.mkdir(exist_ok=True)
    n = 0
    for k, w in enumerate(WARMUPS):
        img = tmp / f"k{k}.png"
        frame(w).write_image(img)
        for _ in range(8 if w == 4000 else 4):                  # 1 s per value at 4 fps; pause on the paper's value
            shutil.copy(img, tmp / f"{n:03d}.png")
            n += 1
    last = tmp / "last.png"
    frame(8000, ghosts=(1000, 2000)).write_image(last)
    for _ in range(14):
        shutil.copy(last, tmp / f"{n:03d}.png")
        n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "4", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=800:-2:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "warmup_slide.gif")], check=True)
    ims = [Image.open(tmp / f"k{k}.png").convert("RGB") for k in (0, 6)] + [Image.open(last).convert("RGB")]
    w0, h0 = ims[0].size
    grid = Image.new("RGB", (3 * w0, h0), "white")
    for k, im in enumerate(ims):
        grid.paste(im, (k * w0, 0))
    grid.save(HERE / "warmup_slide_frames.png")
    shutil.rmtree(tmp)
