"""Still figures (Plotly): products.png (section 3.1: a product of k equal factors) and
slopes.png (section 6.2: the slope of sigmoid against the slope of ReLU)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from common import BLUE, ORANGE, GREEN, RED, GREY, FONT

here = Path(__file__).parent
F = dict(FONT, size=20)

k = np.arange(0, 11)
assert np.isclose(0.1 ** 10, 1e-10) and round(0.25 ** 10 * 1e7, 1) == 9.5 and round(1.5 ** 10) == 58   # Sections 3.1, 3.2, 7.1
fig = go.Figure()
for f, c, lab, end in ((1.5, BLUE, "factor 1.5: explodes", "58"), (1.0, GREY, "factor 1: stays", "1"),
                       (0.25, RED, "factor 0.25 (sigmoid's largest slope)", "9.5 × 10⁻⁷"), (0.1, ORANGE, "factor 0.1", "10⁻¹⁰")):
    fig.add_trace(go.Scatter(x=k, y=f ** k, mode="lines+markers", line=dict(color=c, width=4), marker=dict(size=9),
                             name=f"{lab}: {f}¹⁰ = {end}"))
fig.update_layout(template="simple_white", width=1000, height=520, font=F,
                  xaxis=dict(title="number of factors k (layers between the weight and the loss)", dtick=1),
                  yaxis=dict(title="product of k factors (log scale)", type="log", dtick=2, exponentformat="power"),
                  legend=dict(x=0.01, y=0.02, yanchor="bottom", bgcolor="rgba(255,255,255,0.85)"),
                  margin=dict(l=90, r=30, t=30, b=70))
fig.write_image(here / "products.png", scale=2)

z = np.linspace(-6, 6, 601)
s = 1 / (1 + np.exp(-z))
ds = s * (1 - s)
assert np.isclose(ds.max(), 0.25)
fig = go.Figure()
fig.add_trace(go.Scatter(x=z, y=ds, line=dict(color=RED, width=5), name="sigmoid slope σ(z)(1 − σ(z)): at most 0.25"))
fig.add_trace(go.Scatter(x=z[z < 0], y=0 * z[z < 0], line=dict(color=GREEN, width=5), name="ReLU slope: 0 or 1"))
fig.add_trace(go.Scatter(x=z[z > 0], y=1 + 0 * z[z > 0], line=dict(color=GREEN, width=5), showlegend=False))
fig.add_annotation(x=0, y=0.25, ax=60, ay=-60, text="0.25", font=dict(size=20, color=RED), arrowcolor=RED)
fig.update_layout(template="simple_white", width=1000, height=460, font=F, xaxis=dict(title="input z of the node"),
                  yaxis=dict(title="slope (one factor of the gradient)", range=[-0.05, 1.15]),
                  legend=dict(x=0.01, y=0.85), margin=dict(l=90, r=30, t=30, b=60))
fig.write_image(here / "slopes.png", scale=2)
