"""The line logistic regression learns as class 0's weight grows: 1 (no weighting), 5, 25, 50."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LogisticRegression
from imb import BLUE, RED, FONT, data

here = Path(__file__).parent
Xtr, Xte, ytr, yte = data()
gx = np.linspace(-4.7, 3.3, 50)
fig = go.Figure()
for label, colour, name in [(1, BLUE, "class 1 (majority)"), (0, RED, "class 0 (minority)")]:
    m = ytr == label
    fig.add_trace(go.Scatter(x=Xtr[m, 0], y=Xtr[m, 1], mode="markers", name=name,
                             marker=dict(color=colour, size=9 if label == 0 else 7, opacity=0.9 if label == 0 else 0.45,
                                         line=dict(width=1, color="black") if label == 0 else None)))
for w, shade in [(1, "#BDBDBD"), (5, "#8C8C8C"), (25, "#4D4D4D"), (50, "#000000")]:
    m = LogisticRegression(class_weight={0: w, 1: 1}).fit(Xtr, ytr)
    (a, b), c = m.coef_[0], m.intercept_[0]
    yy = -(a * gx + c) / b
    fig.add_trace(go.Scatter(x=gx, y=yy, mode="lines", line=dict(color=shade, width=3), showlegend=False))
    fig.add_annotation(x=3.3, y=yy[-1], text=f"weight {w}", showarrow=False, xanchor="left",
                       font=dict(family=FONT["family"], size=17))
fig.update_layout(template="simple_white", width=1000, height=600, font=FONT,
                  title=dict(text="class_weight={0: w, 1: 1}: the heavier class 0, the further the line moves", x=0.5),
                  xaxis=dict(range=[-4.7, 3.3], title="x1"), yaxis=dict(range=[-4, 4.3], title="x2"),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.15), margin=dict(l=60, r=110, t=60, b=110))
fig.write_image(here / "class_weight.png", scale=2)
fig.write_image(here / "class_weight.pdf")
