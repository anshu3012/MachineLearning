"""Mean Titanic fare per passenger class with 95% confidence intervals as error bars (seaborn's default for an
estimated mean). Training file, 891 passengers."""
from pathlib import Path
import pandas as pd
import seaborn as sns
import seaborn.objects as so

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "titanic_train.csv")
df["class"] = df["Pclass"].map({1: "first", 2: "second", 3: "third"})
plot = (
    so.Plot(df, x="class", y="Fare")
    .add(so.Bar(color="#4C78A8", alpha=0.6), so.Agg("mean"))
    .add(so.Range(color="black", linewidth=2.5), so.Est("mean", errorbar=("ci", 95), seed=0))
    .scale(x=so.Nominal(order=["first", "second", "third"]))
    .label(x="passenger class", y="mean fare (pounds)")
    .layout(size=(6, 4))
    .theme({**sns.axes_style("whitegrid"), "font.family": "Latin Modern Roman", "font.size": 14,
            "axes.labelsize": 15})
)
plot.save(here / "error_bars.png", dpi=200, bbox_inches="tight")
plot.save(here / "error_bars.pdf", bbox_inches="tight")
