"""Section 2: the risk of at least one false alarm when every pair of k groups gets its own t-test at alpha = 0.05,
1 - 0.95^m with m = k(k - 1)/2 pairs, against ANOVA's single test. The simulated points (2,000 datasets, 20 values
per group, all true means equal) are the notebook's numbers quoted in the Note.
Run: python false_alarm.py  -> false_alarm.png/.pdf (Plotly)"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
k = np.arange(2, 9)
m = k * (k - 1) // 2
risk = 1 - 0.95 ** m
assert np.isclose(risk[k == 3][0], 0.143, atol=5e-4) and np.isclose(risk[k == 5][0], 0.401, atol=5e-4)
SIM_T = {3: 0.110, 5: 0.290}                      # notebook: pairwise t-tests, simulated
SIM_ANOVA = {3: 0.050, 5: 0.050}                  # notebook: ANOVA, simulated

fig = go.Figure()
fig.add_trace(go.Scatter(x=k, y=100 * risk, mode="lines+markers+text", name="pairwise t-tests: 1 − 0.95<sup>m</sup>",
                         line=dict(color=RED, width=4), marker=dict(size=10),
                         text=[f"{m_} tests" if m_ > 1 else "" for m_ in m], textposition="top left", textfont=dict(size=15, color=RED)))
fig.add_trace(go.Scatter(x=list(SIM_T), y=[100 * v for v in SIM_T.values()], mode="markers", name="pairwise t-tests, simulated",
                         marker=dict(size=16, color=RED, symbol="diamond-open", line=dict(width=3))))
fig.add_trace(go.Scatter(x=[2, 8], y=[5, 5], mode="lines", name="ANOVA: one test, 5%", line=dict(color=BLUE, width=4)))
fig.add_trace(go.Scatter(x=list(SIM_ANOVA), y=[100 * v for v in SIM_ANOVA.values()], mode="markers",
                         name="ANOVA, simulated", marker=dict(size=16, color=BLUE, symbol="diamond-open", line=dict(width=3))))
fig.update_layout(template="simple_white", width=950, height=560, font=dict(family="Latin Modern Roman", size=20),
                  title=dict(text="More groups, more pairs, more false alarms", x=0.5),
                  xaxis=dict(title="number of groups k", dtick=1, range=[1.7, 8.3]),
                  yaxis=dict(title="chance of at least one false alarm (percent)", range=[0, 80]),
                  legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.9)"), margin=dict(l=80, r=20, t=60, b=60))
fig.write_image(HERE / "false_alarm.png", scale=2)
fig.write_image(HERE / "false_alarm.pdf")
