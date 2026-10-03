"""Still charts for Note 24 (Social Network Ads, training set): scatter, KDE and outliers, before vs after StandardScaler."""
from pathlib import Path
import numpy as np
import pandas as pd
import seaborn as sns
import seaborn.objects as so
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

here = Path(__file__).parent
BLUE, ORANGE, RED = "#4C78A8", "#F58518", "#E45756"
STAGES = ["Before scaling", "After scaling"]
THEME = {**sns.axes_style("whitegrid"), "font.family": "Latin Modern Roman", "font.size": 14,
         "axes.titlesize": 15, "axes.labelsize": 15}


def before_after(df):
    """Training set before and after StandardScaler, stacked into one long table with a 'stage' column."""
    X = df.drop(columns="Purchased")
    X_train, _, _, _ = train_test_split(X, df["Purchased"], test_size=0.3, random_state=0)
    scaled = pd.DataFrame(StandardScaler().fit_transform(X_train), columns=X.columns, index=X_train.index)
    return pd.concat([X_train.assign(stage=STAGES[0]), scaled.assign(stage=STAGES[1])])


def save(plot, name):
    plot = plot.theme(THEME)
    plot.save(here / f"{name}.png", dpi=200, bbox_inches="tight")
    plot.save(here / f"{name}.pdf", bbox_inches="tight")


df = pd.read_csv(here.parent / "data" / "Social_Network_Ads.csv").iloc[:, 2:]
both = before_after(df).rename(columns={"EstimatedSalary": "Salary"}).reset_index()

# 1. scatter: same cloud, new numbers on the axes
save(so.Plot(both, x="Age", y="Salary")
     .facet(col="stage", order=STAGES).share(x=False, y=False)
     .add(so.Dot(color=BLUE, pointsize=4, alpha=0.6))
     .label(col="", x="Age", y="Estimated salary")
     .layout(size=(10, 4.2)), "scatter_before_after")

# 2. KDE of both columns on one axis: before, salary is a flat line; after, the two curves overlap
long = both.melt(id_vars=["index", "stage"], value_vars=["Age", "Salary"], var_name="Column", value_name="value")
save(so.Plot(long, x="value", color="Column")
     .facet(col="stage", order=STAGES).share(x=False, y=False)
     .add(so.Line(linewidth=2.5), so.KDE(common_grid=False, common_norm=False))
     .scale(color={"Age": BLUE, "Salary": ORANGE})
     .label(col="", x="value", y="Density")
     .layout(size=(10, 4.2)), "kde_before_after")

# 3. each column alone: the shape of the curve does not change, only the numbers on the x axis
save(so.Plot(long, x="value", color="Column")
     .facet(col="stage", row="Column", order={"col": STAGES}).share(x=False, y=False)
     .add(so.Line(linewidth=2.5), so.KDE(common_grid=False, common_norm=False))
     .scale(color={"Age": BLUE, "Salary": ORANGE})
     .label(col="", row="", x="value", y="Density")
     .layout(size=(10, 6.4)), "shape_unchanged")

# 4. three made-up extreme users: after scaling they are just as far from the rest
extra = pd.DataFrame({"Age": [5, 90, 95], "EstimatedSalary": [1000, 250000, 350000], "Purchased": [0, 1, 1]})
out = before_after(pd.concat([df, extra], ignore_index=True)).rename(columns={"EstimatedSalary": "Salary"})
out["point"] = np.where(out.index >= len(df), "added outlier", "normal user")
save(so.Plot(out.reset_index(), x="Age", y="Salary", color="point")
     .facet(col="stage", order=STAGES).share(x=False, y=False)
     .add(so.Dot(pointsize=5, alpha=0.8))
     .scale(color={"normal user": BLUE, "added outlier": RED})
     .label(col="", x="Age", y="Estimated salary", color="")
     .layout(size=(10, 4.2)), "outliers")
