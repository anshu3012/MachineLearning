"""Plain gradient descent on the narrow valley L = (w1^2 + 100 w2^2)/2 with three learning rates, 50 steps each (Plotly).
The steep direction w2 caps the learning rate; with that rate the flat direction w1 crawls."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, RED, GREY, FONT

here = Path(__file__).parent
K, START, STEPS = 100, np.array([-10.0, 0.4]), 50
grad = lambda w: np.array([w[0], K * w[1]])


def path(eta):
    w, P = START.copy(), [START.copy()]
    for _ in range(STEPS):
        w = w - eta * grad(w)
        P.append(w.copy())
    return np.array(P)


gx, gy = np.linspace(-11, 2, 200), np.linspace(-0.6, 0.6, 200)
X, Y = np.meshgrid(gx, gy)
Z = 0.5 * (X ** 2 + K * Y ** 2)
titles = ("η = 0.002: too small", "η = 0.019: largest that converges", "η = 0.021: too large")
fig = make_subplots(rows=3, cols=1, subplot_titles=titles, vertical_spacing=0.09)
for row, eta in enumerate((0.002, 0.019, 0.021), start=1):
    P = path(eta)
    fig.add_trace(go.Contour(x=gx, y=gy, z=np.log10(Z + 0.01), colorscale="Greys", reversescale=True, showscale=False,
                             contours=dict(start=-2, end=2.2, size=0.3), line=dict(width=0.5), opacity=0.4), row=row, col=1)
    keep = np.abs(P[:, 1]) < 0.6
    fig.add_trace(go.Scatter(x=P[keep, 0], y=P[keep, 1], mode="lines+markers", line=dict(color=BLUE, width=2),
                             marker=dict(size=5), showlegend=False), row=row, col=1)
    fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers", marker=dict(symbol="star", size=16, color=RED),
                             showlegend=False), row=row, col=1)
    fig.add_annotation(x=1.9, y=0.45, xanchor="right", showarrow=False, font=dict(size=15, color=GREY),
                       bgcolor="white", text=f"loss after 50 steps: {0.5 * (P[-1, 0] ** 2 + K * P[-1, 1] ** 2):,.3g}", row=row, col=1)
fig.update_xaxes(range=[-11, 2], title_text="w₁ (flat direction)", row=3, col=1)
fig.update_yaxes(range=[-0.6, 0.6], title_text="w₂")
fig.update_layout(template="simple_white", width=950, height=850, font=FONT, margin=dict(l=70, r=20, t=40, b=60))
fig.write_image(here / "valley_lr.png", scale=2)
fig.write_image(here / "valley_lr.pdf")
