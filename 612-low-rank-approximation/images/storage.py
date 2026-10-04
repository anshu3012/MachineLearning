"""What a rank k approximation costs to store (Plotly), for the 427 x 640 photo: k (m + n + 1) numbers against the
273,280 of the full matrix. k = 20 needs 21,360 (7.8%); the layers stop paying off at k = 256, where they cost as
much as the matrix itself."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, ORANGE, RED

here = Path(__file__).parent
m, n = 427, 640
full = m * n
cost = lambda k: k * (m + n + 1)
assert full == 273_280 and cost(20) == 21_360 and round(100 * cost(20) / full, 1) == 7.8
even = full / (m + n + 1)
assert int(np.ceil(even)) == 256
ks = np.arange(0, 428)
fig = go.Figure([go.Scatter(x=ks, y=cost(ks), mode="lines", line=dict(color=BLUE, width=4), name="stored: k (m + n + 1)"),
                 go.Scatter(x=[0, 427], y=[full, full], mode="lines", line=dict(color=GREY, width=3, dash="dash"),
                            name="full matrix: 273,280")])
for k, c in ((5, ORANGE), (20, ORANGE), (50, ORANGE), (100, ORANGE)):
    fig.add_scatter(x=[k], y=[cost(k)], mode="markers+text", text=[f"k = {k}: {100 * cost(k) / full:.1f}%"],
                    textposition="middle right", textfont=dict(size=18, color=c), marker=dict(size=11, color=c), showlegend=False)
fig.add_vline(x=even, line=dict(color=RED, width=2, dash="dot"), opacity=1)
fig.add_annotation(x=even, y=full * 1.25, text="k = 256: break-even", showarrow=False, xanchor="left", xshift=6,
                   font=dict(size=18, color=RED))
fig.update_layout(template="simple_white", width=1000, height=560, font=FONT,
                  xaxis=dict(title="number of layers kept, k", range=[0, 430]),
                  yaxis=dict(title="numbers to store", range=[0, 470_000]),
                  legend=dict(x=0.01, y=0.99), margin=dict(l=90, r=30, t=20, b=70))
fig.write_image(here / "storage.png", scale=2)
