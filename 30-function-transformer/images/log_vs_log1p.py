"""Why log(1 + x): near 0 the plain log falls to minus infinity (log 0 does not exist), while log(1 + x) starts at 0;
for large values the two are almost the same. The 15 Titanic fares of 0 become 0, not minus infinity."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go

here = Path(__file__).parent
fare = pd.read_csv(here.parent / "data" / "titanic_train.csv").Fare
assert (fare == 0).sum() == 15 and np.log1p(0) == 0
x = np.linspace(0.005, 20, 800)
fig = go.Figure()
fig.add_scatter(x=x, y=np.log(x), mode="lines", line=dict(color="#E45756", width=4), name="np.log(x): falls to −∞ at 0")
fig.add_scatter(x=np.r_[0, x], y=np.log1p(np.r_[0, x]), mode="lines", line=dict(color="#54A24B", width=4),
                name="np.log1p(x) = log(1 + x): 0 at 0")
fig.add_scatter(x=[0], y=[0], mode="markers+text", marker=dict(size=14, color="#54A24B"), text=["15 fares of 0 → 0"],
                textposition="bottom right", showlegend=False, textfont=dict(size=18))
fig.add_hline(y=0, line=dict(color="#bbbbbb", width=1))
fig.update_layout(template="simple_white", width=1000, height=520, font=dict(family="Latin Modern Roman", size=19),
                  xaxis=dict(title="x", range=[-0.5, 20]), yaxis=dict(title="transformed value", range=[-4, 3.5]),
                  legend=dict(x=0.4, y=0.2), margin=dict(l=80, r=30, t=30, b=70))
fig.write_image(here / "log_vs_log1p.png", scale=2)
fig.write_image(here / "log_vs_log1p.pdf")
