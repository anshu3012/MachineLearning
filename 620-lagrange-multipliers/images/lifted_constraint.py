"""The constrained problem seen on the surface first (Plotly 3-D frames). f = x^2 + 2y^2 is a bowl; the constraint
x + y = 3 is a line on the floor. Lifted onto the bowl it becomes a curve, and the answer is the lowest point of that
curve: (2, 1) with f = 6, not the bottom of the bowl. The camera then turns to the top view, where the bowl becomes
contour rings and the lifted curve becomes the line again (the flat picture the rest of the Note uses).
Idea after Khan Academy, "Constrained optimization introduction"; our own problem.
Run: python lifted_constraint.py -> lifted_constraint.gif, lifted_constraint_frames.png"""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from gifkit import FONT, GREEN, GREY, RED, make_gif

here = Path(__file__).parent
f = lambda x, y: x ** 2 + 2 * y ** 2
X, Y = np.meshgrid(np.linspace(-1, 3.6, 60), np.linspace(-1.2, 3, 60))
t = np.linspace(0.3, 3.6, 120)
on_line = f(t, 3 - t)
assert abs(t[np.argmin(on_line)] - 2) < 0.03 and f(2, 1) == 6          # lowest point of the lifted curve


def frame(stage, a):
    """stage 0: bowl and floor line; 1: + lifted curve; 2: + lowest point. a in [0, 1]: camera from side (0) to top (1)."""
    top = a > 0.99
    fig = go.Figure(go.Surface(x=X, y=Y, z=f(X, Y), colorscale="Blues", reversescale=True, showscale=False, opacity=0.55,
                               contours=dict(z=dict(show=True, start=2, end=26, size=4, color="#2F4B7C", width=2))))
    fig.add_trace(go.Scatter3d(x=t, y=3 - t, z=0 * t, mode="lines", line=dict(color=GREEN, width=6, dash="dash")))
    fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0], mode="markers", marker=dict(size=5, color=GREY)))
    if stage >= 1:
        fig.add_trace(go.Scatter3d(x=t, y=3 - t, z=on_line + 0.05, mode="lines", line=dict(color=GREEN, width=10)))
    if stage >= 2:
        fig.add_trace(go.Scatter3d(x=[2, 2], y=[1, 1], z=[0, 6], mode="lines", line=dict(color=RED, width=4, dash="dot")))
        fig.add_trace(go.Scatter3d(x=[2], y=[1], z=[6.1], mode="markers", marker=dict(size=8, color=RED)))
    eye = dict(x=-1.25 * (1 - a), y=-1.75 * (1 - a) - 0.03 * a, z=1.0 * (1 - a) + 2.4 * a)
    tick = dict(tickfont=dict(size=14))
    fig.update_scenes(xaxis=dict(title="x", range=[-1, 3.6], nticks=5, **tick), yaxis=dict(title="y", range=[-1.2, 3], nticks=5, **tick),
                      zaxis=dict(title="" if top else "f", range=[0, 26], nticks=4, showticklabels=not top, **tick),
                      aspectmode="manual", aspectratio=dict(x=1, y=1, z=0.8), camera=dict(eye=eye, center=dict(x=0, y=0, z=-0.15 * (1 - a)), projection=dict(type="orthographic")))
    title = ["The bowl f = x² + 2y² and the line x + y = 3 on the floor (dashed)",
             "Lift the line onto the bowl: only this curve is allowed",
             "The answer is the lowest point of the curve: (2, 1), f = 6"][stage]
    if a > 0:
        title = "Seen from above: contour rings, and the curve is the line again" if top else "Turn to the top view …"
    fig.update_layout(template="simple_white", width=900, height=720, font=FONT, showlegend=False,
                      margin=dict(l=0, r=0, t=60, b=0), title=dict(text=title, x=0.5, y=0.97, font=dict(size=22)))
    return fig


cams = [0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1.0]
figs = [frame(0, 0), frame(1, 0), frame(2, 0)] + [frame(2, a) for a in cams]
holds = [9, 9, 12] + [2] * (len(cams) - 1) + [14]
make_gif(figs, here / "lifted_constraint", fps=6, holds=holds, keys=[0, 1, 2, len(figs) - 1])
