"""Why one bell curve cannot hold the belief: the exact belief after the second reading (from a fine grid) has two
bumps, at door 2 and door 3. The single normal curve with the same mean and standard deviation peaks at 5.73 m,
in front of plain wall, where the reading says the robot cannot be.
Run: python gaussian_fails.py -> gaussian_fails.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, ORANGE, RED
from pfsim import DOORS, grid_belief

here = Path(__file__).parent
xs, _, bels = grid_belief()
dx = xs[1] - xs[0]
bel = bels[1]
m = np.sum(xs * bel) * dx
s = np.sqrt(np.sum((xs - m) ** 2 * bel) * dx)
assert abs(m - 5.73) < 0.01 and abs(s - 1.31) < 0.01, (m, s)
gauss = np.exp(-0.5 * ((xs - m) / s) ** 2) / (s * np.sqrt(2 * np.pi))

fig = go.Figure()
for a, b in DOORS:
    fig.add_vrect(x0=a, x1=b, fillcolor=ORANGE, opacity=0.15, line_width=0)
fig.add_trace(go.Scatter(x=xs, y=bel, mode="lines", line=dict(color=BLUE, width=4), name="exact belief: two bumps"))
fig.add_trace(go.Scatter(x=xs, y=gauss, mode="lines", line=dict(color=RED, width=4, dash="dash"),
                         name="one normal curve, same mean and spread"))
fig.add_vline(x=m, line=dict(color=RED, width=2, dash="dot"))
fig.add_annotation(x=m, y=0.62, text=f"its peak: {m:.2f} m,<br>in front of plain wall", showarrow=False,
                   font=dict(size=19, color=RED), yanchor="bottom")
for c, t in ((2, "door 1"), (4.5, "door 2"), (7, "door 3")):
    fig.add_annotation(x=c, y=-0.06, text=t, showarrow=False, font=dict(size=17, color=ORANGE))
fig.update_layout(template="simple_white", font=FONT, width=1000, height=560, margin=dict(l=80, r=30, t=120, b=70),
                  title=dict(x=0.5, y=0.97, text="belief after the second reading (doors shaded)"),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=1.02, yanchor="bottom", font=dict(size=18)),
                  xaxis=dict(title="position x (m)", range=[0, 10], dtick=1),
                  yaxis=dict(title="belief density (per m)", range=[-0.1, 0.8]))
fig.write_image(here / "gaussian_fails.png")
