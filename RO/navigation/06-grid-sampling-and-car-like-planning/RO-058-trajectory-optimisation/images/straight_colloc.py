"""Collocation checked on the straight drive, whose least time is known: 6.2 s (speed up at 0.5 m/s^2 to 0.6 m/s,
cruise, brake). The speed at the knot points of the least-time collocation with 10, 20 and 40 intervals, against
the exact profile (grey). The times: 6.364, 6.239 and 6.209 s; more knots, closer to 6.2 s. Run ->
straight_colloc.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import trajkit as tk
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE

here = Path(__file__).parent
T_exact = tk.bang_coast_bang()
assert round(T_exact, 3) == 6.2
fig = go.Figure()
fig.add_trace(go.Scatter(x=[0, 1.2, 5.0, 6.2], y=[0, 0.6, 0.6, 0], mode="lines", line=dict(color=GREY, width=6),
                         name="exact: 6.2 s"))
Ts = []
for N, col in ((10, ORANGE), (20, GREEN), (40, BLUE)):
    r = tk.straight_collocation(N=N)
    Ts.append(round(r["T"], 3))
    t = np.linspace(0, r["T"], N + 1)
    fig.add_trace(go.Scatter(x=t, y=r["v"], mode="lines+markers", line=dict(color=col, width=2),
                             marker=dict(size=8, color=col), name=f"{N} intervals: {r['T']:.3f} s"))
assert Ts == [6.364, 6.239, 6.209], Ts
fig.update_xaxes(title="time (s)", range=[0, 6.6])
fig.update_yaxes(title="speed v (m/s)", range=[0, 0.75])
fig.update_layout(template="simple_white", font=FONT, width=1000, height=600,
                  legend=dict(x=0.32, y=0.25, font_size=19, bgcolor="rgba(255,255,255,0.9)"),
                  margin=dict(l=80, r=20, t=20, b=60))
fig.write_image(here / "straight_colloc.png", scale=2)
