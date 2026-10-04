"""Why +lambda I always gives an inverse (Plotly), on the diabetes data of Section 3.4 (training split, test size 0.2,
random state 4), with the column of 1s. The smallest eigenvalue of X^T X + lambda I' (I' = identity with top-left 0
as in the Note) and its condition number (largest / smallest eigenvalue) against lambda. X^T X alone has a tiny
smallest eigenvalue because s1 and s2 are strongly correlated; adding lambda lifts it and the condition number falls."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from gifkit import BLUE, FONT, ORANGE

here = Path(__file__).parent
X, y = load_diabetes(return_X_y=True)
Xtr, _, _, _ = train_test_split(X, y, test_size=0.2, random_state=4)
Xa = np.insert(Xtr, 0, 1, axis=1)
G = Xa.T @ Xa
I = np.identity(G.shape[0]); I[0, 0] = 0
lams = np.r_[0, np.logspace(-4, 2, 61)]
ev = [np.linalg.eigvalsh(G + l * I) for l in lams]
small = np.array([e.min() for e in ev]); cond = np.array([e.max() / e.min() for e in ev])
c01 = np.linalg.cond(G + 0.1 * I)
assert np.all(np.diff(small) > 0) and np.all(np.diff(cond) < 0) and round(cond[0], -3) == 48_000 and round(c01, -1) == 3290
fig = make_subplots(1, 2, horizontal_spacing=0.13, subplot_titles=["smallest eigenvalue of XᵀX + λI", "condition number"])
fig.update_annotations(font_size=21)
fig.add_trace(go.Scatter(x=lams[1:], y=small[1:], mode="lines", line=dict(color=BLUE, width=4)), 1, 1)
fig.add_trace(go.Scatter(x=lams[1:], y=cond[1:], mode="lines", line=dict(color=ORANGE, width=4)), 1, 2)
for col, v, t in ((1, small[0], f"λ = 0: {small[0]:.4f}"), (2, cond[0], f"λ = 0: {cond[0]:,.0f}")):
    fig.add_hline(y=v, line=dict(dash="dot", color="#666", width=2), opacity=1, row=1, col=col)
    fig.add_annotation(x=0.02, y=np.log10(v), xref=f"x{col if col > 1 else ''} domain", yref=f"y{col if col > 1 else ''}",
                       text=t, showarrow=False, xanchor="left", yshift=14 if col == 1 else -14, font=dict(size=18))
fig.update_xaxes(title="λ (log scale)", type="log", exponentformat="power")
fig.update_yaxes(type="log", exponentformat="power")
fig.update_layout(template="simple_white", width=1200, height=520, font=FONT, showlegend=False,
                  margin=dict(l=80, r=30, t=60, b=70))
fig.write_image(here / "invertible.png", scale=2)
