"""The soft-margin loss in two parts (Plotly), for the line of the slack figure (||w|| = 0.900, slacks 1.33 and
1.32): margin error 0.45 plus C x classification error 2.65. With C = 1 the loss is 3.10, with C = 10 it is 26.95:
a larger C makes the same mistakes cost much more."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.svm import SVC
from gifkit import BLUE, FONT, ORANGE

here = Path(__file__).parent
G = np.array([(2, 6), (3.5, 7.5), (4.5, 6), (6, 7.5), (2.5, 8.5), (5, 9), (7, 9), (7.5, 6.8), (6, 4.3)])
R = np.array([(1, 1.5), (2.5, 3), (3.5, 1), (5, 2.5), (6.5, 1.5), (7, 3.5), (1.5, 3.8), (4, 3.5), (2.8, 5.2)])
X, y = np.r_[G, R], np.r_[np.ones(len(G)), -np.ones(len(R))]
m = SVC(kernel="linear", C=1).fit(X, y)
w, b = m.coef_[0], m.intercept_[0]
xi = np.maximum(0, 1 - y * (X @ w + b))
me, ce = np.linalg.norm(w) / 2, xi.sum()
assert round(np.linalg.norm(w), 3) == 0.900 and sorted(np.round(xi[xi > 1e-6], 2)) == [1.32, 1.33] and round(ce, 2) == 2.65
Cs = [1, 10]
fig = go.Figure([go.Bar(x=[f"C = {c}" for c in Cs], y=[me] * 2, name="margin error ‖w‖/2", marker_color=BLUE,
                        text=[f"{me:.2f}"] * 2, textposition="inside", textfont=dict(size=20)),
                 go.Bar(x=[f"C = {c}" for c in Cs], y=[c * ce for c in Cs], name="C × classification error Σξ", marker_color=ORANGE,
                        text=[f"{c} × {ce:.2f} = {c * ce:.2f}" for c in Cs], textposition="inside", textfont=dict(size=20))])
for i, c in enumerate(Cs):
    fig.add_annotation(x=i, y=me + c * ce, text=f"loss {me + c * ce:.2f}", showarrow=False, yshift=16, font=dict(size=21))
fig.update_layout(template="simple_white", width=850, height=560, font=FONT, barmode="stack",
                  yaxis=dict(title="soft-margin loss", range=[0, 30]), legend=dict(x=0.01, y=0.98), margin=dict(l=70, r=30, t=20, b=60))
fig.write_image(here / "loss_bars.png", scale=2)
