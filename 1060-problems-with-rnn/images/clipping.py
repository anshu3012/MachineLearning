"""Gradient clipping by norm (section 6.2): a gradient longer than the threshold is scaled down to the threshold,
keeping its direction. Example: g = (3, 4), norm 5, threshold 1 -> (0.6, 0.8). Plotly."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from common import BLUE, RED, GREY, FONT

here = Path(__file__).parent
g = np.array([3.0, 4.0])
c = 1.0
clipped = g * c / np.linalg.norm(g)
assert np.linalg.norm(g) == 5 and np.allclose(clipped, [0.6, 0.8])
th = np.linspace(0, 2 * np.pi, 200)
fig = go.Figure()
fig.add_scatter(x=c * np.cos(th), y=c * np.sin(th), mode="lines", line=dict(color=GREY, dash="dash", width=2),
                fill="toself", fillcolor="rgba(107,107,107,0.08)", name="threshold: norm 1")
for v, col, txt in ((g, RED, "gradient g = (3, 4), norm 5"), (clipped, BLUE, "clipped: g x 1/5 = (0.6, 0.8), norm 1")):
    fig.add_annotation(x=v[0], y=v[1], ax=0, ay=0, xref="x", yref="y", axref="x", ayref="y", showarrow=True,
                       arrowhead=2, arrowsize=1.5, arrowwidth=4, arrowcolor=col, text="")
    fig.add_annotation(x=v[0], y=v[1], text=txt, showarrow=False, xanchor="left", xshift=12, font=dict(size=19, color=col))
fig.update_layout(template="simple_white", width=900, height=620, font=dict(FONT, size=20),
                  xaxis=dict(range=[-1.5, 6.8], title="gradient component 1", zeroline=True),
                  yaxis=dict(range=[-1.3, 4.6], title="gradient component 2", scaleanchor="x", zeroline=True),
                  legend=dict(x=0.6, y=0.08), margin=dict(l=70, r=20, t=20, b=70))
fig.write_image(here / "clipping.png", scale=2)
fig.write_image(here / "clipping.pdf")
