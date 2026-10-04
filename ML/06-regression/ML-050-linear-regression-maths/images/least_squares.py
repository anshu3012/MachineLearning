"""Least squares, watched: the 160 training students with a line and each error drawn as a square (left), linked to
the same line as one dot on the contour map of E(m, b) (right). Both axes on the left use the same unit, so the squares
are true squares and E is their total area. First the line turns (m changes, b fixed at its best value), then it
slides (b changes, m fixed): each time E is smallest at the OLS values m = 0.558, b = -0.896.
Run: python least_squares.py  -> least_squares.gif, least_squares_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image

from common import B, M, X_train, y_train

HERE = Path(__file__).parent
BLUE, ORANGE, RED, GREY = "#4C78A8", "#F58518", "#E45756", "#6B6B6B"
x, y = X_train["cgpa"].to_numpy(), y_train.to_numpy()
E = lambda m, b: float(((y - m * x - b) ** 2).sum())
DM, DB = 0.06, 0.4                                          # sweep ranges: E rises to about 3 times its minimum
ms, bs = np.linspace(M - 1.1 * DM, M + 1.1 * DM, 120), np.linspace(B - 1.1 * DB, B + 1.1 * DB, 120)
Z = np.array([[E(m, b) for m in ms] for b in bs])
EMIN = E(M, B)


def sweep(a, z, k):
    return list(np.linspace(a, z, k))


turn = sweep(M + DM, M - DM, 24) + sweep(M - DM, M, 12)[1:]
slide = sweep(B + DB, B - DB, 24) + sweep(B - DB, B, 12)[1:]
PLAN = ([(m, B, "turn") for m in turn] + [(M, B, "turn")] * 5 + [(M, b, "slide") for b in slide]
        + [(M, B, "best")] * 12)


def squares(m, b):
    """One closed outline per student: the square between the point and the line, side |error|."""
    px, py = [], []
    for xi, yi in zip(x, y):
        d = yi - (m * xi + b)
        s = abs(d)
        sx = xi - s if d > 0 else xi                         # put the square on alternate sides to cut overlap
        px += [sx, sx + s, sx + s, sx, sx, None]
        py += [yi, yi, yi - d, yi - d, yi, None]
    return px, py


def frame(i):
    m, b, phase = PLAN[i]
    trail = np.array([(p[0], p[1]) for p in PLAN[:i + 1]])
    fig = make_subplots(1, 2, column_widths=[0.5, 0.5], horizontal_spacing=0.1,
                        subplot_titles=["each error drawn as a square", "the same line as one dot on E(m, b)"])
    px, py = squares(m, b)
    fig.add_trace(go.Scatter(x=px, y=py, mode="lines", fill="toself", fillcolor="rgba(245,133,24,0.22)",
                             line=dict(color=ORANGE, width=0.8)), 1, 1)
    fig.add_trace(go.Scatter(x=x, y=y, mode="markers", marker=dict(size=6, color=GREY)), 1, 1)
    xs = np.array([3.8, 10.2])
    fig.add_trace(go.Scatter(x=xs, y=m * xs + b, mode="lines", line=dict(color=BLUE, width=4)), 1, 1)
    fig.add_trace(go.Contour(x=ms, y=bs, z=np.log10(Z), colorscale="Blues", reversescale=True, showscale=False,
                             contours=dict(start=np.log10(EMIN) + 0.04, end=np.log10(Z.max()), size=0.07),
                             line=dict(width=0.5), opacity=0.55), 1, 2)
    fig.add_trace(go.Scatter(x=trail[:, 0], y=trail[:, 1], mode="lines", line=dict(color=GREY, width=2, dash="dot")), 1, 2)
    fig.add_trace(go.Scatter(x=[M], y=[B], mode="markers", marker=dict(symbol="x", size=16, color="black")), 1, 2)
    fig.add_trace(go.Scatter(x=[m], y=[b], mode="markers", marker=dict(size=18, color=BLUE, line=dict(color="white", width=2))), 1, 2)
    head = {"turn": "turning the line: m changes, b stays",
            "slide": "sliding the line: b changes, m stays",
            "best": "smallest total area: m = 0.558, b = −0.896"}[phase]
    fig.add_annotation(x=0.5, y=1.2, xref="paper", yref="paper", showarrow=False, font=dict(size=28), text=head)
    e = E(m, b)
    fig.add_annotation(x=4.1, y=5.2, xref="x", yref="y", xanchor="left", showarrow=False, font=dict(size=26, color=ORANGE),
                       text=f"E = total area = {e:.1f}")
    fig.update_xaxes(title="CGPA", range=[3.8, 10.2], row=1, col=1)
    fig.update_yaxes(title="package", range=[0.3, 5.7], scaleanchor="x", scaleratio=1, row=1, col=1)
    fig.update_xaxes(title="m (slope)", range=[M - 1.1 * DM, M + 1.1 * DM], row=1, col=2)
    fig.update_yaxes(title="b (intercept)", range=[B - 1.1 * DB, B + 1.1 * DB], row=1, col=2)
    fig.update_layout(template="simple_white", width=1200, height=640, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=20), margin=dict(l=70, r=30, t=130, b=70))
    fig.update_annotations(selector=dict(text="each error drawn as a square"), font_size=22)
    fig.update_annotations(selector=dict(text="the same line as one dot on E(m, b)"), font_size=22)
    return fig


# Checks: E falls to its minimum at the OLS values along both sweeps, and E is the squares' total area.
assert min(turn, key=lambda m: E(m, B)) == M and min(slide, key=lambda b: E(M, b)) == B
assert abs(EMIN - 16.55) < 0.01, EMIN
print("E at start of turn", round(E(turn[0], B), 2), "start of slide", round(E(M, slide[0]), 2), "minimum", round(EMIN, 2))

if __name__ == "__main__":
    tmp = HERE / ".ls_frames"
    tmp.mkdir(exist_ok=True)
    done = {}
    for i, key in enumerate(PLAN):
        if key in done:
            shutil.copy(tmp / f"{done[key]:03d}.png", tmp / f"{i:03d}.png")
        else:
            frame(i).write_image(tmp / f"{i:03d}.png")
            done[key] = i
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "8", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=960:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "least_squares.gif")], check=True)
    picks = [0, 23, len(turn) + 6, len(PLAN) - 1]               # bad slope, other side, bad intercept, best line
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in picks]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "least_squares_frames.png")
    shutil.rmtree(tmp)
