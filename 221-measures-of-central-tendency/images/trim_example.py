"""Section 7's worked example: the 10 class salaries (thousand rupees) sorted; a 10% trim cuts 28 and 2000, and the
mean of the 8 left is 34.375, against a plain mean of 230.3. Plotly (log x-axis so 2000 fits next to the others)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy import stats

here = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=18)
x = np.array([28, 30, 31, 32, 33, 35, 36, 38, 40, 2000])
assert stats.trim_mean(x, 0.1) == 34.375 and round(x.mean(), 1) == 230.3
kept = x[1:-1]
fig = go.Figure()
fig.add_scatter(x=kept, y=[0] * len(kept), mode="markers", marker=dict(size=16, color="#4C78A8"), name="kept")
fig.add_scatter(x=[x[0], x[-1]], y=[0, 0], mode="markers", marker=dict(size=18, color="#E45756", symbol="x"), name="cut (10% from each end)")
for v, txt, col, yy in ((34.375, "trimmed mean 34.4", "#54A24B", 0.6), (x.mean(), "plain mean 230.3", "#E45756", 0.6)):
    fig.add_vline(x=v, line=dict(color=col, width=3, dash="dash"), opacity=1)
    fig.add_annotation(x=np.log10(v), y=yy, text=txt, showarrow=False, xanchor="left", xshift=6, font=dict(size=18, color=col))
fig.add_annotation(x=np.log10(2000), y=-0.35, text="2000: the founder", showarrow=False, font=dict(size=16, color="#E45756"))
fig.add_annotation(x=np.log10(28), y=-0.35, text="28", showarrow=False, font=dict(size=16, color="#E45756"))
fig.update_layout(template="simple_white", width=1000, height=330, font=FONT,
                  xaxis=dict(type="log", title="monthly salary (thousand rupees, log scale)", tickvals=[25, 30, 40, 50, 100, 200, 500, 1000, 2000]),
                  yaxis=dict(visible=False, range=[-0.6, 1]), legend=dict(orientation="h", x=0.5, xanchor="center", y=1.15),
                  margin=dict(l=20, r=20, t=40, b=60))
fig.write_image(here / "trim_example.png", scale=2)
fig.write_image(here / "trim_example.pdf")
