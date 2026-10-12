"""Stanley's cross-track gain per metre of lateral error against speed: k / v without a softening speed and
k / (ks + v) with ks = 1 m/s, for k = 1 per s. Without it the gain grows without limit as the car slows (2 per m at
0.5 m/s); with it, it never exceeds 1 per m (0.667 per m at 0.5 m/s).
Run: python softening.py -> softening.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

from gifkit import BLUE, FONT, RED

here = Path(__file__).parent
K, KS = 1.0, 1.0
v = np.linspace(0.05, 6, 600)
raw, soft = K / v, K / (KS + v)
assert abs(np.interp(0.5, v, raw) - 2.0) < 1e-2 and abs(np.interp(0.5, v, soft) - 0.6667) < 1e-3

fig = go.Figure()
fig.add_trace(go.Scatter(x=v, y=raw, mode="lines", line=dict(color=RED, width=4), name="k / v: no softening"))
fig.add_trace(go.Scatter(x=v, y=soft, mode="lines", line=dict(color=BLUE, width=4),
                         name="k / (1 m/s + v): softening speed 1 m/s"))
fig.add_trace(go.Scatter(x=[0.5, 0.5], y=[2.0, 0.6667], mode="markers+text", marker=dict(size=13, color=[RED, BLUE]),
                         text=["2 per m at 0.5 m/s", ""], textposition=["middle right", "bottom right"],
                         textfont=dict(size=19), showlegend=False))
fig.add_annotation(x=0.5, y=0.6667, ax=1.3, ay=0.1, axref="x", ayref="y", text="0.667 per m at 0.5 m/s",
                   showarrow=True, arrowhead=2, arrowcolor=BLUE, font=dict(size=19, color=BLUE), xanchor="left")
fig.update_layout(template="simple_white", font=FONT, width=900, height=600, margin=dict(l=90, r=30, t=60, b=80),
                  title=dict(x=0.5, text="Stanley's gain on the lateral error, against speed (k = 1 per s)"),
                  legend=dict(x=0.45, y=0.95, font=dict(size=19), bgcolor="rgba(255,255,255,0.85)"),
                  xaxis=dict(title="speed (m/s)", range=[0, 6], dtick=1),
                  yaxis=dict(title="gain on the lateral error (per m)", range=[0, 4], dtick=0.5))
fig.write_image(here / "softening.png")
