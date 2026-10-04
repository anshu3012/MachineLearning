"""From soft to hard assignment, animated: two components with equal weights and equal variance sigma^2, centred at
0 and 4; sigma shrinks from 3 to 0.1. Top: the two weighted normal curves. Bottom: the responsibility of component 1
across x; the observation at x = 1 is marked (0.731 at sigma = 2, 0.982 at sigma = 1, then 1). The curve becomes a
step at the midpoint 2: each observation goes wholly to the nearer centre, as in k-means.
Run: python hard_soft.py -> hard_soft.gif, hard_soft_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from scipy import stats
from scipy.special import expit

from em_core import BLUE, FONT, GREEN, ORANGE, RED

HERE = Path(__file__).parent
x = np.linspace(-2, 6, 801)
SIGMAS = np.round(np.geomspace(3, 0.1, 22), 3)
r1 = lambda v, s: expit(stats.norm(0, s).logpdf(v) - stats.norm(4, s).logpdf(v))   # N1 / (N1 + N2), stable
assert abs(r1(1, 2) - 0.731) < 1e-3 and abs(r1(1, 1) - 0.982) < 1e-3
assert r1(x[x < 1.9], 0.1).min() > 0.999 and r1(x[x > 2.1], 0.1).max() < 0.001


def frame(s):
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.16, row_heights=[0.45, 0.55],
                        subplot_titles=("two components, equal weights, same σ",
                                        "responsibility of the component at 0"))
    for m, c in ((0, ORANGE), (4, BLUE)):
        fig.add_trace(go.Scatter(x=x, y=0.5 * stats.norm(m, s).pdf(x), mode="lines", line=dict(color=c, width=4)), 1, 1)
    fig.add_trace(go.Scatter(x=x, y=r1(x, s), mode="lines", line=dict(color=GREEN, width=4)), 2, 1)
    fig.add_trace(go.Scatter(x=[1], y=[r1(1, s)], mode="markers", marker=dict(size=16, color=RED)), 2, 1)
    fig.add_annotation(x=1, y=r1(1, s), text=f"x = 1: {r1(1, s):.3f}", showarrow=False, xanchor="right", xshift=-12,
                       yshift=-18, font=dict(size=20, color=RED), row=2, col=1)
    for r in (1, 2):
        fig.add_vline(x=2, line=dict(color="black", dash="dot", width=2), row=r, col=1)
    fig.update_xaxes(range=[-2, 6], row=1, col=1)
    fig.update_yaxes(range=[0, 0.6], title_text="weighted density", row=1, col=1)
    fig.update_xaxes(range=[-2, 6], title_text="x", row=2, col=1)
    fig.update_yaxes(range=[-0.05, 1.08], title_text="responsibility", row=2, col=1)
    fig.update_layout(template="simple_white", width=900, height=780, showlegend=False, font=FONT,
                      title=dict(text=f"σ = {s:.2f}", x=0.5, y=0.985), margin=dict(l=80, r=30, t=100, b=60))
    fig.update_annotations(font_size=20)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".hard_frames"
    tmp.mkdir(exist_ok=True)
    for k, s in enumerate(SIGMAS):
        frame(s).write_image(tmp / f"{k:03d}.png")
    last = len(SIGMAS) - 1
    for k in range(last + 1, last + 7):                        # hold the last frame
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "hard_soft.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (0, 7, 14, last)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "hard_soft_frames.png")
    shutil.rmtree(tmp)
