"""Step 1 of a cycle on numbers, at 2.4 s (the cycle the person appears): the global plan (grey dashed, a pose every
0.05 m), the local costmap (thin grey square, 3 m x 3 m round the robot), the circle of 0.85 x 1.5 = 1.275 m round
the robot (dotted), the part of the plan TEB keeps (dark), up to the first pose outside the circle, and the local goal
(orange cross) with its heading (arrow) from the plan's next pieces. Run -> plan_cut.png"""
import math
from pathlib import Path

import bandkit as bk
import numpy as np
import plotly.graph_objects as go
import roomdraw as rd
import tebkit as tk
from gifkit import BLUE, FONT, GREY, ORANGE

here = Path(__file__).parent
c = tk.results()["person"][24]
x, tp, g = c["x"], c["tplan"], c["goal"]
dist = float(np.hypot(*(g[:2] - x[:2])))
assert round(c["t"], 1) == 2.4 and len(tp) == 32 and round(dist, 2) == 1.29 and round(math.degrees(g[2])) == 90

fig = go.Figure()
rd.room(fig)
plan = c["plan"]
fig.add_trace(go.Scatter(x=plan[:, 0], y=plan[:, 1], mode="lines+markers", line=dict(color=GREY, width=2, dash="dash"),
                         marker=dict(size=4, color=GREY)))
fig.add_trace(go.Scatter(x=tp[:, 0], y=tp[:, 1], mode="lines+markers", line=dict(color="#333333", width=4),
                         marker=dict(size=6, color="#333333")))
ox, oy = c["cm"]["origin"]
s = tk.COSTMAP_SIZE
fig.add_trace(go.Scatter(x=[ox, ox + s, ox + s, ox, ox], y=[oy, oy, oy + s, oy + s, oy], mode="lines",
                         line=dict(color="#999999", width=2)))
t = np.linspace(0, 2 * math.pi, 120)
fig.add_trace(go.Scatter(x=x[0] + 1.275 * np.cos(t), y=x[1] + 1.275 * np.sin(t), mode="lines",
                         line=dict(color=BLUE, width=2, dash="dot")))
rd.robot(fig, *x, BLUE)
fig.add_trace(go.Scatter(x=[g[0]], y=[g[1]], mode="markers", marker=dict(symbol="x", size=20, color=ORANGE)))
fig.add_annotation(x=g[0] + 0.35 * math.cos(g[2]), y=g[1] + 0.35 * math.sin(g[2]), ax=g[0], ay=g[1], xref="x", yref="y",
                   axref="x", ayref="y", showarrow=True, arrowhead=2, arrowwidth=3, arrowcolor=ORANGE, text="")
fig.add_annotation(x=g[0] + 0.08, y=g[1] - 0.05, text=f"local goal<br>{dist:.2f} m away,<br>facing 90°", showarrow=False,
                   xanchor="left", font=dict(size=19, color=ORANGE), bgcolor="rgba(255,255,255,0.85)")
fig.add_annotation(x=x[0] - 1.0, y=x[1] + 0.35, text="1.275 m", showarrow=False, font=dict(size=19, color=BLUE),
                   bgcolor="rgba(255,255,255,0.85)")
fig.add_annotation(x=ox + 0.05, y=oy + s - 0.05, text="local costmap, 3 m × 3 m", showarrow=False, xanchor="left",
                   yanchor="top", font=dict(size=18, color="#777777"), bgcolor="rgba(255,255,255,0.85)")
fig.add_annotation(x=2.0, y=0.62, text="start", showarrow=False, font=dict(size=18, color="#555555"))
fig.add_annotation(x=3.05, y=2.1, text=f"kept: {len(tp)} poses", showarrow=False, xanchor="left",
                   font=dict(size=19, color="#333333"), bgcolor="rgba(255,255,255,0.85)")
rd.zoom(fig, (0.75, 4.6), (0.3, 4.25))
fig.update_layout(template="simple_white", font=FONT, width=820, height=840, showlegend=False,
                  margin=dict(l=10, r=10, t=10, b=10))
fig.write_image(here / "plan_cut.png")
