"""A front leaving the door's cell centre at 1 m/s, on the room's free cells cut into 0.1 m cells, computed two ways.
Top: 8-connected Dijkstra, whose distances can only follow the 8 grid directions, so its fronts are octagons. Bottom:
the fast marching method, which takes each cell's arrival time from two neighbours at once, so the front can cross the
grid at any angle and comes out round. Coloured: cells the front has reached, by arrival time; lines: the front every
0.5 s. One frame per 0.25 s. At S's centre the times are 3.180 s (Dijkstra) and 3.121 s (fast marching); the shortest
way round the blocked cells is 2.965 m. Run -> fmm_anim.gif, fmm_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from drawkit import VSCALE, axes, furniture, layout, sg, title_at
from gifkit import make_gif
from gridplan import GOAL, START, dijkstra8, fine_grid, fmm
from plotly.subplots import make_subplots

here = Path(__file__).parent
K = 5
FREE, H = fine_grid(K)
SRC = (GOAL[0] * K + K // 2, GOAL[1] * K + K // 2)
SS = (START[0] * K + K // 2, START[1] * K + K // 2)
TF, _ = fmm(FREE, H, SRC)
TD, _ = dijkstra8(FREE, H, SRC)
assert np.allclose(((SRC[0] + 0.5) * H, (SRC[1] + 0.5) * H), (3.75, 3.75))
assert round(TF[SS[1], SS[0]], 3) == 3.121 and round(TD[SS[1], SS[0]], 3) == 3.180
TMAX = 3.25


def panel(fig, r, T, t):
    Z = np.where(T <= t + 1e-9, T, np.nan)
    Zb = np.where(FREE, np.nan, 1.0)
    fig.add_trace(go.Heatmap(z=np.where(FREE, 0.0, np.nan), x0=H / 2, dx=H, y0=H / 2, dy=H, colorscale=[[0, "white"],
                             [1, "white"]], showscale=False, hoverinfo="skip"), row=r, col=1)
    fig.add_trace(go.Heatmap(z=Zb, x0=H / 2, dx=H, y0=H / 2, dy=H, colorscale=[[0, "#8A8A8A"], [1, "#8A8A8A"]],
                             showscale=False, hoverinfo="skip"), row=r, col=1)
    fig.add_trace(go.Heatmap(z=Z, x0=H / 2, dx=H, y0=H / 2, dy=H, zmin=0, zmax=TMAX, colorscale=VSCALE,
                             showscale=False, hoverinfo="skip"), row=r, col=1)
    if t >= 0.5:
        Zc = np.where(np.isfinite(T), T, np.nan)
        fig.add_trace(go.Contour(z=Zc, x0=H / 2, dx=H, y0=H / 2, dy=H, showscale=False, hoverinfo="skip",
                                 contours=dict(start=0.5, end=np.floor(t * 2) / 2 + 1e-6, size=0.5, coloring="none"),
                                 line=dict(color="#333333", width=2.2)), row=r, col=1)
    furniture(fig, (r, 1))
    sg(fig, (r, 1), dy=0.0, size=18)
    axes(fig, (r, 1))


def frame(t):
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.08)
    panel(fig, 1, TD, t)
    panel(fig, 2, TF, t)
    last = t >= TMAX - 1e-9
    title_at(fig, "8-connected Dijkstra" + (f": S reached at {TD[SS[1], SS[0]]:.3f} s" if last else ""), 1.0)
    title_at(fig, "fast marching" + (f": S reached at {TF[SS[1], SS[0]]:.3f} s" if last else ""), 0.47)
    t_txt = (f"t = {t:.2f} s: the front 1 m/s from the door, a line every 0.5 s" if not last else
             "shortest way round the blocked cells from the door to S: 2.965 m")
    return layout(fig, t_txt, width=900, height=1080, margin=dict(l=30, r=30, t=110, b=30))


ts = np.arange(0.25, TMAX + 1e-9, 0.25)
figs = [frame(t) for t in ts]
holds = [6] + [3] * (len(ts) - 2) + [30]
make_gif(figs, here / "fmm_anim", fps=4, holds=holds, keys=[1, 5, 9, len(ts) - 1], cols=2, width=700)
