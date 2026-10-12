"""Animation: relaxation on a corridor of 11 nodes 0.1 m apart. Node 0 touches an obstacle and is held at 1, node 10 is
the door and is held at 0; the 9 nodes between start at 1. A Gauss-Seidel sweep visits nodes 1 to 9 in turn and sets
each to the average of its two neighbours' latest values. Sweep 1 is shown node by node (node 9 becomes
(1 + 0) / 2 = 0.5), then whole sweeps. The values settle on the straight line 0.9, 0.8, ..., 0.1: every node is the
average of its neighbours, so no node is lower than both of them, and from every node one neighbour is lower.
Run -> relax1d.gif, relax1d_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, RED, make_gif

here = Path(__file__).parent
n = 11
v = np.ones(n)
v[-1] = 0.0
states = [("sweep 0: inside nodes start at 1", v.copy(), None)]
for i in range(1, n - 1):                      # sweep 1, node by node
    v[i] = 0.5 * (v[i - 1] + v[i + 1])
    states.append((f"sweep 1, node {i}: the average of nodes {i - 1} and {i + 1}", v.copy(), i))
assert v[9] == 0.5 and np.allclose(v[1:9], 1)
done = 1
for target in (2, 3, 4, 5, 10, 20, 40, 80):
    while done < target:
        for i in range(1, n - 1):
            v[i] = 0.5 * (v[i - 1] + v[i + 1])
        done += 1
    states.append((f"after sweep {target}", v.copy(), None))
line = 1 - np.arange(n) / 10
assert np.abs(v - line).max() < 1e-3
states.append(("settled: a straight line, each node the average of its neighbours", line.copy(), None))


def frame(title, vals, hi):
    fig = go.Figure()
    xs = np.arange(n) * 0.1
    fig.add_trace(go.Scatter(x=xs, y=line, mode="lines", line=dict(color=GREY, width=2, dash="dot")))
    fig.add_trace(go.Scatter(x=xs, y=vals, mode="lines", line=dict(color=BLUE, width=3)))
    col = [RED] + [BLUE] * (n - 2) + [GREEN]
    if hi is not None:
        col[hi] = ORANGE
        for j in (hi - 1, hi + 1):
            fig.add_annotation(x=xs[hi], y=vals[hi], ax=xs[j], ay=vals[j], xref="x", yref="y", axref="x", ayref="y",
                               showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=2, arrowcolor=ORANGE, text="")
        fig.add_annotation(x=0.02, y=0.62, xref="x", yref="y", xanchor="left", showarrow=False, font=dict(size=20, color=ORANGE),
                           text=f"node {hi}: ({vals[hi - 1]:.2f} + {vals[hi + 1]:.2f}) / 2 = {vals[hi]:.2f}")
    fig.add_trace(go.Scatter(x=xs, y=vals, mode="markers+text", marker=dict(size=18, color=col),
                             text=[f"{u:.2f}" for u in vals], textposition="top center", textfont=dict(size=17)))
    fig.add_annotation(x=0, y=-0.13, text="obstacle: held at 1", showarrow=False, font=dict(size=18, color=RED),
                       xanchor="left")
    fig.add_annotation(x=1.0, y=-0.13, text="door: held at 0", showarrow=False, font=dict(size=18, color=GREEN),
                       xanchor="right")
    fig.update_xaxes(title="position along the corridor (m)", range=[-0.05, 1.05], dtick=0.1, showgrid=False)
    fig.update_yaxes(title="value", range=[-0.22, 1.22], dtick=0.2, showgrid=False)
    fig.update_layout(template="simple_white", width=1000, height=560, font=FONT, showlegend=False,
                      margin=dict(l=80, r=30, t=70, b=70), title=dict(text=title, x=0.5, y=0.96, font=dict(size=22)))
    return fig


figs = [frame(t, s, h) for t, s, h in states]
holds = [10] + [5] * 9 + [5] * 8 + [30]
holds[9] = 10
make_gif(figs, here / "relax1d", fps=4, holds=holds, keys=[0, 9, 13, len(figs) - 1],
         cols=2, width=900)
