"""150 iris flowers as feature vectors: each flower is one point (one vector) in a 3D space of three input columns."""
from pathlib import Path
import plotly.graph_objects as go
from sklearn.datasets import load_iris

here = Path(__file__).parent
iris = load_iris(as_frame=True)
X, y = iris.data, iris.target
colours = ["#4C78A8", "#F58518", "#54A24B"]
cols = ["sepal length (cm)", "sepal width (cm)", "petal length (cm)"]

fig = go.Figure()
for k, name in enumerate(iris.target_names):
    d = X[y == k]
    fig.add_trace(go.Scatter3d(x=d[cols[0]], y=d[cols[1]], z=d[cols[2]], mode="markers", name=name,
                               marker=dict(size=4, color=colours[k], opacity=0.75)))
for i, dash in [(0, "solid"), (50, "dash")]:                                       # one setosa and one versicolor, drawn as arrows from the origin
    v = X.loc[i, cols]
    fig.add_trace(go.Scatter3d(x=[0, v.iloc[0]], y=[0, v.iloc[1]], z=[0, v.iloc[2]], mode="lines+markers",
                               line=dict(color="#E45756", width=6, dash=dash), marker=dict(size=[0, 7], color="#E45756"),
                               name=f"{iris.target_names[y[i]]} flower [{v.iloc[0]}, {v.iloc[1]}, {v.iloc[2]}]"))
fig.update_layout(template="simple_white", width=900, height=650, font=dict(family="Latin Modern Roman", size=16),
                  title=dict(text="150 iris flowers = 150 feature vectors in 3D", x=0.5),
                  scene=dict(xaxis_title="sepal length", yaxis_title="sepal width", zaxis_title="petal length",
                             xaxis=dict(range=[0, 8]), yaxis=dict(range=[0, 4.5]), zaxis=dict(range=[0, 7]),
                             camera=dict(eye=dict(x=1.55, y=-1.5, z=0.75), center=dict(x=0, y=0, z=-0.12)), aspectmode="cube"),
                  legend=dict(x=0.02, y=0.98), margin=dict(l=0, r=0, t=60, b=0))
fig.write_image(here / "iris_vectors.png", scale=2)
fig.write_image(here / "iris_vectors.pdf")
