"""The hiker picture of the gradient (Plotly 3-D frames). A dot climbs the surface f = x1^2 + x1 x2 + 2 x2^2 by always
stepping along the gradient arrow drawn on the contour map under it (the map is placed below the bowl so that both are visible). Its shadow on the floor crosses each contour line at a
right angle. Start (0.25, 0.1); each step has length 0.13 along the gradient. Idea after Khan Academy, "Gradient and graphs".
Run: python hiker.py -> hiker.gif, hiker_frames.png"""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from gifkit import FONT, GREY, ORANGE, make_gif

here = Path(__file__).parent
f = lambda a, b: a ** 2 + a * b + 2 * b ** 2
grad = lambda p: np.array([2 * p[0] + p[1], p[0] + 4 * p[1]])
g = np.linspace(-1.6, 1.6, 70)
X, Y = np.meshgrid(g, g)
path = [np.array([0.25, 0.1])]
while len(path) < 11:
    path.append(path[-1] + 0.13 * grad(path[-1]) / np.linalg.norm(grad(path[-1])))
path = np.array(path)
assert np.all(np.diff(f(path[:, 0], path[:, 1])) > 0) and np.abs(path).max() < 1.6      # always uphill, stays on the map
FLOOR = -5.0                       # the contour map is drawn on a floor below the bowl
th = np.linspace(0, 2 * np.pi, 200)
lam, Q = np.linalg.eigh(np.array([[1, 0.5], [0.5, 2]]))


def frame(k):
    p, gr = path[k], grad(path[k])
    fig = go.Figure(go.Surface(x=X, y=Y, z=f(X, Y), colorscale="Blues", reversescale=True, showscale=False, opacity=0.6))
    for c in (0.25, 1, 2, 3.5, 5.5):                                             # contour lines on the floor
        e = Q @ (np.sqrt(c / lam)[:, None] * np.vstack([np.cos(th), np.sin(th)]))
        e[:, (np.abs(e) > 1.6).any(axis=0)] = np.nan
        fig.add_trace(go.Scatter3d(x=e[0], y=e[1], z=FLOOR + 0 * th, mode="lines", line=dict(color=GREY, width=3)))
    fig.add_trace(go.Scatter3d(x=path[:k + 1, 0], y=path[:k + 1, 1], z=f(path[:k + 1, 0], path[:k + 1, 1]), mode="lines",
                               line=dict(color="black", width=7)))
    fig.add_trace(go.Scatter3d(x=path[:k + 1, 0], y=path[:k + 1, 1], z=FLOOR + 0 * path[:k + 1, 0], mode="lines",
                               line=dict(color="black", width=5, dash="dash")))
    fig.add_trace(go.Scatter3d(x=[p[0], p[0]], y=[p[1], p[1]], z=[FLOOR, f(*p)], mode="lines", line=dict(color=GREY, width=3, dash="dot")))
    fig.add_trace(go.Scatter3d(x=[p[0]], y=[p[1]], z=[f(*p)], mode="markers", marker=dict(size=8, color="black")))
    fig.add_trace(go.Scatter3d(x=[p[0]], y=[p[1]], z=[FLOOR], mode="markers", marker=dict(size=5, color="black")))
    tip = p + 0.12 * gr
    fig.add_trace(go.Scatter3d(x=[p[0], tip[0]], y=[p[1], tip[1]], z=[FLOOR, FLOOR], mode="lines", line=dict(color=ORANGE, width=10)))
    fig.add_trace(go.Cone(x=[tip[0]], y=[tip[1]], z=[FLOOR], u=[gr[0]], v=[gr[1]], w=[0], sizemode="absolute", sizeref=0.28,
                          anchor="tip", showscale=False, colorscale=[[0, ORANGE], [1, ORANGE]]))
    fig.update_scenes(xaxis=dict(title="x1", range=[-1.6, 1.6], nticks=5, tickfont=dict(size=15)), yaxis=dict(title="x2", range=[-1.6, 1.6], nticks=5, tickfont=dict(size=15)),
                      zaxis=dict(title="f", range=[FLOOR, 9], tickvals=[0, 3, 6, 9], tickfont=dict(size=15)), aspectmode="manual", aspectratio=dict(x=1, y=1, z=1.0),
                      camera=dict(eye=dict(x=1.2, y=-1.8, z=0.75), center=dict(x=0, y=0, z=-0.1)))
    fig.update_layout(template="simple_white", width=900, height=720, font=FONT, showlegend=False,
                      margin=dict(l=0, r=0, t=60, b=0),
                      title=dict(x=0.5, y=0.96, font=dict(size=22),
                                 text=f"height f = {f(*p):.2f}   gradient = [{gr[0]:.1f}, {gr[1]:.1f}]   "
                                      f"steepness = {np.linalg.norm(gr):.1f}"))
    return fig


figs = [frame(k) for k in range(len(path))]
holds = [8] + [3] * (len(path) - 2) + [14]
make_gif(figs, here / "hiker", fps=6, holds=holds, keys=[0, 4, 7, len(path) - 1])
