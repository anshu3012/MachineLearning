"""SimpleImputer in two steps on the Titanic toy data: fit learns the median of Age (28.75) and the mean of Fare
(32.62) from the training set; transform fills the gaps of the first test rows with those same training values.
Plotly table frames -> GIF."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from anim import save_gif, FONT

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "titanic_toy.csv")
Xtr, Xte, _, _ = train_test_split(df.drop(columns="Survived"), df["Survived"], test_size=0.2, random_state=2)
trf = ColumnTransformer([("imputer1", SimpleImputer(strategy="median"), ["Age"]),
                         ("imputer2", SimpleImputer(strategy="mean"), ["Fare"])], remainder="passthrough",
                        verbose_feature_names_out=False).set_output(transform="pandas").fit(Xtr)
med, mean = trf.named_transformers_["imputer1"].statistics_[0], trf.named_transformers_["imputer2"].statistics_[0]
assert med == 28.75 and round(mean, 4) == 32.6176
rows = Xte[Xte.isna().any(axis=1)].head(6)
out = trf.transform(rows)


def frame(stage):
    a = rows.Age if stage < 2 else out.Age
    f = rows.Fare if stage < 2 else out.Fare
    fmt = lambda v: "NaN" if pd.isna(v) else f"{v:g}"
    fill_a = ["#ffe2c4" if (stage == 2 and pd.isna(x)) else ("#fbe3e3" if pd.isna(x) else "white") for x in rows.Age]
    fill_f = ["#ffe2c4" if (stage == 2 and pd.isna(x)) else ("#fbe3e3" if pd.isna(x) else "white") for x in rows.Fare]
    fig = go.Figure(go.Table(header=dict(values=["test row", "Age", "Fare", "Family"], fill_color="#4C78A8",
                                         font=dict(color="white", size=20), height=40),
                             cells=dict(values=[list(rows.index), [fmt(v) for v in a], [fmt(v) for v in f], list(rows.Family)],
                                        fill_color=[["white"] * len(rows), fill_a, fill_f, ["white"] * len(rows)],
                                        font=dict(size=20), height=38)))
    head = ["Six test rows with gaps (red)",
            f"<b>fit</b> on the 712 training rows: median Age = {med:g}, mean Fare = {mean:.2f}",
            "<b>transform</b>: every gap gets the training value (orange)"][stage]
    fig.update_layout(width=1000, height=400, font=FONT, title=dict(text=head, x=0.5, y=0.93), margin=dict(l=10, r=10, t=70, b=0))
    return fig


if __name__ == "__main__":
    save_gif([frame(s) for s in range(3)], "imputer_fit_transform", here, keys=[0, 2], fps=1, holds=[3, 3, 6], cols=2)
