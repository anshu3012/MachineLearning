"""Why all-positive inputs make training zigzag (section 5.4 and Figure 3), as a worked illustration. One linear node
y_hat = w1 a1 + w2 a2 learns by stochastic gradient descent (squared error, one observation per step, learning rate
2.5) from 200 observations whose target follows w* = (1, -1). Left: inputs a1, a2 between 0.1 and 0.9, like sigmoid
outputs (all positive). Right: the same inputs minus 0.5, like tanh outputs (centred on 0). Both start at w = (-1, 1).
Each step's gradient is (y_hat - y) * (a1, a2): with positive inputs both weights move the same way.
Plotly frames -> ffmpeg GIF, plus the final frame for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from common import BLUE, GREEN, ORANGE

HERE = Path(__file__).parent
rng = np.random.default_rng(0)
A_pos = rng.uniform(0.1, 0.9, (200, 2))
A_cen = A_pos - 0.5
W_STAR = np.array([1.0, -1.0])
STEPS, LR = 40, 2.5


def sgd(A):
    y = A @ W_STAR
    w, path = np.array([-1.0, 1.0]), [np.array([-1.0, 1.0])]
    for t in range(STEPS):
        i = t % len(A)
        g = (A[i] @ w - y[i]) * A[i]
        w = w - LR * g
        path.append(w.copy())
    return np.array(path)


P_pos, P_cen = sgd(A_pos), sgd(A_cen)
same_sign = np.mean([np.sign(d[0]) == np.sign(d[1]) for d in np.diff(P_pos, axis=0) if np.all(d != 0)])
assert same_sign == 1.0                                       # every positive-input step moves both weights together
dist = lambda P, t: np.linalg.norm(P[t] - W_STAR)
assert round(dist(P_pos, 20), 2) == 1.01 and round(dist(P_cen, 20), 2) == 0.10, (dist(P_pos, 20), dist(P_cen, 20))
g = np.linspace(-3.5, 3.5, 141)
G1, G2 = np.meshgrid(g, g)


def loss_surface(A):
    y = A @ W_STAR
    W = np.stack([G1.ravel(), G2.ravel()], 1)
    return ((A @ W.T - y[:, None]) ** 2).mean(0).reshape(G1.shape)


L_pos, L_cen = loss_surface(A_pos), loss_surface(A_cen)


def frame(t):
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1, subplot_titles=(
        f"Inputs all positive (like sigmoid): {dist(P_pos, t):.2f} from the target",
        f"Inputs centred on 0 (like tanh): {dist(P_cen, t):.2f} from the target"))
    for col, L, P, c in ((1, L_pos, P_pos, ORANGE), (2, L_cen, P_cen, BLUE)):
        fig.add_trace(go.Contour(x=g, y=g, z=np.log10(L + 1e-3), showscale=False, colorscale="Greys", reversescale=True,
                                 contours=dict(coloring="lines"), line=dict(width=1), hoverinfo="skip"), 1, col)
        fig.add_scatter(x=P[:t + 1, 0], y=P[:t + 1, 1], mode="lines+markers", line=dict(color=c, width=3),
                        marker=dict(size=6), showlegend=False, row=1, col=col)
        fig.add_scatter(x=[1], y=[-1], mode="markers", marker=dict(size=20, symbol="star", color=GREEN,
                        line=dict(width=1, color="black")), showlegend=False, row=1, col=col)
        fig.add_scatter(x=[-1], y=[1], mode="markers", marker=dict(size=12, color="black"), showlegend=False,
                        row=1, col=col)
        fig.update_xaxes(title_text="w₁", range=[-3.5, 3.5], row=1, col=col)
        fig.update_yaxes(title_text="w₂", range=[-3.5, 3.5], row=1, col=col, scaleanchor="x" if col == 1 else "x2")
    fig.update_layout(template="simple_white", width=1300, height=660, font=dict(family="Latin Modern Roman", size=19),
                      title=dict(text=f"Stochastic gradient descent, step {t} (black dot: start; star: target w = (1, −1))",
                                 x=0.5, y=0.97, font=dict(size=21)),
                      margin=dict(l=70, r=20, t=110, b=70))
    for a in fig.layout.annotations[:2]:
        a.font.size = 19
    return fig


if __name__ == "__main__":
    from surftilt import tilt_gif                              # the two loss surfaces, tilting down to the maps of zigzag.gif
    i0 = np.argmin(abs(g + 1))                                  # grid index of w = (-1, 1) is checked below
    print("loss at start (-1, 1): positive", round(float(((A_pos @ [-1, 1] - A_pos @ W_STAR) ** 2).mean()), 3),
          "centred", round(float(((A_cen @ [-1, 1] - A_cen @ W_STAR) ** 2).mean()), 3))
    zl = lambda L: np.log10(L + 1e-3)
    pane = lambda A, L, P, c, t: dict(
        x=g[::2], y=g[::2], Z=zl(L)[::2, ::2], xlab="w₁", ylab="w₂", zlab="log10 loss", cscale="Greys", reverse=True, title=t,
        contours=dict(start=-3, end=float(zl(L).max()), size=float((zl(L).max() + 3) / 14)),
        zrange=(-3, float(max(zl(L_pos).max(), zl(L_cen).max()))),
        marks=[dict(x=P[:, 0], y=P[:, 1], z=[float(zl(((A @ q - A @ W_STAR) ** 2).mean())) for q in P], color=c, size=3),
               dict(x=[-1], y=[1], z=[float(zl(((A @ [-1, 1] - A @ W_STAR) ** 2).mean()))], color="black", size=7, line=False),
               dict(x=[1], y=[-1], z=[-3], color=GREEN, size=9, symbol="diamond", line=False)])
    tilt_gif("loss_surfaces", HERE, [pane(A_pos, L_pos, P_pos, ORANGE, "inputs all positive"),
                                     pane(A_cen, L_cen, P_cen, BLUE, "inputs centred on 0")], zasp=0.6, floor=0.3)
    print("distance after", STEPS, "steps: positive", round(dist(P_pos, STEPS), 3), "centred", round(dist(P_cen, STEPS), 3))
    tmp = HERE / ".zz_frames"
    tmp.mkdir(exist_ok=True)
    SHOW = [0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25, 30, 40]
    keys = []
    for t in SHOW:
        keys.append(tmp / f"t{t}.png")
        frame(t).write_image(keys[-1])
    seq = [0] * 2 + list(range(1, len(SHOW))) + [len(SHOW) - 1] * 6
    for j, i in enumerate(seq):
        shutil.copy(keys[i], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=96[p];[b][p]paletteuse",
                    str(HERE / "zigzag.gif")], check=True)
    shutil.copy(keys[-1], HERE / "zigzag_frames.png")
    shutil.rmtree(tmp)
