"""Titanic: survival rate (%) by class, sex and port of boarding (groupby + mean x 100)."""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import load, save_px, FONT, BLUE

t = load("titanic_train")
t["Pclass"] = t.Pclass.map({1: "1st", 2: "2nd", 3: "3rd"})
t["Embarked"] = t.Embarked.map({"C": "Cherbourg", "Q": "Queenstown", "S": "Southampton"})
names = {"Pclass": "Ticket class", "Sex": "Sex", "Embarked": "Port of boarding"}
fig = make_subplots(rows=3, cols=1, subplot_titles=list(names.values()), vertical_spacing=0.12, row_heights=[3, 2, 3])
for i, c in enumerate(names, start=1):
    rate = t.groupby(c)["Survived"].mean()[::-1] * 100          # first group on top
    fig.add_trace(go.Bar(x=rate.values, y=rate.index, orientation="h", marker=dict(color=BLUE, opacity=0.8),
                         text=[f"{v:.0f}%" for v in rate.values], textposition="outside"), i, 1)
    fig.update_xaxes(range=[0, 90], showgrid=True, row=i, col=1)
fig.update_xaxes(title="Survived (%)", row=3, col=1)
fig.update_layout(template="simple_white", width=900, height=740, font=FONT, showlegend=False, margin=dict(l=120, r=20, t=40, b=70))
save_px(fig, "survival_rates")
