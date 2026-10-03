"""Distances from one point to 500 random points, in 2, 10, 100 and 1000 columns (Seaborn objects).
Each distance is divided by the average distance, so the panels share one scale."""
from pathlib import Path
import numpy as np
import pandas as pd
import seaborn.objects as so

here = Path(__file__).parent
rng = np.random.default_rng(0)
rows = []
for d in (2, 10, 100, 1000):
    pts = rng.uniform(0, 1, (501, d))
    dist = np.linalg.norm(pts[1:] - pts[0], axis=1)
    print(f"{d:5d} columns: farthest / nearest = {dist.max() / dist.min():.1f}")
    rows += [{"columns": f"{d} columns (farthest is {dist.max() / dist.min():.1f}× the nearest)",
              "distance": x / dist.mean()} for x in dist]
df = pd.DataFrame(rows)
font = {"font.family": "Latin Modern Roman", "font.size": 15, "axes.titlesize": 15}
plot = (so.Plot(df, x="distance")
        .facet(col="columns", wrap=2)
        .add(so.Bars(color="#4C78A8"), so.Hist(binwidth=0.1, stat="percent", common_norm=False))
        .limit(x=(0, 2.2))
        .label(x="Distance ÷ average distance", y="% of points")
        .layout(size=(10, 6.2))
        .theme({**so.Plot.config.theme, **font, "axes.spines.top": False, "axes.spines.right": False,
                "axes.facecolor": "white", "axes.edgecolor": "#6B6B6B", "axes.grid": False}))
plot.save(here / "distances.png", dpi=200, bbox_inches="tight")
plot.save(here / "distances.pdf", bbox_inches="tight")
