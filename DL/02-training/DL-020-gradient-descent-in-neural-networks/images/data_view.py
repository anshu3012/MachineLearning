"""The Social Network Ads data the experiments train on: 400 customers, standardized age and salary,
coloured by whether they bought (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import BLUE, RED, FONT

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "Social_Network_Ads.csv")
assert len(df) == 400
z = (df[["Age", "EstimatedSalary"]] - df[["Age", "EstimatedSalary"]].mean()) / df[["Age", "EstimatedSalary"]].std(ddof=0)
fig = go.Figure()
for v, name, c, s in ((0, "did not buy", BLUE, "circle"), (1, "bought", RED, "x")):
    m = df.Purchased == v
    fig.add_trace(go.Scatter(x=z.Age[m], y=z.EstimatedSalary[m], mode="markers", name=f"{name} ({m.sum()})",
                             marker=dict(color=c, symbol=s, size=8, opacity=0.8)))
fig.update_layout(template="simple_white", width=760, height=520, font=dict(FONT, size=18),
                  xaxis_title="age (standardized)", yaxis_title="estimated salary (standardized)",
                  legend=dict(x=0.0, y=1.02, yanchor="bottom", orientation="h"), margin=dict(l=70, r=20, t=50, b=60))
fig.write_image(here / "data_view.png", scale=2)
fig.write_image(here / "data_view.pdf")
