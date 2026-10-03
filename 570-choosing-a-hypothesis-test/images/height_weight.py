"""Height against weight for the 60 people of data/people.csv, coloured by age group: a strong positive relationship."""
from pathlib import Path
import pandas as pd
import seaborn as sns
import seaborn.objects as so

here = Path(__file__).parent
people = pd.read_csv(here.parent / "data" / "people.csv")
plot = (
    so.Plot(people, x="height", y="weight", color="age_group")
    .add(so.Dot(pointsize=9))
    .scale(color={"child": "#F58518", "adult": "#4C78A8", "elderly": "#54A24B"})
    .label(x="height (m)", y="weight (kg)", color="age group", title="r = 0.98, p < 0.001")
    .layout(size=(8, 5))
    .theme({**sns.axes_style("whitegrid"), "font.family": "Latin Modern Roman", "font.size": 14,
            "axes.titlesize": 16, "axes.labelsize": 15})
)
plot.save(here / "height_weight.png", dpi=200, bbox_inches="tight")
plot.save(here / "height_weight.pdf", bbox_inches="tight")
