"""Titanic fares: the population of 1308 known fares (right-skewed) against the means of 100 samples of 50
passengers (close to a bell). Same sampling as the Notebook."""
from pathlib import Path
import numpy as np
import pandas as pd
import seaborn as sns
import seaborn.objects as so

here = Path(__file__).parent
data = here.parent / "data"
df = pd.concat([pd.read_csv(data / "titanic_train.csv").drop(columns="Survived"),
                pd.read_csv(data / "titanic_test.csv")]).sample(frac=1, random_state=42)
fare = df["Fare"].dropna()
rng = np.random.default_rng(42)
means = np.array([fare.sample(50, random_state=rng).mean() for _ in range(100)])
long = pd.concat([pd.DataFrame({"fare": fare, "panel": "population: 1308 fares"}),
                  pd.DataFrame({"fare": means, "panel": "100 sample means, n = 50"})], ignore_index=True)
plot = (
    so.Plot(long, x="fare", color="panel")
    .facet(col="panel")
    .add(so.Bars(alpha=0.45), so.Hist(stat="density", binwidth=5, common_norm=False), legend=False)
    .add(so.Line(linewidth=3), so.KDE(common_norm=False, cut=0), legend=False)
    .limit(x=(0, 150))
    .scale(color={"population: 1308 fares": "#F58518", "100 sample means, n = 50": "#54A24B"})
    .label(x="fare (pounds); fares above 150 not shown", y="density", col="")
    .layout(size=(11, 4))
    .theme({**sns.axes_style("whitegrid"), "font.family": "Latin Modern Roman", "font.size": 14,
            "axes.titlesize": 16, "axes.labelsize": 15})
)
plot.save(here / "fare_clt.png", dpi=200, bbox_inches="tight")
plot.save(here / "fare_clt.pdf", bbox_inches="tight")
