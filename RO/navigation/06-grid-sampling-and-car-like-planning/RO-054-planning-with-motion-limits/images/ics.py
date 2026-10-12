"""Figure: the phase plane of the straight drive with its two kinds of forbidden states. Dark red: the door, every
state with s >= 3.117 m, at any speed (the obstacle region in phase space). Orange: the region of inevitable
collision, every state with s + v^2 / (2 a) > 3.117 m, which needs more room to stop than it has; its edge is the
braking curve that just touches the door. Its width is the stopping distance: 0.04 m at 0.2 m/s, 0.16 m at 0.4 m/s,
0.36 m at 0.6 m/s, growing with the square of the speed. Robot A (2.8 m, 0.3 m/s) is outside, robot B (2.8 m,
0.6 m/s) inside. Run -> ics.png (and ics.html)"""
from pathlib import Path

import numpy as np

import drawkit as k
import motionkit as m
from gifkit import GREEN, ORANGE, PURPLE
import plotly.graph_objects as go

here = Path(__file__).parent
fig = go.Figure()
k.phase_regions(fig)
for name, v0, col in (("A", 0.3, GREEN), ("B", 0.6, PURPLE)):
    t, s, v = m.brake_run(2.8, v0)
    k.line(fig, s, v, color=col, width=3, dash="dash")
    k.point(fig, 2.8, v0, col, size=16)
    k.text(fig, 2.76, v0 - 0.035, f"{name}: 0.{int(v0 * 10)} m/s", color=col, size=18, xanchor="right",
           bg="rgba(0,0,0,0)")
widths = {}
for v in (0.2, 0.4, 0.6):
    w = m.stopping_distance(v)
    widths[v] = w
    s0 = m.S_DOOR - w
    fig.add_trace(go.Scatter(x=[s0, m.S_DOOR], y=[v, v], mode="lines+markers", line=dict(color="black", width=2),
                             marker=dict(symbol="line-ns", size=12, line=dict(width=2, color="black")),
                             hoverinfo="skip"))
    k.text(fig, s0 - 0.07, v + 0.02, f"{w:.2f} m to stop", size=17, xanchor="right", bg="rgba(0,0,0,0)")
assert [round(w, 2) for w in widths.values()] == [0.04, 0.16, 0.36]
assert m.inevitable(2.8, 0.6) and not m.inevitable(2.8, 0.3)
k.text(fig, (m.S_DOOR + k.S_MAX) / 2, 0.45, "door:<br>s ≥ 3.117 m", color=k.DOOR, size=18)
k.text(fig, 2.35, 0.135, "free: the robot can still stop", size=18, color="#333333", bg="rgba(255,255,255,0.8)")
k.text(fig, 2.93, 0.66, "inevitable collision", color="#B35806", size=18, bg="rgba(0,0,0,0)")
k.text(fig, 2.3, m.V_TOP + 0.03, "top speed 0.6 m/s", color="#6B6B6B", size=16)
k.phase_axes(fig, xr=(2.0, k.S_MAX))
k.layout(fig, 1000, 640, "the phase plane near the closed door", margin=dict(l=80, r=30, t=70, b=70))
fig.write_image(here / "ics.png", scale=2)
