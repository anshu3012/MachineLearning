"""The data (counts per class, scatter) and the line logistic regression learns on it as it is."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.linear_model import LogisticRegression
from imb import BLUE, RED, FONT, data

here = Path(__file__).parent
Xtr, Xte, ytr, yte = data()
clf = LogisticRegression().fit(Xtr, ytr)
(a, b), c = clf.coef_[0], clf.intercept_[0]
gx = np.linspace(-4.7, 3.3, 50)

fig = make_subplots(rows=1, cols=2, column_widths=[0.3, 0.7], horizontal_spacing=0.12,
                    subplot_titles=("Training rows per class", "Logistic regression on the data as it is"))
counts = np.bincount(ytr)
fig.add_trace(go.Bar(x=["class 1", "class 0"], y=[counts[1], counts[0]], marker_color=[BLUE, RED],
                     text=[counts[1], counts[0]], textposition="outside", showlegend=False), 1, 1)
for label, colour, name in [(1, BLUE, "class 1 (majority)"), (0, RED, "class 0 (minority)")]:
    m = ytr == label
    fig.add_trace(go.Scatter(x=Xtr[m, 0], y=Xtr[m, 1], mode="markers", name=name,
                             marker=dict(color=colour, size=9 if label == 0 else 7, opacity=0.85 if label == 0 else 0.5,
                                         line=dict(width=1, color="black") if label == 0 else None)), 1, 2)
fig.add_trace(go.Scatter(x=gx, y=-(a * gx + c) / b, mode="lines", name="decision boundary",
                         line=dict(color="black", width=3)), 1, 2)
fig.update_yaxes(range=[0, 340], title_text="rows", row=1, col=1)
fig.update_xaxes(range=[-4.7, 3.3], title_text="x1", row=1, col=2)
fig.update_yaxes(range=[-4, 4.3], title_text="x2", row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=520, font=FONT,
                  legend=dict(orientation="h", x=0.32, y=-0.18), margin=dict(l=60, r=20, t=50, b=110))
fig.update_annotations(font=dict(family=FONT["family"], size=19))
fig.write_image(here / "baseline.png", scale=2)
fig.write_image(here / "baseline.pdf")
