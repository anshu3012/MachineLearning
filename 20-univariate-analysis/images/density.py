"""Titanic ages: a density histogram with the smooth KDE curve on top (what seaborn's old distplot drew)."""
from pathlib import Path
import pandas as pd
import seaborn as sns
import seaborn.objects as so

here = Path(__file__).parent
age = pd.read_csv(here.parent / "data" / "titanic_train.csv")["Age"].dropna().to_frame()
plot = (
    so.Plot(age, x="Age")
    .add(so.Bars(color="#4C78A8", alpha=0.45), so.Hist(stat="density", binwidth=5, binrange=(0, 80)))
    .add(so.Line(color="#F58518", linewidth=3), so.KDE(cut=0))
    .label(x="Age (years)", y="Density", title="Histogram (bars) and KDE curve (line) of 714 ages")
    .layout(size=(8, 4.6))
    .theme({**sns.axes_style("whitegrid"), "font.family": "Latin Modern Roman", "font.size": 14,
            "axes.titlesize": 15, "axes.labelsize": 15})
)
plot.save(here / "density.png", dpi=200, bbox_inches="tight")
plot.save(here / "density.pdf", bbox_inches="tight")
