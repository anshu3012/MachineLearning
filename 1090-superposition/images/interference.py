"""Section 3's formula on a small example of our own: two features, both active with strength 1 (x1 = x2 = 1),
h = f1 + f2. Reading feature 1 with h . f1 gives x1 plus a leak x2 (f1 . f2). Left: perpendicular directions, the
reading is exactly 1. Right: directions 80 degrees apart, the reading is 1 + cos 80 = 1.17. Plotly."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, PURPLE, RED, GREY, FONT

here = Path(__file__).parent
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08,
                    subplot_titles=("perpendicular: h · f1 = 1 (no leak)", "80 degrees apart: h · f1 = 1.17 (leak 0.17)"))
for col, ang in ((1, 90), (2, 80)):
    f1 = np.array([1.0, 0.0])
    f2 = np.array([np.cos(np.radians(ang)), np.sin(np.radians(ang))])
    h = f1 + f2
    read = h @ f1
    assert abs(read - (1 + f1 @ f2)) < 1e-12
    xa, ya = ("x", "y") if col == 1 else ("x2", "y2")
    for v, c, name, w in ((f1, BLUE, "f1", 4), (f2, ORANGE, "f2", 4), (h, PURPLE, "h = f1 + f2", 5)):
        fig.add_annotation(x=v[0], y=v[1], ax=0, ay=0, xref=xa, yref=ya, axref=xa, ayref=ya, showarrow=True,
                           arrowhead=2, arrowwidth=w, arrowcolor=c, text="")
        fig.add_annotation(x=v[0], y=v[1], xref=xa, yref=ya, text=name, showarrow=False, xshift=30 if name != "f2" else -18,
                           yshift=10, font=dict(size=18, color=c))
    fig.add_scatter(x=[h[0], read], y=[h[1], 0], mode="lines", line=dict(color=GREY, dash="dash", width=2),
                    showlegend=False, row=1, col=col)
    fig.add_scatter(x=[read], y=[0], mode="markers+text", marker=dict(size=13, color=RED), text=[f"reading {read:.2f}"],
                    textposition="bottom center", textfont=dict(color=RED, size=18), showlegend=False, row=1, col=col)
    fig.update_xaxes(range=[-0.3, 1.6], zeroline=True, row=1, col=col)
    fig.update_yaxes(range=[-0.35, 1.25], zeroline=True, scaleanchor=xa, row=1, col=col)
fig.update_layout(template="simple_white", width=1100, height=520, font=dict(FONT, size=18), margin=dict(l=40, r=20, t=50, b=40))
fig.write_image(here / "interference.png", scale=2)
fig.write_image(here / "interference.pdf")
