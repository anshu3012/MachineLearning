"""Titanic ages: histogram with the 25%, 50% and 75% lines that df.describe() reports."""
from pathlib import Path
import pandas as pd
import seaborn as sns
import seaborn.objects as so

here = Path(__file__).parent
age = pd.read_csv(here.parent / "data" / "titanic_train.csv")["Age"].dropna()
q = age.quantile([0.25, 0.5, 0.75])
top = 125
# each quartile is a vertical line: two points (x, 0) and (x, top) in the same group
lines = pd.DataFrame([(f"{p:.0%}", v, y) for p, v in q.items() for y in (0, top)], columns=["q", "x", "y"])
# one label per line: 25% to the left, 75% to the right, 50% higher up, so they never overlap
lab = [(f"{p:.0%}: {v:.1f}".replace(".0", ""), v) for p, v in q.items()]
left = pd.DataFrame({"x": [lab[0][1]], "y": [top + 5], "t": [lab[0][0]]})
mid = pd.DataFrame({"x": [lab[1][1]], "y": [top + 17], "t": [lab[1][0]]})
right = pd.DataFrame({"x": [lab[2][1]], "y": [top + 5], "t": [lab[2][0]]})
plot = (
    so.Plot(age.to_frame(), x="Age")
    .add(so.Bars(color="#4C78A8", alpha=0.6), so.Hist(binwidth=5, binrange=(0, 80)))
    .add(so.Path(color="#F58518", linewidth=2.5, linestyle="--"), data=lines, x="x", y="y", group="q")
    .add(so.Text(color="#F58518", fontsize=13, halign="right"), data=left, x="x", y="y", text="t")
    .add(so.Text(color="#F58518", fontsize=13), data=mid, x="x", y="y", text="t")
    .add(so.Text(color="#F58518", fontsize=13, halign="left"), data=right, x="x", y="y", text="t")
    .limit(y=(0, top + 24))
    .label(x="Age (years)", y="Passengers", title="714 known ages, split into four equal groups")
    .layout(size=(8, 4.8))
    .theme({**sns.axes_style("whitegrid"), "font.family": "Latin Modern Roman", "font.size": 14,
            "axes.titlesize": 15, "axes.labelsize": 15})
)
plot.save(here / "age_quartiles.png", dpi=200, bbox_inches="tight")
plot.save(here / "age_quartiles.pdf", bbox_inches="tight")
