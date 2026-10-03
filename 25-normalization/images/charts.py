"""Still charts for Note 25: wine data before vs after MinMaxScaler (training set), and all scalers on one small
column with an outlier."""
from pathlib import Path
import numpy as np
import pandas as pd
import seaborn as sns
import seaborn.objects as so
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler, RobustScaler, StandardScaler

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
STAGES = ["Before scaling", "After min-max scaling"]
THEME = {**sns.axes_style("whitegrid"), "font.family": "Latin Modern Roman", "font.size": 14,
         "axes.titlesize": 15, "axes.labelsize": 15}


def save(plot, name):
    plot = plot.theme(THEME)
    plot.save(here / f"{name}.png", dpi=200, bbox_inches="tight")
    plot.save(here / f"{name}.pdf", bbox_inches="tight")


df = pd.read_csv(here.parent / "data" / "wine_data.csv", header=None, usecols=[0, 1, 2])
df.columns = ["Class", "Alcohol", "Malic acid"]
X_train, _, y_train, _ = train_test_split(df.drop(columns="Class"), df["Class"], test_size=0.3, random_state=0)
scaled = pd.DataFrame(MinMaxScaler().fit_transform(X_train), columns=X_train.columns, index=X_train.index)
cls = "class " + y_train.astype(str)
both = pd.concat([X_train.assign(stage=STAGES[0], Class=cls), scaled.assign(stage=STAGES[1], Class=cls)], ignore_index=True)

# 1. scatter: same cloud, now inside the unit square
save(so.Plot(both, x="Alcohol", y="Malic acid", color="Class")
     .facet(col="stage", order=STAGES).share(x=False, y=False)
     .add(so.Dot(pointsize=5, alpha=0.8))
     .scale(color={"class 1": BLUE, "class 2": ORANGE, "class 3": GREEN})
     .label(col="", color="")
     .layout(size=(10, 4.2)), "scatter_before_after")

# 2. one small column with an outlier (130), scaled five ways, all on one shared axis
w = np.array([[32.0], [54], [60], [67], [130]])
methods = {
    "Standardization": StandardScaler().fit_transform(w),
    "Min-max": MinMaxScaler().fit_transform(w),
    "Mean normalization": (w - w.mean()) / (w.max() - w.min()),
    "Max-abs": MaxAbsScaler().fit_transform(w),
    "Robust": RobustScaler().fit_transform(w),
}
rows = pd.DataFrame([(m, v, "outlier (130)" if raw == 130 else "other values")
                     for m, vals in methods.items() for raw, v in zip(w.ravel(), vals.ravel())],
                    columns=["method", "scaled value", "point"])
save(so.Plot(rows, x="scaled value", y="method", color="point")
     .add(so.Dot(pointsize=11, alpha=0.85))
     .scale(color={"other values": BLUE, "outlier (130)": RED}, y=so.Nominal(order=list(methods)))
     .label(y="", color="")
     .limit(x=(-2.5, 5.8))
     .layout(size=(10, 4.2)), "scalers_outlier")
