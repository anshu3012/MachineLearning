"""Exploring the placement data: CGPA vs IQ, coloured by placement."""
from pathlib import Path
import plotly.graph_objects as go
from toy_model import load

here = Path(__file__).parent
df = load()[0]
fig = go.Figure()
for label, colour, name in [(1, "#54A24B", "placed"), (0, "#E45756", "not placed")]:
    d = df[df.placement == label]
    fig.add_scatter(x=d.cgpa, y=d.iq, mode="markers", name=name, marker=dict(color=colour, size=11, opacity=0.85))
fig.update_layout(template="simple_white", width=900, height=560, font=dict(family="Latin Modern Roman", size=18),
                  title=dict(text="100 students: CGPA vs IQ", x=0.5),
                  xaxis=dict(title="CGPA", showgrid=True), yaxis=dict(title="IQ", showgrid=True),
                  legend=dict(x=1.01, y=1), margin=dict(l=70, r=20, t=70, b=60))
fig.write_image(here / "eda_scatter.png", scale=2)
fig.write_image(here / "eda_scatter.pdf")
