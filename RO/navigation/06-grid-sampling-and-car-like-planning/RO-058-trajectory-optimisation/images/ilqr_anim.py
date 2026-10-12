"""iLQR on the 8 s least-effort drive, one iteration per frame (thinning out later), from the first shot. Left:
the drive after each iteration (blue; earlier ones pale). Right: the cost after each iteration, on a scale where
each grid line is 10 times the one below: iLQR (blue) against plain gradient descent on the same cost from the
same first shot (orange). The cost is the effort plus large penalties for missing the door pose, breaking a wheel
limit or touching the table. Run -> ilqr.gif, ilqr_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import roomdraw as rd
import trajkit as tk
from gifkit import BLUE, FONT, ORANGE, RED, make_gif
from plotly.subplots import make_subplots

here = Path(__file__).parent
S = tk.solutions()
il, gd = S["ilqr"], S["gd"]
ci = [h[2] for h in il["hist"]]
cg = gd["costs"]
n = len(ci)
k13 = 13
assert round(ci[0]) == round(cg[0]) and ci[-1] < 0.22 and cg[1000] > 1000
assert ci[k13] < 0.25


def fmt(c):
    return f"{c:,.0f}" if c >= 10 else f"{c:.4f}"


TV = [0.1, 1, 10, 100, 1e3, 1e4, 1e5, 1e6]
TT = ["0.1", "1", "10", "100", "1,000", "10,000", "100,000", "1,000,000"]


def frame(i):
    fig = make_subplots(rows=1, cols=2, column_widths=[0.48, 0.52], horizontal_spacing=0.1,
                        subplot_titles=[f"iLQR, iteration {i}", "cost after each iteration"])
    rd.room(fig, rc=(1, 1))
    for j in range(max(0, i - 3), i):
        x = il["hist"][j][0]
        fig.add_trace(go.Scatter(x=x[:, 0], y=x[:, 1], mode="lines", line=dict(color="#C9D6E8", width=2)), row=1, col=1)
    x = il["hist"][i][0]
    fig.add_trace(go.Scatter(x=x[:, 0], y=x[:, 1], mode="lines", line=dict(color=BLUE, width=5)), row=1, col=1)
    fig.add_trace(go.Scatter(x=[x[-1, 0], tk.GOAL[0]], y=[x[-1, 1], tk.GOAL[1]], mode="lines",
                             line=dict(color=RED, width=4)), row=1, col=1)
    rd.robot(fig, *tk.GOAL[:3], "#BBBBBB", rc=(1, 1), width=2, fill="rgba(0,0,0,0)")
    rd.axes(fig, rc=(1, 1))
    it = np.arange(i + 1)
    fig.add_trace(go.Scatter(x=it, y=cg[:i + 1], mode="lines", line=dict(color=ORANGE, width=3)), row=1, col=2)
    fig.add_trace(go.Scatter(x=it, y=ci[:i + 1], mode="lines+markers", line=dict(color=BLUE, width=3),
                             marker=dict(size=5)), row=1, col=2)
    fig.add_annotation(x=0.98, y=0.98, xref="x2 domain", yref="y2 domain", xanchor="right", yanchor="top",
                       text=f"<span style='color:{BLUE}'>iLQR: {fmt(ci[i])}</span><br>"
                            f"<span style='color:{ORANGE}'>gradient descent: {fmt(cg[i])}</span>",
                       showarrow=False, align="right", font=dict(size=19), bgcolor="rgba(255,255,255,0.9)")
    fig.update_xaxes(title="iteration", range=[0, n + 1], row=1, col=2)
    fig.update_yaxes(type="log", range=[-1, 6.5], title="cost", tickvals=TV, ticktext=TT, row=1, col=2)
    fig.update_layout(template="simple_white", font=FONT, width=1300, height=800, showlegend=False,
                      margin=dict(l=10, r=20, t=50, b=60))
    return fig


ks = sorted(set(list(range(min(n, 16))) + list(range(16, n, max(1, (n - 16) // 8))) + [n - 1]))
figs = [frame(i) for i in ks]
make_gif(figs, here / "ilqr", fps=2, holds=[4] + [2] * (len(figs) - 2) + [12],
         keys=[0, 2, ks.index(k13), len(figs) - 1], cols=2, width=900)
print("iLQR iterations", n - 1, "cost", ci[-1], "at 13:", ci[k13], "GD after 1000:", cg[1000])
