"""Map-consistent sampling. A wall (grey box, y from 1.45 to 1.53 m, x from 1.7 to 2.8 m) lies across the cloud of the
Note's odometry step. Left: one big step, samples inside the wall are rejected (red), but samples beyond the wall
(purple) are free and still kept, although the robot cannot drive through the wall. Right: the same motion in twenty small
steps with the noise per step raised so the total spread is the same, rejecting and redrawing at each step: no
sample gets beyond the wall. Seeded.
Run: python map_reject.py -> map_reject.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, PURPLE, RED
from motion import A_ODO, START, sample_odometry
from plotly.subplots import make_subplots

here = Path(__file__).parent
WALL = (1.7, 2.8, 1.45, 1.53)
inside = lambda x, y: (x > WALL[0]) & (x < WALL[1]) & (y > WALL[2]) & (y < WALL[3])
beyond = lambda x, y: (x > WALL[0]) & (x < WALL[1]) & (y >= WALL[3])


def big_step(rng, n=500):
    return sample_odometry((0.500, 0.479, 0.500), START, rng, n)


def small_steps(rng, n=500, k=20):
    """k sub-steps along the arc; any sample that lands in the wall is redrawn from its previous pose."""
    x, y, th = (np.full(n, v) for v in START)
    u = (0.5 / k, 0.479 / k, 0.5 / k)                 # one k-th of the turn and of the arc
    a = tuple(np.sqrt(k) * v for v in A_ODO)          # noise per sub-step raised so the total spread matches one big step
    for _ in range(k):
        nx, ny, nth = sample_odometry(u, (x, y, th), rng, n, a)
        bad = inside(nx, ny)
        while bad.any():
            rx, ry, rth = sample_odometry(u, (x[bad], y[bad], th[bad]), rng, bad.sum(), a)
            nx[bad], ny[bad], nth[bad] = rx, ry, rth
            bad = inside(nx, ny)
        x, y, th = nx, ny, nth
    return x, y, th


if __name__ == "__main__":
    bx, by, _ = big_step(np.random.default_rng(5))
    sx, sy, _ = small_steps(np.random.default_rng(5))
    nin, nbe = inside(bx, by).sum(), beyond(bx, by).sum()
    print("big step: inside wall", nin, " beyond wall", nbe, "  small steps: beyond wall", beyond(sx, sy).sum())
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08,
                        subplot_titles=[f"one big step: {nin} rejected, {nbe} beyond the wall",
                                        f"twenty small steps: {beyond(sx, sy).sum()} beyond the wall"])
    for c in (1, 2):
        fig.add_shape(type="rect", x0=WALL[0], x1=WALL[1], y0=WALL[2], y1=WALL[3], fillcolor="#777", line_width=0,
                      row=1, col=c)
        fig.add_trace(go.Scatter(x=[2.0], y=[1.0], mode="markers", marker=dict(size=12, color="black")), 1, c)
        fig.update_xaxes(range=[1.7, 2.8], dtick=0.2, title="x (m)", row=1, col=c)
        fig.update_yaxes(range=[0.95, 1.7], dtick=0.1, row=1, col=c)
    ok = ~inside(bx, by) & ~beyond(bx, by)
    fig.add_trace(go.Scatter(x=bx[ok], y=by[ok], mode="markers", marker=dict(size=4, color=BLUE, opacity=0.6)), 1, 1)
    m = inside(bx, by)
    fig.add_trace(go.Scatter(x=bx[m], y=by[m], mode="markers", marker=dict(size=7, color=RED, symbol="x")), 1, 1)
    m = beyond(bx, by)
    fig.add_trace(go.Scatter(x=bx[m], y=by[m], mode="markers", marker=dict(size=6, color=PURPLE)), 1, 1)
    fig.add_trace(go.Scatter(x=sx, y=sy, mode="markers", marker=dict(size=4, color=BLUE, opacity=0.6)), 1, 2)
    fig.add_annotation(x=2.5, y=1.49, text="wall", showarrow=False, font=dict(size=16, color="white"), row=1, col=1)
    fig.add_annotation(x=2.5, y=1.49, text="wall", showarrow=False, font=dict(size=16, color="white"), row=1, col=2)
    fig.update_yaxes(title="y (m)", row=1, col=1)
    fig.update_layout(template="simple_white", width=1100, height=560, font=FONT, showlegend=False,
                      margin=dict(l=80, r=30, t=110, b=70),
                      title=dict(text="blue: kept   red: inside the wall, rejected   purple: free but unreachable",
                                 x=0.5, y=0.95, font=dict(size=21)))
    fig.update_annotations(selector=dict(text="wall"), font_size=16)
    fig.write_image(here / "map_reject.png")
