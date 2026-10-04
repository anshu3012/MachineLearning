"""The cost of one update (Plotly), for the Note's example of 100,000 observations, 100 features and 1,000 epochs.
Left: multiplications per update: batch reads every row (10^7), SGD one row (100). Right: updates per epoch: batch 1,
SGD 100,000. Per epoch both read the whole table once; SGD turns that work into 100,000 small steps instead of one."""
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import FONT, ORANGE, RED

here = Path(__file__).parent
n, m, epochs = 100_000, 100, 1_000
assert n * m * epochs == 10 ** 10
fig = make_subplots(1, 2, horizontal_spacing=0.14,
                    subplot_titles=["multiplications for one update", "updates in one epoch"])
fig.update_annotations(font_size=22)
for col, vals in ((1, [n * m, m]), (2, [1, n])):
    fig.add_trace(go.Bar(x=["batch", "stochastic"], y=vals, marker_color=[RED, ORANGE],
                         text=[f"{v:,}" for v in vals], textposition="outside", textfont=dict(size=22)), 1, col)
    fig.update_yaxes(type="log", range=[0, 8.3], row=1, col=col)
fig.update_yaxes(title="count (log scale)", row=1, col=1)
fig.update_layout(template="simple_white", width=1100, height=500, font=FONT, showlegend=False,
                  margin=dict(l=90, r=30, t=60, b=60))
fig.write_image(here / "cost_bars.png", scale=2)
