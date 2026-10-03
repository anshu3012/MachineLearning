"""Poisson PMFs for lambda = 1, 4, 10 with the mean marked; the shape moves right and spreads out as lambda grows."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
COLOURS = {1: "#E45756", 4: "#4C78A8", 10: "#54A24B"}
y = np.arange(0, 21)
fig = make_subplots(rows=1, cols=3, shared_yaxes=True, horizontal_spacing=0.05,
                    subplot_titles=[f"λ = {lam}: mean {lam}, variance {lam}" for lam in COLOURS])
for i, (lam, colour) in enumerate(COLOURS.items(), start=1):
    fig.add_bar(x=y, y=stats.poisson.pmf(y, lam), marker_color=colour, showlegend=False, row=1, col=i)
    fig.add_vline(x=lam, line_dash="dash", line_color="black", line_width=2, row=1, col=i)
    fig.update_xaxes(tickvals=list(range(0, 21, 5)), title_text="count, y", row=1, col=i)
fig.update_yaxes(title_text="P(Y = y)", row=1, col=1)
fig.update_annotations(font_size=20)
fig.update_layout(template="simple_white", width=1100, height=420, bargap=0.15,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=70, r=20, t=40, b=40))
fig.write_image(here / "poisson_shapes.png", scale=2)
fig.write_image(here / "poisson_shapes.pdf")
