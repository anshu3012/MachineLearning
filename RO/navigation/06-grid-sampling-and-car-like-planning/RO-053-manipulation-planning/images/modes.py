"""Figure: the arm's C-space (joint 1 across, joint 2 up, each from -180 to 180 degrees; opposite edges are the same
angles) in the three stages of the task, each blocked configuration coloured by what it hits: grey the table or the
robot's top, green the bottle, orange the cup in the way. Transit with the cup at A: 49.4 percent free. Transfer, the cup held
under the hand: 42.3 percent free. Transit with the cup at B: 51.3 percent free. Black: home (90, 0); blue: the grasp
at A (34.0, -144.1); red: the placing at B (23.2, -67.0). Run -> modes.png"""
from pathlib import Path

from plotly.subplots import make_subplots

import armdraw as ad
import manip as m
from gifkit import BLUE, RED

here = Path(__file__).parent
GA = [s for s in m.ik(m.lid(m.A_X)) if not m.collide(*s, "transit A")[0]][0]
GB = [s for s in m.ik(m.lid(m.B_X)) if not m.collide(*s, "transit B")[0]][0]
FREE = {"transit A": 0.494, "transfer": 0.423, "transit B": 0.513}
TITLES = ["transit, cup standing at A", "transfer, cup held", "transit, cup standing at B"]
fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.07,
                    subplot_titles=[f"{t}<br>{100 * FREE[k]:.1f} percent free" for t, k in zip(TITLES, FREE)])
for col, mode in enumerate(FREE, start=1):
    C = ad.cspace(fig, mode, row=1, col=col)
    assert round((C == 0).mean(), 3) == FREE[mode]
    for q, c, t, pos in ((m.HOME, "black", "home", "top center"), (GA, BLUE, "grasp", "bottom center"),
                         (GB, RED, "place", "top center")):
        ad.point(fig, q, c, t, pos, row=1, col=col)
    ad.cs_axes(fig, row=1, col=col, ytitle=col == 1)
    fig.update_yaxes(scaleanchor=f"x{col if col > 1 else ''}", row=1, col=col)
for a in fig.layout.annotations:
    a.font = dict(size=20)
LX = [0.0, 0.10, 0.41, 0.65]                                    # legend swatch positions, spaced to the label lengths
for k, (lab, col) in enumerate((("free", "#FFFFFF"), ("collides with the table or the robot's top", ad.CS_COLORS[1]),
                                ("collides with the bottle", ad.CS_COLORS[2]), ("the cup in the way", ad.CS_COLORS[3]))):
    fig.add_shape(type="rect", xref="paper", yref="paper", x0=LX[k], x1=LX[k] + 0.025, y0=-0.335,
                  y1=-0.285, fillcolor=col, line=dict(color="black", width=1.5), opacity=1)
    fig.add_annotation(xref="paper", yref="paper", x=LX[k] + 0.03, y=-0.31, xanchor="left", yanchor="middle", text=lab,
                       showarrow=False, font=dict(size=17))
ad.layout(fig, 1500, 680, margin=dict(l=80, r=30, t=90, b=190))
fig.write_image(here / "modes.png")
