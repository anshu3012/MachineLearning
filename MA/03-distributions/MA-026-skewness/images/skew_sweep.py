"""Skewness swept from 0 to +1.6, back, and to -1.6. Each shape is a gamma distribution with shape k = 4 / skew^2
(skewness of a gamma is 2 / sqrt(k)), mirrored for negative skew, shifted so its mode sits at 0 and scaled to
standard deviation 1; skew 0 is the normal limit. Mode, median and mean separate as the tail grows; the bar below
reads the skewness on the scale of section 6.
Run: python skew_sweep.py -> skew_sweep.gif, skew_sweep_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image
from plotly.subplots import make_subplots
from scipy import stats

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
x = np.linspace(-4, 6, 800)
SKEWS = np.r_[np.linspace(0, 1.6, 9), np.linspace(1.4, 0, 8), np.linspace(-0.2, -1.6, 8)]


def shape(g):
    """pdf on x, and mode, median, mean, for skewness g (mode at 0, standard deviation 1)."""
    if abs(g) < 1e-9:
        return stats.norm.pdf(x), 0.0, 0.0, 0.0
    k = 4 / g ** 2
    d = stats.gamma(k, loc=-(k - 1), scale=1)                # mode (k - 1) moved to 0
    sd, s = np.sqrt(k), np.sign(g)
    pdf = sd * d.pdf(s * x * sd)                             # mirror for negative skew, rescale to sd 1
    return pdf, 0.0, s * d.median() / sd, s * d.mean() / sd


for g in (0.8, -1.2):                                        # the construction really has skewness g
    k = 4 / g ** 2
    assert abs(np.sign(g) * float(stats.gamma(k).stats(moments="s")) - g) < 1e-9


for g in SKEWS[SKEWS > 0]:                                   # the order the Note states holds in every frame
    _, mo, me, mn = shape(g)
    assert mo < me < mn


def band(g):
    a = abs(g)
    return ("approximately symmetric", GREEN) if a < 0.5 else ("moderately skewed", ORANGE) if a <= 1 else \
        ("highly skewed", RED)


def frame(g):
    pdf, mo, me, mn = shape(g)
    name, col = band(g)
    fig = make_subplots(rows=2, cols=1, row_heights=[0.8, 0.2], vertical_spacing=0.16)
    fig.add_scatter(x=x, y=pdf, mode="lines", line=dict(color=BLUE, width=4), fill="tozeroy",
                    fillcolor="rgba(76,120,168,0.15)", row=1, col=1)
    marks = [("mode", mo, GREEN, "dot"), ("median", me, ORANGE, "dash"), ("mean", mn, RED, "solid")]
    for i, (lab, v, c, dash) in enumerate(marks):
        fig.add_shape(type="line", x0=v, x1=v, y0=0, y1=0.62, line=dict(color=c, width=4, dash=dash), opacity=1,
                      row=1, col=1)
        fig.add_annotation(x=0.99, y=0.97 - 0.1 * i, xref="x domain", yref="y domain", xanchor="right",
                           showarrow=False, text=f"{lab} {v:+.2f}", font=dict(size=22, color=c))
    for lo, hi, c in [(-2, -1, RED), (-1, -0.5, ORANGE), (-0.5, 0.5, GREEN), (0.5, 1, ORANGE), (1, 2, RED)]:
        fig.add_shape(type="rect", x0=lo, x1=hi, y0=0, y1=1, fillcolor=c, opacity=0.35, line_width=0, row=2, col=1)
    fig.add_scatter(x=[g], y=[0.5], mode="markers", marker=dict(symbol="diamond", size=24, color="black"),
                    row=2, col=1)
    fig.update_xaxes(range=[-4, 6], dtick=1, title_text="value (standard deviations from the mode)", row=1, col=1)
    fig.update_yaxes(range=[0, 0.66], title_text="density", row=1, col=1)
    fig.update_xaxes(range=[-2, 2], dtick=0.5, title_text="skewness", row=2, col=1)
    fig.update_yaxes(visible=False, range=[0, 1], row=2, col=1)
    fig.update_layout(template="simple_white", width=900, height=720, showlegend=False,
                      title=dict(text=f"skewness {g:+.1f}: <span style='color:{col}'>{name}</span>", x=0.5, y=0.97),
                      font=dict(family="Latin Modern Roman", size=20), margin=dict(l=70, r=30, t=70, b=60))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".sweep_frames"
    tmp.mkdir(exist_ok=True)
    seq = list(SKEWS)
    for i, g in enumerate(seq):
        frame(g).write_image(tmp / f"{i:03d}.png")
    last = len(seq) - 1
    for k in range(last + 1, last + 7):                      # hold the last frame
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "4", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "skew_sweep.gif")], check=True)
    keys = [Image.open(tmp / f"{seq.index(g):03d}.png").convert("RGB") for g in (SKEWS[0], SKEWS[4], SKEWS[8], SKEWS[-1])]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "skew_sweep_frames.png")
    shutil.rmtree(tmp)
