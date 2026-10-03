"""Age of Titanic passengers by class (714 with a known age): every passenger as a jittered dot, with the class mean
and one standard deviation either side in black."""
from pathlib import Path
import pandas as pd
import seaborn as sns
import seaborn.objects as so

here = Path(__file__).parent
titanic = pd.read_csv(here.parent / "data" / "titanic_train.csv").dropna(subset=["Age"])
titanic["class"] = "class " + titanic["Pclass"].astype(str)
titanic = titanic.sort_values("class")
plot = (
    so.Plot(titanic, x="class", y="Age")
    .add(so.Dots(color="#4C78A8", alpha=0.35, pointsize=4), so.Jitter(0.6))
    .add(so.Range(color="black", linewidth=3), so.Est(errorbar="sd"))
    .add(so.Dot(color="black", pointsize=12), so.Agg())
    .label(x="", y="age (years)")
    .layout(size=(8, 4.5))
    .theme({**sns.axes_style("whitegrid"), "font.family": "Latin Modern Roman", "font.size": 14,
            "axes.labelsize": 15})
)
plot.save(here / "titanic_age_class.png", dpi=200, bbox_inches="tight")
plot.save(here / "titanic_age_class.pdf", bbox_inches="tight")
