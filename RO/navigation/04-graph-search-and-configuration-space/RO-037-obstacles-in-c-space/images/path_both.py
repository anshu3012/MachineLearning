"""Animation: one path in two pictures at once. Left, the room: the robot (disk footprint, radius 0.25 m) turns on the
spot from 30 to 61.9 degrees, then drives straight 3.4 m from (2, 1) to the doorway centre (3.6, 4.0). Right, C-space
seen from above: the same motion is a point moving among the grown obstacles. At its closest, after 2.471 m, the
centre passes 0.382 m from the table's corner, so the point passes 0.132 m from the grown table.
Run -> path_both.gif, path_both_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from shapely.geometry import LineString, Point, Polygon

import cspace as c
import drawkit as k
from gifkit import GREEN, ORANGE, RED, make_gif

here = Path(__file__).parent
D = c.cobs_disk()
T = Polygon(c.TABLE)
a, b = np.array(c.START[:2]), np.array(c.GOAL)
L = LineString([a, b])
head = np.arctan2(*(b - a)[::-1])
tc = 2.471 / 3.4                                            # closest approach to the table's corner (3.5, 3.0)
assert round(L.length, 3) == 3.4 and round(np.degrees(head), 1) == 61.9
assert round(L.distance(T), 3) == 0.382 and round(L.distance(D), 3) == 0.132
assert round(Point(*(a + tc * (b - a))).distance(Point(3.5, 3.0)), 3) == 0.382


def frame(p, th, title, close=False, done=0.0):
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.05,
                        subplot_titles=["the room: the robot moves", "C-space seen from above: a point moves"])
    k.room(fig, 1, 1)
    fig.add_trace(k.geom_trace(D.intersection(c.box(-0.12, -0.12, c.W + 0.12, c.H + 0.12)).difference(c.obstacles()),
                               k.COBS_FILL, ORANGE, 2),
                  row=1, col=2)
    k.room(fig, 1, 2, walls=False)
    for col in (1, 2):
        fig.add_trace(go.Scatter(x=[a[0], b[0]], y=[a[1], b[1]], mode="lines", line=dict(color="black", width=1.5,
                                 dash="dot"), hoverinfo="skip"), row=1, col=col)
        q = a + done * (b - a)
        fig.add_trace(go.Scatter(x=[a[0], q[0]], y=[a[1], q[1]], mode="lines", line=dict(color=GREEN, width=4),
                                 hoverinfo="skip"), row=1, col=col)
    k.disk(fig, p[0], p[1], th, row=1, col=1)
    k.point(fig, p[0], p[1], GREEN, None, size=13, row=1, col=2)
    if close:
        fig.add_trace(go.Scatter(x=[p[0], 3.5], y=[p[1], 3.0], mode="lines", line=dict(color=RED, width=3),
                                 hoverinfo="skip"), row=1, col=1)
        g = D.boundary.interpolate(D.boundary.project(Point(*p)))
        fig.add_trace(go.Scatter(x=[p[0], g.x], y=[p[1], g.y], mode="lines", line=dict(color=RED, width=3),
                                 hoverinfo="skip"), row=1, col=2)
        fig.add_annotation(x=0.25, y=0.5, xanchor="left", text="centre to corner: 0.382 m", showarrow=False,
                           font=dict(size=18, color=RED), bgcolor="white", row=1, col=1)
        fig.add_annotation(x=0.35, y=0.5, xanchor="left", text="point to grown table: 0.132 m", showarrow=False,
                           font=dict(size=18, color=RED), bgcolor="white", row=1, col=2)
    for col in (1, 2):
        fig.update_xaxes(range=[-0.25, 7.25], dtick=1, title="x (m)", row=1, col=col)
    fig.update_yaxes(range=[-0.25, 4.35], dtick=1, title="y (m)", scaleanchor="x", row=1, col=1)
    fig.update_yaxes(range=[-0.25, 4.35], dtick=1, scaleanchor="x2", row=1, col=2)
    k.layout(fig, 1400, 600, title, margin=dict(l=70, r=20, t=110, b=60))
    fig.update_annotations(font_size=20, selector=dict(text="the room: the robot moves"))
    fig.update_annotations(font_size=20, selector=dict(text="C-space seen from above: a point moves"))
    return fig


figs, holds = [frame(a, c.START[2], "start: (2, 1) facing 30°")], [5]
for th in np.linspace(c.START[2], head, 4)[1:]:
    figs.append(frame(a, th, f"turn on the spot to {np.degrees(th):.1f}°: the point stays put"))
    holds.append(2)
for s in [0.4, 0.8, 1.2, 1.6, 2.0, 2.471, 2.8, 3.1, 3.4]:
    t = s / 3.4
    p = a + t * (b - a)
    clear = Point(*p).distance(D.boundary)
    close = s == 2.471
    title = (f"closest to the table after {s:.3f} m: clearance 0.132 m" if close else
             "at the doorway centre (3.6, 4.0): the whole drive is free" if s == 3.4 else
             f"driven {s:.1f} m of 3.4 m")
    figs.append(frame(p, head, title, close=close, done=t))
    holds.append(8 if close else 14 if s == 3.4 else 2)
make_gif(figs, here / "path_both", fps=3, holds=holds, keys=[0, 3, 9, len(figs) - 1], cols=2, width=1000)
