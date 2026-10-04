"""Four very different dice. For each, the exact distribution of the sum of n rolls (repeated convolution),
re-centred by n*mu and re-scaled by sqrt(n)*sigma, drawn as a density. As n grows from 1 to 50, all four
settle onto the same curve, the standard normal N(0, 1).
Run: python dice_standardised.py -> dice_standardised.gif, dice_standardised_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from scipy import stats

HERE = Path(__file__).parent
BLUE, ORANGE, GREY = "#4C78A8", "#F58518", "#6B6B6B"
FACES = np.arange(1, 7)
DICE = {"fair": [1, 1, 1, 1, 1, 1], "skewed low": [40, 25, 15, 10, 6, 4],
        "U-shaped": [35, 10, 5, 5, 10, 35], "mostly sixes": [5, 5, 5, 5, 10, 70]}
DICE = {k: np.array(v, float) / sum(v) for k, v in DICE.items()}
NS = [1, 2, 3, 5, 10, 20, 50]
z = np.linspace(-4, 4, 400)


def standardised(p, n):
    mu, var = FACES @ p, (FACES ** 2) @ p - (FACES @ p) ** 2
    out = np.array([1.0])
    for _ in range(n):
        out = np.convolve(out, p)
    sums = np.arange(n, 6 * n + 1)
    assert abs(out.sum() - 1) < 1e-9 and abs(sums @ out - n * mu) < 1e-9          # means add: n * mu
    assert abs((sums ** 2) @ out - (sums @ out) ** 2 - n * var) < 1e-6           # variances add: n * sigma^2
    scale = np.sqrt(n * var)
    return (sums - n * mu) / scale, out * scale, scale                           # density: probability / spacing


def frame(n):
    fig = make_subplots(rows=2, cols=4, subplot_titles=list(DICE), vertical_spacing=0.2, horizontal_spacing=0.06)
    gap = 0
    for c, (name, p) in enumerate(DICE.items(), start=1):
        fig.add_bar(x=FACES, y=p, marker_color=GREY, row=1, col=c, showlegend=False)
        zs, dens, scale = standardised(p, n)
        width = 1 / scale
        fig.add_bar(x=zs, y=dens, width=width * 0.9 if n < 10 else width, marker_color=BLUE, row=2, col=c,
                    showlegend=False)
        fig.add_scatter(x=z, y=stats.norm.pdf(z), mode="lines", line=dict(color=ORANGE, width=3), row=2, col=c,
                        showlegend=False)
        cdf = np.cumsum(dens / scale)
        gap = max(gap, np.max(np.abs(cdf - stats.norm.cdf(zs + width / 2))))     # largest CDF gap at the jumps
    fig.update_yaxes(range=[0, 0.75], row=1, dtick=0.25)
    fig.update_yaxes(range=[0, 1.0], row=2, dtick=0.2)
    fig.update_xaxes(dtick=1, row=1)
    fig.update_xaxes(range=[-4, 4], dtick=2, row=2)
    fig.update_layout(template="simple_white", width=1200, height=680, bargap=0,
                      font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text=f"sum of n = {n} roll{'s' if n > 1 else ''}, re-centred and re-scaled"
                                      f"<br><sup>top: one roll of each die.  bottom: (sum − n·μ) / (√n·σ); "
                                      f"orange: N(0, 1)</sup>", x=0.5, y=0.97),
                      margin=dict(l=50, r=20, t=130, b=40))
    fig.update_annotations(font_size=22)
    return fig, gap


if __name__ == "__main__":
    tmp = HERE / ".dice_frames"
    tmp.mkdir(exist_ok=True)
    k, gaps = 0, {}
    for n in NS:
        fig, gaps[n] = frame(n)
        fig.write_image(tmp / f"key_{n}.png")
        for _ in range(3 if n != NS[-1] else 8):
            shutil.copy(tmp / f"key_{n}.png", tmp / f"{k:03d}.png")
            k += 1
    print("largest gap between the standardised CDF and the normal CDF, over the 4 dice:",
          {n: round(g, 3) for n, g in gaps.items()})
    assert gaps[50] < gaps[5] < gaps[1]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1.5", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=800:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "dice_standardised.gif")], check=True)
    keys = [Image.open(tmp / f"key_{n}.png").convert("RGB") for n in (1, 3, 10, 50)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "dice_standardised_frames.png")
    shutil.rmtree(tmp)
