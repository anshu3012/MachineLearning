"""Titanic: correlation of each numeric column with Survived (df.corr(numeric_only=True))."""
from pathlib import Path
import pandas as pd
import seaborn as sns
import seaborn.objects as so

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "titanic_train.csv")
r = df.corr(numeric_only=True)["Survived"].drop("Survived").sort_values()
d = r.rename_axis("column").reset_index(name="r")
d["sign"] = d["r"].map(lambda v: "positive" if v > 0 else "negative")
d["label"] = d["r"].map(lambda v: f"{v:+.2f}".replace("-", "\u2212"))
d["lx"] = d["r"] + d["r"].map(lambda v: 0.045 if v > 0 else -0.045)
plot = (
    so.Plot(d, x="r", y="column", color="sign")
    .add(so.Bar(alpha=0.85), legend=False)
    .add(so.Text(fontsize=13, color="black"), x="lx", text="label")
    .scale(color={"positive": "#54A24B", "negative": "#E45756"},
           x=so.Continuous().tick(at=[-0.4, -0.2, 0, 0.2, 0.4]))
    .limit(x=(-0.48, 0.38))
    .label(x="Correlation with Survived", y="", title="Which numeric columns move with survival?")
    .layout(size=(8, 4.5))
    .theme({**sns.axes_style("whitegrid"), "font.family": "Latin Modern Roman", "font.size": 14,
            "axes.titlesize": 15, "axes.labelsize": 15})
)
plot.save(here / "corr_survived.png", dpi=200, bbox_inches="tight")
plot.save(here / "corr_survived.pdf", bbox_inches="tight")
