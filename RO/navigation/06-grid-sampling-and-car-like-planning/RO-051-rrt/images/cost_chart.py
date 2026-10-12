"""Chart: the best route's length against the number of samples, median of 20 seeds, from under the table (4.0, 0.5) to
the doorway centre. RRT keeps growing after its first route and keeps the best one (MR 10.5): it stays at 6.07 m.
RRT* falls towards the shortest route, 4.55 m (dashed): 5.01 m at 500 samples, 4.71 m at 2,000, 4.66 m at 4,000.
Run -> cost_chart.png (and cost_chart.html)"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

import rrt
from gifkit import BLUE, FONT, GREEN

here = Path(__file__).parent
REC = (100, 150, 200, 300, 400, 500, 750, 1000, 1500, 2000, 3000, 4000)
star = np.median([[r["best"][k] for k in REC] for r in
                  (rrt.rrt_star(np.random.default_rng(s), n_max=4000, record=REC) for s in range(20))], axis=0)
plain = np.median([[o[k] for k in REC] for o in (rrt.rrt_best(np.random.default_rng(s), REC) for s in range(20))], axis=0)
L_star = rrt.shortest_route()[0]
S = dict(zip(REC, star))
assert round(S[500], 2) == 5.01 and round(S[2000], 2) == 4.71 and round(S[4000], 2) == 4.66
assert all(round(v, 2) == 6.07 for k, v in zip(REC, plain) if k >= 250) and round(L_star, 2) == 4.55
fig = go.Figure()
fig.add_trace(go.Scatter(x=REC, y=plain, mode="lines+markers", name="RRT, best route so far", line=dict(color=BLUE, width=4),
                         marker=dict(size=9)))
fig.add_trace(go.Scatter(x=REC, y=star, mode="lines+markers", name="RRT*", line=dict(color=GREEN, width=4), marker=dict(size=9)))
fig.add_trace(go.Scatter(x=[0, 4100], y=[L_star, L_star], mode="lines", name="shortest route, 4.55 m",
                         line=dict(color="black", width=3, dash="dash")))
fig.update_xaxes(title="samples", range=[0, 4100], dtick=500, showgrid=False)
fig.update_yaxes(title="route length (m), median of 20 seeds", range=[4.3, 6.8], dtick=0.25, showgrid=False)
fig.update_layout(template="simple_white", width=1000, height=560, font=FONT,
                  legend=dict(x=0.98, y=0.98, xanchor="right", yanchor="top", font=dict(size=19)),
                  margin=dict(l=80, r=30, t=30, b=70))
fig.write_image(here / "cost_chart.png", scale=1)
