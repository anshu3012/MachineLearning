"""Titanic ages: the 1046 known ages (population) and our random sample of 25 (random_state=0), as density
histograms, with the H0 value 35 and the two means marked."""
from pathlib import Path
import pandas as pd
import seaborn as sns
import seaborn.objects as so

here = Path(__file__).parent
data = here.parent / "data"
ages = pd.concat([pd.read_csv(data / "titanic_train.csv"), pd.read_csv(data / "titanic_test.csv")]).Age.dropna().reset_index(drop=True)
sample = ages.sample(25, random_state=0)
df = pd.concat([pd.DataFrame({"Age": ages, "group": "all 1046 passengers"}),
                pd.DataFrame({"Age": sample, "group": "our sample of 25"})], ignore_index=True)
lines = pd.DataFrame({
    "Age": [35, 35, ages.mean(), ages.mean(), sample.mean(), sample.mean()],
    "y": [0, 0.045] * 3,
    "line": [r"$H_0$: $\mu = 35$"] * 2 + [f"true mean {ages.mean():.2f}"] * 2 + [f"sample mean {sample.mean():.2f}"] * 2,
})
THEME = {**sns.axes_style("whitegrid"), "font.family": "Latin Modern Roman", "font.size": 15,
         "axes.labelsize": 15, "xtick.labelsize": 14, "ytick.labelsize": 14, "legend.fontsize": 14, "mathtext.fontset": "cm"}
plot = (
    so.Plot(df, x="Age")
    .add(so.Bars(alpha=0.55, edgewidth=0.5), so.Hist(stat="density", binwidth=5, common_norm=False), color="group")
    .add(so.Line(linewidth=2.5, color="black"), data=lines, x="Age", y="y", linestyle="line", group="line")
    .scale(color={"all 1046 passengers": "#4C78A8", "our sample of 25": "#F58518"},
           linestyle={r"$H_0$: $\mu = 35$": "-", f"true mean {ages.mean():.2f}": ":",
                      f"sample mean {sample.mean():.2f}": "--"})
    .label(x="Age (years)", y="Density", color="", linestyle="")
    .layout(size=(9, 4.6))
    .theme(THEME)
)
plot.save(here / "titanic_age_sample.png", dpi=200, bbox_inches="tight")
plot.save(here / "titanic_age_sample.pdf", bbox_inches="tight")
