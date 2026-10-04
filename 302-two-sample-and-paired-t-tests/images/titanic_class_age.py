"""Titanic: random samples of 40 first-class and 40 third-class ages (random_state=5), each dot one passenger,
with the sample mean and its 95% confidence interval."""
from pathlib import Path
import pandas as pd
import seaborn as sns
import seaborn.objects as so

here = Path(__file__).parent
data = here.parent / "data"
t = pd.concat([pd.read_csv(data / "titanic_train.csv"), pd.read_csv(data / "titanic_test.csv")])
first = t[t.Pclass == 1].Age.dropna().reset_index(drop=True).sample(40, random_state=5)
third = t[t.Pclass == 3].Age.dropna().reset_index(drop=True).sample(40, random_state=5)
df = pd.concat([pd.DataFrame({"Class": "first class", "Age": first}),
                pd.DataFrame({"Class": "third class", "Age": third})], ignore_index=True)
THEME = {**sns.axes_style("whitegrid"), "font.family": "Latin Modern Roman", "font.size": 15,
         "axes.labelsize": 15, "xtick.labelsize": 15, "ytick.labelsize": 14}
plot = (
    so.Plot(df, x="Class", y="Age")
    .add(so.Dots(pointsize=7, alpha=0.6), so.Jitter(0.35, seed=0), color="Class", legend=False)
    .add(so.Range(color="black", linewidth=2.5), so.Est("mean", errorbar=("ci", 95), seed=0))
    .add(so.Dot(color="black", pointsize=11), so.Agg("mean"))
    .scale(color={"first class": "#4C78A8", "third class": "#F58518"})
    .label(x="", y="Age (years)", color="")
    .layout(size=(6, 4.6))
    .theme(THEME)
)
plot.save(here / "titanic_class_age.png", dpi=200, bbox_inches="tight")
plot.save(here / "titanic_class_age.pdf", bbox_inches="tight")
