"""A few outliers pull a linear regression line away from the main pattern. Example data."""
from pathlib import Path
import numpy as np
import pandas as pd
import seaborn as sns
import seaborn.objects as so

here = Path(__file__).parent
rng = np.random.default_rng(3)
x = rng.uniform(1, 10, 25)
y = 2 * x + 3 + rng.normal(0, 1.2, 25)
xo, yo = np.array([8.5, 9.2, 9.8]), np.array([2.0, 1.0, 3.0])   # three outliers
pts = pd.DataFrame({"x": np.r_[x, xo], "y": np.r_[y, yo],
                    "point": ["normal point"] * 25 + ["outlier"] * 3})

# Least-squares lines with and without the outliers
grid = np.linspace(0, 10.5, 50)
fit = lambda a, b: np.polyval(np.polyfit(a, b, 1), grid)
lines = pd.DataFrame({"x": np.r_[grid, grid],
                      "y": np.r_[fit(pts.x, pts.y), fit(x, y)],
                      "line": ["fitted with outliers"] * 50 + ["fitted without outliers"] * 50})

# Text labels next to each line, so the legend only lists the points
labels = pd.DataFrame({"x": [0.2, 0.2], "y": [21, 18.5],
                       "text": ["green: line fitted without the outliers", "red: line fitted with the outliers"]})

plot = (
    so.Plot()
    .add(so.Line(linewidth=3, color="#E45756"), data=lines[lines.line == "fitted with outliers"], x="x", y="y")
    .add(so.Line(linewidth=3, color="#54A24B"), data=lines[lines.line == "fitted without outliers"], x="x", y="y")
    .add(so.Text(fontsize=14, halign="left", color="#54A24B"), data=labels[:1], x="x", y="y", text="text")
    .add(so.Text(fontsize=14, halign="left", color="#E45756"), data=labels[1:], x="x", y="y", text="text")
    .add(so.Dot(pointsize=10), data=pts, x="x", y="y", color="point")
    .scale(color={"normal point": "#4C78A8", "outlier": "#E45756"})
    .label(x="input column", y="output column", color="",
           title="Three outliers pull the regression line  (example data)")
    .layout(size=(8.5, 5))
    .theme({**sns.axes_style("whitegrid"), "font.family": "Latin Modern Roman", "font.size": 14,
            "axes.titlesize": 15, "axes.labelsize": 15})
)
plot.save(here / "outlier_line.png", dpi=200, bbox_inches="tight")
plot.save(here / "outlier_line.pdf", bbox_inches="tight")
