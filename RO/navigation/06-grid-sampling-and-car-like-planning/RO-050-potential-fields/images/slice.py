"""Chart: the potential along the line x = 3.6 m under the table, from the bottom wall's band (y = 0.25 m) to the
table's band (y = 0.75 m). The pull of the door, U_att = 1/2 (4 - y)^2, falls as the robot moves up; the table's hill
rises as it nears the table, the wall's hill as it nears the wall. Their sum has its lowest point at y = 0.593 m,
U = 6.003: the trap of the robot that started at (4.0, 0.5).
Run -> slice.png (and slice.html)"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

import pf
from gifkit import BLUE, FONT, ORANGE, PURPLE, RED

here = Path(__file__).parent
y = np.linspace(0.262, 0.738, 800)
ua = 0.5 * pf.ZETA * (4.0 - y) ** 2
ut = np.array([pf.u_rep_one(0.75 - v) for v in y])
uw = np.array([pf.u_rep_one(v - 0.25) for v in y])
tot = ua + ut + uw
k = int(np.argmin(tot))
assert abs(y[k] - 0.593) < 0.002 and round(tot[k], 3) == 6.003
assert all(abs(pf.U((3.6, v)) - t) < 1e-9 for v, t in zip(y[::50], tot[::50]))
fig = go.Figure()
for z, col, name, w in ((ua, BLUE, "pull of the door", 3), (ut, ORANGE, "table's hill", 3),
                         (uw, PURPLE, "bottom wall's hill", 3), (tot, "black", "total U", 5)):
    fig.add_trace(go.Scatter(x=y, y=z, mode="lines", name=name, line=dict(color=col, width=w)))
fig.add_trace(go.Scatter(x=[y[k]], y=[tot[k]], mode="markers", marker=dict(size=14, color=RED), showlegend=False))
fig.add_annotation(x=y[k], y=tot[k], text="lowest point: y = 0.593 m, U = 6.003", ax=0, ay=-70,
                   font=dict(size=20, color=RED), arrowcolor=RED)
fig.add_annotation(x=0.27, y=0.3, text="towards the bottom wall", xanchor="left", showarrow=False, font=dict(size=17))
fig.add_annotation(x=0.73, y=0.3, text="towards the table", xanchor="right", showarrow=False, font=dict(size=17))
fig.update_xaxes(title="y (m), along the line x = 3.6 m", range=[0.25, 0.75], dtick=0.05, showgrid=False)
fig.update_yaxes(title="U", range=[0, 9], dtick=1, showgrid=False)
fig.update_layout(template="simple_white", width=1000, height=600, font=FONT,
                  legend=dict(x=0.5, y=1.02, xanchor="center", yanchor="bottom", orientation="h", font=dict(size=18)),
                  margin=dict(l=80, r=30, t=70, b=70))
fig.write_image(here / "slice.png", scale=1)
