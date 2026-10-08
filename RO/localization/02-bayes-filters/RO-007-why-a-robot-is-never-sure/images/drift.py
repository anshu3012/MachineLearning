"""Dead reckoning without readings: on a long straight track the robot starts surely at 0 m and is told "move 2"
(cells of 1 m) eight times. Each move goes 1 m (10 %), 2 m (80 %) or 3 m (10 %). Bars: the probability of each true position after each move.
Run: python drift.py -> drift.gif, drift_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from corrdraw import MOVE
from gifkit import BLUE, FONT, GREY, RED, make_gif

here = Path(__file__).parent
n = 25
bs = [np.eye(n)[0]]
for _ in range(8):
    b = np.zeros(n)
    for i, p in enumerate(bs[-1]):
        for d, q in MOVE.items():
            if i + d < n:
                b[i + d] += p * q
    bs.append(b)
x = np.arange(n)
sd = [np.sqrt((b * (x - 2 * k) ** 2).sum()) for k, b in enumerate(bs)]
assert np.allclose([sd[1], sd[2], sd[4], sd[8]], [0.447, 0.632, 0.894, 1.265], atol=5e-4)
assert abs(bs[8][16] - 0.332) < 5e-4 and abs(bs[2][4] - 0.66) < 1e-9


def frame(k):
    b = bs[k]
    fig = go.Figure(go.Bar(x=x, y=b, marker_color=BLUE, width=0.6,
                           text=[f"{v:.2f}" if v >= 0.005 else "" for v in b], textposition="outside", constraintext="none", cliponaxis=False,
                           textfont=dict(size=12)))
    fig.add_vline(x=2 * k, line=dict(color=RED, dash="dash", width=2))
    fig.add_annotation(x=2 * k, y=1.08, text=f"the robot thinks: {2 * k} m", showarrow=False, font=dict(color=RED, size=18))
    fig.update_xaxes(tickvals=list(x), range=[-0.6, n - 0.4], title="true position (m)")
    fig.update_yaxes(range=[0, 1.15], title="probability")
    fig.update_layout(template="simple_white", width=900, height=560, font=FONT, showlegend=False,
                      margin=dict(l=90, r=30, t=110, b=70),
                      title=dict(x=0.5, y=0.93, font=dict(size=22),
                                 text=f"after {k} move{'s' if k != 1 else ''} of 2 m, no readings:  "
                                      f"spread (standard deviation) {sd[k]:.2f} m"))
    return fig


figs = [frame(k) for k in range(9)]
make_gif(figs, here / "drift", fps=1, holds=[2, 2, 2, 1, 2, 1, 1, 1, 4], keys=[1, 2, 4, 8], cols=2, width=900)
