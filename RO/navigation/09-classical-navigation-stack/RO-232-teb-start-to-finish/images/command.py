"""Step 7 on numbers, at 2.4 s: the feasibility check and the command. Orange: the band TEB picked. Blue circles: the
robot's disk at poses 0 to 5, the poses isTrajectoryFeasible checks against the lethal cells (grey; the person's
pink); each is clear, so the band is kept. The arrow is the band's first piece, 0.0906 m in 0.2551 s, which gives the
command. Run -> command.png"""
import math
from pathlib import Path

import bandkit as bk
import numpy as np
import plotly.graph_objects as go
import roomdraw as rd
import tebkit as tk
from gifkit import BLUE, FONT, ORANGE

here = Path(__file__).parent
c = tk.results()["person"][24]
pl = c["planner"]
b = pl["candidates"][pl["best"]]
cells = c["cm"]["cells"]
gaps = [float(np.min(np.hypot(*(cells - b.P[i, :2]).T)) - tk.R_ROBOT) for i in range(6)]
d0, dt0 = float(np.hypot(*(b.P[1, :2] - b.P[0, :2]))), float(b.DT[0])
dth = float(tk.wrap(b.P[1, 2] - b.P[0, 2]))
assert c["feasible"] and round(d0, 4) == 0.0906 and round(dt0, 4) == 0.2551 and round(min(gaps), 3) == 0.414
assert np.allclose(c["cmd"], (d0 / dt0, dth / dt0), atol=1e-9)

fig = go.Figure()
rd.room(fig, band=False)
pers = np.hypot(*(cells - bk.PERSON).T) <= bk.PERSON_R + 0.025
for m, col in ((~pers, "#AAAAAA"), (pers, "#C2185B")):
    fig.add_trace(go.Scatter(x=cells[m, 0], y=cells[m, 1], mode="markers", marker=dict(symbol="square", size=7, color=col)))
rd.band(fig, b.P, ORANGE, size=7)
t = np.linspace(0, 2 * math.pi, 60)
for i in range(6):
    fig.add_trace(go.Scatter(x=b.P[i, 0] + tk.R_ROBOT * np.cos(t), y=b.P[i, 1] + tk.R_ROBOT * np.sin(t), mode="lines",
                             line=dict(color=BLUE, width=1.5 if i else 3)))
fig.add_annotation(x=b.P[1, 0], y=b.P[1, 1], ax=b.P[0, 0], ay=b.P[0, 1], xref="x", yref="y", axref="x", ayref="y",
                   showarrow=True, arrowhead=2, arrowwidth=4, arrowcolor="#333333", text="")
first5 = float(np.sum(np.hypot(*np.diff(b.P[:6, :2], axis=0).T)))
assert round(first5, 3) == 0.176
lines = ["<b>t = 2.4 s</b>: poses 0 to 5 checked, all clear",
         f"(they lie within {first5:.3f} m, so the disks overlap);",
         f"closest gap to a lethal cell {min(gaps):.3f} m",
         f"first piece: {d0:.4f} m in {dt0:.4f} s",
         f"v = {d0 / dt0:.4f} m/s, ω = {dth / dt0:.4f} rad/s",
         "both inside 0.5 m/s and 1.0 rad/s: sent as they are"]
fig.add_annotation(x=1.45, y=3.55, text="<br>".join(lines), showarrow=False, xanchor="left", yanchor="top", align="left",
                   font=dict(size=19), bgcolor="rgba(255,255,255,0.92)")
rd.zoom(fig, (1.4, 3.6), (1.35, 3.6))
fig.update_layout(template="simple_white", font=FONT, width=760, height=780, showlegend=False,
                  margin=dict(l=10, r=10, t=10, b=10))
fig.write_image(here / "command.png")
print("gaps", [round(g, 3) for g in gaps])
