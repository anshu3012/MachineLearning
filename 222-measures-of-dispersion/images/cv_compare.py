"""Coefficient of variation: Titanic ages and fares, each divided by its own mean, so both are on one scale."""
from pathlib import Path
import pandas as pd
import seaborn as sns
import seaborn.objects as so

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "titanic_train.csv")
rows = []
for col in ["Age", "Fare"]:
    v = df[col].dropna()
    cv = v.std() / v.mean() * 100
    rows.append(pd.DataFrame({"relative": (v / v.mean()).clip(upper=4.99),     # fares above 5x the mean go in the last bin
                              "column": f"{col}: CV = {cv:.0f}%"}))
long = pd.concat(rows)
plot = (
    so.Plot(long, x="relative", color="column")
    .facet(row="column")
    .add(so.Bars(), so.Hist(stat="percent", binwidth=0.25, binrange=(0, 5), common_norm=False), legend=False)
    .scale(color=["#4C78A8", "#F58518"])
    .label(x="value ÷ column mean  (1 = the mean)", y="% of passengers", row="", color="")
    .layout(size=(8, 5.5))
    .theme({**sns.axes_style("whitegrid"), "font.family": "Latin Modern Roman", "font.size": 14,
            "axes.titlesize": 15, "axes.labelsize": 15})
)
plot.save(here / "cv_compare.png", dpi=200, bbox_inches="tight")
plot.save(here / "cv_compare.pdf", bbox_inches="tight")
