"""Same data, two approaches: KNN (instance-based) vs logistic regression (model-based).
Both are really trained with scikit-learn on the example data."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

from placement_data import placement_data

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, PURPLE, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"
X, y = placement_data()
query = np.array([[94.5, 8.3]])
scaler = StandardScaler().fit(X)                   # put IQ and CGPA on the same scale for distances
Xs, qs = scaler.transform(X), scaler.transform(query)

knn = KNeighborsClassifier(n_neighbors=3).fit(Xs, y)
_, idx = knn.kneighbors(qs)
knn_answer = "Placed" if knn.predict(qs)[0] else "Not placed"
logreg = LogisticRegression().fit(Xs, y)
log_answer = "Placed" if logreg.predict(qs)[0] else "Not placed"

fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1, subplot_titles=(
    f"<b>Instance-based</b> (KNN, k = 3): {knn_answer}", f"<b>Model-based</b> (a learned boundary): {log_answer}"))

for col in (1, 2):
    for label, colour, name, symbol in [(1, GREEN, "Placed", "circle"), (0, RED, "Not placed", "x")]:
        m = y == label
        fig.add_trace(go.Scatter(x=X[m, 0], y=X[m, 1], mode="markers", name=name, showlegend=(col == 1),
                                 marker=dict(color=colour, size=10, symbol=symbol)), 1, col)
    fig.add_trace(go.Scatter(x=query[:, 0], y=query[:, 1], mode="markers", name="new student", showlegend=(col == 1),
                             marker=dict(color=BLUE, size=18, symbol="star", line=dict(color="black", width=1))), 1, col)

# Left: lines to the 3 nearest neighbours
for i in idx[0]:
    fig.add_trace(go.Scatter(x=[query[0, 0], X[i, 0]], y=[query[0, 1], X[i, 1]], mode="lines", showlegend=False,
                             line=dict(color=BLUE, width=2, dash="dot")), 1, 1)

# Right: the boundary where the model switches from "not placed" to "placed" (probability 0.5)
w, b = logreg.coef_[0], logreg.intercept_[0]
iq_line = np.linspace(75, 135, 50)
iq_s = (iq_line - scaler.mean_[0]) / scaler.scale_[0]
cg_s = -(w[0] * iq_s + b) / w[1]
cg_line = cg_s * scaler.scale_[1] + scaler.mean_[1]
fig.add_trace(go.Scatter(x=iq_line, y=cg_line, mode="lines", name="learned boundary", line=dict(color=PURPLE, width=4)), 1, 2)

for col in (1, 2):
    fig.update_xaxes(title_text="IQ", range=[73, 137], row=1, col=col)
    fig.update_yaxes(title_text="CGPA", range=[4.8, 10.0], row=1, col=col)
fig.update_layout(template="simple_white", width=1300, height=600, font=dict(family="Latin Modern Roman", size=17),
                  legend=dict(orientation="h", x=0.25, y=-0.18), margin=dict(l=70, r=20, t=80, b=110))
fig.update_annotations(font_size=19)
fig.add_annotation(x=1, y=-0.3, xref="paper", yref="paper", xanchor="right", showarrow=False,
                   text="example data", font=dict(size=13, color=GREY))
fig.write_image(here / "two_approaches.png", scale=2)
fig.write_image(here / "two_approaches.pdf")
print("KNN:", knn_answer, "| neighbours:", X[idx[0]].round(1).tolist(), y[idx[0]].tolist(), "| logistic:", log_answer)
