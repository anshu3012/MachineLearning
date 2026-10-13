"""The speeds our robot can drive and the speeds TEB is told it may drive, in the (forward speed v, turn rate omega)
plane. Our robot: each wheel at most 0.6 m/s, wheels 0.2 m apart, so |v| + 0.1 |omega| <= 0.6: a diamond. TEB:
two separate limits, max_vel_x and max_vel_theta: a box. Grey: TEB's defaults (0.4 m/s, 0.3 rad/s); orange: our
setting (0.5 m/s, 1.0 rad/s), whose corner touches the diamond. Run -> box_diamond.png"""
from pathlib import Path

import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, ORANGE

here = Path(__file__).parent
VW, HALF = 0.6, 0.1                                   # wheel limit (m/s), half the wheel separation (m)
assert abs(0.5 + 1.0 * HALF - VW) < 1e-12              # our box's corner lies on the diamond

fig = go.Figure()
fig.add_trace(go.Scatter(x=[0, VW, 0, -VW, 0], y=[VW / HALF, 0, -VW / HALF, 0, VW / HALF], fill="toself",
                         fillcolor="rgba(76,120,168,0.12)", line=dict(color=BLUE, width=3), name="our wheels"))
for (v, w), col, name in (((0.4, 0.3), GREY, "TEB defaults"), ((0.5, 1.0), ORANGE, "our TEB setting")):
    fig.add_trace(go.Scatter(x=[-0.2, v, v, -0.2, -0.2], y=[-w, -w, w, w, -w], line=dict(color=col, width=3,
                             dash="dash" if col == GREY else "solid"), name=name, mode="lines"))
fig.add_annotation(x=0.5, y=1.0, ax=70, ay=-60, text="(0.5 m/s, 1.0 rad/s)<br>0.5 + 1.0 × 0.1 = 0.6", font=dict(
    size=20, color=ORANGE), arrowcolor=ORANGE, arrowwidth=2)
fig.add_annotation(x=0.0, y=6.0, ax=160, ay=50, xanchor="left", text="spin on the spot: 6 rad/s", font=dict(size=20, color=BLUE),
                   arrowcolor=BLUE, arrowwidth=2)
fig.add_annotation(x=0.6, y=0.0, ax=40, ay=60, text="straight: 0.6 m/s", font=dict(size=20, color=BLUE),
                   arrowcolor=BLUE, arrowwidth=2)
fig.update_xaxes(title="forward speed v (m/s)", range=[-0.75, 0.9], zeroline=True, zerolinecolor="#BBBBBB")
fig.update_yaxes(title="turn rate ω (rad/s)", range=[-6.6, 6.9], zeroline=True, zerolinecolor="#BBBBBB")
fig.update_layout(template="simple_white", font=FONT, width=900, height=720, margin=dict(l=90, r=20, t=20, b=80),
                  legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.9)"))
fig.write_image(here / "box_diamond.png", scale=1)
