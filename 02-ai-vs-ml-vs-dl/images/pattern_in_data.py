"""A pattern in data: marks rise with hours studied. Example data, not real."""
from pathlib import Path
import numpy as np
import pandas as pd
import seaborn as sns
import seaborn.objects as so

here = Path(__file__).parent
rng = np.random.default_rng(7)
hours = np.array([1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 7])
marks = np.clip(10 * hours + 15 + rng.normal(0, 5, hours.size), 0, 100).round()
df = pd.DataFrame({"Hours studied": hours, "Exam marks": marks})

plot = (
    so.Plot(df, x="Hours studied", y="Exam marks")
    .add(so.Dot(color="#4C78A8", pointsize=11))
    .add(so.Line(color="#F58518", linewidth=4), so.PolyFit(order=1))
    .label(title="Pattern found: about 10 extra marks per hour studied")
    .layout(size=(8, 5))
    .theme({**sns.axes_style("whitegrid"), "font.family": "Roboto", "font.size": 14,
            "axes.titlesize": 16, "axes.labelsize": 15})
)
plot.save(here / "pattern_in_data.png", dpi=200, bbox_inches="tight")
plot.save(here / "pattern_in_data.pdf", bbox_inches="tight")
