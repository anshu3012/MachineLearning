"""Titanic: survival rate (%) by class, sex and port of boarding (groupby + mean x 100)."""
import pandas as pd
import seaborn.objects as so
from common import load, save_so, THEME, BLUE

t = load("titanic_train")
t["Pclass"] = t.Pclass.map({1: "1st", 2: "2nd", 3: "3rd"})
t["Embarked"] = t.Embarked.map({"C": "Cherbourg", "Q": "Queenstown", "S": "Southampton"})
names = {"Pclass": "Ticket class", "Sex": "Sex", "Embarked": "Port of boarding"}
rows = [(names[c], str(k), v * 100) for c in names for k, v in t.groupby(c)["Survived"].mean().items()]
d = pd.DataFrame(rows, columns=["column", "group", "rate"])
d["label"] = d.rate.map(lambda v: f"{v:.0f}%")
plot = (
    so.Plot(d, x="rate", y="group")
    .facet(row="column")
    .share(y=False)
    .add(so.Bar(color=BLUE, alpha=0.8))
    .add(so.Text(halign="left", fontsize=13, offset=6), text="label")
    .limit(x=(0, 90))
    .label(x="Survived (%)", y="", row="")
    .layout(size=(8, 6.6))
    .theme(THEME)
)
save_so(plot, "survival_rates")
