"""Step 2 on numbers, at 2.4 s: every lethal cell of the local costmap (grey squares; the person's 60 cells pink)
becomes a point obstacle, except the cells behind the robot and more than 1.5 m away (pale, dropped). Orange: the
band TEB picks in this cycle, after optimising; purple lines join each pose to the obstacle points its obstacle edges
use (the nearest on its left and on its right within 0.5 m, and any closer than 0.15 m). The closest pair is marked.
Run -> obstacles.png"""
import math
from pathlib import Path

import bandkit as bk
import numpy as np
import plotly.graph_objects as go
import roomdraw as rd
import tebkit as tk
from gifkit import BLUE, FONT, ORANGE, PURPLE

here = Path(__file__).parent
c = tk.results()["person"][24]
x, cells, ob = c["x"], c["cm"]["cells"], c["obst"]
pl = c["planner"]
b = pl["candidates"][pl["best"]]
idx, O = b.associate(ob)
dd = np.hypot(*(b.P[idx, :2] - O).T) - tk.R_ROBOT
j = int(np.argmin(dd))
d_ = cells - x[:2]
behind = ((d_ @ [math.cos(x[2]), math.sin(x[2])]) < 0) & (np.hypot(*d_.T) > 1.5)
pers = np.hypot(*(cells - bk.PERSON).T) <= bk.PERSON_R + 0.025
assert len(cells) == 590 and len(ob) == 534 and behind.sum() == 26 and pers.sum() == 60 and len(idx) == 28
assert round(float(dd[j]), 3) == 0.147

fig = go.Figure()
rd.room(fig, band=False)
for m, col in ((~behind & ~pers, "#888888"), (behind, "#DDDDDD"), (pers, "#C2185B")):
    fig.add_trace(go.Scatter(x=cells[m, 0], y=cells[m, 1], mode="markers", marker=dict(symbol="square", size=7, color=col)))
xs, ys = [], []
for i, o in zip(idx, O):
    xs += [b.P[i, 0], o[0], None]
    ys += [b.P[i, 1], o[1], None]
fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=PURPLE, width=2)))
rd.band(fig, b.P, ORANGE, size=8)
rd.robot(fig, *x, BLUE)
fig.add_annotation(x=bk.POLES[0][0], y=bk.POLES[0][1] + 0.22, text="pole", showarrow=False, font=dict(size=18, color="#555555"))
i = idx[j]
fig.add_annotation(x=(b.P[i, 0] + O[j, 0]) / 2, y=(b.P[i, 1] + O[j, 1]) / 2, ax=-190, ay=-10,
                   text=f"closest pair:<br>disk edge to cell {dd[j]:.3f} m", font=dict(size=18, color=PURPLE),
                   arrowcolor=PURPLE, arrowwidth=2, bgcolor="rgba(255,255,255,0.9)")
lines = [f"{len(cells)} lethal cells", f"<span style='color:#BBBBBB'>{int(behind.sum())} dropped: behind, over 1.5 m</span>",
         f"{len(ob)} point obstacles", f"<span style='color:#C2185B'>{int(pers.sum())} of them the person</span>",
         f"<span style='color:{PURPLE}'>{len(idx)} obstacle edges</span>"]
fig.add_annotation(x=0.95, y=0.45, text="<br>".join(lines), showarrow=False, xanchor="left", yanchor="bottom",
                   align="left", font=dict(size=19), bgcolor="rgba(255,255,255,0.9)")
rd.zoom(fig, (0.75, 3.85), (0.35, 3.6))
fig.update_layout(template="simple_white", font=FONT, width=820, height=840, showlegend=False,
                  margin=dict(l=10, r=10, t=10, b=10))
fig.write_image(here / "obstacles.png")
