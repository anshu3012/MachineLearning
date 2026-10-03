"""Titanic: mean age per class, split by sex, with 95% confidence intervals (seaborn barplot defaults)."""
import seaborn.objects as so
from common import load, save_so, THEME, BLUE, ORANGE

t = load("titanic_train").assign(Class=lambda d: d.Pclass.map({1: "1st", 2: "2nd", 3: "3rd"}))
plot = (
    so.Plot(t, x="Class", y="Age", color="Sex")
    .add(so.Bar(alpha=0.8), so.Agg("mean"), so.Dodge())
    .add(so.Range(color="black", linewidth=1.6), so.Est("mean", errorbar=("ci", 95), seed=0), so.Dodge())
    .scale(color={"male": BLUE, "female": ORANGE}, x=so.Nominal(order=["1st", "2nd", "3rd"]))
    .label(x="Ticket class", y="Mean age (years)", title="Older passengers travelled in higher classes")
    .layout(size=(8, 4.8))
    .theme(THEME)
)
save_so(plot, "bar_age_class")
