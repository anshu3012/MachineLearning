"""Section 5.1 drawn: men's heights N(68, 3^2), the area above 72 inches shaded; the same area above z = 1.33 on
the standard normal axis below. Area 1 - Phi(1.33) = 0.09176."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy import stats

here = Path(__file__).parent
assert round(1 - stats.norm.cdf(1.33), 5) == 0.09176
x = np.linspace(56, 80, 400)
y = stats.norm(68, 3).pdf(x)
fig = go.Figure()
fig.add_scatter(x=x, y=y, mode="lines", line=dict(color="#4C78A8", width=4))
m = x >= 72
fig.add_scatter(x=np.r_[72, x[m], x[m][-1]], y=np.r_[0, y[m], 0], fill="toself", fillcolor="rgba(245,133,24,0.5)",
                line=dict(width=0), mode="lines")
fig.add_annotation(x=74.5, y=0.045, text="P(X > 72) = 1 − Φ(1.33)<br>= 1 − 0.90824 = <b>0.09176</b>", showarrow=False,
                   font=dict(size=20), xanchor="left")
fig.add_vline(x=72, line=dict(color="#F58518", width=2))
fig.add_annotation(x=72, y=0.142, text="72 inches = z 1.33", showarrow=False, xanchor="left", xshift=6, font=dict(size=20, color="#c55a00"))
ticks = [59, 62, 65, 68, 71, 74, 77]
fig.update_layout(template="simple_white", width=1100, height=560, font=dict(family="Latin Modern Roman", size=19),
                  showlegend=False, title=dict(text="Heights X ~ N(68, 3²): taller than 72 inches", x=0.5),
                  xaxis=dict(title="height (inches)  /  z = (height − 68) / 3", tickvals=ticks,
                             ticktext=[f"{t}<br>z = {(t - 68) / 3:.2f}" for t in ticks]),
                  yaxis=dict(title="density", range=[0, 0.15]), margin=dict(l=80, r=30, t=70, b=110))
fig.write_image(here / "heights_tail.png", scale=2)
fig.write_image(here / "heights_tail.pdf")
