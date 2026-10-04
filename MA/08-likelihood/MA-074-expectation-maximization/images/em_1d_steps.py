"""EM on the seven-point example of MML Section 11.2: the weighted components (dashed) and the mixture (black) at the
start, after 1 and 2 iterations, and at convergence, with the log-likelihood of each."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

from em_core import COLS, FONT, SEVEN, START, run_em

HERE = Path(__file__).parent
hist = run_em(SEVEN, *START, 8)
SHOW = (0, 1, 2, 8)
g = np.linspace(-6, 10, 600)
fig = make_subplots(rows=2, cols=2, vertical_spacing=0.16, horizontal_spacing=0.08,
                    subplot_titles=[("start" if i == 0 else f"after {i} iteration{'s' if i > 1 else ''}"
                                     if i < 8 else "converged") + f": ℓ = {hist[i][4]:.2f}" for i in SHOW])
for j, i in enumerate(SHOW):
    pi, mu, cov = hist[i][:3]
    r, c = j // 2 + 1, j % 2 + 1
    comp = np.column_stack([pi[k] * stats.norm(mu[k, 0], np.sqrt(cov[k, 0, 0])).pdf(g) for k in range(3)])
    for k in range(3):
        fig.add_trace(go.Scatter(x=g, y=comp[:, k], mode="lines", line=dict(color=COLS[k], width=3, dash="dash"),
                                 showlegend=False), r, c)
    fig.add_trace(go.Scatter(x=g, y=comp.sum(axis=1), mode="lines", line=dict(color="black", width=2),
                             showlegend=False), r, c)
    fig.add_trace(go.Scatter(x=SEVEN[:, 0], y=np.zeros(7), mode="markers", marker=dict(size=10, color="black"),
                             showlegend=False), r, c)
    fig.update_yaxes(range=[0, 0.5 if i == 0 else 0.62], row=r, col=c)
    fig.update_xaxes(title_text="x" if r == 2 else None, row=r, col=c)
fig.update_layout(template="simple_white", width=1100, height=700, font=FONT, margin=dict(l=60, r=20, t=50, b=60))
fig.update_annotations(font_size=21)
fig.write_image(HERE / "em_1d_steps.png", scale=2)
fig.write_image(HERE / "em_1d_steps.pdf")
