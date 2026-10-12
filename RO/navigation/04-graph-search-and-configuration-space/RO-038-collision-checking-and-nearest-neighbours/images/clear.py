"""Animation: checking the straight drive from the start (2, 1) to the doorway centre (3.6, 4.0) with clearances.
Each checked point gets a circle whose radius is its clearance, its distance from the grown obstacles: the robot
can move anywhere inside that circle and stay free. A piece of the segment is cleared when the circles at its two
ends reach each other (length <= clearance at one end + clearance at the other); otherwise its middle is checked
too. 9 checks clear all 3.4 m. Run -> clear.gif, clear_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from shapely.geometry import box

import collide as k
import cspace as c
import drawkit as dk
from gifkit import GREEN, ORANGE, make_gif

here = Path(__file__).parent
a, b = np.array(c.START[:2]), np.array(c.GOAL)
log = []
ok = k.exact_check(a, b, log)
assert ok and len(log) == 9 and round(log[0][1], 3) == 0.75 and round(log[1][1], 3) == 0.35
D = c.cobs_disk().intersection(box(-0.2, -0.2, 7.2, 4.12)).difference(c.obstacles())


def frame(n, title):
    fig = go.Figure()
    fig.add_trace(dk.geom_trace(D, dk.COBS_FILL, ORANGE, 2))
    dk.room(fig)
    fig.add_trace(go.Scatter(x=[a[0], b[0]], y=[a[1], b[1]], mode="lines", line=dict(color="black", width=3)))
    for i, (p, cl) in enumerate(log[:n]):
        g = c.circle(p[0], p[1], cl)
        fig.add_trace(dk.geom_trace(g, "rgba(84,162,75,0.12)", GREEN, 3 if i == n - 1 else 1.5))
        dk.point(fig, p[0], p[1], GREEN, None, size=11)
    if n:
        p, cl = log[n - 1]
        fig.add_annotation(x=0.66, y=0.95, xref="paper", yref="paper", xanchor="left", yanchor="top", align="left",
                           text=f"checks: {n}<br>last point ({p[0]:.2f}, {p[1]:.2f})<br>clearance {cl:.3f} m",
                           showarrow=False, font=dict(size=18))
    fig.update_xaxes(range=[1.4, 4.4], dtick=0.5, title="x (m)", domain=[0, 0.62], constrain="domain")
    fig.update_yaxes(range=[0.4, 4.3], dtick=0.5, title="y (m)", scaleanchor="x", constrain="domain")
    dk.layout(fig, 1200, 700, title, margin=dict(l=70, r=20, t=80, b=60))
    return fig


titles = ["the start: clearance 0.75 m", "the doorway centre: clearance 0.35 m; 3.4 m > 0.75 + 0.35, check the middle"]
titles += ["check the middle of a piece whose end circles do not meet"] * (len(log) - 3)
titles += ["the last circles meet: the whole segment is free"]
figs = [frame(n, t) for n, t in zip(range(1, len(log) + 1), titles)]
holds = [3] * (len(figs) - 1) + [14]
make_gif(figs, here / "clear", fps=2, holds=holds, keys=[1, 4, 6, len(figs) - 1], cols=2, width=950)
