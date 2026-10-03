"""Heights ~ Normal(165, 10): the PDF (area to the left shaded) and the CDF that reads that area off."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
h = stats.norm(165, 10)
x = np.linspace(125, 205, 500)
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.13,
                    subplot_titles=["PDF f(x): height = density; shaded area = P(X ≤ 150)",
                                    "CDF F(x) = P(X ≤ x): the area to the left of x"])
fig.add_scatter(x=x, y=h.pdf(x), mode="lines", line=dict(color="#4C78A8", width=4), row=1, col=1)
s = np.linspace(125, 150, 200)
fig.add_scatter(x=np.r_[s, 150, 125], y=np.r_[h.pdf(s), 0, 0], fill="toself", fillcolor="rgba(228,87,86,0.4)",
                line=dict(width=0), row=1, col=1)
fig.add_annotation(x=165, y=h.pdf(165), text=f"f(165) = {h.pdf(165):.4f}", ax=90, ay=-10, font=dict(size=18),
                   row=1, col=1)
fig.add_annotation(x=145, y=0.004, text=f"area {h.cdf(150):.3f}", ax=-70, ay=-50, font=dict(size=18, color="#E45756"),
                   arrowcolor="#E45756", row=1, col=1)
fig.add_scatter(x=x, y=h.cdf(x), mode="lines", line=dict(color="#F58518", width=4), row=2, col=1)
for xv, c in [(150, "#E45756"), (165, "#54A24B")]:
    yv = h.cdf(xv)
    fig.add_shape(type="line", x0=xv, x1=xv, y0=0, y1=yv, line=dict(color=c, dash="dash", width=2.5), row=2, col=1)
    fig.add_shape(type="line", x0=125, x1=xv, y0=yv, y1=yv, line=dict(color=c, dash="dash", width=2.5), row=2, col=1)
    fig.add_annotation(x=xv - 1, y=yv, text=f"F({xv}) = {yv:.3f}", showarrow=False, xanchor="right", yanchor="bottom",
                       font=dict(color=c, size=19), row=2, col=1)
fig.update_xaxes(title_text="height x (cm)", dtick=10, row=2, col=1)
fig.update_yaxes(title_text="density", range=[0, 0.045], row=1, col=1)
fig.update_yaxes(title_text="F(x)", range=[0, 1.05], dtick=0.25, row=2, col=1)
fig.update_annotations(selector=dict(xref="paper"), font_size=20)
fig.update_layout(template="simple_white", width=1000, height=760, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=18), margin=dict(l=70, r=20, t=50, b=50))
fig.write_image(here / "pdf_cdf_heights.png", scale=2)
fig.write_image(here / "pdf_cdf_heights.pdf")
