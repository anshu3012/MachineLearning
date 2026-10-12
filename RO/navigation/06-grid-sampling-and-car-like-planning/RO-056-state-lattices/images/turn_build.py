"""How a 45 deg turn is made to end exactly on a lattice point: from (0, 0) facing 0 deg, a straight piece of 0.929 m,
an arc of 45 deg on the 5 m circle (3.927 m), and a straight piece of 0.757 m along 45 deg end on (5, 2) facing
45 deg. The arc alone would end at (3.536, 1.464), between lattice points. Run -> turn_build.png"""
import math
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from carpaths import sample
from gifkit import BLUE, GREY, ORANGE, RED
from latticekit import turn_piece
from lotdraw import FONT

here = Path(__file__).parent
a, b, end = turn_piece(0, 1)
assert end == (5, 2) and round(a, 3) == 0.929 and round(b, 3) == 0.757
arc_only = sample((0, 0, 0), [("L", math.pi / 4 * 5)], 5)
full = sample((0, 0, 0), [("S", a), ("L", math.pi / 4 * 5), ("S", b)], 5)
assert np.allclose(arc_only[-1, :2], [3.5355, 1.4645], atol=1e-4)
fig = go.Figure()
gx, gy = np.meshgrid(np.arange(0, 7), np.arange(-1, 4))
fig.add_trace(go.Scatter(x=gx.ravel(), y=gy.ravel(), mode="markers", marker=dict(color=GREY, size=9), hoverinfo="skip"))
fig.add_trace(go.Scatter(x=arc_only[:, 0], y=arc_only[:, 1], mode="lines", line=dict(color=RED, width=3, dash="dash"),
                         hoverinfo="skip"))
n1 = int(round(a / 0.02))
seg1, seg2, seg3 = full[:n1 + 1], full[n1:n1 + 197], full[n1 + 196:]
for seg, col in ((seg1, ORANGE), (seg2, BLUE), (seg3, ORANGE)):
    fig.add_trace(go.Scatter(x=seg[:, 0], y=seg[:, 1], mode="lines", line=dict(color=col, width=6), hoverinfo="skip"))
fig.add_trace(go.Scatter(x=[5, 5 + 0.8 * math.cos(math.pi / 4)], y=[2, 2 + 0.8 * math.sin(math.pi / 4)], mode="lines",
                         line=dict(color="black", width=4), hoverinfo="skip"))
for x, y, t, pos in ((0.45, -0.35, "straight 0.929 m", "middle center"), (2.5, -0.5, "arc of 45 deg, 3.927 m", "middle right"),
                     (4.65, 2.55, "straight 0.757 m", "middle left"), (5.1, 1.75, "ends on (5, 2), 45 deg", "middle right"),
                     (0.05, 1.55, "the arc alone ends at (3.536, 1.464)", "middle right"), (0, 0.35, "start (0, 0), 0 deg", "middle right")):
    fig.add_trace(go.Scatter(x=[x], y=[y], mode="text", text=[t], textposition=pos, hoverinfo="skip",
                             textfont=dict(size=16, color="black")))
fig.update_layout(template="simple_white", width=900, height=520, showlegend=False, font=FONT,
                  title=dict(text="a 45 deg turn that ends on a lattice point", x=0.5, xanchor="center", font_size=22),
                  margin=dict(l=30, r=30, t=70, b=30))
fig.update_xaxes(range=[-0.5, 7.6], showgrid=False, zeroline=False, tickvals=list(range(0, 8)), tickfont=dict(size=15))
fig.update_yaxes(range=[-1.2, 3.6], showgrid=False, zeroline=False, scaleanchor="x", tickvals=list(range(-1, 4)),
                 tickfont=dict(size=15))
fig.write_image(here / "turn_build.png")
