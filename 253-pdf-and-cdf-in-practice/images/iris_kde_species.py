"""One KDE per iris species for each of the four measurements: the petal measurements separate the species,
the sepal measurements overlap."""
from pathlib import Path
import pandas as pd
import seaborn as sns
import seaborn.objects as so
from sklearn.datasets import load_iris

here = Path(__file__).parent
iris = load_iris(as_frame=True)
df = iris.frame.rename(columns=lambda c: c.replace(" (cm)", ""))
df["species"] = df["target"].map(dict(enumerate(iris.target_names)))
long = df.melt(id_vars="species", value_vars=["sepal length", "sepal width", "petal length", "petal width"],
               var_name="measurement", value_name="cm")
plot = (
    so.Plot(long, x="cm", color="species")
    .facet(col="measurement", wrap=2, order=["petal length", "petal width", "sepal length", "sepal width"])
    .add(so.Area(alpha=0.25, edgewidth=2.5), so.KDE(common_norm=False))
    .share(x=True, y=False)
    .limit(x=(0, 8.5))
    .scale(color={"setosa": "#4C78A8", "versicolor": "#F58518", "virginica": "#54A24B"})
    .label(x="cm", y="density", color="species")
    .layout(size=(10, 6.2))
    .theme({**sns.axes_style("ticks"), "font.family": "Latin Modern Roman", "font.size": 14,
            "axes.titlesize": 15, "axes.labelsize": 14, "axes.spines.right": False, "axes.spines.top": False})
)
plot.save(here / "iris_kde_species.png", dpi=200, bbox_inches="tight")
plot.save(here / "iris_kde_species.pdf", bbox_inches="tight")
