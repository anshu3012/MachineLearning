"""Four ways to drive a differential-drive robot (r = 0.05 m, L = 0.2 m), each played for 2 s from pose (0, 0, 0):
equal wheel speeds 0.5/0.5 -> straight; 0.2/-0.2 -> spin on the spot; 0.4/0 -> pivot about the left wheel (R = 0.1 m);
0.6/0.4 -> circle of radius 0.5 m. v = (vR + vL)/2, omega = (vR - vL)/L. Green dot: the turning point.
Run: python four_cases.py -> four_cases.gif, four_cases_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import FONT, GREEN, GREY, make_gif
from robotdraw import L, robot, step

here = Path(__file__).parent
CASES = [("equal speeds: straight line", 0.5, 0.5), ("opposite speeds: spin on the spot", 0.2, -0.2),
         ("left wheel stopped: pivot", 0.4, 0.0), ("unequal speeds: circle", 0.6, 0.4)]
DT, T = 0.01, 2.0
paths = []
for _, vR, vL in CASES:
    v, w = (vR + vL) / 2, (vR - vL) / L
    q, path = (0.0, 0.0, 0.0), [(0.0, 0.0, 0.0)]
    for _ in range(round(T / DT)):
        q = step(q, v, w, DT)
        path.append(q)
    paths.append((np.array(path), v, w))
assert abs(paths[0][0][-1, 0] - 1.0) < 1e-9                   # straight: 0.5 m/s for 2 s = 1 m
assert np.allclose(paths[1][0][-1, :2], 0)                    # spin: the midpoint stays put
assert abs((0.4 + 0) / 2 / ((0.4 - 0) / L) - 0.1) < 1e-12     # pivot radius = L/2


def frame(t):
    titles = []
    for (name, vR, vL), (p, v, w) in zip(CASES, paths):
        titles.append(f"<b>{name}</b><br>v<sub>R</sub> = {vR}, v<sub>L</sub> = {vL}  →  v = {v:.1f}, ω = {w:.0f}")
    fig = make_subplots(rows=2, cols=2, subplot_titles=titles, horizontal_spacing=0.08, vertical_spacing=0.16)
    k = round(t / DT)
    for i, ((name, vR, vL), (p, v, w)) in enumerate(zip(CASES, paths)):
        r, c = i // 2 + 1, i % 2 + 1
        fig.add_trace(go.Scatter(x=p[:k + 1, 0], y=p[:k + 1, 1], mode="lines", line=dict(color=GREY, width=3, dash="dot")),
                      row=r, col=c)
        for tr in robot(tuple(p[k])):
            fig.add_trace(tr, row=r, col=c)
        if abs(w) > 1e-9:                                     # turning point: distance v/w to the robot's left
            R = v / w
            x, y, th = p[k]
            fig.add_trace(go.Scatter(x=[x - R * np.sin(th)], y=[y + R * np.cos(th)], mode="markers",
                                     marker=dict(size=13, color=GREEN)), row=r, col=c)
    fig.update_xaxes(range=[-0.45, 1.15], dtick=0.5, showgrid=True, gridcolor="#eee", scaleanchor=None)
    fig.update_yaxes(range=[-0.35, 1.05], dtick=0.5, showgrid=True, gridcolor="#eee")
    for i in range(1, 5):
        fig.update_yaxes(scaleanchor=f"x{i if i > 1 else ''}", scaleratio=1, row=(i - 1) // 2 + 1, col=(i - 1) % 2 + 1)
    fig.update_layout(template="simple_white", width=1100, height=1000, font=FONT, showlegend=False,
                      margin=dict(l=40, r=20, t=150, b=50),
                      title=dict(x=0.5, y=0.975, font=dict(size=24), text=f"t = {t:.1f} s   (green dot: turning point; speeds in m/s, ω in rad/s)"))
    fig.update_annotations(selector=dict(yref="paper"), font_size=19)
    return fig


ts = [0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]
figs = [frame(t) for t in ts]
holds = [4] + [3] * (len(ts) - 2) + [16]
make_gif(figs, here / "four_cases", fps=6, holds=holds, keys=[len(ts) - 1], cols=1, width=950)
