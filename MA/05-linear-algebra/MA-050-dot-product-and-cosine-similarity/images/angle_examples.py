"""The angle from the components: a = [3, 4] and b = [4, 3] have a . b = 24, lengths 5 and 5, so cos(theta) = 0.96
and theta = 16.26 degrees; [3, 4] and [-4, 3] have dot product 0, so they are perpendicular (orthogonal)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
a, b, c = np.array([3, 4.0]), np.array([4, 3.0]), np.array([-4, 3.0])
th = np.degrees(np.arccos(a @ b / (np.linalg.norm(a) * np.linalg.norm(b))))
assert a @ b == 24 and round(th, 2) == 16.26 and a @ c == 0
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1, subplot_titles=[
    "a · b = 24, cos θ = 24 / (5 × 5) = 0.96, θ = 16.26°", "[3, 4] · [−4, 3] = −12 + 12 = 0: a right angle"])
for col, (u, v) in enumerate(((a, b), (a, c)), start=1):
    for w, colr, name in ((u, "#4C78A8", f"[{u[0]:g}, {u[1]:g}]"), (v, "#F58518", f"[{v[0]:g}, {v[1]:g}]")):
        fig.add_annotation(x=w[0], y=w[1], ax=0, ay=0, xref=f"x{col}", yref=f"y{col}", axref=f"x{col}", ayref=f"y{col}",
                           arrowhead=3, arrowwidth=4, arrowcolor=colr, showarrow=True)
        fig.add_annotation(x=w[0], y=w[1], text=name, showarrow=False, yshift=18, xref=f"x{col}", yref=f"y{col}",
                           font=dict(size=19, color=colr))
    t0, t1 = sorted([np.arctan2(u[1], u[0]), np.arctan2(v[1], v[0])])
    ts = np.linspace(t0, t1, 40)
    fig.add_scatter(x=1.3 * np.cos(ts), y=1.3 * np.sin(ts), mode="lines", line=dict(color="black", width=2), row=1, col=col)
    fig.update_xaxes(range=[-5, 5.5], zeroline=True, row=1, col=col)
    fig.update_yaxes(range=[-0.8, 5.2], zeroline=True, scaleanchor=f"x{col}", row=1, col=col)
for ann in fig.layout.annotations[:2]:
    ann.font.size = 19
fig.update_layout(template="simple_white", width=1400, height=520, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=40, r=20, t=60, b=40))
fig.write_image(here / "angle_examples.png", scale=2)
fig.write_image(here / "angle_examples.pdf")
