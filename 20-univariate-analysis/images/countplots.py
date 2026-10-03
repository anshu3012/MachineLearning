"""Count plots of four categorical Titanic columns: how many passengers fall in each group."""
from pathlib import Path
import pandas as pd
import seaborn as sns
import seaborn.objects as so

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "titanic_train.csv")
cols = ["Survived", "Pclass", "Sex", "Embarked"]
# long table: one row per (column, group) with its count
counts = pd.concat(
    [df[c].astype(str).value_counts().sort_index().rename_axis("group").reset_index().assign(column=c) for c in cols], ignore_index=True
)
plot = (
    so.Plot(counts, x="group", y="count", text="count")
    .facet(col="column", wrap=2, order=cols)
    .share(x=False)
    .add(so.Bar(color="#4C78A8", alpha=0.85))
    .add(so.Text(valign="bottom", offset=3, fontsize=13))
    .limit(y=(0, 730))
    .label(x="", y="Passengers", title="{}".format)
    .layout(size=(8, 6.5))
    .theme({**sns.axes_style("whitegrid"), "font.family": "Latin Modern Roman", "font.size": 14,
            "axes.titlesize": 15, "axes.labelsize": 15})
)
plot.save(here / "countplots.png", dpi=200, bbox_inches="tight")
plot.save(here / "countplots.pdf", bbox_inches="tight")
