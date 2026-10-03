"""What the trained logistic regression learned: its boundary, and how it does on the 10 test students."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from toy_model import load

here = Path(__file__).parent
df, X_train, X_test, y_train, y_test, scaler, clf = load()
g_c, g_i = np.meshgrid(np.linspace(3, 9, 300), np.linspace(30, 240, 300))
grid = pd.DataFrame({"cgpa": g_c.ravel(), "iq": g_i.ravel()})      # same column names as training
zz = clf.predict(scaler.transform(grid)).reshape(g_c.shape)
pred = clf.predict(scaler.transform(X_test))
right = pred == y_test.values

fig = go.Figure()
fig.add_trace(go.Contour(x=g_c[0], y=g_i[:, 0], z=zz, showscale=False, opacity=0.25, hoverinfo="skip",
                         colorscale=[[0, "#E45756"], [1, "#54A24B"]], contours=dict(start=0.5, end=0.5, size=1)))
for label, colour, name in [(1, "#54A24B", "placed (training)"), (0, "#E45756", "not placed (training)")]:
    m = y_train.values == label
    fig.add_trace(go.Scatter(x=X_train.cgpa[m], y=X_train.iq[m], mode="markers", name=name,
                             marker=dict(color=colour, size=8, opacity=0.6)))
fig.add_trace(go.Scatter(x=X_test.cgpa[right], y=X_test.iq[right], mode="markers", name="test student: predicted right",
                         marker=dict(symbol="star", size=17, color="#4C78A8", line=dict(color="black", width=1))))
fig.add_trace(go.Scatter(x=X_test.cgpa[~right], y=X_test.iq[~right], mode="markers", name="test student: predicted wrong",
                         marker=dict(symbol="x", size=17, color="black")))
fig.update_layout(template="simple_white", width=1000, height=600, font=dict(family="Latin Modern Roman", size=17),
                  title=dict(text=f"The trained model: test accuracy {right.mean():.0%} ({right.sum()} of {right.size} right)", x=0.5),
                  xaxis=dict(title="CGPA", range=[3, 9]), yaxis=dict(title="IQ", range=[30, 240]),
                  legend=dict(x=1.01, y=1), margin=dict(l=70, r=20, t=70, b=60))
fig.write_image(here / "decision_boundary.png", scale=2)
fig.write_image(here / "decision_boundary.pdf")
print("test accuracy", right.mean())
