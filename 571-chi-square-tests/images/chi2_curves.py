"""Chi-square densities for 1, 2, 4 and 8 degrees of freedom: always positive, right-skewed, centred near df."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy import stats

here = Path(__file__).parent
x = np.linspace(0.05, 20, 600)
fig = go.Figure()
for df, colour in zip([1, 2, 4, 8], ["#E45756", "#F58518", "#4C78A8", "#54A24B"]):
    fig.add_scatter(x=x, y=stats.chi2.pdf(x, df), mode="lines", line=dict(color=colour, width=3), name=f"df = {df}")
fig.update_layout(template="simple_white", width=900, height=450, xaxis_title="χ² value", yaxis_title="density",
                  yaxis_range=[0, 0.55], legend=dict(x=0.75, y=0.95),
                  font=dict(family="Latin Modern Roman", size=18), margin=dict(l=70, r=20, t=20, b=60))
fig.write_image(here / "chi2_curves.png", scale=2)
fig.write_image(here / "chi2_curves.pdf")
