"""From soft to hard assignment: two components with equal weights and equal variance sigma^2, centred at 0 and 4.
The responsibility of component 1 across x for sigma = 2, 1, 0.5 and 0.1. As sigma shrinks, the curve becomes a
step at the midpoint 2: each observation goes wholly to the nearer centre, as in k-means."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from scipy import stats
from scipy.special import expit

from em_core import BLUE, FONT, GREEN, ORANGE, RED

HERE = Path(__file__).parent
x = np.linspace(-2, 6, 801)
fig = go.Figure()
for s, c in ((2, GREEN), (1, ORANGE), (0.5, BLUE), (0.1, RED)):
    a, b = stats.norm(0, s).logpdf(x), stats.norm(4, s).logpdf(x)
    r1 = expit(a - b)                                         # = N1 / (N1 + N2), computed stably
    fig.add_trace(go.Scatter(x=x, y=r1, mode="lines", line=dict(color=c, width=4), name=f"σ = {s}"))
    if s == 0.1:
        assert r1[x < 1.9].min() > 0.999 and r1[x > 2.1].max() < 0.001
fig.add_vline(x=2, line=dict(color="black", dash="dot", width=2))
fig.add_annotation(x=2, y=1.06, text="midpoint between the centres 0 and 4", showarrow=False, bgcolor="white")
fig.update_layout(template="simple_white", width=900, height=480, font=FONT,
                  xaxis=dict(title="x"), yaxis=dict(title="responsibility of component 1", range=[-0.05, 1.12]),
                  legend=dict(x=0.8, y=0.85), margin=dict(l=70, r=20, t=30, b=60))
fig.write_image(HERE / "hard_soft.png", scale=2)
fig.write_image(HERE / "hard_soft.pdf")
