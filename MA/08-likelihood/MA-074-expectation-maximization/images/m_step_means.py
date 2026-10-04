"""The M-step for the means, drawn (Plotly). One row per component of the seven-observation example. Each observation
is drawn with its responsibility r_nk from the starting E-step (dot size and label); the new mean is the
responsibility-weighted average, the balance point of the dots. Arrows: old means -4, 0, 8 move to -2.70, -0.40, 3.70."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

from em_core import COLS, FONT, GREY, SEVEN, START, e_step, m_step

HERE = Path(__file__).parent
X = SEVEN.ravel()
R = e_step(SEVEN, *START)
_, mu, _ = m_step(SEVEN, R)
old = START[1].ravel()
new = mu.ravel()
assert np.allclose(new, [-2.70, -0.40, 3.70], atol=0.01)
assert np.allclose(R.sum(axis=0), [2.057, 2.009, 2.934], atol=0.001)

fig = go.Figure()
for k in range(3):
    yk = 2 - k
    fig.add_trace(go.Scatter(x=[-5, 9], y=[yk, yk], mode="lines", line=dict(color="#DDDDDD", width=1)))
    keep = R[:, k] > 0.005
    fig.add_trace(go.Scatter(x=X[keep], y=[yk] * keep.sum(), mode="markers+text",
                             marker=dict(size=10 + 30 * R[keep, k], color=COLS[k], opacity=0.85),
                             text=[f"{r:.2f}".rstrip("0").rstrip(".") for r in R[keep, k]], textposition="top center",
                             textfont=dict(size=24, color=COLS[k])))
    fig.add_trace(go.Scatter(x=X[~keep], y=[yk] * (~keep).sum(), mode="markers",
                             marker=dict(size=7, color="white", line=dict(color="#BBBBBB", width=1.5))))
    fig.add_trace(go.Scatter(x=[old[k]], y=[yk - 0.33], mode="markers", marker=dict(symbol="triangle-up-open", size=20,
                             color=GREY, line=dict(width=3))))
    fig.add_trace(go.Scatter(x=[new[k]], y=[yk - 0.33], mode="markers", marker=dict(symbol="triangle-up", size=22,
                             color=COLS[k])))
    fig.add_annotation(x=new[k], y=yk - 0.33, ax=old[k], ay=yk - 0.33, xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowwidth=2.5, arrowcolor=COLS[k], standoff=12, startstandoff=10,
                       text="")
    fig.add_annotation(x=new[k], y=yk - 0.33, text=f"{old[k]:g} → {new[k]:.2f}".replace("-", "−"), showarrow=False,
                       yshift=-32, font=dict(size=25, color=COLS[k]))
    fig.add_annotation(x=-0.01, xref="paper", y=yk, text=f"component {k + 1}<br>N<sub>{k + 1}</sub> = {R[:, k].sum():.3f}",
                       showarrow=False, xanchor="right", font=dict(size=24, color=COLS[k]))
fig.update_layout(template="simple_white", width=1150, height=640, showlegend=False, font=FONT,
                  xaxis=dict(title="x", range=[-5.5, 9], dtick=1),
                  yaxis=dict(visible=False, range=[-0.75, 2.45]), margin=dict(l=230, r=20, t=20, b=60))
fig.write_image(HERE / "m_step_means.png", scale=2)
fig.write_image(HERE / "m_step_means.pdf")
