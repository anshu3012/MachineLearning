"""The recipe data from train.json: how many dishes of each cuisine (the label we would predict)."""
from pathlib import Path
import pandas as pd
import seaborn as sns
import seaborn.objects as so

here = Path(__file__).parent
df = pd.read_json(here.parent / "data" / "train.json")
counts = df["cuisine"].value_counts().rename_axis("cuisine").reset_index(name="dishes")
plot = (
    so.Plot(counts, x="dishes", y="cuisine")
    .add(so.Bar(color="#4C78A8", alpha=0.85))
    .label(x="Number of dishes", y="", title=f"{len(df):,} dishes, {len(counts)} cuisines")
    .layout(size=(8, 6.5))
    .theme({**sns.axes_style("whitegrid"), "font.family": "Latin Modern Roman", "font.size": 14,
            "axes.titlesize": 15, "axes.labelsize": 15})
)
plot.save(here / "cuisines.png", dpi=200, bbox_inches="tight")
plot.save(here / "cuisines.pdf", bbox_inches="tight")
