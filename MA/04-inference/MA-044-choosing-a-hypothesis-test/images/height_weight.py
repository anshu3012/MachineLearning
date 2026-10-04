"""Height against weight for the 60 people of data/people.csv, coloured by age group: a strong positive relationship.
Tool: Plotly (a scatter chart)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from scipy import stats

here = Path(__file__).parent
people = pd.read_csv(here.parent / "data" / "people.csv")
r, p = stats.pearsonr(people.height, people.weight)
assert round(r, 2) == 0.98 and p < 0.001
fig = go.Figure()
for group, colour in (("child", "#F58518"), ("adult", "#4C78A8"), ("elderly", "#54A24B")):
    g = people[people.age_group == group]
    fig.add_scatter(x=g.height, y=g.weight, mode="markers", name=group, marker=dict(size=11, color=colour))
fig.update_layout(template="simple_white", width=900, height=560, font=dict(family="Latin Modern Roman", size=20),
                  title=dict(text="r = 0.98, p < 0.001", x=0.5), legend=dict(title="age group", x=0.02, y=0.98),
                  xaxis=dict(title="height (m)", showgrid=True), yaxis=dict(title="weight (kg)", showgrid=True),
                  margin=dict(l=80, r=30, t=60, b=70))
fig.write_image(here / "height_weight.png", scale=2)
fig.write_image(here / "height_weight.pdf")
