"""Two students with few study hours and very high marks pull the regression line. Example data."""
from pathlib import Path
import numpy as np
import pandas as pd
import seaborn as sns
import seaborn.objects as so

here = Path(__file__).parent
rng = np.random.default_rng(7)
x = rng.uniform(2, 12, 25)
y = 6 * x + 20 + rng.normal(0, 3.5, 25)
xo, yo = np.array([1.5, 2.2]), np.array([93.0, 96.0])   # two outliers: few hours, top marks
pts = pd.DataFrame({"x": np.r_[x, xo], "y": np.r_[y, yo],
                    "point": ["student"] * 25 + ["outlier"] * 2})

grid = np.linspace(0.5, 12.5, 50)
fit = lambda a, b: np.polyval(np.polyfit(a, b, 1), grid)
with_o = pd.DataFrame({"x": grid, "y": fit(pts.x, pts.y)})
without = pd.DataFrame({"x": grid, "y": fit(x, y)})
labels = pd.DataFrame({"x": [6.6, 6.6], "y": [36, 29],
                       "text": ["green: fitted without the outliers", "red: fitted with the outliers"]})

plot = (
    so.Plot()
    .add(so.Line(linewidth=3, color="#E45756"), data=with_o, x="x", y="y")
    .add(so.Line(linewidth=3, color="#54A24B"), data=without, x="x", y="y")
    .add(so.Text(fontsize=14, halign="left", color="#54A24B"), data=labels[:1], x="x", y="y", text="text")
    .add(so.Text(fontsize=14, halign="left", color="#E45756"), data=labels[1:], x="x", y="y", text="text")
    .add(so.Dot(pointsize=10), data=pts, x="x", y="y", color="point")
    .scale(color={"student": "#4C78A8", "outlier": "#E45756"})
    .label(x="study hours per week", y="marks", color="",
           title="Two outliers pull the regression line  (example data)")
    .layout(size=(8.5, 5))
    .theme({**sns.axes_style("whitegrid"), "font.family": "Latin Modern Roman", "font.size": 14,
            "axes.titlesize": 15, "axes.labelsize": 15})
)
plot.save(here / "hours_marks.png", dpi=200, bbox_inches="tight")
plot.save(here / "hours_marks.pdf", bbox_inches="tight")
