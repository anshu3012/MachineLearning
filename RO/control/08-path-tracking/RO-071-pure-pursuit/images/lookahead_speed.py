"""Look-ahead distance against speed. Ours: ld = v x 2 s, kept between 2 and 10 m, so 4 m at 2 m/s and 10 m at 5 m/s.
Autoware's pure pursuit (pure_pursuit.param.yaml): 2.4 s times the speed, minus 120 m^2 times the path curvature, kept
between 4.35 and 15 m; drawn on a straight and on our 10 m arc (curvature 0.1 per m, so 12 m less).
Run: python lookahead_speed.py -> lookahead_speed.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

from gifkit import BLUE, FONT, GREY, ORANGE

here = Path(__file__).parent
v = np.linspace(0, 10, 401)
ours = np.clip(2.0 * v, 2.0, 10.0)
aw_straight = np.clip(2.4 * v, 4.35, 15.0)
aw_arc = np.clip(2.4 * v - 120 * 0.1, 4.35, 15.0)
assert np.interp(2, v, ours) == 4 and np.interp(5, v, ours) == 10
assert abs(np.interp(5, v, aw_straight) - 12) < 1e-9 and abs(np.interp(5, v, aw_arc) - 4.35) < 1e-9

fig = go.Figure()
fig.add_trace(go.Scatter(x=v, y=ours, mode="lines", line=dict(color=BLUE, width=4),
                         name="ours: speed × 2 s, from 2 to 10 m"))
fig.add_trace(go.Scatter(x=v, y=aw_straight, mode="lines", line=dict(color=ORANGE, width=4),
                         name="Autoware, straight: speed × 2.4 s, from 4.35 to 15 m"))
fig.add_trace(go.Scatter(x=v, y=aw_arc, mode="lines", line=dict(color=ORANGE, width=4, dash="dash"),
                         name="Autoware, on our 10 m arc: 12 m less"))
fig.add_trace(go.Scatter(x=[2, 5], y=[4, 10], mode="markers+text", marker=dict(color=BLUE, size=14),
                         text=["4 m at 2 m/s", "10 m at 5 m/s"], textposition=["bottom right", "top left"],
                         textfont=dict(size=19, color=BLUE), showlegend=False))
fig.update_layout(template="simple_white", font=FONT, width=900, height=640, margin=dict(l=90, r=30, t=60, b=80),
                  title=dict(x=0.5, text="look-ahead distance against speed"),
                  legend=dict(x=0.02, y=0.98, font=dict(size=18), bgcolor="rgba(255,255,255,0.85)"),
                  xaxis=dict(title="speed (m/s)", range=[0, 10], dtick=1),
                  yaxis=dict(title="look-ahead distance (m)", range=[0, 16], dtick=2))
fig.write_image(here / "lookahead_speed.png")
