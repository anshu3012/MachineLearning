"""Titanic passengers by class and outcome: observed counts against the counts expected if class and survival were
independent. First class has far more survivors than expected, third class far fewer."""
from pathlib import Path
import pandas as pd
import seaborn as sns
import seaborn.objects as so
from scipy import stats

here = Path(__file__).parent
titanic = pd.read_csv(here.parent / "data" / "titanic_train.csv")
table = pd.crosstab(titanic["Pclass"], titanic["Survived"])
expected = stats.chi2_contingency(table).expected_freq
rows = []
for i, cls in enumerate(table.index):
    for j, outcome in enumerate(["died", "survived"]):
        rows.append(dict(cls=f"class {cls}", outcome=outcome, kind="observed", count=table.iloc[i, j]))
        rows.append(dict(cls=f"class {cls}", outcome=outcome, kind="expected if independent", count=expected[i, j]))
long = pd.DataFrame(rows)
plot = (
    so.Plot(long, x="cls", y="count", color="kind")
    .facet(col="outcome")
    .add(so.Bar(), so.Dodge())
    .scale(color={"observed": "#4C78A8", "expected if independent": "#54A24B"})
    .label(x="", y="passengers", color="")
    .layout(size=(10, 4.5))
    .theme({**sns.axes_style("whitegrid"), "font.family": "Latin Modern Roman", "font.size": 14,
            "axes.titlesize": 16, "axes.labelsize": 15})
)
plot.save(here / "titanic_class.png", dpi=200, bbox_inches="tight")
plot.save(here / "titanic_class.pdf", bbox_inches="tight")
