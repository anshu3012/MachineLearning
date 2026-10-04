"""Share of production vs share of defects for the three machines (Plotly)."""
from pathlib import Path
import plotly.graph_objects as go

here = Path(__file__).parent
m = ["M1", "M2", "M3"]
prior = [0.2, 0.3, 0.5]
defect = [0.05, 0.03, 0.01]
joint = [p * d for p, d in zip(prior, defect)]
post = [j / sum(joint) for j in joint]
print(sum(joint), [round(p, 3) for p in post])
fig = go.Figure()
fig.add_trace(go.Bar(x=m, y=prior, name="prior: share of all markers, P(M)", marker_color="#BBBBBB",
                     text=[f"{v:.0%}" for v in prior], textposition="outside"))
fig.add_trace(go.Bar(x=m, y=post, name="posterior: share of defective markers, P(M | D)", marker_color="#E45756",
                     text=[f"{v:.1%}" for v in post], textposition="outside"))
fig.update_layout(template="simple_white", width=900, height=430, barmode="group", font=dict(family="Latin Modern Roman", size=16),
                  legend=dict(x=0.01, y=0.98), margin=dict(l=60, r=20, t=30, b=50), yaxis=dict(range=[0, 0.62], title="probability"))
fig.write_image(here / "posterior.png", scale=2); fig.write_image(here / "posterior.pdf")
