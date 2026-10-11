"""Two robots at (2, 1) drive forward at 0.5 m/s for 1 s: one facing along x (theta = 0), one along y (theta = 90 deg).
The one facing x ends at (2.5, 1), the one facing y at (2, 1.5): same position, same speed, different heading,
different place. Faint: the start pose; orange: the path so far.
Run: python heading_anim.py -> heading_anim.gif, heading_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import FONT, GREY, ORANGE, RED, make_gif
from robotdraw import robot, step

here = Path(__file__).parent
V, T, DT = 0.5, 1.0, 0.1
RUNS = [("facing along x (θ = 0°)", 0.0), ("facing along y (θ = 90°)", np.pi / 2)]
paths = []
for _, th in RUNS:
    q, p = (2.0, 1.0, th), [(2.0, 1.0, th)]
    for _ in range(round(T / DT)):
        q = step(q, V, 0.0, DT)
        p.append(q)
    paths.append(np.array(p))
assert np.allclose(paths[0][-1, :2], (2.5, 1)) and np.allclose(paths[1][-1, :2], (2, 1.5))
END = [("(2.5, 1) after 1 s", 2.5, 0.86, "center", "top"), ("(2, 1.5) after 1 s", 2.13, 1.5, "left", "middle")]


def frame(k):
    titles = [f"<b>{name}</b><br>at ({p[k, 0]:.2f}, {p[k, 1]:.2f})" for (name, _), p in zip(RUNS, paths)]
    fig = make_subplots(rows=1, cols=2, subplot_titles=titles, horizontal_spacing=0.1)
    for c, p in enumerate(paths, start=1):
        for tr in robot(tuple(p[0]), scale=0.8, opacity=0.25, arrow=False):
            fig.add_trace(tr, row=1, col=c)
        for tr in robot(tuple(p[k]), scale=0.8, arrow=False):
            fig.add_trace(tr, row=1, col=c)
        fig.add_trace(go.Scatter(x=p[:k + 1, 0], y=p[:k + 1, 1], mode="lines", line=dict(color=ORANGE, width=5)),
                      row=1, col=c)
        fig.add_trace(go.Scatter(x=[2], y=[1], mode="markers", marker=dict(size=9, color="black")), row=1, col=c)
        if k == len(p) - 1:
            s, x, y, xa, ya = END[c - 1]
            fig.add_trace(go.Scatter(x=[p[k, 0]], y=[p[k, 1]], mode="markers", marker=dict(size=13, color=RED)),
                          row=1, col=c)
            fig.add_annotation(x=x, y=y, xref=f"x{c}", yref=f"y{c}", text=s, showarrow=False, xanchor=xa, yanchor=ya,
                               font=dict(color=RED, size=21), bgcolor="white")
    fig.update_xaxes(range=[1.5, 2.8], dtick=0.25, title="x (m)", showgrid=True, gridcolor="#eee")
    fig.update_yaxes(range=[0.6, 1.75], dtick=0.25, title="y (m)", showgrid=True, gridcolor="#eee")
    fig.update_yaxes(scaleanchor="x", scaleratio=1, row=1, col=1)
    fig.update_yaxes(scaleanchor="x2", scaleratio=1, row=1, col=2)
    fig.add_annotation(x=0.5, y=-0.28, xref="paper", yref="paper", showarrow=False, font=dict(color=GREY, size=20),
                       text="same position (2, 1), same speed 0.5 m/s: different heading, different place one second later")
    fig.update_layout(template="simple_white", width=1100, height=700, font=FONT, showlegend=False,
                      margin=dict(l=70, r=20, t=150, b=130),
                      title=dict(x=0.5, y=0.96, font=dict(size=24),
                                 text=f"t = {k * DT:.1f} s   (both drive forward at 0.5 m/s)"))
    fig.update_annotations(selector=dict(xref="paper", yref="paper", showarrow=False), font_size=20)
    return fig


ks = list(range(len(paths[0])))
figs = [frame(k) for k in ks]
holds = [6] + [2] * (len(ks) - 2) + [20]
make_gif(figs, here / "heading_anim", fps=6, holds=holds, keys=[5, len(ks) - 1], cols=1, width=950)
