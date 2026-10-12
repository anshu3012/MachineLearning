"""Figure: the cup holder at B. Left, the room (side view): two posts 1.5 cm thick and 2 cm tall with 1 cm chamfers,
7 cm apart at the bottom, and the 6 cm cup above them. Right, the same in the cup's C-space: the cup becomes the point
at the middle of its bottom, every obstacle grows by the cup's shape (RO-037's Minkowski sum), and the holder becomes
a slot 1 cm wide whose chamfers widen to a mouth 3 cm wide. Run -> holder_fig.png"""
from pathlib import Path

import plotly.graph_objects as go
from plotly.subplots import make_subplots

import armdraw as ad
import holder as H
import manip as m
from gifkit import FONT, ORANGE, PURPLE

here = Path(__file__).parent
left, right = H.posts()
assert round(H.GOAL_HALF * 2, 3) == 0.01
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1,
                    subplot_titles=["the holder and the cup", "the cup's C-space: the cup is a point"])
for col in (1, 2):
    ad.poly(fig, m.box(0.30, -0.13, 0.55, m.TOP), ad.TABLE_FILL, ad.TABLE_LINE, row=1, col=col)
ad.poly(fig, m.bottle(), ad.BOTTLE_FILL, ad.BOTTLE_LINE, row=1, col=1)
for p in (left, right):
    ad.poly(fig, p, "#C9B3D6", PURPLE, row=1, col=1)
ad.poly(fig, m.cup_at(H.B, H.TOP + 0.05), ad.CUP_FILL, ad.CUP_LINE, row=1, col=1)
fig.add_trace(go.Scatter(x=[H.B], y=[H.TOP + 0.05], mode="markers", marker=dict(size=10, color="black")), row=1, col=1)
O = H.O.intersection(m.box(0.30, -0.13, 0.55, 0.10))
for g in getattr(O, "geoms", [O]):
    ad.poly(fig, g, "rgba(245,133,24,0.28)", ORANGE, row=1, col=2)
fig.add_trace(go.Scatter(x=[H.B], y=[H.TOP + 0.05], mode="markers", marker=dict(size=12, color="black")), row=1, col=2)
notes = [(1, H.B, H.TOP - 0.018, "gap 7 cm, cup 6 cm"), (2, H.B, H.TOP - 0.018, "slot 1 cm"),
         (2, H.B, H.MOUTH + 0.009, "mouth 3 cm"), (1, 0.33, 0.055, "bottle"), (2, 0.33, 0.055, "grown bottle")]
for col, x, y, t in notes:
    fig.add_trace(go.Scatter(x=[x], y=[y], mode="text", text=[t], textfont=dict(size=17)), row=1, col=col)
for col in (1, 2):
    fig.update_xaxes(range=[0.30, 0.51], dtick=0.05, title="x (m)", showgrid=False, row=1, col=col, constrain="domain")
    fig.update_yaxes(range=[-0.13, 0.07], dtick=0.05, title="y (m)" if col == 1 else None, showgrid=False,
                     row=1, col=col, scaleanchor="x" if col == 1 else "x2", constrain="domain")
fig.update_layout(template="simple_white", width=1400, height=700, font=FONT, showlegend=False,
                  margin=dict(l=80, r=30, t=70, b=60))
for a in fig.layout.annotations:
    a.font = dict(size=20)
fig.write_image(here / "holder_fig.png")
