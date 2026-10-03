"""The Naive Bayes lookup table for Play Tennis (Plotly): P(value | class) for every column, plus the class priors."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "play_tennis.csv")
cols = ["outlook", "temperature", "humidity", "wind"]
counts = df["play"].value_counts()
fig = make_subplots(rows=1, cols=5, horizontal_spacing=0.075, column_widths=[0.22, 0.22, 0.17, 0.17, 0.17],
                    subplot_titles=[f"P({c} | play)" for c in cols] + ["P(play)"])
for k, col in enumerate(cols):
    tab = pd.crosstab(df[col], df["play"])           # counts per value and class
    prob = tab / counts                               # divide each class column by the class size
    text = [[f"{tab.loc[v, c]}/{counts[c]}" for c in ["No", "Yes"]] for v in prob.index]
    fig.add_trace(go.Heatmap(z=prob[["No", "Yes"]].values, x=["No", "Yes"], y=list(prob.index), colorscale="Blues",
                             zmin=0, zmax=1, showscale=False, text=text, texttemplate="%{text}", textfont=dict(size=15),
                             xgap=2, ygap=2), 1, k + 1)
    print(col, "\n", tab)
fig.add_trace(go.Heatmap(z=[[counts["No"] / len(df), counts["Yes"] / len(df)]], x=["No", "Yes"], y=["all days"], colorscale="Blues",
                         zmin=0, zmax=1, showscale=False, text=[[f"{counts['No']}/14", f"{counts['Yes']}/14"]],
                         texttemplate="%{text}", textfont=dict(size=15), xgap=2, ygap=2), 1, 5)
fig.update_layout(template="simple_white", width=1350, height=330, font=dict(family="Latin Modern Roman", size=14),
                  margin=dict(l=70, r=10, t=40, b=30))
fig.write_image(here / "lookup.png", scale=2); fig.write_image(here / "lookup.pdf")
