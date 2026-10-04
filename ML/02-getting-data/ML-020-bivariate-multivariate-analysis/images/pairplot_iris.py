"""Iris: pair plot of the four measurements, coloured by species (histograms on the diagonal)."""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import load, save_px, FONT, BLUE, ORANGE, GREEN

iris = load("iris")
cols = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
colours = {"setosa": BLUE, "versicolor": ORANGE, "virginica": GREEN}
n = len(cols)
fig = make_subplots(rows=n, cols=n, horizontal_spacing=0.03, vertical_spacing=0.03)
for i, yc in enumerate(cols):
    for j, xc in enumerate(cols):
        for k, (sp, c) in enumerate(colours.items()):
            d = iris[iris.species == sp]
            first = i == 0 and j == 0
            if i == j:  # a column against itself: show its distribution instead
                tr = go.Histogram(x=d[xc], marker_color=c, opacity=0.6, xbins=dict(start=iris[xc].min(), end=iris[xc].max(), size=(iris[xc].max() - iris[xc].min()) / 15), name=sp, showlegend=first)
            else:
                tr = go.Scatter(x=d[xc], y=d[yc], mode="markers", marker=dict(color=c, size=5, opacity=0.75),
                                name=sp, showlegend=False)
            fig.add_trace(tr, i + 1, j + 1)
        if i == n - 1:
            fig.update_xaxes(title_text=xc.replace("_", " "), row=i + 1, col=j + 1)
        if j == 0:
            fig.update_yaxes(title_text=yc.replace("_", " "), row=i + 1, col=j + 1)
fig.update_layout(template="simple_white", barmode="overlay", width=1000, height=950, font={**FONT, "size": 15},
                  title=dict(text="Iris: every pair of measurements", x=0.5),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.08),
                  margin=dict(l=70, r=20, t=70, b=110))
save_px(fig, "pairplot_iris")
