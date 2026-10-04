"""1D data that no single threshold separates becomes separable after adding x squared as a second axis (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
GREEN, RED, GREY = "#54A24B", "#E45756", "#6B6B6B"
crosses = np.array([-1.3, -0.8, -0.3, 0.2, 0.7, 1.2])             # middle class
circles = np.array([-3.3, -2.8, -2.2, 2.1, 2.6, 3.2])             # outer class
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1,
                    subplot_titles=("1D: no single point separates the classes", "2D after adding x²: a line does"))
for xs, c, sym, name in ((circles, GREEN, "circle", "circles"), (crosses, RED, "x", "crosses")):
    fig.add_trace(go.Scatter(x=xs, y=np.zeros_like(xs), mode="markers", name=name,
                             marker=dict(color=c, size=16, symbol=sym, line=dict(color="black", width=1))), 1, 1)
    fig.add_trace(go.Scatter(x=xs, y=xs ** 2, mode="markers", showlegend=False,
                             marker=dict(color=c, size=16, symbol=sym, line=dict(color="black", width=1))), 1, 2)
xx = np.linspace(-3.6, 3.6, 200)
fig.add_trace(go.Scatter(x=xx, y=xx ** 2, mode="lines", line=dict(color=GREY, width=1.5, dash="dot"), showlegend=False), 1, 2)
fig.add_trace(go.Scatter(x=[-3.6, 3.6], y=[3, 3], mode="lines", line=dict(color="black", width=4), showlegend=False), 1, 2)
fig.add_annotation(x=0, y=3.7, text="separating line: x² = 3", showarrow=False, bgcolor="white", font=dict(size=17), row=1, col=2)
fig.update_xaxes(title="x", range=[-3.8, 3.8])
fig.update_yaxes(visible=False, range=[-1, 1], row=1, col=1)
fig.update_yaxes(title="x²", range=[-0.5, 12], row=1, col=2)
fig.update_layout(template="simple_white", width=820, height=380, font=dict(family="Latin Modern Roman", size=18),
                  legend=dict(x=0.01, y=0.98), margin=dict(l=40, r=20, t=50, b=60))
fig.write_image(here / "lift_1d.png", scale=2); fig.write_image(here / "lift_1d.pdf")
