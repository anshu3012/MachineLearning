"""Power iteration on the website example (Plotly frames -> GIF). T has columns [0.9, 0.1] and [0.5, 0.5]; its
eigenvalues are 1 and 0.4. Two different starting splits of users (all on page A, all on page B) are multiplied by
T day after day. Left: the split as a point on the line share_A + share_B = 1, with the eigenvector lines; the 0.4
part shrinks each day, so both points slide onto the eigenvector of eigenvalue 1, [0.833, 0.167]. Right: the share
on page A by day."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, RED, make_gif

here = Path(__file__).parent
T = np.array([[0.9, 0.5], [0.1, 0.5]])
vals, vecs = (a.real for a in np.linalg.eig(T))
assert np.allclose(sorted(vals), [0.4, 1.0])
v1 = vecs[:, np.argmax(vals)]; v1 = v1 / v1.sum()
assert np.allclose(v1, [5 / 6, 1 / 6]) and round(v1[0], 3) == 0.833
DAYS = 12
starts = {"start: all on A": np.array([1.0, 0.0]), "start: all on B": np.array([0.0, 1.0])}
paths = {k: [s] for k, s in starts.items()}
for k in paths:
    for _ in range(DAYS):
        paths[k].append(T @ paths[k][-1])
assert all(abs(p[-1][0] - v1[0]) < 1e-4 for p in paths.values())
COL = {"start: all on A": BLUE, "start: all on B": ORANGE}


def frame(d):
    fig = make_subplots(1, 2, column_widths=[0.45, 0.55], horizontal_spacing=0.12,
                        subplot_titles=["the split of users, day by day", "share of users on page A"])
    fig.update_annotations(font_size=22)
    fig.add_trace(go.Scatter(x=[0, 1], y=[1, 0], mode="lines", line=dict(color=GREY, width=1.5)), 1, 1)
    fig.add_trace(go.Scatter(x=[0, 1.2 * v1[0] / v1.max()], y=[0, 1.2 * v1[1] / v1.max()], mode="lines",
                             line=dict(color=GREEN, width=4)), 1, 1)
    fig.add_annotation(x=1.02, y=0.2, xref="x", yref="y", text="eigenvalue 1", showarrow=False, xanchor="left",
                       font=dict(color=GREEN, size=20))
    for k, p in paths.items():
        P = np.array(p[:d + 1])
        fig.add_trace(go.Scatter(x=P[:, 0], y=P[:, 1], mode="lines+markers", line=dict(color=COL[k], width=2),
                                 marker=dict(size=7)), 1, 1)
        fig.add_trace(go.Scatter(x=[P[-1, 0]], y=[P[-1, 1]], mode="markers",
                                 marker=dict(size=16, color=COL[k], line=dict(color="white", width=2))), 1, 1)
        fig.add_trace(go.Scatter(x=list(range(d + 1)), y=P[:, 0], mode="lines+markers", name=k,
                                 line=dict(color=COL[k], width=4), marker=dict(size=8)), 1, 2)
    fig.add_hline(y=v1[0], line=dict(color=GREEN, dash="dash", width=3), row=1, col=2)
    fig.add_annotation(x=DAYS, y=v1[0], xref="x2", yref="y2", text="0.833", showarrow=False, yshift=-18,
                       xanchor="right", font=dict(color=GREEN, size=22))
    fig.update_xaxes(title="share on A", range=[-0.05, 1.25], row=1, col=1)
    fig.update_yaxes(title="share on B", range=[-0.05, 1.05], scaleanchor="x", row=1, col=1)
    fig.update_xaxes(title="day", range=[-0.3, DAYS + 0.3], row=1, col=2)
    fig.update_yaxes(range=[-0.02, 1.02], row=1, col=2)
    fig.update_layout(template="simple_white", width=1200, height=560, font=FONT, showlegend=True,
                      legend=dict(x=0.6, y=0.25, traceorder="normal"), margin=dict(l=70, r=30, t=60, b=70),
                      title=dict(text=f"day {d}", x=0.02, y=0.98))
    for tr in fig.data:
        if tr.name is None or not tr.name.startswith("start"):
            tr.showlegend = False
    return fig


if __name__ == "__main__":
    make_gif([frame(d) for d in range(DAYS + 1)], here / "power_iteration", fps=2, holds=[3] + [1] * (DAYS - 1) + [6],
             keys=[0, 1, 3, DAYS], width=900)
