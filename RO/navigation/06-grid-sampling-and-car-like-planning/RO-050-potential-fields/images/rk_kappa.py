"""Animation: the contour map of the Rimon-Koditschek function phi on the world of disks (as in the rk_surface
animation) as kappa grows: 1, 1.25, 1.5, 1.75, 1.9, 2, 3, 4. The red robot starts at (4.0, 0.5) and follows the
gradient downhill. For kappa below about 1.98 it stops in a local minimum the formula makes left of the table, (1.76, 0.19) at
kappa = 1; from kappa = 2 on the local minimum is gone and it reaches the door. phi at the start grows from 0.074 (kappa = 1)
to 0.998 (kappa = 4): a larger kappa makes the function flatter.
Run -> rk_kappa.gif, rk_kappa_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from shapely.geometry import Point

import drawkit as dk
import pf
from gifkit import FONT, GREEN, RED, make_gif

here = Path(__file__).parent
xs = np.arange(0.2, 6.8001, 0.025)
ys = np.arange(-1.3, 5.3001, 0.025)
X, Y = np.meshgrid(xs, ys)
KAPPAS = [1, 1.25, 1.5, 1.75, 1.9, 2, 3, 4]
runs = {k: pf.rk_descend(pf.START2, k) for k in KAPPAS}
reach = {k: bool(np.hypot(*(P[-1] - pf.GOAL)) < 0.03) for k, P in runs.items()}
assert [reach[k] for k in KAPPAS] == [False] * 5 + [True] * 3
assert np.allclose(runs[1][-1], (1.76, 0.19), atol=0.01)
assert round(float(pf.rk(pf.START2, 1)), 3) == 0.074 and round(float(pf.rk(pf.START2, 4)), 3) == 0.998
disks = [Point(*cc).buffer(r, quad_segs=32) for cc, r in pf.SW_OBS]
ring = Point(*pf.SW_C0).buffer(pf.SW_R0, quad_segs=96)


def frame(k):
    Z = np.nan_to_num(pf.rk(np.stack([X, Y], -1), k), nan=1.0)
    P = runs[k]
    fig = go.Figure(go.Contour(x=xs, y=ys, z=Z, colorscale="Blues", reversescale=True, zmin=0, zmax=1,
                               contours=dict(start=0, end=1, size=0.1, coloring="heatmap"),
                               line=dict(color="rgba(30,30,30,0.45)", width=1), showscale=False, hoverinfo="skip"))
    for d in disks:
        fig.add_trace(dk.geom_trace(d, "rgba(200,200,200,1)", "rgba(120,120,120,1)", 2))
    rx, ry = ring.exterior.xy
    fig.add_trace(go.Scatter(x=list(rx), y=list(ry), mode="lines", line=dict(color="rgba(120,120,120,1)", width=2)))
    fig.add_trace(go.Scatter(x=P[:, 0], y=P[:, 1], mode="lines", line=dict(color=RED, width=4)))
    dk.point(fig, *pf.START2, RED, None, size=12)
    dk.point(fig, *pf.GOAL, "black", None, size=12)
    end = P[-1]
    if reach[k]:
        lines = [(f"κ = {k:g}", "black"), (f"φ at the start: {float(pf.rk(pf.START2, k)):.3f}", "black"), ("", "black"),
                 ("the robot reaches the door", GREEN), ("no local minimum left", GREEN)]
    else:
        fig.add_trace(go.Scatter(x=[end[0]], y=[end[1]], mode="markers",
                                 marker=dict(symbol="star", size=20, color=RED, line=dict(color="white", width=1))))
        lines = [(f"κ = {k:g}", "black"), (f"φ at the start: {float(pf.rk(pf.START2, k)):.3f}", "black"), ("", "black"),
                 ("the robot stops in a local minimum", RED), (f"at ({end[0]:.2f}, {end[1]:.2f})", RED)]
    for i, (t, col) in enumerate(lines):
        fig.add_annotation(x=0.62, y=0.9 - 0.08 * i, xref="paper", yref="paper", xanchor="left", yanchor="top", text=t,
                           showarrow=False, font=dict(size=21, color=col))
    fig.update_xaxes(range=[0.1, 6.9], dtick=1, title="x (m)", showgrid=False, domain=[0, 0.6], constrain="domain")
    fig.update_yaxes(range=[-1.4, 5.4], dtick=1, title="y (m)", showgrid=False, scaleanchor="x", constrain="domain")
    fig.update_layout(template="simple_white", width=1100, height=720, font=FONT, showlegend=False,
                      margin=dict(l=70, r=20, t=80, b=60),
                      title=dict(text="larger κ: the local minimum moves, then vanishes", x=0.5, y=0.97, font=dict(size=22)))
    return fig


figs = [frame(k) for k in KAPPAS]
holds = [14, 10, 10, 10, 10, 18, 10, 30]
make_gif(figs, here / "rk_kappa", fps=4, holds=holds, keys=[0, 4, 5, 7], cols=2, width=1000)
