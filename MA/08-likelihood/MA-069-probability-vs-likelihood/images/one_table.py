"""Probability and likelihood are two readings of one table (Plotly heatmap): P(k heads in 5 tosses | p) for p from
0 to 1 (rows, steps of 0.1) and k from 0 to 5 (columns). Read along a row (p fixed, here 0.5): the probabilities of
the possible events, which add to 1. Read down a column (data fixed, here k = 5): the likelihood of each p, which
is p^5 and does not add to 1."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy import stats
from gifkit import FONT, GREEN, ORANGE

here = Path(__file__).parent
ps = np.round(np.linspace(0, 1, 11), 1)
ks = np.arange(6)
T = np.array([[stats.binom.pmf(k, 5, p) for k in ks] for p in ps])
assert np.isclose(T[5].sum(), 1) and np.allclose(T[:, 5], ps ** 5) and np.isclose(T[5, 5], 0.03125)
fig = go.Figure(go.Heatmap(z=T, x=[str(k) for k in ks], y=[f"{p:.1f}" for p in ps], colorscale="Blues", showscale=False,
                           text=[[f"{v:.3f}" for v in row] for row in T], texttemplate="%{text}", textfont=dict(size=15)))
fig.add_shape(type="rect", x0=-0.5, x1=5.5, y0=4.5, y1=5.5, line=dict(color=ORANGE, width=5), fillcolor="rgba(0,0,0,0)")
fig.add_shape(type="rect", x0=4.5, x1=5.5, y0=-0.5, y1=10.5, line=dict(color=GREEN, width=5), fillcolor="rgba(0,0,0,0)")
fig.add_annotation(x=5.6, y=5, xref="x", yref="y", xanchor="left", showarrow=False, align="left", font=dict(size=18, color=ORANGE),
                   text="row p = 0.5:<br>probabilities of<br>every event,<br>sum = 1<br>(0.998 after<br>rounding)")
fig.add_annotation(x=5, y=10.6, xref="x", yref="y", yanchor="bottom", showarrow=False, font=dict(size=18, color=GREEN),
                   text="column k = 5: likelihood of every p")
fig.update_layout(template="simple_white", width=1000, height=780, font=FONT,
                  xaxis=dict(title="event: number of heads in 5 tosses, k", range=[-0.5, 7.3]),
                  yaxis=dict(title="parameter p (probability of heads)"), margin=dict(l=90, r=20, t=50, b=70))
fig.write_image(here / "one_table.png", scale=2)
