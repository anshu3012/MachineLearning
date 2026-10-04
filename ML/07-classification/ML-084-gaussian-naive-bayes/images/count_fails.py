"""Why counting fails for a numerical feature (Plotly): P(height = x | male) by counting is a spike at each of the
4 male heights and exactly 0 everywhere else, including the new person's 185 cm."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "people.csv")
h = df.loc[df.gender == "male", "height_cm"]
p = h.value_counts(normalize=True).sort_index()
assert len(h) == 4 and (h == 185).sum() == 0 and abs(p[180.4] - 0.5) < 1e-12
fig = go.Figure()
for x, y in p.items():
    fig.add_trace(go.Scatter(x=[x, x], y=[0, y], mode="lines", line=dict(color="#4C78A8", width=6), showlegend=False))
fig.add_trace(go.Scatter(x=p.index, y=p.values, mode="markers+text", marker=dict(color="#4C78A8", size=14),
                         text=[f"{v:.2f}" for v in p.values], textposition="top center", showlegend=False))
fig.add_trace(go.Scatter(x=[185], y=[0], mode="markers", marker=dict(color="#E45756", size=20, symbol="x"),
                         showlegend=False))
fig.add_annotation(x=185, y=0.01, axref="x", ayref="y", ax=186.5, ay=0.45, text="new man, 185 cm:<br>count 0 → probability 0",
                   font=dict(color="#E45756"), arrowcolor="#E45756", arrowwidth=3)
fig.update_layout(template="simple_white", width=1000, height=470, font=dict(family="Latin Modern Roman", size=24),
                  title=dict(text="P(height = x | male) by counting the 4 men", x=0.5),
                  xaxis=dict(title="height (cm)", range=[165, 192]), yaxis=dict(title="probability", range=[0, 0.62]),
                  margin=dict(l=80, r=30, t=70, b=70))
fig.write_image(here / "count_fails.png", scale=2); fig.write_image(here / "count_fails.pdf")
