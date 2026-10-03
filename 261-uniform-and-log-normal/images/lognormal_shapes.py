"""Log-normal PDFs with mu = 0 and growing sigma: the larger sigma, the more spread and the longer the right tail."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy import stats

here = Path(__file__).parent
x = np.linspace(0.001, 4, 800)
fig = go.Figure()
for s, colour, dash in ((0.25, "#4C78A8", "solid"), (0.5, "#F58518", "dash"), (1.0, "#E45756", "dot")):
    fig.add_scatter(x=x, y=stats.lognorm(s=s, scale=1).pdf(x), mode="lines", name=f"μ = 0, σ = {s}",
                    line=dict(color=colour, width=4, dash=dash))
fig.update_layout(template="simple_white", width=900, height=430, xaxis=dict(title="x", range=[0, 4], dtick=0.5), yaxis_title="density f(x)",
                  legend=dict(x=0.65, y=0.95, font=dict(size=18)),
                  font=dict(family="Latin Modern Roman", size=18), margin=dict(l=70, r=20, t=20, b=50))
fig.write_image(here / "lognormal_shapes.png", scale=2)
fig.write_image(here / "lognormal_shapes.pdf")
