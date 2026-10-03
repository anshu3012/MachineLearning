"""PMF (bars) and CDF (steps) of the sum of two dice, with the readings F(5) and F(9)."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots

here = Path(__file__).parent
x = np.arange(2, 13)
pmf = (6 - np.abs(x - 7)) / 36
cdf = np.cumsum(pmf)
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.12, row_heights=[0.4, 0.6],
                    subplot_titles=["PMF: P(X = x), the probability of exactly x",
                                    "CDF: F(x) = P(X ≤ x), the probability of x or less"])
fig.add_bar(x=x, y=pmf, marker_color="#4C78A8", row=1, col=1)
fig.add_scatter(x=np.r_[0.5, x, 13.5], y=np.r_[0, cdf, 1], mode="lines", line_shape="hv",
                line=dict(color="#F58518", width=4), row=2, col=1)
fig.add_scatter(x=x, y=cdf, mode="markers", marker=dict(color="#F58518", size=10), row=2, col=1)
for xv, c in [(5, "#54A24B"), (9, "#E45756")]:
    yv = cdf[x == xv][0]
    fig.add_shape(type="line", x0=xv, x1=xv, y0=0, y1=yv, line=dict(color=c, dash="dash", width=2.5), row=2, col=1)
    fig.add_shape(type="line", x0=0.5, x1=xv, y0=yv, y1=yv, line=dict(color=c, dash="dash", width=2.5), row=2, col=1)
    fig.add_annotation(x=xv - 0.15, y=yv, text=f"F({xv}) = {round(yv * 36)}/36 = {yv:.3f}", showarrow=False,
                       xanchor="right", yanchor="bottom", font=dict(color=c, size=19), row=2, col=1)
fig.update_xaxes(dtick=1, range=[0.5, 13.5])
fig.update_xaxes(title_text="sum of two dice x", row=2, col=1)
fig.update_yaxes(title_text="P(X = x)", range=[0, 0.2], row=1, col=1)
fig.update_yaxes(title_text="F(x)", range=[0, 1.05], dtick=0.25, row=2, col=1)
fig.update_annotations(selector=dict(xref="paper"), font_size=20)
fig.update_layout(template="simple_white", width=1000, height=780, showlegend=False, bargap=0.3,
                  font=dict(family="Latin Modern Roman", size=18), margin=dict(l=70, r=20, t=50, b=50))
fig.write_image(here / "pmf_cdf.png", scale=2)
fig.write_image(here / "pmf_cdf.pdf")
