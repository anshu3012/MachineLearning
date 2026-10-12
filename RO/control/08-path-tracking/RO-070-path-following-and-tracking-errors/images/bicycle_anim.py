"""The kinematic bicycle model at work, one frame per 0.25 s for 8 s, both cars at 2 m/s. Left: full lock,
delta = 26.6 deg (tan = 0.5): the heading turns at 2 x 0.5 / 2.5 = 0.4 rad/s and the rear axle circles the ICC at
R = 5 m. Right: delta = 14.04 deg (tan = 0.25), the steering the course's arc needs: 0.2 rad/s, R = 10 m. Green: the
ICC and the lines from it to the rear and front wheels, square to each wheel. After 8 s the left car has turned
3.2 rad (183 deg) and the right car 1.6 rad (92 deg). Run -> bicycle_anim.gif, bicycle_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from coursedraw import car, label, minus, trail
from gifkit import BLUE, FONT, GREEN, make_gif
from plotly.subplots import make_subplots
from trackkit import DELTA_MAX, WHEELBASE, run

here = Path(__file__).parent
deg = np.degrees
CASES = [(DELTA_MAX, "full lock, δ = 26.6°"), (np.arctan(0.25), "the arc's steering, δ = 14.04°")]
R = [run(lambda q, t, d=d: (2.0, d), q0=(0.0, 0.0, 0.0), stop=lambda q: False, t_max=8.0) for d, _ in CASES]
assert abs(deg(np.arctan(0.25)) - 14.04) < 0.005
for r, (d, _), rad in zip(R, CASES, (5.0, 10.0)):
    assert abs(WHEELBASE / np.tan(d) - rad) < 1e-9
    assert abs(2.0 * np.tan(d) / WHEELBASE - 2.0 / rad) < 1e-9
assert round(R[0]["th"][800], 1) == 3.2 and round(R[1]["th"][800], 1) == 1.6


def frame(t):
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08)
    k = int(round(t / 0.01))
    for c, (r, (d, name)) in enumerate(zip(R, CASES), start=1):
        rad = WHEELBASE / np.tan(d)
        x, y, th = r["x"][k], r["y"][k], r["th"][k]
        icc = (0.0, rad)
        trail(fig, r["x"][:k + 1], r["y"][:k + 1], BLUE, (1, c))
        fx, fy = x + WHEELBASE * np.cos(th), y + WHEELBASE * np.sin(th)
        fig.add_trace(go.Scatter(x=[x, icc[0], fx], y=[y, icc[1], fy], mode="lines",
                                 line=dict(color=GREEN, width=2.5, dash="dash"), showlegend=False), row=1, col=c)
        fig.add_trace(go.Scatter(x=[icc[0]], y=[icc[1]], mode="markers", marker=dict(color=GREEN, size=13),
                                 showlegend=False), row=1, col=c)
        label(fig, icc[0] - 0.6, icc[1], "ICC", GREEN, (1, c), size=17, anchor="right")
        car(fig, (x, y, th), d, BLUE, (1, c))
        label(fig, 0.0, -4.2 if c == 1 else -3.4, name, BLUE, (1, c), size=18)
        label(fig, 0.0, -5.4 if c == 1 else -5.0, f"R = {rad:.0f} m, turning {2.0 / rad:.1f} rad/s", BLUE, (1, c),
              size=17)
        lim = 7.5 if c == 1 else 13.0
        fig.update_xaxes(range=[-lim, lim], showgrid=True, gridcolor="#EEEEEE", zeroline=False, row=1, col=c,
                         title=dict(text="x (m)", standoff=2))
        fig.update_yaxes(range=[-6.2, 2 * lim - 4.0], showgrid=True, gridcolor="#EEEEEE", zeroline=False, row=1, col=c,
                         scaleanchor="x" if c == 1 else "x2", scaleratio=1, title=dict(text="y (m)", standoff=2))
    title = (f"t = {t:.2f} s at 2 m/s<br><span style='font-size:19px'>heading turned: left {deg(R[0]['th'][k]):.0f}°,"
             f" right {deg(R[1]['th'][k]):.0f}°</span>")
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=720, showlegend=False,
                      margin=dict(l=80, r=30, t=110, b=50), title=dict(x=0.5, y=0.97, yanchor="top", text=minus(title)))
    return fig


ts = list(np.arange(0, 8.0, 0.25)) + [8.0]
figs = [frame(t) for t in ts]
holds = [4] + [1] * (len(ts) - 2) + [12]
make_gif(figs, here / "bicycle_anim", fps=5, holds=holds, keys=[0, 8, 16, len(ts) - 1], cols=2, width=800)
