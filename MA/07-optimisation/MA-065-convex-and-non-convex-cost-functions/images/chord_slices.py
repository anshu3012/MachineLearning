"""The chord test in two dimensions, cut down to one (Plotly). We walk along the straight line between two parameter
points and plot the loss along it (curve) against the chord between the end values (dashed). Left: the line model
y = m x + b from (m, b) = (-1, 0) to (3, 0): the curve stays below the chord (0.18 against 6.05 at the midpoint).
Right: the network y = w2 tanh(w1 x) from (-2, -1.5) to (2, 1.5), its two minima: the curve rises to 1.71 at the
midpoint (0, 0), above the chord at 0."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREEN, RED

here = Path(__file__).parent
xs = np.linspace(-2, 2, 21)
ys = 1.5 * np.tanh(2 * xs)
line = lambda p: float(np.mean((ys - p[0] * xs - p[1]) ** 2))
net = lambda p: float(np.mean((ys - p[1] * np.tanh(p[0] * xs)) ** 2))
cases = [(line, np.array([-1.0, 0.0]), np.array([3.0, 0.0]), "line y = mx + b: from (−1, 0) to (3, 0)"),
         (net, np.array([-2.0, -1.5]), np.array([2.0, 1.5]), "network y = w₂ tanh(w₁x): from (−2, −1.5) to (2, 1.5)")]
assert round(line([1, 0]), 2) == 0.18 and round(0.5 * line([-1, 0]) + 0.5 * line([3, 0]), 2) == 6.05
assert round(net([0, 0]), 2) == 1.71 and net([2, 1.5]) < 1e-12 and net([-2, -1.5]) < 1e-12
t = np.linspace(0, 1, 201)
fig = make_subplots(1, 2, horizontal_spacing=0.1, subplot_titles=[c[3] for c in cases])
fig.update_annotations(font_size=20)
for col, (L, a, b, _) in enumerate(cases, 1):
    curve = [L((1 - s) * a + s * b) for s in t]
    chord = (1 - t) * L(a) + t * L(b)
    above = np.array(curve) > chord + 1e-9
    fig.add_trace(go.Scatter(x=t, y=curve, mode="lines", line=dict(color=BLUE, width=4), name="loss along the path",
                             showlegend=col == 1), 1, col)
    fig.add_trace(go.Scatter(x=t, y=chord, mode="lines", line=dict(color=GREEN, width=3, dash="dash"), name="chord",
                             showlegend=col == 1), 1, col)
    if above.any():
        fig.add_trace(go.Scatter(x=t[above], y=np.array(curve)[above], mode="lines", line=dict(color=RED, width=6),
                                 name="curve above the chord", showlegend=True), 1, col)
    mid = L(0.5 * a + 0.5 * b)
    fig.add_annotation(x=0.5, y=mid, text=f"midpoint: curve {mid:.2f}, chord {0.5 * L(a) + 0.5 * L(b):.2f}",
                       ax=0, ay=-50 if col == 2 else 60, font=dict(size=18), row=1, col=col)
    fig.update_xaxes(title="fraction of the way along the path", row=1, col=col)
fig.update_yaxes(title="mean squared error", row=1, col=1)
fig.update_layout(template="simple_white", width=1300, height=540, font=FONT,
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2), margin=dict(l=70, r=30, t=60, b=120))
fig.write_image(here / "chord_slices.png", scale=2)
