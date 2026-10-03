"""Note 79 figures (Plotly): softmax turns scores into probabilities; decision regions of softmax regression on iris."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

here = Path(__file__).parent
font = dict(family="Latin Modern Roman", size=16)
cols = ["#4C78A8", "#F58518", "#54A24B"]

z = np.array([2.815, 1.840, -4.655])       # the query flower's three scores (computed below)
p = np.exp(z) / np.exp(z).sum()
names = ["setosa", "versicolor", "virginica"]
fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.08, column_widths=[0.34, 0.32, 0.34],
                    subplot_titles=("1. scores z (any number)", "2. e to the power z (positive)", "3. divide by the total: probabilities"))
fig.add_trace(go.Bar(x=names, y=z, marker_color=cols, text=[f"{v:.2f}".replace("-", "−") for v in z], textposition="outside"), 1, 1)
fig.add_trace(go.Bar(x=names, y=np.exp(z), marker_color=cols, text=[f"{v:.2f}" for v in np.exp(z)], textposition="outside"), 1, 2)
fig.add_trace(go.Bar(x=names, y=p, marker_color=cols, text=[f"{v:.3f}" for v in p], textposition="outside"), 1, 3)
fig.update_yaxes(range=[-6, 4.5], row=1, col=1)
fig.update_yaxes(range=[0, 20], row=1, col=2)
fig.update_yaxes(range=[0, 1.1], row=1, col=3)
fig.add_annotation(x=1, y=1.02, xref="x3", yref="y3", text="sum = 1", showarrow=False, font=dict(color="#777777"))
fig.update_layout(template="simple_white", width=1150, height=440, font=font, showlegend=False, margin=dict(l=50, r=20, t=50, b=50))
fig.write_image(here / "softmax_steps.png", scale=2); fig.write_image(here / "softmax_steps.pdf")

iris = load_iris()
X, y = iris.data[:, [0, 2]], iris.target
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=2)
clf = LogisticRegression().fit(Xtr, ytr)
print("z of query", clf.decision_function([[3.4, 2.7]]).round(3))
xs, ys = np.linspace(3.0, 8.5, 300), np.linspace(0.5, 7.5, 300)
XX, YY = np.meshgrid(xs, ys)
Z = clf.predict(np.c_[XX.ravel(), YY.ravel()]).reshape(XX.shape)
fig = go.Figure(go.Heatmap(x=xs, y=ys, z=Z, colorscale=[[0, "#DCE6F2"], [0.5, "#FDE5CC"], [1, "#DDEFD9"]], showscale=False, hoverinfo="skip"))
for k in range(3):
    fig.add_trace(go.Scatter(x=X[y == k, 0], y=X[y == k, 1], mode="markers", marker=dict(color=cols[k], size=8, line=dict(color="white", width=0.5)),
                             name=names[k]))
fig.add_trace(go.Scatter(x=[3.4], y=[2.7], mode="markers+text", marker=dict(symbol="star", size=16, color="black"),
                         text=["query (3.4, 2.7): setosa 0.73,<br>versicolor 0.27, virginica 0.0004"], textposition="middle right",
                         textfont=dict(size=13), showlegend=False))
fig.update_layout(template="simple_white", width=900, height=560, font=font, margin=dict(l=60, r=20, t=30, b=60),
                  legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.85)"),
                  xaxis=dict(title="sepal length (cm)", range=[3.0, 8.5]), yaxis=dict(title="petal length (cm)", range=[0.5, 7.5]))
fig.write_image(here / "regions.png", scale=2); fig.write_image(here / "regions.pdf")
