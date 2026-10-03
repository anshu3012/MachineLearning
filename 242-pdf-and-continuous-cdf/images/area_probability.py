"""Probability = area under the PDF. Left: P(8 <= X <= 9) for CGPA. Right: a thin slice is about height x width."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
cg = stats.beta(7, 3, scale=10)
x = np.linspace(0, 10, 600)
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1,
                    subplot_titles=[f"P(8 ≤ X ≤ 9) = area = {cg.cdf(9) - cg.cdf(8):.3f}",
                                    "Zoom: P(8 ≤ X ≤ 8.1) ≈ f(8) × 0.1"])
for col in (1, 2):
    fig.add_scatter(x=x, y=cg.pdf(x), mode="lines", line=dict(color="#F58518", width=4), row=1, col=col)
s = np.linspace(8, 9, 100)
fig.add_scatter(x=np.r_[8, s, 9], y=np.r_[0, cg.pdf(s), 0], fill="toself", fillcolor="rgba(76,120,168,0.45)",
                line=dict(width=0), row=1, col=1)
s = np.linspace(8, 8.1, 20)
fig.add_scatter(x=np.r_[8, s, 8.1], y=np.r_[0, cg.pdf(s), 0], fill="toself", fillcolor="rgba(76,120,168,0.45)",
                line=dict(width=0), row=1, col=2)
fig.add_shape(type="rect", x0=8, x1=8.1, y0=0, y1=cg.pdf(8), line=dict(color="#E45756", width=2.5, dash="dash"), fillcolor="rgba(0,0,0,0)",
              row=1, col=2)
fig.add_annotation(x=8.05, y=cg.pdf(8) / 2, text=f"area {cg.cdf(8.1) - cg.cdf(8):.4f}<br>≈ {cg.pdf(8):.3f} × 0.1",
                   ax=-120, ay=0, font=dict(size=18), arrowcolor="#6B6B6B", row=1, col=2)
fig.add_annotation(x=8.05, y=cg.pdf(8), text=f"f(8) = {cg.pdf(8):.3f}", showarrow=True, ax=60, ay=-40,
                   font=dict(size=18, color="#E45756"), arrowcolor="#E45756", row=1, col=2)
fig.update_xaxes(title_text="CGPA x", dtick=1, row=1, col=1)
fig.update_xaxes(title_text="CGPA x", range=[7.6, 8.5], dtick=0.1, row=1, col=2)
fig.update_yaxes(title_text="density f(x)", range=[0, 0.31])
fig.update_annotations(selector=dict(xref="paper"), font_size=20)
fig.update_layout(template="simple_white", width=1100, height=470, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=18), margin=dict(l=70, r=20, t=50, b=50))
fig.write_image(here / "area_probability.png", scale=2)
fig.write_image(here / "area_probability.pdf")
