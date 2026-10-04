"""Zero covariance without "no relationship": five points on y = x^2. The rectangles from the mean lines to each
point have areas -4, +1, 0, -1, +4, which cancel, so the covariance is 0 although y is fixed by x. Plotly."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go

here = Path(__file__).parent
BLUE, RED = "#4C78A8", "#E45756"
x = np.array([-2, -1, 0, 1, 2.0])
y = x ** 2
mx, my = x.mean(), y.mean()
prod = (x - mx) * (y - my)
assert prod.tolist() == [-4, 1, 0, -1, 4] and prod.sum() == 0
xs = np.linspace(-2.3, 2.3, 100)
fig = go.Figure(go.Scatter(x=xs, y=xs ** 2, mode="lines", line=dict(color="#9a9a9a", width=2, dash="dot")))
for xi, yi, p in zip(x, y, prod):
    if p:
        c = BLUE if p > 0 else RED
        fig.add_shape(type="rect", x0=mx, x1=xi, y0=my, y1=yi, line=dict(color=c, width=2), fillcolor=c, opacity=0.25)
        fig.add_annotation(x=(mx + xi) / 2, y=(my + yi) / 2, text=f"<b>{p:+.0f}</b>", showarrow=False,
                           font=dict(size=22, color=c))
fig.add_vline(x=mx, line=dict(color="black", width=1.5, dash="dash"))
fig.add_hline(y=my, line=dict(color="black", width=1.5, dash="dash"))
fig.add_scatter(x=x, y=y, mode="markers", marker=dict(size=14, color="black"))
fig.add_annotation(x=2.3, y=my, text="mean of y = 2", showarrow=False, yshift=14, xanchor="right", font=dict(size=17))
fig.add_annotation(x=mx, y=4.6, text="mean of x = 0", showarrow=False, xshift=8, xanchor="left", font=dict(size=17))
fig.update_layout(template="simple_white", width=800, height=520, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=20), xaxis=dict(title="x", range=[-2.6, 2.6]),
                  yaxis=dict(title="y = x²", range=[-0.4, 4.9]), margin=dict(l=70, r=20, t=20, b=60))
fig.write_image(here / "zero_cov_curve.png", scale=2)
fig.write_image(here / "zero_cov_curve.pdf")
