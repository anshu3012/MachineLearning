"""The optimisation problem as a search (Plotly frames -> GIF), on the 16 points of the SVM intuition Note. For each
direction of w (angle from 60 to 120 degrees) we take the widest margin that still satisfies every constraint: the
gap between the lowest green projection and the highest red projection onto w. Left: that direction's pi, pi+ and
pi-. Right: the margin against the angle; its maximum, 2.22 at the angle of the SVM's w = (0.049, 0.898), is the
answer of arg max 2/||w|| subject to y (w.x + b) >= 1."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.svm import SVC
from gifkit import FONT, GREEN, GREY, ORANGE, RED, make_gif

here = Path(__file__).parent
G = np.array([(2, 6), (3.5, 7.5), (4.5, 6), (6, 7.5), (2.5, 8.5), (5, 9), (7, 9), (7.5, 6.8)])
R = np.array([(1, 1.5), (2.5, 3), (3.5, 1), (5, 2.5), (6.5, 1.5), (7, 3.5), (1.5, 3.8), (4, 3.5)])
X, y = np.r_[G, R], np.r_[np.ones(8), -np.ones(8)]
svm = SVC(kernel="linear", C=1e6).fit(X, y)
th_svm = np.degrees(np.arctan2(svm.coef_[0][1], svm.coef_[0][0]))


def best(theta):
    u = np.array([np.cos(np.radians(theta)), np.sin(np.radians(theta))])
    lo, hi = (G @ u).min(), (R @ u).max()
    return u, lo, hi, lo - hi


angles = np.linspace(60, 120, 601)
gaps = np.array([best(t)[3] for t in angles])
t_best = angles[np.argmax(gaps)]
assert abs(t_best - th_svm) < 0.2 and round(gaps.max(), 2) == 2.22 == round(2 / np.linalg.norm(svm.coef_[0]), 2)
SHOW = [60, 66, 72, 78, 84, round(th_svm, 1), 92, 100, 110, 120]
xs = np.array([0, 8.5])


def frame(t):
    u, lo, hi, gap = best(t)
    fig = make_subplots(1, 2, horizontal_spacing=0.1, column_widths=[0.5, 0.5],
                        subplot_titles=[f"direction of w at {t:.1f}°: margin {gap:.2f}", "widest feasible margin against the direction"])
    fig.update_annotations(font_size=21)
    for c, col in ((lo, ORANGE), (hi, ORANGE), ((lo + hi) / 2, "black")):
        fig.add_trace(go.Scatter(x=xs, y=(c - u[0] * xs) / u[1], mode="lines",
                                 line=dict(color=col, width=3 if col == "black" else 2, dash=None if col == "black" else "dash")), 1, 1)
    for P, cc in ((G, GREEN), (R, RED)):
        fig.add_trace(go.Scatter(x=P[:, 0], y=P[:, 1], mode="markers", marker=dict(size=12, color=cc, line=dict(color="black", width=1))), 1, 1)
    fig.add_trace(go.Scatter(x=angles, y=gaps, mode="lines", line=dict(color=GREY, width=3)), 1, 2)
    fig.add_trace(go.Scatter(x=[t], y=[gap], mode="markers", marker=dict(size=15, color=ORANGE)), 1, 2)
    fig.add_annotation(x=th_svm, y=gaps.max(), xref="x2", yref="y2", text="SVM: 2.22", ax=60, ay=-30, font=dict(size=18))
    fig.update_xaxes(range=[0, 8.5], title="x₁", row=1, col=1)
    fig.update_yaxes(range=[0, 10], title="x₂", scaleanchor="x", row=1, col=1)
    fig.update_xaxes(title="angle of w (degrees)", row=1, col=2)
    fig.update_yaxes(title="margin d", range=[0, 2.6], row=1, col=2)
    fig.update_layout(template="simple_white", width=1200, height=600, font=FONT, showlegend=False, margin=dict(l=60, r=30, t=60, b=70))
    return fig


if __name__ == "__main__":
    holds = [1] * len(SHOW); holds[5] = 5; holds[-1] = 3
    make_gif([frame(t) for t in SHOW], here / "margin_sweep", fps=2, holds=holds, keys=[1, 5], cols=1)
