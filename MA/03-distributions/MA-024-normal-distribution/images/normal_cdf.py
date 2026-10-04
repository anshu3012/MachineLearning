"""Normal PDFs (top) and CDFs (bottom): three standard deviations around mean 0, and one curve with mean -2.
Every CDF passes 0.5 at its mean; a small standard deviation makes the S steep."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
x = np.linspace(-5, 5, 800)
curves = [(0, 0.5, "#4C78A8", "solid"), (0, 1, "#E45756", "dash"), (0, 2, "#F58518", "dot"), (-2, 0.7, "#54A24B", "dashdot")]
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08, subplot_titles=["PDF", "CDF"])
for mu, sd, colour, dash in curves:
    d = stats.norm(mu, sd)
    fig.add_scatter(x=x, y=d.pdf(x), mode="lines", name=f"μ = {mu}, σ = {sd}",
                    line=dict(color=colour, width=3.5, dash=dash), row=1, col=1)
    fig.add_scatter(x=x, y=d.cdf(x), mode="lines", showlegend=False, line=dict(color=colour, width=3.5, dash=dash),
                    row=2, col=1)
fig.add_hline(y=0.5, line=dict(color="#6B6B6B", width=1.5, dash="dot"), row=2, col=1)
fig.add_annotation(x=-4.2, y=0.56, text="0.5 at the mean", showarrow=False, font=dict(size=16, color="#6B6B6B"),
                   row=2, col=1)
fig.update_xaxes(title_text="x", dtick=1, row=2, col=1)
fig.update_yaxes(title_text="density f(x)", row=1, col=1)
fig.update_yaxes(title_text="F(x) = P(X ≤ x)", range=[0, 1.02], row=2, col=1)
fig.update_annotations(selector=dict(xref="paper"), font_size=19)
fig.update_layout(template="simple_white", width=1000, height=720, legend=dict(x=0.78, y=0.98, font=dict(size=17)),
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=80, r=20, t=40, b=50))
fig.write_image(here / "normal_cdf.png", scale=2)
fig.write_image(here / "normal_cdf.pdf")
