"""Titanic data: how many values are missing in each column (df.isnull().sum())."""
from pathlib import Path
import pandas as pd
import seaborn as sns
import seaborn.objects as so

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "titanic_train.csv")
miss = df.isnull().sum().rename_axis("column").reset_index(name="missing")
miss["label"] = miss["missing"].map(lambda m: f"{m} ({m / len(df):.0%})" if m else "0")
plot = (
    so.Plot(miss, x="missing", y="column", text="label")
    .add(so.Bar(color="#E45756", alpha=0.85))
    .add(so.Text(halign="left", offset=6, fontsize=13))
    .scale(x=so.Continuous().tick(at=[0, 200, 400, 600, 800]))
    .limit(x=(0, 891))
    .label(x="Missing values (out of 891 rows)", y="", title="Missing values per column")
    .layout(size=(8, 5.5))
    .theme({**sns.axes_style("whitegrid"), "font.family": "Latin Modern Roman", "font.size": 14,
            "axes.titlesize": 15, "axes.labelsize": 15})
)
plot.save(here / "missing_values.png", dpi=200, bbox_inches="tight")
plot.save(here / "missing_values.pdf", bbox_inches="tight")
