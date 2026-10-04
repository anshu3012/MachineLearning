"""The trade-off curve drawn one degree at a time, with the fits that produce it. Top: 20 fits of the current degree
(orange), their average (blue) and the true wave (dashed). Bottom: bias squared, variance and expected test error,
measured over the 10,000 training sets of common.py, drawn up to the current degree. Bias falls, variance rises, and
the total is lowest in between. Our own design; no source to credit.
Plotly frames -> ffmpeg GIF + _frames.png grid. Run: python tradeoff_build.py"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image

from common import NOISE, decompose, f, fits, xs

HERE = Path(__file__).parent
BLUE, ORANGE, RED, GREY = "#4C78A8", "#F58518", "#E45756", "#6B6B6B"
DEGS = list(range(1, 12))
B2, VAR, GRID = [], [], {}
for d in DEGS:
    at_x, on_grid = fits(d)
    b, v = decompose(at_x)
    B2.append(b), VAR.append(v)
    GRID[d] = on_grid[:, :20]
TOTAL = np.array(B2) + np.array(VAR) + NOISE ** 2
BEST = DEGS[int(np.argmin(TOTAL))]
assert BEST == 5 and round(TOTAL[4], 3) == 0.326 and round(TOTAL[0], 3) == 0.695      # the Note's numbers
assert all(np.diff(VAR) > 0) and B2[0] > 100 * B2[4]


def frame(d, final=False):
    fig = make_subplots(2, 1, row_heights=[0.5, 0.5], vertical_spacing=0.2)
    g = GRID[d]
    for j in range(20):
        fig.add_trace(go.Scatter(x=xs, y=g[:, j], mode="lines", line=dict(color=ORANGE, width=1.5), opacity=0.45), 1, 1)
    fig.add_trace(go.Scatter(x=xs, y=f(xs), mode="lines", line=dict(color="black", width=3, dash="dash")), 1, 1)
    fig.add_trace(go.Scatter(x=xs, y=g.mean(axis=1), mode="lines", line=dict(color=BLUE, width=4)), 1, 1)
    k = d                                                     # degrees 1..d are drawn
    for y, c, w in ((B2, BLUE, 3), (VAR, ORANGE, 3), (TOTAL, RED, 5)):
        fig.add_trace(go.Scatter(x=DEGS[:k], y=list(y[:k]), mode="lines+markers", line=dict(color=c, width=w),
                                 marker=dict(size=10)), 2, 1)
    fig.add_trace(go.Scatter(x=[1, 11], y=[NOISE ** 2] * 2, mode="lines", line=dict(color=GREY, dash="dash")), 2, 1)
    for txt, c, xx in (("bias²", BLUE, 2), ("variance", ORANGE, 4.5), ("test error", RED, 7.5), ("noise", GREY, 10.3)):
        fig.add_annotation(x=xx, y=0.98, xref="x2", yref="y2", text=txt, showarrow=False, font=dict(size=22, color=c))
    if final:
        fig.add_annotation(x=BEST, y=float(TOTAL[BEST - 1]), xref="x2", yref="y2", ax=0, ay=-70,
                           text=f"lowest test error: degree {BEST}", font=dict(size=22, color=RED), arrowcolor=RED)
    fig.update_xaxes(title="x", range=[-2.9, 2.9], row=1, col=1)
    fig.update_yaxes(title="y", range=[-4, 4], row=1, col=1)
    fig.update_xaxes(title="polynomial degree", range=[0.7, 11.3], dtick=1, row=2, col=1)
    fig.update_yaxes(title="squared error", range=[0, 1.05], row=2, col=1)
    fig.update_layout(template="simple_white", width=1000, height=900, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=20), margin=dict(l=80, r=20, t=80, b=70),
                      title=dict(text=f"degree {d}: 20 fits (orange), their average (blue), the truth (dashed)", x=0.5))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".trade_frames"
    tmp.mkdir(exist_ok=True)
    n = 0
    for d in DEGS:
        frame(d).write_image(tmp / f"d{d}.png")
        shutil.copy(tmp / f"d{d}.png", tmp / f"{n:03d}.png")
        n += 1
    frame(11, final=True).write_image(tmp / "final.png")
    for _ in range(5):                                        # hold the final frame
        shutil.copy(tmp / "final.png", tmp / f"{n:03d}.png")
        n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "tradeoff_build.gif")], check=True)
    keys = [Image.open(tmp / name).convert("RGB") for name in ("d1.png", "final.png")]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, h), "white")                # one row: the PDF caps figure height
    for i, im in enumerate(keys):
        sheet.paste(im, (i * (w + 16), 0))
    sheet.save(HERE / "tradeoff_build_frames.png")
    shutil.rmtree(tmp)
