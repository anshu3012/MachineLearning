"""Cutting a bell curve to a range does not make it flat: a normal height distribution (mean 5.8 ft, sd 0.2 ft, an
illustrative choice) restricted to 5.6 to 6 ft, rescaled to area 1, against the uniform U(5.6, 6)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy import stats

here = Path(__file__).parent
a, b, mu, sd = 5.6, 6.0, 5.8, 0.2
tn = stats.truncnorm((a - mu) / sd, (b - mu) / sd, loc=mu, scale=sd)
x = np.linspace(5.5, 6.1, 400)
assert np.isclose(tn.cdf(b), 1) and tn.pdf(5.8) > 1.3 * tn.pdf(5.6)   # centre clearly denser than the ends
fig = go.Figure()
fig.add_scatter(x=x, y=stats.uniform(a, b - a).pdf(x), mode="lines", line=dict(color="#9a9a9a", width=4, dash="dash"),
                name="uniform U(5.6, 6): flat")
fig.add_scatter(x=x, y=tn.pdf(x), mode="lines", line=dict(color="#4C78A8", width=4),
                name="normal cut to 5.6 to 6: still a bell")
fig.update_layout(template="simple_white", width=1000, height=520, font=dict(family="Latin Modern Roman", size=19),
                  title=dict(text="Restricting a normal variable to a range keeps its bell shape", x=0.5),
                  xaxis=dict(title="height (feet)"), yaxis=dict(title="density", range=[0, 3.6]),
                  legend=dict(x=0.02, y=0.98), margin=dict(l=80, r=30, t=70, b=70))
fig.write_image(here / "truncated_normal.png", scale=2)
fig.write_image(here / "truncated_normal.pdf")
