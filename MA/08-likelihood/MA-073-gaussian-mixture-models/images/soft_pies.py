"""Soft membership drawn (Plotly): the six points and the two starting curves A and B (top); below each point a pie
that splits the point between A and B by its responsibility. Own design, own data (six_points.py)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from six_points import COLS, FONT, START, X, e_step, weighted

here = Path(__file__).parent
R = e_step(*START)
g = np.linspace(-1, 11, 400)
W = weighted(g, *START)
LO, HI = -1, 11
fig = go.Figure()
fig.update_layout(xaxis=dict(domain=[0.04, 0.96], range=[LO, HI], dtick=1, title="x", anchor="y"),
                  yaxis=dict(domain=[0.40, 1.0], range=[0, 0.12], showticklabels=False, anchor="x"))
for k, nm in enumerate("AB"):
    fig.add_trace(go.Scatter(x=g, y=W[:, k], mode="lines", line=dict(color=COLS[k], width=4), xaxis="x", yaxis="y"))
    mx = START[1][k]
    fig.add_annotation(x=mx, y=0.108, text=f"<b>curve {nm}</b>", showarrow=False, font=dict(size=24, color=COLS[k]),
                       xshift=-70 if k == 0 else 70)
fig.add_trace(go.Scatter(x=X, y=np.zeros(6), mode="markers", marker=dict(size=16, color="black"), xaxis="x", yaxis="y"))
for i, x in enumerate(X):
    cx = 0.04 + 0.92 * (x - LO) / (HI - LO)
    fig.add_trace(go.Pie(values=R[i], marker=dict(colors=COLS), sort=False, direction="clockwise", textinfo="none",
                         hoverinfo="skip", domain=dict(x=[cx - 0.03, cx + 0.03], y=[0.10, 0.34])))
    fig.add_annotation(x=cx, y=0.07, xref="paper", yref="paper", showarrow=False, align="center",
                       text=f"<span style='color:{COLS[0]}'>{R[i, 0]:.2f}</span><br><span style='color:{COLS[1]}'>{R[i, 1]:.2f}</span>",
                       font=dict(size=21))
fig.update_layout(template="simple_white", width=1150, height=640, font=FONT, showlegend=False,
                  margin=dict(l=20, r=20, t=20, b=60))
fig.write_image(here / "soft_pies.png", scale=2)
fig.write_image(here / "soft_pies.pdf")
