"""Two stills. mean_balance: the values 3, 4, 1, 2, 5 as equal weights on a beam; the mean 3 is the balance point.
median_middle: 1..5 and 1..6 sorted in a row; the middle one (or the two middle ones, averaged) is the median.
Plotly: a chart with a marked position."""
from pathlib import Path
import plotly.graph_objects as go

HERE = Path(__file__).parent
BLUE, ORANGE, GREY = "#4C78A8", "#F58518", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=20)

x = [3, 4, 1, 2, 5]
m = sum(x) / len(x)
assert m == 3
fig = go.Figure()
fig.add_shape(type="line", x0=0.5, x1=5.5, y0=0, y1=0, line=dict(color=GREY, width=4))
fig.add_scatter(x=x, y=[0.12] * 5, mode="markers+text", text=[str(v) for v in x], textposition="top center",
                marker=dict(size=36, color=BLUE), textfont=dict(size=20))
fig.add_scatter(x=[m], y=[-0.1], mode="markers", marker=dict(symbol="triangle-up", size=34, color=ORANGE))
fig.add_annotation(x=m, y=-0.28, text="mean = 15 / 5 = 3: the beam balances here", showarrow=False,
                   font=dict(size=20, color=ORANGE))
fig.update_layout(template="simple_white", width=800, height=360, font=FONT, showlegend=False,
                  margin=dict(l=30, r=30, t=20, b=60), xaxis=dict(title="value", range=[0.5, 5.5], dtick=1),
                  yaxis=dict(visible=False, range=[-0.4, 0.4]))
fig.write_image(HERE / "mean_balance.png", scale=2)
fig.write_image(HERE / "mean_balance.pdf")

fig = go.Figure()
for row, vals, mid in [(1, [1, 2, 3, 4, 5], [2]), (0, [1, 2, 3, 4, 5, 6], [2, 3])]:
    fig.add_scatter(x=list(range(len(vals))), y=[row] * len(vals), mode="markers+text", text=[str(v) for v in vals],
                    textposition="top center", textfont=dict(size=20),
                    marker=dict(size=38, color=[ORANGE if i in mid else BLUE for i in range(len(vals))]))
fig.add_annotation(x=5.9, y=1, text="median = 3", showarrow=False, xanchor="left", font=dict(size=20, color=ORANGE))
fig.add_annotation(x=5.9, y=0, text="median = (3 + 4) / 2 = 3.5", showarrow=False, xanchor="left",
                   font=dict(size=20, color=ORANGE))
fig.update_layout(template="simple_white", width=900, height=360, font=FONT, showlegend=False,
                  margin=dict(l=20, r=20, t=20, b=20), xaxis=dict(visible=False, range=[-0.5, 9.5]),
                  yaxis=dict(visible=False, range=[-0.5, 1.6]))
fig.write_image(HERE / "median_middle.png", scale=2)
fig.write_image(HERE / "median_middle.pdf")
