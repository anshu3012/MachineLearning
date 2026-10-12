"""Why fixed moves do not make a finite graph (LaValle 14.2.2.3): the car of RO-055 repeats Hybrid A*'s full-left arc
of 1.5 m on its 5 m circle. One lap is 31.42 m, which is 20.94 arcs, not a whole number, so the arc ends never come
back to the start or to each other: after three laps (63 arcs) there are 64 different end points. A quarter turn of
the same circle (7.85 m), as a lattice move, ends back on the start after 4 moves. Run -> circle_anim.gif,
circle_anim_frames.png"""
import math
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from carpaths import step
from gifkit import BLUE, GREEN, ORANGE, make_gif
from lotdraw import FONT

here = Path(__file__).parent
RHO, ARC = 5.0, 1.5
P0 = (0.0, -5.0, 0.0)                      # start on the bottom of a circle of radius 5 m centred on the origin
ENDS = [P0]
for _ in range(63):
    ENDS.append(step(ENDS[-1], "L", ARC, RHO))
ENDS = np.array(ENDS)
PER_LAP = 2 * math.pi * RHO / ARC
GAPS = [math.hypot(*(ENDS[i, :2] - ENDS[j, :2])) for i in range(64) for j in range(i)]
QUARTER = [P0]
for _ in range(4):
    QUARTER.append(step(QUARTER[-1], "L", math.pi / 2 * RHO, RHO))
assert round(PER_LAP, 2) == 20.94 and min(GAPS) > 1e-3
assert math.hypot(QUARTER[-1][0] - P0[0], QUARTER[-1][1] - P0[1]) < 1e-9
assert round(math.hypot(*(ENDS[21, :2] - ENDS[0, :2])), 3) == 0.084


def frame(k, quarter=False):
    fig = go.Figure()
    t = np.linspace(0, 2 * math.pi, 300)
    fig.add_trace(go.Scatter(x=RHO * np.cos(t), y=RHO * np.sin(t), mode="lines", line=dict(color="#D0D0D0", width=2),
                             hoverinfo="skip"))
    if quarter:
        q = np.array(QUARTER)
        fig.add_trace(go.Scatter(x=q[:, 0], y=q[:, 1], mode="markers", marker=dict(color=GREEN, size=16, symbol="square"),
                                 hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=ENDS[:k + 1, 0], y=ENDS[:k + 1, 1], mode="markers",
                             marker=dict(color=[BLUE if i <= 20 else (ORANGE if i <= 41 else "#B279A2")
                                                for i in range(k + 1)], size=10), hoverinfo="skip"))
    x, y, th = ENDS[k]
    fig.add_trace(go.Scatter(x=[x, x + 1.4 * math.cos(th)], y=[y, y + 1.4 * math.sin(th)], mode="lines",
                             line=dict(color="black", width=4), hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=[0], y=[-5], mode="markers+text", text=["start"], textposition="bottom center",
                             marker=dict(color="black", size=8), textfont=dict(size=17), hoverinfo="skip"))
    lap = k / PER_LAP
    if quarter:
        title, sub = "a quarter-turn move: back on the start after 4 moves", "green: the ends of four 7.85 m moves"
    elif k == 0:
        title, sub = "full left, 1.5 m at a time, on the 5 m circle", "one lap is 20.94 arcs, not a whole number"
    else:
        title = f"{k} arcs ({lap:.2f} laps): {k + 1} different end points"
        sub = "lap 1 blue, lap 2 orange, lap 3 purple: no end repeats"
    fig.update_layout(template="simple_white", width=760, height=820, showlegend=False, font=FONT,
                      title=dict(text=title, x=0.5, xanchor="center", font_size=22), margin=dict(l=30, r=30, t=110, b=30))
    fig.add_annotation(x=0.5, y=1.02, xref="paper", yref="paper", text=sub, showarrow=False, font=dict(size=18))
    fig.update_xaxes(range=[-6.5, 6.5], showgrid=False, zeroline=False, tickvals=[-5, 0, 5], tickfont=dict(size=15))
    fig.update_yaxes(range=[-6.8, 6.5], showgrid=False, zeroline=False, scaleanchor="x", tickvals=[-5, 0, 5],
                     tickfont=dict(size=15))
    return fig


ks = list(range(0, 22)) + list(range(24, 64, 3)) + [63]
figs = [frame(k) for k in ks] + [frame(63, quarter=True)]
holds = [8] + [2] * 20 + [10] + [2] * (len(ks) - 23) + [16, 30]
make_gif(figs, here / "circle_anim", fps=6, holds=holds, keys=[0, 21, len(ks) - 1, len(figs) - 1], cols=2, width=640)
