"""The column transformer's output with names: set_output(transform="pandas") on the COVID training set. Each header
is transformer name + two underscores + column; colours mark which transformer made the column."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "covid_toy.csv")
Xtr, Xte, _, _ = train_test_split(df.drop(columns=["has_covid"]), df["has_covid"], test_size=0.2, random_state=0)
ct = ColumnTransformer([("tnf1", SimpleImputer(), ["fever"]),
                        ("tnf2", OrdinalEncoder(categories=[["Mild", "Strong"]]), ["cough"]),
                        ("tnf3", OneHotEncoder(sparse_output=False, drop="first"), ["gender", "city"])],
                       remainder="passthrough").set_output(transform="pandas")
out = ct.fit_transform(Xtr).head(3)
assert list(out.columns) == ["tnf1__fever", "tnf2__cough", "tnf3__gender_Male", "tnf3__city_Delhi",
                             "tnf3__city_Kolkata", "tnf3__city_Mumbai", "remainder__age"]
assert out.iloc[:, 0].tolist() == [99, 104, 98] and out["remainder__age"].tolist() == [22, 56, 31]
COL = {"tnf1": "#E45756", "tnf2": "#B279A2", "tnf3": "#54A24B", "remainder": "#9a9a9a"}
heads = list(out.columns)
fig = go.Figure(go.Table(header=dict(values=[h.replace("__", "__<br>") for h in heads],
                                     fill_color=[COL[h.split("__")[0]] for h in heads],
                                     font=dict(color="white", size=19), height=56),
                         cells=dict(values=[[f"{v:g}" for v in out[h]] for h in heads], font=dict(size=20), height=40,
                                    fill_color="white", line_color="#dddddd")))
fig.update_layout(width=1400, height=290, font=dict(family="Latin Modern Roman", size=18), margin=dict(l=10, r=10, t=60, b=0),
                  title=dict(text="First three training patients after set_output(transform=\"pandas\")", x=0.5))
fig.write_image(here / "named_output.png", scale=2)
fig.write_image(here / "named_output.pdf")
