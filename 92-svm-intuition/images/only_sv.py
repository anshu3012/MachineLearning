"""Only the support vectors matter (Plotly). Left: the hard-margin SVM (SVC, linear, C = 1e6) on all 16 points, with
its margin and its 3 support vectors ringed. Right: the same SVM retrained on the 3 support vectors alone gives the
same line (w and b equal to 3 decimals; the rest is solver tolerance)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.svm import SVC
from gifkit import FONT, GREEN, GREY, RED
from svm_data import X, line, xs, y

here = Path(__file__).parent
full = SVC(kernel="linear", C=1e6).fit(X, y)
sv = full.support_
small = SVC(kernel="linear", C=1e6).fit(X[sv], y[sv])
assert len(sv) == 3 and np.allclose(full.coef_, small.coef_, atol=1e-3) and np.allclose(full.intercept_, small.intercept_, atol=1e-3)
fig = make_subplots(1, 2, horizontal_spacing=0.08, subplot_titles=["trained on all 16 points", "retrained on the 3 support vectors only"])
fig.update_annotations(font_size=21)
for col, (Xd, yd, m) in enumerate(((X, y, full), (X[sv], y[sv], small)), 1):
    w, b = m.coef_[0], m.intercept_[0]
    for s, dash in ((0, "solid"), (1, "dash"), (-1, "dash")):
        fig.add_trace(go.Scatter(x=xs, y=line(w, b, s), mode="lines", line=dict(color="black" if s == 0 else GREY, width=3 if s == 0 else 2, dash=dash)), 1, col)
    for cls, c in ((1, GREEN), (-1, RED)):
        k = yd == cls
        fig.add_trace(go.Scatter(x=Xd[k, 0], y=Xd[k, 1], mode="markers", marker=dict(size=12, color=c, line=dict(color="black", width=1))), 1, col)
    fig.add_trace(go.Scatter(x=X[sv, 0], y=X[sv, 1], mode="markers", marker=dict(size=26, color="rgba(0,0,0,0)", line=dict(color="black", width=2.5))), 1, col)
    fig.add_annotation(x=0.5, y=0.02, xref=f"x{col if col > 1 else ''} domain", yref=f"y{col if col > 1 else ''} domain", showarrow=False,
                       text=f"w = ({w[0]:.3f}, {w[1]:.3f}), b = {b:.2f}", font=dict(size=18), bgcolor="white")
    fig.update_xaxes(range=[0, 8.5], title="x₁", row=1, col=col)
    fig.update_yaxes(range=[0, 10], title="x₂" if col == 1 else None, scaleanchor=f"x{col if col > 1 else ''}", row=1, col=col)
fig.update_layout(template="simple_white", width=1150, height=640, font=FONT, showlegend=False, margin=dict(l=60, r=20, t=60, b=60))
fig.write_image(here / "only_sv.png", scale=2)
