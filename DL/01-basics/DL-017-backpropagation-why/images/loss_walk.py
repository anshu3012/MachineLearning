"""Two of the nine knobs at once: gradient descent on W121 (input 2 -> hidden 1) and the output bias b21 of the
2-2-1 linear network, all other parameters frozen at their starting values (weights 0.1, biases 0).
Loss = mean squared error over the four students. Left: the path on the loss contours. Right: the predicted
packages move onto the real ones. Learning rate 0.2, start W121 = 0.1, b21 = 0.
Run: python loss_walk.py -> loss_walk.gif, loss_walk_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots

from common import BLUE, ORANGE, RED, GREY

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=22)
x1, x2, y = np.array([8, 7, 6, 5.]), np.array([8, 9, 10, 12.]), np.array([4, 5, 6, 7.])


def y_hat(W121, b21):                                       # network with the 7 other parameters at their start
    O11 = 0.1 * x1 + W121 * x2
    O12 = 0.1 * x1 + 0.1 * x2
    return 0.1 * O11 + 0.1 * O12 + b21


def grad(p):                                                # mean over students of d(y - y_hat)^2
    r = y_hat(*p) - y
    return np.array([2 * np.mean(r * 0.1 * x2), 2 * np.mean(r)])


loss = lambda p: np.mean((y - y_hat(*p)) ** 2)
LR, N = 0.2, 3000
P = [np.array([0.1, 0.0])]
for _ in range(N):
    P.append(P[-1] - LR * grad(P[-1]))
P = np.array(P)
A = np.c_[0.1 * x2, np.ones(4)]
best = np.linalg.lstsq(A, y - y_hat(0, 0), rcond=None)[0]   # exact minimum of this 2-knob loss
assert np.allclose(P[-1], best, atol=1e-3), (P[-1], best)
assert all(loss(a) >= loss(b) for a, b in zip(P, P[1:]))    # every step goes downhill
assert np.isclose(y_hat(0.1, 0)[0], 0.32)                    # student 1 at the start, as in the Note
STEPS = [0, 1, 2, 3, 5] + sorted({int(round(v)) for v in np.geomspace(8, N, 30)})

gw, gb = np.linspace(-1, 9, 220), np.linspace(-4, 4, 220)
GW, GB = np.meshgrid(gw, gb)
Z = np.log10(np.mean([(yy - (0.1 * (0.1 * a + GW * b) + 0.01 * (a + b) + GB)) ** 2 for a, b, yy in zip(x1, x2, y)], 0))


def frame(k):
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.13,
                        subplot_titles=("loss over two knobs", "predicted vs real package"))
    fig.add_trace(go.Contour(x=gw, y=gb, z=Z, colorscale="Greys", reversescale=True, showscale=False, opacity=0.5,
                             contours=dict(start=-1.5, end=2.5, size=0.25), line=dict(width=0.6)), 1, 1)
    Q = P[:k + 1]
    fig.add_trace(go.Scatter(x=Q[:, 0], y=Q[:, 1], mode="lines", line=dict(color=ORANGE, width=4)), 1, 1)
    fig.add_trace(go.Scatter(x=[Q[-1, 0]], y=[Q[-1, 1]], mode="markers", marker=dict(size=20, color=ORANGE,
                             line=dict(color="black", width=2))), 1, 1)
    fig.add_trace(go.Scatter(x=[best[0]], y=[best[1]], mode="markers", marker=dict(symbol="star", size=22, color=RED)), 1, 1)
    yh = y_hat(*P[k])
    for xi, a, b in zip(x2, y, yh):                          # residual sticks
        fig.add_trace(go.Scatter(x=[xi, xi], y=[a, b], mode="lines", line=dict(color=GREY, width=2, dash="dot")), 1, 2)
    fig.add_trace(go.Scatter(x=x2, y=y, mode="markers", marker=dict(size=16, color=BLUE)), 1, 2)
    fig.add_trace(go.Scatter(x=x2, y=yh, mode="markers", marker=dict(size=16, color=ORANGE, symbol="diamond")), 1, 2)
    fig.add_annotation(x=8, y=7.6, text="● real   ◆ predicted", showarrow=False, xanchor="left", row=1, col=2,
                       font=dict(size=22, color=GREY))
    fig.update_layout(template="simple_white", width=1150, height=580, font=FONT, showlegend=False,
                      title=dict(text=f"step {k}   ·   mean loss {loss(P[k]):.3f}", x=0.5, y=0.97),
                      margin=dict(l=80, r=30, t=110, b=70))
    fig.update_annotations(font_size=24, selector=dict(text="loss over two knobs"))
    fig.update_annotations(font_size=24, selector=dict(text="predicted vs real package"))
    fig.update_xaxes(title="W121", range=[-1, 9], row=1, col=1)
    fig.update_yaxes(title="b21", range=[-4, 4], row=1, col=1)
    fig.update_xaxes(title="profile score", range=[7.5, 12.5], row=1, col=2)
    fig.update_yaxes(title="package (LPA)", range=[-0.5, 8], row=1, col=2)
    return fig


if __name__ == "__main__":
    from surftilt import tilt_gif                              # the same loss as a surface, tilting to the map
    sub = slice(None, None, 2)
    zl = lambda p: np.log10(loss(p))
    Q = P[STEPS]
    tilt_gif("loss_surface", HERE, dict(x=gw[sub], y=gb[sub], Z=Z[sub, sub], xlab="W121", ylab="b21", zlab="log10 loss",
             cscale="Greys", reverse=True, contours=dict(start=-1.5, end=2.5, size=0.25), marks=[dict(x=Q[:, 0], y=Q[:, 1], z=[zl(q) for q in Q], color=ORANGE, size=4),
                    dict(x=[P[0, 0]], y=[P[0, 1]], z=[zl(P[0])], color="black", size=8, line=False),
                    dict(x=[best[0]], y=[best[1]], z=[zl(best)], color=RED, size=10, symbol="diamond", line=False)]), zasp=0.6, floor=0.3)
    tmp = HERE / ".walk_frames"
    tmp.mkdir(exist_ok=True)
    for i, k in enumerate(STEPS):
        frame(k).write_image(tmp / f"{i:03d}.png")
    for i in range(len(STEPS), len(STEPS) + 12):              # hold the last frame
        shutil.copy(tmp / f"{len(STEPS) - 1:03d}.png", tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "5", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "loss_walk.gif")], check=True)
    keys = [Image.open(tmp / f"{STEPS.index(k):03d}.png").convert("RGB")
            for k in (0, 1, min(STEPS, key=lambda s: abs(s - 100)), N)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "loss_walk_frames.png")
    shutil.rmtree(tmp)
    print("best", best.round(3), "loss", round(loss(best), 4), {k: round(loss(P[k]), 3) for k in (1, 10, 100, 1000, N)})
