"""A non-representative sample tells the wrong story. Simulated data."""
from pathlib import Path
import numpy as np
import pandas as pd
import seaborn as sns
import seaborn.objects as so

here = Path(__file__).parent
rng = np.random.default_rng(2)
true = lambda x: 30 + 12 * x - 1.1 * x ** 2      # the real relationship: rises, then falls
x_all = rng.uniform(0, 10, 160)
y_all = true(x_all) + rng.normal(0, 4, x_all.size)
in_sample = (x_all > 1) & (x_all < 3.5)          # we only collected data from one narrow range

slope, intercept = np.polyfit(x_all[in_sample], y_all[in_sample], 1)
xs = np.linspace(0, 10, 100)
points = pd.DataFrame({"x": x_all, "y": y_all,
                       "Data": np.where(in_sample, "our sample", "data we never collected")})
lines = pd.concat([pd.DataFrame({"x": xs, "y": slope * xs + intercept, "Line": "fitted to our sample"}),
                   pd.DataFrame({"x": xs, "y": true(xs), "Line": "the real pattern"})], ignore_index=True)

labels = pd.DataFrame({"x": [9.6, 9.6], "y": [slope * 9.6 + intercept, true(9.6) - 9],
                       "t": ["fitted to our sample", "the real pattern"], "Line": ["fitted to our sample", "the real pattern"]})

plot = (
    so.Plot(points, x="x", y="y")
    .add(so.Dot(pointsize=7), color="Data")
    .add(so.Line(linewidth=3.5), data=lines, x="x", y="y", color="Line", legend=False)
    .add(so.Text(halign="right", valign="bottom", fontsize=14, offset=6), data=labels, x="x", y="y", text="t", color="Line", legend=False)
    .scale(color={"our sample": "#4C78A8", "data we never collected": "#C8C8C8",
                  "fitted to our sample": "#F58518", "the real pattern": "#54A24B"})
    .limit(y=(0, 110))
    .label(x="Input", y="Output", color="",
           title="A small, one-sided sample suggests the wrong pattern  (simulated data)")
    .layout(size=(9, 5))
    .theme({**sns.axes_style("whitegrid"), "font.family": "Latin Modern Roman", "font.size": 14,
            "axes.titlesize": 15, "axes.labelsize": 15})
)
plot.save(here / "non_representative.png", dpi=200, bbox_inches="tight")
plot.save(here / "non_representative.pdf", bbox_inches="tight")
