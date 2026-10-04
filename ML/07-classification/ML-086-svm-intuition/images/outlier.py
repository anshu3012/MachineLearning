"""Hard margin against soft margin with one outlier (Plotly). One extra green point is added at (4.5, 4.2), close to
the red class. Left: the hard-margin SVM (C = 1e6) must squeeze past it, so the line tilts and the margin shrinks.
Right: a soft-margin SVM (C = 1) lets the point sit inside the margin and keeps the line it had without the
outlier (dotted)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.svm import SVC
from gifkit import FONT, GREEN, GREY, ORANGE, RED
from svm_data import X, line, xs, y

here = Path(__file__).parent
out = np.array([[4.5, 4.2]])
Xo, yo = np.r_[X, out], np.r_[y, 1]
base = SVC(kernel="linear", C=1e6).fit(X, y)
hard = SVC(kernel="linear", C=1e6).fit(Xo, yo)
soft = SVC(kernel="linear", C=1).fit(Xo, yo)
d = lambda m: 2 / np.linalg.norm(m.coef_[0])
ang = lambda m: np.degrees(np.arctan2(m.coef_[0][1], m.coef_[0][0]))
assert round(d(base), 2) == 2.22 and round(d(hard), 2) == 0.56 and abs(d(soft) - d(base)) < 0.01 and np.allclose(soft.coef_, base.coef_, atol=1e-3)
fig = make_subplots(1, 2, horizontal_spacing=0.08,
                    subplot_titles=[f"hard margin: margin {d(base):.2f} → {d(hard):.2f}", f"soft margin (C = 1): margin stays {d(soft):.2f}"])
fig.update_annotations(font_size=21)
for col, m in ((1, hard), (2, soft)):
    w, b = m.coef_[0], m.intercept_[0]
    fig.add_trace(go.Scatter(x=xs, y=line(base.coef_[0], base.intercept_[0]), mode="lines", line=dict(color=GREY, width=2, dash="dot")), 1, col)
    for s, dash in ((0, "solid"), (1, "dash"), (-1, "dash")):
        fig.add_trace(go.Scatter(x=xs, y=line(w, b, s), mode="lines", line=dict(color="black" if s == 0 else ORANGE, width=3 if s == 0 else 2, dash=dash)), 1, col)
    for cls, c in ((1, GREEN), (-1, RED)):
        k = y == cls
        fig.add_trace(go.Scatter(x=X[k, 0], y=X[k, 1], mode="markers", marker=dict(size=12, color=c, line=dict(color="black", width=1))), 1, col)
    fig.add_trace(go.Scatter(x=out[:, 0], y=out[:, 1], mode="markers+text", text=["outlier"], textposition="middle right",
                             textfont=dict(size=18), marker=dict(size=16, color=GREEN, symbol="star", line=dict(color="black", width=1.5))), 1, col)
    fig.update_xaxes(range=[0, 8.5], title="x₁", row=1, col=col)
    fig.update_yaxes(range=[0, 10], title="x₂" if col == 1 else None, scaleanchor=f"x{col if col > 1 else ''}", row=1, col=col)
fig.update_layout(template="simple_white", width=1150, height=640, font=FONT, showlegend=False, margin=dict(l=60, r=20, t=60, b=60))
fig.write_image(here / "outlier.png", scale=2)
