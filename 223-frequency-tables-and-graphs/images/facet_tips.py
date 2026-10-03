"""A facet grid: one scatter plot of bill vs tip per meal time, smokers by colour: four columns in one figure."""
from pathlib import Path
import pandas as pd
import seaborn as sns
import seaborn.objects as so

here = Path(__file__).parent
tips = pd.read_csv(here.parent / "data" / "tips.csv")
plot = (
    so.Plot(tips, x="total_bill", y="tip", color="smoker")
    .facet(col="time", order=["Lunch", "Dinner"])
    .add(so.Dot(pointsize=6, alpha=0.8))
    .scale(color={"No": "#4C78A8", "Yes": "#F58518"})
    .label(x="total bill", y="tip", color="smoker", col="")
    .layout(size=(10, 4.5))
    .theme({**sns.axes_style("whitegrid"), "font.family": "Latin Modern Roman", "font.size": 14,
            "axes.titlesize": 16, "axes.labelsize": 15, "legend.fontsize": 14, "legend.title_fontsize": 14})
)
plot.save(here / "facet_tips.png", dpi=200, bbox_inches="tight")
plot.save(here / "facet_tips.pdf", bbox_inches="tight")
