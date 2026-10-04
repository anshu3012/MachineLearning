"""One KDE per iris species for each of the four measurements: the petal measurements separate the species,
the sepal measurements overlap. Gaussian KDE with Scott's rule (scipy), drawn with Plotly."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from scipy.stats import gaussian_kde
from sklearn.datasets import load_iris

here = Path(__file__).parent
iris = load_iris(as_frame=True)
df = iris.frame.rename(columns=lambda c: c.replace(" (cm)", ""))
df["species"] = df["target"].map(dict(enumerate(iris.target_names)))
COLOURS = {"setosa": "#4C78A8", "versicolor": "#F58518", "virginica": "#54A24B"}
FILLS = {"setosa": "rgba(76,120,168,0.25)", "versicolor": "rgba(245,133,24,0.25)", "virginica": "rgba(84,162,75,0.25)"}
order = ["petal length", "petal width", "sepal length", "sepal width"]
x = np.linspace(0, 8.5, 500)
fig = make_subplots(rows=2, cols=2, subplot_titles=order, horizontal_spacing=0.1, vertical_spacing=0.16)
for i, m in enumerate(order):
    for sp, col in COLOURS.items():
        fig.add_scatter(x=x, y=gaussian_kde(df.loc[df.species == sp, m])(x), mode="lines", fill="tozeroy",
                        fillcolor=FILLS[sp], line=dict(color=col, width=3), name=sp, legendgroup=sp,
                        showlegend=i == 0, row=i // 2 + 1, col=i % 2 + 1)
fig.update_xaxes(range=[0, 8.5])
fig.update_xaxes(title_text="cm", row=2)
fig.update_yaxes(title_text="density", col=1)
fig.update_annotations(font_size=20)
fig.update_layout(template="simple_white", width=1000, height=640, font=dict(family="Latin Modern Roman", size=17),
                  legend=dict(title="species"), margin=dict(l=70, r=20, t=40, b=60))
fig.write_image(here / "iris_kde_species.png", scale=2)
fig.write_image(here / "iris_kde_species.pdf")
