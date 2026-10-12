"""Figure: where the three motion primitives come from: every pair (forward speed v,
turn rate omega) it can produce with each wheel at most 0.6 m/s: a diamond with corners at v = +-0.6 m/s (both wheels
at full speed) and omega = +-6 rad/s (spinning on the spot). At the cruising speed v = 0.5 m/s only turn rates from
-1 to +1 rad/s remain (green segment); the three primitives take its two ends and its middle. Run -> controls.png (and controls.html)"""
import math
from pathlib import Path

import plotly.graph_objects as go
from plotly.subplots import make_subplots

import drawkit as k
import motionkit as m
from gifkit import BLUE, GREEN, ORANGE, PURPLE

here = Path(__file__).parent
COL = {"left": BLUE, "straight": GREEN, "right": PURPLE}
wmax_spin = 2 * m.V_WHEEL / m.L_AXLE
assert round(wmax_spin, 6) == 6 and round(m.W_MAX, 6) == 1
assert round(math.degrees(m.W_MAX * m.DT_PRIM)) == 43 and round(m.V_CRUISE * m.DT_PRIM, 3) == 0.375

fig = make_subplots(rows=1, cols=1, subplot_titles=["every (v, ω) the wheels allow"])
dx, dy = [0.6, 0, -0.6, 0, 0.6], [0, wmax_spin, 0, -wmax_spin, 0]
fig.add_trace(k.poly_trace(dx, dy, "rgba(76,120,168,0.12)", BLUE, 2), row=1, col=1)
fig.add_trace(go.Scatter(x=[0.5, 0.5], y=[-1, 1], mode="lines", line=dict(color=GREEN, width=6), hoverinfo="skip"),
              row=1, col=1)
for name, om in m.PRIMS.items():
    k.point(fig, 0.5, om, COL[name], size=16, row=1, col=1)
    k.text(fig, 0.64, om + 0.25 * (om > 0) - 0.25 * (om < 0), name, color=COL[name], size=17, row=1, col=1,
           xanchor="left", bg="rgba(0,0,0,0)")
k.text(fig, 0.0, 6.35, "spin on the spot: ω = 6 rad/s", size=16, row=1, col=1)
fig.add_annotation(x=-0.6, y=0, ax=-10, ay=-90, text="full speed back", showarrow=True, arrowhead=2, arrowwidth=1.5,
                   font=dict(size=16), bgcolor="white", row=1, col=1)
k.text(fig, 0.33, -2.6, "at v = 0.5 m/s:<br>ω from −1 to 1 rad/s", color=GREEN, size=17, row=1, col=1)
fig.update_xaxes(range=[-0.95, 0.95], dtick=0.2, title="forward speed v (m/s)", zeroline=True, showgrid=False,
                 row=1, col=1)
fig.update_yaxes(range=[-6.8, 7.0], dtick=2, title="turn rate ω (rad/s)", zeroline=True, showgrid=False,
                 row=1, col=1)
k.layout(fig, 900, 640, None, margin=dict(l=80, r=30, t=60, b=70))
for s in ("every (v, ω) the wheels allow",):
    fig.update_annotations(font_size=20, selector=dict(text=s))
fig.write_image(here / "controls.png", scale=2)
