"""AdaGrad (eta = 2) on the students data from (m, b) = (-4, -4), step by step: the path (left) and, for m and b,
the size of the gradient, the learning rate eta / sqrt(v) and the size of the update (right).
b's gradients are large, so its sum v grows fast and its learning rate falls; m keeps a large learning rate.
Run: python adagrad_rates.py -> adagrad_rates.gif, adagrad_rates_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from surf import beside, data_quad, quad_surface, BOWL_LEVELS
from common import BLUE, ORANGE, GREEN, RED, GREY, FONT
from shared import X, y, BEST, grad, loss, run, steps_to

HERE = Path(__file__).parent
ETA = 2.0
P = run("adagrad", ETA)
DONE = steps_to(P)
G = np.array([grad(p) for p in P[:-1]])           # gradient used at step t (t = 1, 2, ...)
V = np.cumsum(G ** 2, axis=0)                      # AdaGrad's running sum of squared gradients
LR = ETA / (np.sqrt(V) + 1e-8)
STEP = np.abs(np.diff(P, axis=0))
assert DONE == 44 and np.allclose(STEP, LR * np.abs(G))
assert np.allclose(STEP[0], ETA) and np.allclose(LR[0], [0.59, 0.126], atol=0.005)   # the Note's worked example
GD = run("gd", 0.3)
m, b = np.linspace(-5, 9, 160), np.linspace(-5, 9, 160)
M, B = np.meshgrid(m, b)
Z = np.log10(((y[None, None, :] - M[..., None] * X[:, 0] - B[..., None]) ** 2).mean(-1))
ZMAX = 80                                                   # the walls go higher than drawn
_p, _H, _l = data_quad(X, y)
TRACES = quad_surface(np.linspace(-5, 9, 90), np.linspace(-5, 9, 90), _p, _H, _l, BOWL_LEVELS, ZMAX, -0.6, 2.4)
height = lambda P: np.array([loss(p) for p in P])
PANELS = [("size of the gradient", np.abs(G), 21), ("learning rate η / √v", LR, 0.8), ("size of the step", STEP, 2.7)]


def frame(k):
    """State after step k (k >= 1)."""
    fig = make_subplots(rows=3, cols=2, column_widths=[0.6, 0.4], specs=[[{"rowspan": 3}, {}], [None, {}], [None, {}]],
                        subplot_titles=["", *[p[0] for p in PANELS]], horizontal_spacing=0.12, vertical_spacing=0.17)
    fig.add_trace(go.Contour(x=m, y=b, z=Z, colorscale="Greys", reversescale=True, showscale=False,
                             contours=dict(start=-0.6, end=2.4, size=0.2), line=dict(width=0.6), opacity=0.5), 1, 1)
    fig.add_trace(go.Scatter(x=GD[:k + 1, 0], y=GD[:k + 1, 1], mode="lines", line=dict(color=GREY, width=2, dash="dot"),
                             name="gradient descent, for comparison"), 1, 1)
    fig.add_trace(go.Scatter(x=P[:k + 1, 0], y=P[:k + 1, 1], mode="lines+markers", name="AdaGrad, η = 2",
                             line=dict(color=GREEN, width=3), marker=dict(size=6, color=GREEN)), 1, 1)
    fig.add_trace(go.Scatter(x=[BEST[0]], y=[BEST[1]], mode="markers", showlegend=False,
                             marker=dict(symbol="star", size=18, color=RED)), 1, 1)
    for row, (title, vals, top) in enumerate(PANELS, start=1):
        v = vals[k - 1]
        fig.add_trace(go.Bar(x=["m", "b"], y=v, marker_color=[BLUE, ORANGE], showlegend=False, width=0.6,
                             text=[f"{a:.2f}" for a in v], textposition="outside", cliponaxis=False), row, 2)
        fig.update_yaxes(range=[0, top], showticklabels=False, ticks="", row=row, col=2)
    fig.update_xaxes(title_text="m (weight of IIT)", range=[-5, 9], row=1, col=1)
    fig.update_yaxes(title_text="b (bias)", range=[-5, 9], row=1, col=1)
    status = f"step {k}" + (f": within 0.01 of the minimum after {DONE} steps" if k >= DONE else "")
    fig.update_layout(template="simple_white", width=1100, height=760, font=dict(FONT, size=22),
                      title=dict(text=status, x=0.5, y=0.98), margin=dict(l=80, r=20, t=140, b=60),
                      legend=dict(x=0, y=1.06, yanchor="bottom", orientation="h"))
    fig.update_annotations(font_size=22)
    beside(fig, TRACES, [(GD[:k + 1], height(GD[:k + 1]), GREY, 4), (P[:k + 1], height(P[:k + 1]), GREEN, 5)], (BEST[0], BEST[1], loss(BEST)), ("m", "b"), (1.0, 1.0, 1.0), ZMAX, xr=[-5, 9], yr=[-5, 9], extra=600)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".rates_frames"
    tmp.mkdir(exist_ok=True)
    for k in range(1, DONE + 1):
        frame(k).write_image(tmp / f"{k - 1:03d}.png")
    for k in range(DONE, DONE + 10):                       # hold the last frame
        shutil.copy(tmp / f"{DONE - 1:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "4", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=1000:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "adagrad_rates.gif")], check=True)
    keys = [Image.open(tmp / f"{k - 1:03d}.png").convert("RGB") for k in (1, 3, 15, DONE)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "adagrad_rates_frames.png")
    shutil.rmtree(tmp)
