"""Smoothing the whole A* route as one optimisation, one solver step per frame. The 7 route points (grey dashed,
the global plan); the two ends stay fixed; each of the 5 others may move only sideways, by at most 0.1 m each way
(green bars). Each step moves every point downhill on the smoothing cost (the sum of squared second differences,
plus 0.001 times the squared moves) and clips it back inside its bar: projected gradient steps. Right: the cost
after each step, from 0.75 m^2 to 0.397 m^2; three points end on the end of their bars. Run -> smooth_anim.gif,
smooth_anim_frames.png"""
from pathlib import Path

import bandkit as bk
import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN, GREY, make_gif
from plotly.subplots import make_subplots

here = Path(__file__).parent
S = bk.smooth(bk.ROUTE)
costs = [S["cost"](d) for d in S["hist"]]
assert round(costs[0], 2) == 0.75 and round(S["cost"](S["exact"]), 3) == 0.397 and abs(costs[-1] - S["cost"](S["exact"])) < 1e-6
assert int(np.sum(np.isclose(np.abs(S["exact"]), 0.1))) == 3
STEPS = list(range(0, 9)) + [20]
n = S["n"]


def frame(k):
    d = S["hist"][k]
    p = S["pts"](d)
    fig = make_subplots(rows=1, cols=2, column_widths=[0.5, 0.5], horizontal_spacing=0.12,
                        subplot_titles=[f"step {k}", "smoothing cost after each step"])
    fig.update_annotations(font_size=22)
    fig.add_trace(go.Scatter(x=bk.ROUTE[:, 0], y=bk.ROUTE[:, 1], mode="lines+markers",
                             line=dict(color=GREY, width=2.5, dash="dash"), marker=dict(size=8, color=GREY)), row=1, col=1)
    for j in range(5):
        a, b = bk.ROUTE[j + 1] - 0.1 * n[j], bk.ROUTE[j + 1] + 0.1 * n[j]
        fig.add_trace(go.Scatter(x=[a[0], b[0]], y=[a[1], b[1]], mode="lines", line=dict(color=GREEN, width=8)),
                      row=1, col=1)
    fig.add_trace(go.Scatter(x=p[:, 0], y=p[:, 1], mode="lines+markers", line=dict(color=BLUE, width=3),
                             marker=dict(size=12, color=BLUE)), row=1, col=1)
    fig.add_annotation(x=2.05, y=3.95, text=f"cost {costs[k]:.3f} m²", showarrow=False, xanchor="left",
                       yanchor="top", font=dict(size=21), bgcolor="rgba(255,255,255,0.9)", row=1, col=1)
    fig.add_annotation(x=bk.ROUTE[0, 0] + 0.05, y=bk.ROUTE[0, 1] - 0.08, text="fixed", showarrow=False,
                       xanchor="left", font=dict(size=18, color=GREY), row=1, col=1)
    fig.add_annotation(x=bk.ROUTE[-1, 0], y=bk.ROUTE[-1, 1] - 0.1, text="fixed", showarrow=False,
                       font=dict(size=18, color=GREY), row=1, col=1)
    fig.update_xaxes(range=[2.0, 4.0], visible=False, row=1, col=1)
    fig.update_yaxes(range=[1.05, 4.0], visible=False, scaleanchor="x", row=1, col=1)
    fig.add_trace(go.Scatter(x=list(range(k + 1)), y=costs[:k + 1], mode="lines+markers", line=dict(color=BLUE, width=3),
                             marker=dict(size=9)), row=1, col=2)
    fig.update_xaxes(title="step", range=[-0.5, 20.5], row=1, col=2)
    fig.update_yaxes(title="cost (m²)", range=[0.3, 0.8], row=1, col=2)
    fig.update_layout(template="simple_white", font=FONT, width=1200, height=800, showlegend=False,
                      margin=dict(l=10, r=20, t=50, b=60))
    return fig


figs = [frame(k) for k in STEPS]
make_gif(figs, here / "smooth_anim", fps=2, holds=[4] + [2] * (len(figs) - 2) + [10], keys=[0, 1, 3, len(figs) - 1],
         cols=2, width=900)
print("costs", [round(c, 4) for c in costs[:10]], "exact", S["cost"](S["exact"]), "moves", np.round(S["exact"], 4))
