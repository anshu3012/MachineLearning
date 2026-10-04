"""Continuous uniform distribution U(5, 6): production time of one product in hours.
Left: the PDF, a flat line at 1/(b - a), with P(5.2 <= X <= 5.5) shaded. Right: the CDF, a straight ramp."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
BLUE, ORANGE, GREY = "#4C78A8", "#F58518", "#6B6B6B"
a, b = 5, 6
u = stats.uniform(loc=a, scale=b - a)
x = np.linspace(4.5, 6.5, 2001)
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1,
                    subplot_titles=["PDF: flat at 1/(b − a) = 1", "CDF: F(x) = (x − a)/(b − a)"])
fig.add_scatter(x=[5.2, 5.2, 5.5, 5.5], y=[0, 1, 1, 0], mode="lines", fill="toself", fillcolor="rgba(76,120,168,0.35)",
                line=dict(width=0), row=1, col=1)
fig.add_scatter(x=x, y=u.pdf(x), mode="lines", line=dict(color=ORANGE, width=4, shape="hv"), row=1, col=1)
fig.add_annotation(x=5.35, y=0.5, text="area = 0.3 × 1<br>= 0.3", showarrow=False, font=dict(size=18), row=1, col=1)
for xx, t in ((a, "a = 5"), (b, "b = 6")):
    fig.add_annotation(x=xx, y=1.08, text=t, showarrow=False, font=dict(size=17, color=GREY), row=1, col=1)
fig.add_scatter(x=x, y=u.cdf(x), mode="lines", line=dict(color=ORANGE, width=4), row=1, col=2)
fig.add_scatter(x=[5.75, 5.75, 4.5], y=[0, 0.75, 0.75], mode="lines", line=dict(color=GREY, width=2, dash="dot"),
                row=1, col=2)
fig.add_annotation(x=5.75, y=0.75, text="F(5.75) = 0.75", ax=-80, ay=-40, font=dict(size=17), arrowcolor=GREY,
                   row=1, col=2)
fig.update_xaxes(title_text="production time x (hours)", dtick=0.5)
fig.update_yaxes(title_text="density f(x)", range=[0, 1.2], row=1, col=1)
fig.update_yaxes(title_text="F(x) = P(X ≤ x)", range=[0, 1.1], row=1, col=2)
fig.update_annotations(selector=dict(xref="paper"), font_size=19)
fig.update_layout(template="simple_white", width=1150, height=450, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=70, r=20, t=50, b=50))
fig.write_image(here / "uniform_pdf_cdf.png", scale=2)
fig.write_image(here / "uniform_pdf_cdf.pdf")
