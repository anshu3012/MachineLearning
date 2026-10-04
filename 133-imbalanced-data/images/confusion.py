"""Section 3.2: the confusion matrix of plain logistic regression on the 80 test observations, next to the "dumb"
model that always answers class 1. 92.5% and 91.25% accuracy, but 1 and 0 of the 7 minority observations found.
Plotly."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from imb import data, FONT

here = Path(__file__).parent
Xtr, Xte, ytr, yte = data()
pred = LogisticRegression().fit(Xtr, ytr).predict(Xte)
cms = [confusion_matrix(yte, pred, labels=[0, 1]), confusion_matrix(yte, np.ones_like(yte), labels=[0, 1])]
assert (pred == yte).mean() == 0.925 and cms[0][0, 0] == 1 and cms[1][1, 1] == 73
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.15,
                    subplot_titles=("logistic regression: accuracy 92.5%, recall of class 0 = 1/7",
                                    "always class 1: accuracy 91.25%, recall of class 0 = 0/7"))
for c, cm in enumerate(cms, start=1):
    fig.add_trace(go.Heatmap(z=cm, x=["predicted 0", "predicted 1"], y=["true 0", "true 1"], colorscale="Blues", showscale=False,
                             zmin=0, zmax=80, text=cm, texttemplate="%{text}", textfont=dict(size=26)), row=1, col=c)
    fig.add_shape(type="rect", x0=-0.5, x1=1.5, y0=-0.5, y1=0.5, line=dict(color="#E45756", width=4), fillcolor="rgba(0,0,0,0)",
                  opacity=1, row=1, col=c)
    fig.update_yaxes(autorange="reversed", row=1, col=c)
fig.update_layout(template="simple_white", width=1100, height=420, font=FONT, margin=dict(l=70, r=20, t=60, b=40))
fig.write_image(here / "confusion.png", scale=2)
fig.write_image(here / "confusion.pdf")
