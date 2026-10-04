"""The z statistic counts standard errors. Training example: if H0 is true, the sample mean of n = 30 days varies
around mu0 = 50 with standard error 5 / sqrt(30) = 0.913. We lay standard-error rulers from 50 towards the
observed 53: three whole ones and 0.29 of a fourth, so z = 3.29.
Run: python count_se.py  -> count_se.gif, count_se_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from scipy import stats

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, GREY = "#4C78A8", "#F58518", "#54A24B", "#6B6B6B"
MU0, XBAR, SIGMA, N = 50, 53, 5, 30
SE = SIGMA / np.sqrt(N)
Z = (XBAR - MU0) / SE
assert round(SE, 3) == 0.913 and round(Z, 2) == 3.29
x = np.linspace(46.5, 54.5, 600)
pdf = stats.norm.pdf(x, MU0, SE)
TOP = pdf.max()


def frame(k):
    """k = number of rulers laid (0..3), 4 = the partial ruler, 5 = the z scale appears."""
    fig = go.Figure()
    fig.add_scatter(x=x, y=pdf, mode="lines", line=dict(color="black", width=3))
    fig.add_vline(x=MU0, line=dict(color=GREY, width=2, dash="dot"), opacity=1)
    fig.add_annotation(x=MU0, y=TOP * 1.08, text="μ₀ = 50", showarrow=False, font=dict(size=24, color=GREY))
    fig.add_scatter(x=[XBAR], y=[0], mode="markers", marker=dict(size=20, color=GREEN, symbol="diamond"))
    fig.add_annotation(x=XBAR, y=0.06, text="x̄ = 53", showarrow=False, font=dict(size=24, color=GREEN))
    y0 = 0.13
    for j in range(min(k, 3)):
        a, b = MU0 + j * SE, MU0 + (j + 1) * SE
        fig.add_shape(type="rect", x0=a, x1=b, y0=y0, y1=y0 + 0.05, fillcolor=BLUE if j % 2 == 0 else "#9ECAE9",
                      line=dict(color="white", width=2), opacity=1, layer="above")
        fig.add_annotation(x=(a + b) / 2, y=y0 + 0.025, text=str(j + 1), showarrow=False,
                           font=dict(size=24, color="white" if j % 2 == 0 else "black"))
    if k >= 4:
        a = MU0 + 3 * SE
        fig.add_shape(type="rect", x0=a, x1=XBAR, y0=y0, y1=y0 + 0.05, fillcolor=ORANGE,
                      line=dict(color="white", width=2), opacity=1, layer="above")
        fig.add_annotation(x=XBAR + 0.05, y=y0 + 0.025, text="0.29", showarrow=False, xanchor="left",
                           font=dict(size=24, color=ORANGE))
    if 1 <= k <= 3:
        fig.add_annotation(x=MU0 + 0.05, y=y0 + 0.09, xanchor="left", showarrow=False, bgcolor="white",
                           text="one ruler = SE = 5/√30 = 0.913", font=dict(size=22, color=BLUE))
    if k >= 5:
        fig.add_annotation(x=(MU0 + XBAR) / 2, y=0.33, showarrow=False, bgcolor="white",
                           text="<b>z = 3 / 0.913 = 3.29</b> standard errors", font=dict(size=28, color="black"))
    ticks = [MU0 + j * SE for j in range(-3, 5)] if k >= 5 else list(range(47, 55))
    labels = [f"z = {j}" if j == 0 else str(j) for j in range(-3, 5)] if k >= 5 else [str(t) for t in range(47, 55)]
    fig.update_layout(template="simple_white", width=900, height=540, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=24),
                      title=dict(text="if H₀ is true, x̄ varies around 50" if k < 5 else "the same axis, counted in SEs",
                                 x=0.5, y=0.96),
                      xaxis=dict(title="cars per day" if k < 5 else "z", range=[46.5, 54.5], tickvals=ticks,
                                 ticktext=labels),
                      yaxis=dict(showticklabels=False, range=[0, TOP * 1.15]), margin=dict(l=30, r=30, t=70, b=60))
    return fig


PLAN = [(0, 5), (1, 4), (2, 4), (3, 4), (4, 6), (5, 12)]

if __name__ == "__main__":
    tmp = HERE / ".se_frames"
    tmp.mkdir(exist_ok=True)
    n, keys = 0, []
    for i, (k, hold) in enumerate(PLAN):
        frame(k).write_image(tmp / f"{n:03d}.png")
        if k in (0, 1, 4, 5):
            keys.append(n)
        for _ in range(hold - 1):
            shutil.copy(tmp / f"{n:03d}.png", tmp / f"{n + 1:03d}.png")
            n += 1
        n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=640:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "count_se.gif")], check=True)
    ims = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in keys]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "count_se_frames.png")
    shutil.rmtree(tmp)
