"""Anomaly detection: one transaction far from all the normal ones. Example data."""
from pathlib import Path
import numpy as np
import pandas as pd
import seaborn as sns
import seaborn.objects as so

here = Path(__file__).parent
rng = np.random.default_rng(5)
normal = pd.DataFrame({"Amount (thousand rupees)": rng.gamma(2.0, 1.2, 80),
                       "Distance from home (km)": rng.gamma(2.0, 2.5, 80), "Type": "normal"})
odd = pd.DataFrame({"Amount (thousand rupees)": [14.5], "Distance from home (km)": [42.0], "Type": "anomaly (flagged)"})
df = pd.concat([normal, odd], ignore_index=True)

plot = (
    so.Plot(df, x="Distance from home (km)", y="Amount (thousand rupees)", color="Type")
    .add(so.Dot(pointsize=10))
    .scale(color={"normal": "#4C78A8", "anomaly (flagged)": "#E45756"})
    .label(title="Anomaly detection: a point far from all the others  (example data)")
    .layout(size=(8.5, 5))
    .theme({**sns.axes_style("whitegrid"), "font.family": "Latin Modern Roman", "font.size": 14,
            "axes.titlesize": 15, "axes.labelsize": 15})
)
plot.save(here / "anomaly.png", dpi=200, bbox_inches="tight")
plot.save(here / "anomaly.pdf", bbox_inches="tight")
