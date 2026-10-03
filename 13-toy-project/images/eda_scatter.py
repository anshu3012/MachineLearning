"""Exploring the placement data: CGPA vs IQ, coloured by placement."""
from pathlib import Path
import seaborn as sns
import seaborn.objects as so
from toy_model import load

here = Path(__file__).parent
df = load()[0].assign(Placed=lambda d: d.placement.map({1: "placed", 0: "not placed"}))
plot = (
    so.Plot(df, x="cgpa", y="iq", color="Placed")
    .add(so.Dot(pointsize=9))
    .scale(color={"placed": "#54A24B", "not placed": "#E45756"})
    .label(x="CGPA", y="IQ", color="", title="100 students: CGPA vs IQ")
    .layout(size=(8, 5))
    .theme({**sns.axes_style("whitegrid"), "font.family": "Latin Modern Roman", "font.size": 14,
            "axes.titlesize": 15, "axes.labelsize": 15})
)
plot.save(here / "eda_scatter.png", dpi=200, bbox_inches="tight")
plot.save(here / "eda_scatter.pdf", bbox_inches="tight")
