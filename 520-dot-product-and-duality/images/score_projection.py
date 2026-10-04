"""Section 7.1: the score w.x + w0 of a linear model, read as a projection. w = [3, 4], w0 = -5, x = [3, 1]:
x's shadow on the line of w sits at w.x / |w| = 13/5 = 2.6; the score is 9 + 4 - 5 = 8 and the signed distance
from the hyperplane (score 0) is 8 / 5 = 1.6. Points on a line perpendicular to w share a shadow, so share a score.
Run: python score_projection.py  -> score_projection.png/.pdf (Plotly)"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, PURPLE, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"
w, w0, x = np.array([3.0, 4.0]), -5.0, np.array([3.0, 1.0])
n = np.linalg.norm(w)
score = w @ x + w0
assert np.isclose(score, 8) and np.isclose(score / n, 1.6)                    # the Note's numbers
u, perp = w / n, np.array([-w[1], w[0]]) / n
shadow = (w @ x) / n * u
assert np.isclose((w @ x) / n, 2.6)

fig = go.Figure()
t = np.linspace(-6, 6, 2)
for s, col, width, label in [(0, RED, 4, "score 0: the hyperplane"), (8, BLUE, 3, "score 8"), (-5, GREY, 1.5, None),
                             (5, GREY, 1.5, None), (15, GREY, 1.5, None)]:
    base = (s - w0) / n * u                                                  # where this score line meets w's line
    pts = base + np.outer(t, perp)
    fig.add_trace(go.Scatter(x=pts[:, 0], y=pts[:, 1], mode="lines", line=dict(color=col, width=width,
                             dash="solid" if label else "dot"), name=label, showlegend=bool(label)))
    if not label:
        fig.add_annotation(x=base[0] + 2.4 * perp[0], y=base[1] + 2.4 * perp[1], text=f"score {s}", showarrow=False,
                           font=dict(size=16, color=GREY), bgcolor="white")
line = np.outer(np.linspace(-1.5, 4.5, 2), u)
fig.add_trace(go.Scatter(x=line[:, 0], y=line[:, 1], mode="lines", line=dict(color=GREY, dash="dash", width=1.5),
                         name="line of w", showlegend=False))
fig.add_trace(go.Scatter(x=[0, shadow[0]], y=[0, shadow[1]], mode="lines", line=dict(color=PURPLE, width=12),
                         opacity=0.7, name="shadow of x on w: 2.6"))
fig.add_trace(go.Scatter(x=[x[0], shadow[0]], y=[x[1], shadow[1]], mode="lines", line=dict(color=GREY, dash="dot", width=2),
                         showlegend=False))
fig.add_annotation(x=u[0] * 1.6, y=u[1] * 1.6, ax=0, ay=0, xref="x", yref="y", axref="x", ayref="y", showarrow=True,
                   arrowhead=2, arrowwidth=4, arrowcolor=GREEN)
fig.add_trace(go.Scatter(x=[None], y=[None], mode="lines", line=dict(color=GREEN, width=4), name="direction of w = [3, 4]"))
fig.add_trace(go.Scatter(x=[x[0]], y=[x[1]], mode="markers+text", marker=dict(size=14, color=ORANGE),
                         text=["<b>x = [3, 1]: score 9 + 4 − 5 = 8</b>"], textposition="bottom right",
                         textfont=dict(size=18, color=ORANGE), showlegend=False))
fig.update_layout(template="simple_white", width=900, height=760, font=dict(family="Latin Modern Roman", size=18),
                  title=dict(text="Equal shadows on w, equal scores; distance from the hyperplane = 8 / 5 = 1.6", x=0.5),
                  xaxis=dict(range=[-2, 6], dtick=1, showgrid=True, zeroline=True),
                  yaxis=dict(range=[-2, 5], dtick=1, showgrid=True, zeroline=True, scaleanchor="x"),
                  legend=dict(x=0.01, y=0.01, yanchor="bottom", bgcolor="rgba(255,255,255,0.9)"),
                  margin=dict(l=40, r=20, t=60, b=40))
fig.write_image(HERE / "score_projection.png", scale=2)
fig.write_image(HERE / "score_projection.pdf")
