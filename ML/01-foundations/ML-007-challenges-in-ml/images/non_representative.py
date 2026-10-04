"""A non-representative sample tells the wrong story. Simulated data. Plotly: scatter plus two lines."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

here = Path(__file__).parent
rng = np.random.default_rng(2)
true = lambda x: 30 + 12 * x - 1.1 * x ** 2      # the real relationship: rises, then falls
x_all = rng.uniform(0, 10, 160)
y_all = true(x_all) + rng.normal(0, 4, x_all.size)
in_sample = (x_all > 1) & (x_all < 3.5)          # we only collected data from one narrow range

slope, intercept = np.polyfit(x_all[in_sample], y_all[in_sample], 1)
xs = np.linspace(0, 10, 100)
BLUE, LIGHT, ORANGE, GREEN = "#4C78A8", "#C8C8C8", "#F58518", "#54A24B"

fig = go.Figure()
fig.add_scatter(x=x_all[~in_sample], y=y_all[~in_sample], mode="markers", name="data we never collected",
                marker=dict(size=9, color=LIGHT))
fig.add_scatter(x=x_all[in_sample], y=y_all[in_sample], mode="markers", name="our sample", marker=dict(size=9, color=BLUE))
fig.add_scatter(x=xs, y=slope * xs + intercept, mode="lines", line=dict(color=ORANGE, width=4), showlegend=False)
fig.add_scatter(x=xs, y=true(xs), mode="lines", line=dict(color=GREEN, width=4), showlegend=False)
fig.add_annotation(x=9.6, y=slope * 9.6 + intercept, text="fitted to our sample", showarrow=False, xanchor="right",
                   yanchor="bottom", yshift=12, font=dict(color=ORANGE, size=20))
fig.add_annotation(x=9.6, y=true(9.6) - 20, text="the real pattern", showarrow=False, xanchor="right", yanchor="bottom",
                   font=dict(color=GREEN, size=20))
fig.update_layout(template="simple_white", width=1000, height=580, font=dict(family="Latin Modern Roman", size=20),
                  title=dict(text="A small, one-sided sample suggests the wrong pattern  (simulated data)", x=0.5),
                  xaxis=dict(title="Input", showgrid=True), yaxis=dict(title="Output", range=[0, 110], showgrid=True),
                  legend=dict(x=0.02, y=0.98), margin=dict(l=80, r=30, t=70, b=70))
fig.write_image(here / "non_representative.png", scale=2)
fig.write_image(here / "non_representative.pdf")
