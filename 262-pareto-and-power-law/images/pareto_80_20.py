"""The 80-20 rule: share of total wealth held by each fifth of the population when wealth follows a Pareto
distribution with alpha = log4(5) = 1.16 (left) and with alpha = 3 (right)."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots

here = Path(__file__).parent
BLUE, ORANGE = "#4C78A8", "#F58518"
fifths = ["poorest fifth", "2nd fifth", "3rd fifth", "4th fifth", "richest fifth"]


def shares(alpha):
    """Share of the total held by each fifth: the richest fraction p holds p^(1 - 1/alpha) of the total."""
    top = np.array([1.0, 0.8, 0.6, 0.4, 0.2]) ** (1 - 1 / alpha)      # held by the top 100%, 80%, ..., 20%
    return np.append(-np.diff(top), top[-1])


a8020 = np.log(5) / np.log(4)
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08,
                    subplot_titles=[f"α = {a8020:.2f}: the 80-20 rule", "α = 3: a thinner tail, less inequality"])
for col, alpha in ((1, a8020), (2, 3)):
    s = shares(alpha) * 100
    colours = [BLUE] * 4 + [ORANGE]
    fig.add_bar(x=fifths, y=s, marker_color=colours, text=[f"{v:.0f}%" for v in s], textposition="outside",
                textfont=dict(size=18), row=1, col=col)
    fig.update_xaxes(tickangle=0, tickfont=dict(size=15), row=1, col=col)
fig.update_yaxes(title_text="share of total wealth (%)", range=[0, 95], row=1, col=1)
fig.update_yaxes(range=[0, 95], row=1, col=2)
fig.update_annotations(font_size=19)
fig.update_layout(template="simple_white", width=1200, height=440, showlegend=False, bargap=0.3,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=70, r=20, t=50, b=40))
fig.write_image(here / "pareto_80_20.png", scale=2)
fig.write_image(here / "pareto_80_20.pdf")
