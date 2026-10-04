"""Graphs for two features on the Titanic: class x survival as a contingency table drawn as bars, an aggregate of
age per sex (mean, median, maximum), and age bands x sex as a contingency table of bins."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
d = pd.read_csv(here.parent / "data" / "titanic_train.csv")
ct = pd.crosstab(d.Pclass, d.Survived)
assert ct.loc[3, 0] == 372 and ct[0].sum() == 549
agg = d.groupby("Sex").Age.agg(["mean", "median", "max"])
assert agg["max"].tolist() == [63, 80] and round(agg.loc["female", "mean"], 1) == 27.9
bands = pd.crosstab(pd.cut(d.Age, [0, 10, 20, 30, 40, 50, 60, 80]), d.Sex)
assert bands.loc[pd.Interval(20, 30), "male"] == 149
BLUE, ORANGE = "#4C78A8", "#F58518"
fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.08, subplot_titles=[
    "Categorical + categorical:<br>class x survival (crosstab)", "Categorical + numerical:<br>an aggregate of age per sex",
    "Categorical + binned numerical:<br>age band x sex (crosstab)"])
for s, c, name in ((0, "#9a9a9a", "died"), (1, "#54A24B", "survived")):
    fig.add_bar(x=[f"class {i}" for i in ct.index], y=ct[s], name=name, marker_color=c, text=ct[s],
                textposition="outside", row=1, col=1)
for sex, c in (("female", ORANGE), ("male", BLUE)):
    fig.add_bar(x=["mean", "median", "maximum"], y=agg.loc[sex].round(1), name=sex, marker_color=c,
                text=agg.loc[sex].round(1), textposition="outside", row=1, col=2)
    fig.add_bar(x=[f"{i.left}-{i.right}" for i in bands.index], y=bands[sex], name=sex, marker_color=c,
                showlegend=False, row=1, col=3)
fig.update_yaxes(title_text="passengers", row=1, col=1)
fig.update_yaxes(title_text="age (years)", range=[0, 92], row=1, col=2)
fig.update_yaxes(title_text="passengers", row=1, col=3)
fig.update_xaxes(title_text="age band", row=1, col=3)
fig.update_annotations(font_size=19)
fig.update_layout(template="simple_white", width=1600, height=600, barmode="group",
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=70, r=20, t=100, b=110),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.22))
fig.write_image(here / "two_features.png", scale=2)
fig.write_image(here / "two_features.pdf")
