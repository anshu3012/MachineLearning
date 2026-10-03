"""Titanic: age density for passengers who died vs survived (the old distplot(hist=False), now a KDE)."""
import seaborn.objects as so
from common import load, save_so, THEME, RED, GREEN

t = load("titanic_train").dropna(subset=["Age"])
t["Outcome"] = t.Survived.map({0: "died", 1: "survived"})
plot = (
    so.Plot(t, x="Age", color="Outcome")
    .add(so.Area(alpha=0.15, edgewidth=0), so.KDE(common_norm=False, cut=0))
    .add(so.Line(linewidth=2.5), so.KDE(common_norm=False, cut=0))
    .scale(color={"died": RED, "survived": GREEN}, x=so.Continuous().tick(every=10))
    .label(x="Age (years)", y="Density", color="", title="Children survived more often than they died")
    .layout(size=(8, 4.6))
    .theme(THEME)
)
save_so(plot, "kde_age_survival")
