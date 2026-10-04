"""Likelihood and log-likelihood of p for 4 orange answers out of 7, one above the other. The two curves have
different shapes but the same peak, p = 4/7 = 0.571, where both tangent lines are flat. Values marked at
p = 0.25, 0.5 and 0.57 (likelihood 0.058, 0.273, 0.294)."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
p = np.linspace(0.02, 0.98, 400)
L = stats.binom(7, p).pmf(4)
ll = np.log(L)
pk = 4 / 7
assert abs(p[L.argmax()] - pk) < 0.003 and abs(p[ll.argmax()] - pk) < 0.003
assert np.allclose(stats.binom(7, [0.25, 0.5, 0.57]).pmf(4), [0.058, 0.273, 0.294], atol=5e-4)

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                    subplot_titles=("likelihood L(p)", "log-likelihood log L(p)"))
for r, y, f in ((1, L, lambda v: v), (2, ll, np.log)):
    fig.add_trace(go.Scatter(x=p, y=y, mode="lines", line=dict(color=BLUE, width=4)), r, 1)
    pts = np.array([0.25, 0.5, 0.57])
    fig.add_trace(go.Scatter(x=pts, y=f(stats.binom(7, pts).pmf(4)), mode="markers+text", marker=dict(size=12, color=ORANGE),
                             text=[f"{v:.3f}" if r == 1 else f"{np.log(v):.2f}" for v in stats.binom(7, pts).pmf(4)],
                             textposition=["top left", "bottom right", "top right"], textfont=dict(size=18, color=ORANGE)), r, 1)
    top = f(stats.binom(7, pk).pmf(4))
    fig.add_trace(go.Scatter(x=[pk - 0.12, pk + 0.12], y=[top, top], mode="lines", line=dict(color=RED, width=3)), r, 1)
    fig.add_vline(x=pk, line=dict(color=GREEN, dash="dash", width=2), row=r, col=1)
fig.add_annotation(x=pk, y=0.06, text="peak at 4/7 = 0.571", showarrow=False, xanchor="left", xshift=8,
                   font=dict(size=19, color=GREEN), row=1, col=1)
fig.update_yaxes(range=[0, 0.36], title_text="likelihood", row=1, col=1)
fig.update_yaxes(range=[-9, 0], title_text="log-likelihood", row=2, col=1)
fig.update_xaxes(title_text="p, probability of preferring orange", range=[0, 1], row=2, col=1)
fig.update_layout(template="simple_white", width=900, height=720, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=20), margin=dict(l=80, r=20, t=50, b=60))
fig.update_annotations(font_size=20)
fig.write_image(HERE / "binomial_log.png", scale=2)
fig.write_image(HERE / "binomial_log.pdf")
