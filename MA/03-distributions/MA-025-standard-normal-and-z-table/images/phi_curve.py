"""The standard normal PDF phi(z) with the two worked values of section 2: phi(0) = 0.3989 and phi(1) = 0.2420."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy import stats

here = Path(__file__).parent
z = np.linspace(-4, 4, 400)
assert round(stats.norm.pdf(0), 4) == 0.3989 and round(stats.norm.pdf(1), 4) == 0.2420
fig = go.Figure(go.Scatter(x=z, y=stats.norm.pdf(z), mode="lines", line=dict(color="#4C78A8", width=4)))
for v in (0, 1):
    h = stats.norm.pdf(v)
    fig.add_shape(type="line", x0=v, x1=v, y0=0, y1=h, line=dict(color="#F58518", width=3, dash="dash"))
    fig.add_annotation(x=v, y=h, text=f"φ({v}) = {h:.4f}", ax=70, ay=-35, font=dict(size=22), arrowwidth=2)
fig.update_layout(template="simple_white", width=1000, height=520, font=dict(family="Latin Modern Roman", size=20),
                  title=dict(text="Z ~ N(0, 1): the x axis counts standard deviations from the mean", x=0.5),
                  xaxis=dict(title="z", dtick=1), yaxis=dict(title="density φ(z)", range=[0, 0.47]),
                  showlegend=False, margin=dict(l=80, r=30, t=70, b=70))
fig.write_image(here / "phi_curve.png", scale=2)
fig.write_image(here / "phi_curve.pdf")
