"""Drawing one Titanic passenger and reading Pclass: the sample space {1, 2, 3}, with the number of the 891
passengers in each class, and the event "not in first class" = {2, 3} (675 passengers)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

here = Path(__file__).parent
c = pd.read_csv(here.parent / "data" / "titanic_pclass.csv").Pclass.value_counts().sort_index()
assert c.to_dict() == {1: 216, 2: 184, 3: 491} and c[[2, 3]].sum() == 675
fig = go.Figure(go.Bar(x=[f"class {i}" for i in c.index], y=c.values, text=c.values, textposition="outside",
                       marker_color=["#cccccc", "#F58518", "#F58518"], textfont=dict(size=22)))
fig.add_annotation(x=1.0, y=590, text="event \"not in first class\" = {2, 3}: 675 of 891 passengers", showarrow=False,
                   font=dict(size=21, color="#c55a00"))
fig.update_layout(template="simple_white", width=1000, height=520, font=dict(family="Latin Modern Roman", size=20),
                  title=dict(text="Sample space of Pclass: {1, 2, 3}", x=0.5), yaxis=dict(title="passengers", range=[0, 640]),
                  margin=dict(l=80, r=30, t=70, b=60))
fig.write_image(here / "pclass_space.png", scale=2)
fig.write_image(here / "pclass_space.pdf")
