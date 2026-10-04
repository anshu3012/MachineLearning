"""Section 2: the Note's 5 observations in the plane of the two features, numbered as in the table, coloured by y.
Run: python toy_data.py  -> toy_data.png (Plotly)"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

HERE = Path(__file__).parent
X = np.array([[3, 7], [2, 9], [1, 9], [9, 8], [7, 4]])        # the Note's table
y = np.array([1, 1, -1, -1, -1])
# the Note's claim: no single cut on x1 or x2 separates the classes (every threshold, both directions)
assert not any(((X[:, f] > c) * 2 - 1 == s * y).all() for f in (0, 1) for c in np.arange(0.5, 10, 0.5) for s in (1, -1))
fig = go.Figure()
for cls, c, name in ((1, "#4C78A8", "y = +1"), (-1, "#F58518", "y = −1")):
    m = y == cls
    fig.add_trace(go.Scatter(x=X[m, 0], y=X[m, 1], mode="markers+text", name=name, text=[f"{i}" for i in np.where(m)[0] + 1],
                             textposition="middle center", textfont=dict(color="white", size=20),
                             marker=dict(color=c, size=38, line=dict(color="white", width=1))))
fig.update_layout(template="simple_white", width=760, height=560, font=dict(family="Latin Modern Roman", size=22),
                  xaxis=dict(title="x1", range=[0, 10], dtick=1), yaxis=dict(title="x2", range=[3, 10], dtick=1),
                  legend=dict(x=0.02, y=0.02, bgcolor="rgba(255,255,255,0.8)"), margin=dict(l=60, r=20, t=20, b=60))
fig.write_image(HERE / "toy_data.png", scale=2)
fig.write_image(HERE / "toy_data.pdf")
