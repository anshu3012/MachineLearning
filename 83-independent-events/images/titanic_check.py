"""Testing independence on real counts (Plotly): the 891 Titanic passengers of the training file. The share who
survived overall (342 of 891) against the share inside each group: women (233 of 314) and men (109 of 577). The shares
differ a lot, so "survived" and "is a woman" are not independent."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, RED

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "titanic_train.csv")
rows = [("all passengers", df), ("given: woman", df[df.Sex == "female"]), ("given: man", df[df.Sex == "male"])]
n = [len(d) for _, d in rows]
k = [int(d.Survived.sum()) for _, d in rows]
assert (k, n) == ([342, 233, 109], [891, 314, 577])
share = [a / b for a, b in zip(k, n)]
fig = go.Figure(go.Bar(x=[r[0] for r in rows], y=share, marker_color=[GREY, RED, BLUE],
                       text=[f"{s:.3f}<br>({a} of {b})" for s, a, b in zip(share, k, n)], textposition="outside", textfont=dict(size=20)))
fig.add_hline(y=share[0], line=dict(color=GREY, dash="dash", width=2))
fig.update_layout(template="simple_white", width=950, height=540, font=FONT, yaxis=dict(title="share who survived", range=[0, 0.95]),
                  margin=dict(l=80, r=30, t=20, b=50))
fig.write_image(here / "titanic_check.png", scale=2)
