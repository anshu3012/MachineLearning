"""Petal width of the three iris species: KDE (top) and empirical CDF (bottom). The rule
'0.7 < width <= 1.7: versicolor, width > 1.7: virginica' comes from the KDEs; the ECDFs at 1.7 say how often it is right."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from scipy import stats
from sklearn.datasets import load_iris

here = Path(__file__).parent
iris = load_iris()
pw = iris.data[:, 3]
colours = {"setosa": "#4C78A8", "versicolor": "#F58518", "virginica": "#54A24B"}
grid = np.linspace(0, 2.8, 500)
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                    subplot_titles=["KDE: where each species is dense", "Empirical CDF: share of the species at or below x"])
for k, name in enumerate(iris.target_names):
    v = np.sort(pw[iris.target == k])
    fig.add_scatter(x=grid, y=stats.gaussian_kde(v)(grid), mode="lines", name=name,
                    line=dict(color=colours[name], width=3.5), row=1, col=1)
    ecdf = np.arange(1, len(v) + 1) / len(v)
    fig.add_scatter(x=np.r_[0, v, 2.8], y=np.r_[0, ecdf, 1], mode="lines", showlegend=False,
                    line=dict(color=colours[name], width=3.5, shape="hv"), row=2, col=1)
for x0 in (0.7, 1.7):
    fig.add_vline(x=x0, line=dict(color="#6B6B6B", width=2, dash="dash"), row="all", col=1)
share_v = np.mean(pw[iris.target == 1] <= 1.7)
share_g = np.mean(pw[iris.target == 2] <= 1.7)
fig.add_annotation(x=1.7, y=share_v, text=f"versicolor: {share_v:.0%} at or below 1.7", ax=0.75, ay=0.8, axref="x2", ayref="y2", xanchor="left",
                   font=dict(size=16, color=colours["versicolor"]), arrowcolor=colours["versicolor"], row=2, col=1)
fig.add_annotation(x=1.7, y=share_g, text=f"virginica: {share_g:.0%} at or below 1.7", ax=2.0, ay=0.2, axref="x2", ayref="y2", xanchor="left",
                   font=dict(size=16, color=colours["virginica"]), arrowcolor=colours["virginica"], row=2, col=1)
fig.update_xaxes(title_text="petal width (cm)", dtick=0.5, row=2, col=1)
fig.update_yaxes(title_text="density", row=1, col=1)
fig.update_yaxes(title_text="share ≤ x", range=[0, 1.05], row=2, col=1)
fig.update_annotations(selector=dict(xref="paper"), font_size=18)
fig.update_layout(template="simple_white", width=1000, height=680, legend=dict(x=0.8, y=0.98, font=dict(size=16)),
                  font=dict(family="Latin Modern Roman", size=16), margin=dict(l=70, r=20, t=40, b=50))
fig.write_image(here / "petal_width_cdf.png", scale=2)
fig.write_image(here / "petal_width_cdf.pdf")
