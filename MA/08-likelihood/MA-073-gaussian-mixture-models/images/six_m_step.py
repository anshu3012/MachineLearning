"""The M-step on the six points, drawn (Plotly): one row per curve; each point is as large as its share (label) for that
curve; each mean moves from its start (hollow triangle) to the share-weighted average (filled triangle)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from six_points import COLS, FONT, GREY, START, X, e_step, m_step

here = Path(__file__).parent
R = e_step(*START)
_, mu, _ = m_step(R)
old = START[1]
fig = go.Figure()
for k, nm in enumerate("AB"):
    yk = 1 - k
    fig.add_trace(go.Scatter(x=[0, 9], y=[yk, yk], mode="lines", line=dict(color="#DDDDDD", width=1)))
    fig.add_trace(go.Scatter(x=X, y=[yk] * 6, mode="markers+text", marker=dict(size=10 + 34 * R[:, k], color=COLS[k], opacity=0.85),
                             text=[f"{r:.2f}" for r in R[:, k]], textposition="top center", textfont=dict(size=22, color=COLS[k])))
    fig.add_trace(go.Scatter(x=[old[k]], y=[yk - 0.3], mode="markers", marker=dict(symbol="triangle-up-open", size=20, color=GREY, line=dict(width=3))))
    fig.add_trace(go.Scatter(x=[mu[k]], y=[yk - 0.3], mode="markers", marker=dict(symbol="triangle-up", size=22, color=COLS[k])))
    fig.add_annotation(x=mu[k], y=yk - 0.3, ax=old[k], ay=yk - 0.3, xref="x", yref="y", axref="x", ayref="y", showarrow=True,
                       arrowhead=2, arrowwidth=2.5, arrowcolor=COLS[k], standoff=12, startstandoff=10, text="")
    fig.add_annotation(x=(mu[k] + old[k]) / 2, y=yk - 0.3, yshift=-34, showarrow=False, font=dict(size=24, color=COLS[k]),
                       text=f"{old[k]:g} → {mu[k]:.2f}")
    fig.add_annotation(x=-0.01, xref="paper", y=yk, showarrow=False, xanchor="right", font=dict(size=24, color=COLS[k]),
                       text=f"curve {nm}<br>total {R[:, k].sum():.2f}")
fig.update_layout(template="simple_white", width=1150, height=520, showlegend=False, font=FONT,
                  xaxis=dict(title="x", range=[0, 9], dtick=1), yaxis=dict(visible=False, range=[-0.75, 1.5]),
                  margin=dict(l=190, r=20, t=20, b=60))
fig.write_image(here / "six_m_step.png", scale=2)
fig.write_image(here / "six_m_step.pdf")
