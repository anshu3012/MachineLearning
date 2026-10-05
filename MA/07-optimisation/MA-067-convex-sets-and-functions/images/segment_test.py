"""The segment test for a convex set, animated (Plotly frames -> GIF). A point walks from x to y along the segment,
theta x + (1 - theta) y for theta = 1, 0.9, ..., 0. Left: the disc of radius 1, x = (1, 0), y = (0, 1); every point
stays inside (green). Right: the ring 1 <= length <= 2, x = (1.5, 0), y = (-1.5, 0); the walk leaves the ring between
(1, 0) and (-1, 0) (red), e.g. at the midpoint (0, 0) with length 0.
Run: python segment_test.py -> segment_test.gif, segment_test_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from gifkit import FONT, GREEN, RED, BLUE, make_gif

HERE = Path(__file__).parent
PANELS = [  # name, x, y, inside test, shapes
    ("disc", np.array([1.0, 0.0]), np.array([0.0, 1.0]), lambda p: np.linalg.norm(p) <= 1 + 1e-9),
    ("ring", np.array([1.5, 0.0]), np.array([-1.5, 0.0]), lambda p: 1 - 1e-9 <= np.linalg.norm(p) <= 2),
]
THETAS = np.round(np.linspace(1, 0, 11), 2)
mid = 0.5 * PANELS[0][1] + 0.5 * PANELS[0][2]
assert abs(np.linalg.norm(mid) - 0.7071) < 1e-3 and not PANELS[1][3](0.5 * PANELS[1][1] + 0.5 * PANELS[1][2])


def frame(j):
    th = THETAS[j]
    titles = []
    for name, x, y, inside in PANELS:
        p = th * x + (1 - th) * y
        ok = inside(p)
        titles.append(f"{name}: θ = {th:.1f}, point ({p[0]:.2f}, {p[1]:.2f})<br>length {np.linalg.norm(p):.2f}: "
                      f"<b>{'inside' if ok else 'OUTSIDE'}</b>")
    fig = make_subplots(1, 2, subplot_titles=titles, horizontal_spacing=0.08)
    for c, (name, x, y, inside) in enumerate(PANELS, start=1):
        ax = "" if c == 1 else "2"
        if name == "disc":
            fig.add_shape(type="circle", x0=-1, y0=-1, x1=1, y1=1, fillcolor="rgba(76,120,168,0.40)",
                          line=dict(color=BLUE, width=2), xref=f"x{ax}", yref=f"y{ax}", layer="below")
        else:
            fig.add_shape(type="circle", x0=-2, y0=-2, x1=2, y1=2, fillcolor="rgba(228,87,86,0.35)",
                          line=dict(color=RED, width=2), xref=f"x{ax}", yref=f"y{ax}", layer="below")
            fig.add_shape(type="circle", x0=-1, y0=-1, x1=1, y1=1, fillcolor="white",
                          line=dict(color=RED, width=2), xref=f"x{ax}", yref=f"y{ax}", layer="below")
        # the full segment, faint
        fig.add_trace(go.Scatter(x=[x[0], y[0]], y=[x[1], y[1]], mode="lines",
                                 line=dict(color="lightgrey", width=3, dash="dot")), 1, c)
        # the path walked so far, coloured point by point
        walked = [t * x + (1 - t) * y for t in np.linspace(1, th, 60)]
        for a, b in zip(walked[:-1], walked[1:]):
            col = GREEN if inside((a + b) / 2) else RED
            fig.add_trace(go.Scatter(x=[a[0], b[0]], y=[a[1], b[1]], mode="lines", line=dict(color=col, width=6)), 1, c)
        fig.add_trace(go.Scatter(x=[x[0], y[0]], y=[x[1], y[1]], mode="markers+text", text=["x", "y"],
                                 textposition=["bottom right", "top left"] if name == "disc" else ["bottom center"] * 2,
                                 textfont=dict(size=26), marker=dict(color="black", size=12)), 1, c)
        p = th * x + (1 - th) * y
        fig.add_trace(go.Scatter(x=[p[0]], y=[p[1]], mode="markers",
                                 marker=dict(color=GREEN if inside(p) else RED, size=22,
                                             line=dict(color="black", width=2))), 1, c)
        lim = 1.3 if name == "disc" else 2.2
        fig.update_xaxes(range=[-lim, lim], zeroline=False, row=1, col=c)
        fig.update_yaxes(range=[-lim, lim], zeroline=False, scaleanchor=f"x{ax}", row=1, col=c)
    fig.update_layout(template="simple_white", width=1100, height=600, showlegend=False, font=FONT,
                      margin=dict(l=40, r=20, t=110, b=40))
    fig.update_annotations(font_size=24)
    return fig


if __name__ == "__main__":
    figs = [frame(j) for j in range(len(THETAS))]
    holds = [3] + [2] * (len(figs) - 2) + [8]
    make_gif(figs, HERE / "segment_test.gif", fps=3, holds=holds, keys=[5, 10], cols=1, width=900)
