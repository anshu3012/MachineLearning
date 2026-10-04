"""Xavier normal and Xavier uniform for a layer with fan-in 250 and fan-out 250: 62,500 weights each (seed 0). Normal:
standard deviation sqrt(2/500) = 0.063. Uniform: between -0.110 and 0.110. Same variance 0.004, different shape.
Plotly."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

from common import BLUE, ORANGE

HERE = Path(__file__).parent
rng = np.random.default_rng(0)
s, L = np.sqrt(2 / 500), np.sqrt(6 / 500)
Wn = rng.standard_normal((250, 250)) * s
Wu = rng.uniform(-L, L, (250, 250))
assert round(s, 3) == 0.063 and round(L, 3) == 0.110
assert abs(Wn.var() - 0.004) < 0.0002 and abs(Wu.var() - 0.004) < 0.0002
fig = go.Figure()
for W, col, name in ((Wn, BLUE, f"Xavier normal: σ = {s:.3f}, variance {Wn.var():.4f}"),
                     (Wu, ORANGE, f"Xavier uniform: from −{L:.3f} to {L:.3f}, variance {Wu.var():.4f}")):
    fig.add_histogram(x=W.ravel(), xbins=dict(start=-0.3, end=0.3, size=0.005), name=name, marker_color=col,
                      opacity=0.6)
fig.update_layout(template="simple_white", barmode="overlay", width=1100, height=520,
                  font=dict(family="Latin Modern Roman", size=20),
                  title=dict(text="62,500 starting weights of a 250 × 250 layer", x=0.5),
                  xaxis=dict(title="starting weight", range=[-0.25, 0.25]), yaxis=dict(title="count"),
                  legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.85)", font=dict(size=17)), margin=dict(l=80, r=30, t=70, b=80))
fig.write_image(HERE / "xavier_shapes.png", scale=2)
