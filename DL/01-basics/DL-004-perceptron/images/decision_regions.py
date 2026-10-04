"""scikit-learn's Perceptron on the 100 placement students: its line and two regions, on raw and on standardized
inputs (Plotly, replaces mlxtend's plot_decision_regions)."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.linear_model import Perceptron
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "placement.csv")
X, y = df[["cgpa", "resume_score"]], df["placed"]
models = [Perceptron(random_state=0).fit(X, y), make_pipeline(StandardScaler(), Perceptron(random_state=0)).fit(X, y)]
titles = [f"Raw inputs: accuracy {models[0].score(X, y):.0%}", f"Standardized inputs: accuracy {models[1].score(X, y):.0%}"]

gx, gy = np.meshgrid(np.linspace(5, 9.6, 300), np.linspace(4.8, 9.3, 300))
grid = pd.DataFrame({"cgpa": gx.ravel(), "resume_score": gy.ravel()})
fig = make_subplots(rows=1, cols=2, subplot_titles=titles, horizontal_spacing=0.08)
for c, model in enumerate(models, start=1):
    zz = model.predict(grid).reshape(gx.shape)
    fig.add_trace(go.Contour(x=gx[0], y=gy[:, 0], z=zz, showscale=False, opacity=0.25, hoverinfo="skip",
                             colorscale=[[0, "#E45756"], [1, "#54A24B"]], contours=dict(start=0.5, end=0.5, size=1),
                             line=dict(color="black", width=3)), row=1, col=c)
    for label, colour, name in [(1, "#54A24B", "placed"), (0, "#E45756", "not placed")]:
        m = y == label
        fig.add_trace(go.Scatter(x=X.cgpa[m], y=X.resume_score[m], mode="markers", name=name, showlegend=c == 1,
                                 marker=dict(color=colour, size=8, line=dict(color="white", width=1))), row=1, col=c)
    fig.update_xaxes(title_text="CGPA", range=[5, 9.6], row=1, col=c)
    fig.update_yaxes(title_text="Resume score" if c == 1 else None, range=[4.8, 9.3], row=1, col=c)
fig.update_layout(template="simple_white", width=1200, height=620, font=dict(family="Latin Modern Roman", size=18),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.16), margin=dict(l=70, r=20, t=60, b=110))
fig.update_annotations(font_size=21)
fig.write_image(here / "decision_regions.png", scale=2)
fig.write_image(here / "decision_regions.pdf")
p = models[0]
print("raw", p.coef_, p.intercept_, "scaled", models[1][-1].coef_, models[1][-1].intercept_)
