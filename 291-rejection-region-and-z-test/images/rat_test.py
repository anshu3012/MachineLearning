"""The rat drug test, step by step: the sampling distribution of the mean if H0 is true (mean 1.2 s, standard
error 0.5/sqrt(100) = 0.05 s), the observed mean 1.05 s counted as 3 standard errors below, the tail area beyond
+-3 (0.27%), the two-tailed rejection region at alpha = 0.05, then the one-tailed region for H1: mu < 1.2.
Run: python rat_test.py  -> rat_test.gif, rat_test_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from scipy import stats

HERE = Path(__file__).parent
RED, BLUE, GREEN = "#E45756", "#4C78A8", "#54A24B"
MU0, SE, XBAR = 1.2, 0.5 / np.sqrt(100), 1.05
Z = (XBAR - MU0) / SE
assert np.isclose(SE, 0.05) and np.isclose(Z, -3)
assert round(2 * stats.norm.cdf(-3), 4) == 0.0027 and round(stats.norm.cdf(-3), 5) == 0.00135
x = np.linspace(MU0 - 4.2 * SE, MU0 + 4.2 * SE, 800)
pdf = stats.norm.pdf(x, MU0, SE)
TOP = pdf.max() * 1.45


def shade(fig, lo, hi, color):
    s = x[(x >= lo) & (x <= hi)]
    fig.add_scatter(x=s, y=stats.norm.pdf(s, MU0, SE), fill="tozeroy", fillcolor=color, line=dict(width=0))


def frame(step):
    fig = go.Figure()
    title, box = "If H₀ is true: means of 100 rats", "centre 1.2 s<br>standard error 0.05 s"
    if step >= 4:
        shade(fig, x[0], MU0 - 3 * SE, "rgba(228,87,86,0.35)")
        shade(fig, MU0 + 3 * SE, x[-1], "rgba(228,87,86,0.35)")
    if step == 4:
        title, box = "How rare is a mean this far out?", "beyond ±3 SE: <b>0.27%</b><br>of samples"
        for s, t in ((-1, ""), (1, "0.135%<br>in each tail")):
            fig.add_annotation(x=MU0 + s * 3.4 * SE, y=stats.norm.pdf(3.4) / SE, ax=0, ay=-70, text=t, arrowhead=2,
                               arrowwidth=3, arrowcolor=RED, font=dict(size=24, color=RED))
    if step == 5:
        fig.data = ()
        c = stats.norm.ppf(0.975)
        shade(fig, x[0], MU0 - c * SE, "rgba(228,87,86,0.45)")
        shade(fig, MU0 + c * SE, x[-1], "rgba(228,87,86,0.45)")
        for s in (-1, 1):
            fig.add_vline(x=MU0 + s * c * SE, line=dict(color=RED, width=3, dash="dash"), opacity=1)
        title = "H₁: μ ≠ 1.2 → two tails, α = 0.05"
        box = "cutoffs 1.2 ± 1.96 × 0.05<br>= 1.102 and 1.298<br>1.05 is in the red: <b>reject H₀</b>"
    if step == 6:
        fig.data = ()
        c = stats.norm.ppf(0.95)
        shade(fig, x[0], MU0 - c * SE, "rgba(228,87,86,0.45)")
        fig.add_vline(x=MU0 - c * SE, line=dict(color=RED, width=3, dash="dash"), opacity=1)
        title = "H₁: μ < 1.2 → left tail only, α = 0.05"
        box = "cutoff 1.2 − 1.645 × 0.05<br>= 1.118<br>1.05 is in the red: <b>reject H₀</b>"
    fig.add_scatter(x=x, y=pdf, mode="lines", line=dict(color="black", width=3))
    if step >= 1:
        fig.add_scatter(x=[XBAR], y=[0], mode="markers", marker=dict(size=22, color=GREEN, line=dict(width=2, color="black")),
                        cliponaxis=False)
        fig.add_annotation(x=XBAR, y=TOP * 0.16, text="our rats<br>1.05 s", showarrow=False, font=dict(size=24, color=GREEN))
    for k in range(1, min(step, 3) + 1) if 2 <= step <= 4 else []:
        a, b = MU0 - (k - 1) * SE, MU0 - k * SE
        y = TOP * (0.74 + 0.06 * k)
        fig.add_annotation(x=b, y=y, ax=a, ay=y, xref="x", yref="y", axref="x", ayref="y", showarrow=True,
                           arrowhead=2, arrowwidth=3, arrowcolor=BLUE, text="")
        fig.add_annotation(x=(a + b) / 2, y=y + TOP * 0.045, text=f"{k} SE", showarrow=False, font=dict(size=22, color=BLUE))
    if step >= 3:
        fig.add_annotation(x=XBAR, y=TOP * 0.30, text="<b>z = −3</b>", showarrow=False, font=dict(size=28, color=BLUE))
    fig.add_annotation(x=0.99, y=0.97, xref="paper", yref="paper", xanchor="right", yanchor="top", showarrow=False,
                       align="left", bgcolor="white", text=box, font=dict(size=24))
    ticks = [round(MU0 + k * SE, 2) for k in range(-4, 5)]
    fig.update_layout(template="simple_white", width=900, height=560, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=24),
                      title=dict(text=title, x=0.5, y=0.96),
                      xaxis=dict(title="mean response time of 100 rats (s)", tickvals=ticks, range=[x[0], x[-1]]),
                      yaxis=dict(showticklabels=False, range=[0, TOP]),
                      margin=dict(l=30, r=30, t=70, b=70))
    return fig


PLAN = [(0, 6), (1, 5), (2, 3), (3, 4), (4, 8), (5, 10), (6, 12)]  # (step, frames to hold)
KEYS = (1, 3, 4, 5, 6)

if __name__ == "__main__":
    tmp = HERE / ".rat_frames"
    tmp.mkdir(exist_ok=True)
    n, keys = 0, {}
    for step, hold in PLAN:
        frame(step).write_image(tmp / f"{n:03d}.png")
        keys[step] = n
        for _ in range(hold - 1):
            shutil.copy(tmp / f"{n:03d}.png", tmp / f"{n + 1:03d}.png")
            n += 1
        n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "4", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=640:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "rat_test.gif")], check=True)
    ims = [Image.open(tmp / f"{keys[k]:03d}.png").convert("RGB") for k in (3, 4, 5, 6)]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "rat_test_frames.png")
    shutil.rmtree(tmp)
