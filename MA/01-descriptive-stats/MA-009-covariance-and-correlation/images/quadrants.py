"""Covariance by quadrants: experience vs salary of 5 employees, with the two mean lines and each point's product."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
x = np.array([2, 5, 8, 12, 13])                  # experience in years (left), backlogs (right)
sets = {"Experience vs salary: cov = +21.5": np.array([1, 2, 5, 12, 10]),
        "Backlogs vs package: cov = -20.75": np.array([10, 12, 5, 2, 1])}
fig = make_subplots(rows=1, cols=2, subplot_titles=list(sets), horizontal_spacing=0.1)
for col, (title, y) in enumerate(sets.items(), start=1):
    xm, ym = x.mean(), y.mean()
    # shade the quadrants: green where the product is positive (I and III), red where negative (II and IV)
    for (x0, x1, y0, y1, c) in [(xm, 15, ym, 14, "#54A24B"), (0, xm, 0, ym, "#54A24B"),
                                (0, xm, ym, 14, "#E45756"), (xm, 15, 0, ym, "#E45756")]:
        fig.add_shape(type="rect", x0=x0, x1=x1, y0=y0, y1=y1, fillcolor=c, opacity=0.08, line_width=0,
                      row=1, col=col)
    fig.add_vline(x=xm, line=dict(color="#6B6B6B", dash="dash"), row=1, col=col)
    fig.add_hline(y=ym, line=dict(color="#6B6B6B", dash="dash"), row=1, col=col)
    prods = (x - xm) * (y - ym)
    fig.add_scatter(x=x, y=y, mode="markers+text", marker=dict(size=13, color="#4C78A8"),
                    text=[f"{p:+.0f}" if p else "0" for p in prods], textposition="top center",
                    textfont=dict(size=17), row=1, col=col)
    for qx, qy, q in [(14, 13.3, "I"), (0.8, 13.3, "II"), (0.8, 0.6, "III"), (14, 0.6, "IV")]:
        fig.add_annotation(x=qx, y=qy, text=q, showarrow=False, font=dict(size=18, color="#6B6B6B"), row=1, col=col)
    fig.add_annotation(x=xm, y=13.6, text=f"mean x = {xm:g}", showarrow=False, xanchor="left", xshift=4,
                       font=dict(size=14, color="#6B6B6B"), row=1, col=col)
    fig.add_annotation(x=15, y=ym, text=f"mean y = {ym:g}", showarrow=False, xanchor="right", yshift=10,
                       font=dict(size=14, color="#6B6B6B"), row=1, col=col)
fig.update_xaxes(range=[0, 15])
fig.update_xaxes(title_text="experience (years)", row=1, col=1)
fig.update_xaxes(title_text="number of backlogs", row=1, col=2)
fig.update_yaxes(title_text="salary (lakh rupees a month)", range=[0, 14], row=1, col=1)
fig.update_yaxes(title_text="package (lakh rupees)", range=[0, 14], row=1, col=2)
fig.update_annotations(selector=dict(text=list(sets)[0]), font_size=18)
fig.update_annotations(selector=dict(text=list(sets)[1]), font_size=18)
fig.update_layout(template="simple_white", width=1400, height=560, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=16), margin=dict(l=70, r=20, t=50, b=60))
fig.write_image(here / "quadrants.png", scale=2)
fig.write_image(here / "quadrants.pdf")
