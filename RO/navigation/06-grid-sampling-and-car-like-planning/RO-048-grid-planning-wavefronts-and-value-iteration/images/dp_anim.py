"""The robot at its true position (2, 1), the corner of S, following the feedback plan from dynamic programming with
interpolation, one move per frame. The background colours the cost-to-go between cell centres by bilinear
interpolation (left white where a blocked cell is among the four centres). At each point the robot tries 16 moves of
0.5 m (grey dots) and takes the one whose 0.5 m plus the interpolated cost-to-go at its end is smallest (orange). The
first move goes at 67.5 degrees, for 0.5 + 3.164 = 3.664. The robot reaches the door's cell centre after 3.564 m;
going by the grid (to S's centre, then the 8-connected route) takes 3.768 m (grey, dashed).
Run -> dp_anim.gif, dp_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from drawkit import VSCALE, axes, centre, furniture, layout, robot, room, route, sg
from gifkit import BLUE, GREY, ORANGE, make_gif
from gridplan import C, NX, NY, START, best_move, cost_to_go, directions, downhill, dp_interp, follow, interp

here = Path(__file__).parent
K = 16
VI, SWEEPS = dp_interp(K)
PTS, LEN = follow(VI, 2.0, 1.0, K)
GRID = [(2.0, 1.0)] + [centre(c) for c in downhill(START, cost_to_go())]
GLEN = sum(np.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(GRID, GRID[1:]))
first = best_move(VI, 2.0, 1.0, K)
assert round(LEN, 3) == 3.564 and round(GLEN, 3) == 3.768 and len(PTS) == 9 and SWEEPS == 17
assert round(first[0], 3) == 3.664 and round(first[0] - 0.5, 3) == 3.164
assert np.allclose(first[1], (2 + 0.5 * np.cos(np.radians(67.5)), 1 + 0.5 * np.sin(np.radians(67.5))))
assert round(VI[START], 3) == 3.338

h = 0.05
xs, ys = np.arange(h / 2, NX * C, h), np.arange(h / 2, NY * C, h)
Z = np.array([[interp(VI, x, y) for x in xs] for y in ys])
Z[~np.isfinite(Z)] = np.nan
ZMAX = np.nanmax(Z)


def frame(k):
    fig = go.Figure()
    room(fig, None, {}, labels=False, walls=False, outlines=False)
    fig.add_trace(go.Heatmap(z=Z, x0=h / 2, dx=h, y0=h / 2, dy=h, zmin=0, zmax=ZMAX, colorscale=VSCALE,
                             showscale=False, hoverinfo="skip"))
    furniture(fig)
    route(fig, None, GREY, width=4, dash="dash", points=GRID)
    n = min(k, len(PTS) - 1)
    if n:
        route(fig, None, ORANGE, width=6, points=PTS[:n + 1])
    p = PTS[n]
    if n < len(PTS) - 1:
        ends = [(p[0] + 0.5 * ux, p[1] + 0.5 * uy) for ux, uy in directions(K)]
        fig.add_trace(go.Scatter(x=[e[0] for e in ends], y=[e[1] for e in ends], mode="markers",
                                 marker=dict(size=8, color="#555555"), hoverinfo="skip"))
        nxt = PTS[n + 1]
        fig.add_trace(go.Scatter(x=[p[0], nxt[0]], y=[p[1], nxt[1]], mode="lines+markers",
                                 line=dict(color=ORANGE, width=3, dash="dot"), marker=dict(size=[0, 13], color=ORANGE),
                                 hoverinfo="skip"))
    robot(fig, p, size=18)
    sg(fig, dy=-0.15, size=16)
    axes(fig)
    if k == 0:
        t = "16 moves of 0.5 m from (2, 1); the best: 67.5 degrees, 0.5 + 3.164"
    elif n == len(PTS) - 1:
        t = f"at the door's cell after {LEN:.3f} m; by the grid's cells {GLEN:.3f} m"
    else:
        t = f"move {k}: again the move with the smallest 0.5 m + value at its end"
    return layout(fig, t, width=900, height=620)


figs = [frame(k) for k in range(len(PTS))]
holds = [16] + [5] * (len(PTS) - 2) + [30]
make_gif(figs, here / "dp_anim", fps=4, holds=holds, keys=[0, 3, 6, len(PTS) - 1], cols=2, width=760)
