"""The dataset built from the TVmaze API: how the 1,208 shows are rated."""
from pathlib import Path
import pandas as pd
import seaborn as sns
import seaborn.objects as so

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "shows.csv")
rated = df.dropna(subset=["rating.average"])
plot = (
    so.Plot(rated, x="rating.average")
    .add(so.Bars(color="#4C78A8", alpha=0.85), so.Hist(binwidth=0.2))
    .label(x="Average viewer rating (out of 10)", y="Number of shows",
           title=f"{len(df):,} shows fetched, {len(rated):,} with a rating")
    .layout(size=(8, 4.5))
    .theme({**sns.axes_style("whitegrid"), "font.family": "Latin Modern Roman", "font.size": 14,
            "axes.titlesize": 15, "axes.labelsize": 15})
)
plot.save(here / "ratings.png", dpi=200, bbox_inches="tight")
plot.save(here / "ratings.pdf", bbox_inches="tight")
