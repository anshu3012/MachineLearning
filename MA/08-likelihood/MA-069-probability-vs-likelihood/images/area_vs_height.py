"""Probability is an area, likelihood is a height (StatQuest's mouse weights). Left: the distribution N(32, 2.5^2) is
fixed and the probability that a mouse weighs 32 to 34 grams is the shaded area, 0.29. Right: the weight 34 grams is
fixed and the likelihood of a distribution is its height above 34: 0.12 for mean 32, 0.16 for mean 34."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=20)
d32, d34 = stats.norm(32, 2.5), stats.norm(34, 2.5)
area = d32.cdf(34) - d32.cdf(32)
assert abs(area - 0.29) < 0.005 and abs(d32.pdf(34) - 0.12) < 0.005 and abs(d34.pdf(34) - 0.16) < 0.005

x = np.linspace(24, 42, 500)
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1,
                    subplot_titles=("probability: distribution fixed, area", "likelihood: data fixed, height"))
fig.add_trace(go.Scatter(x=x, y=d32.pdf(x), mode="lines", line=dict(color=BLUE, width=4), name="N(32, 2.5²)"), 1, 1)
xs = np.linspace(32, 34, 100)
fig.add_trace(go.Scatter(x=np.r_[32, xs, 34], y=np.r_[0, d32.pdf(xs), 0], fill="toself", mode="lines",
                         line=dict(color=ORANGE, width=1), fillcolor="rgba(245,133,24,0.5)", showlegend=False), 1, 1)
fig.add_annotation(x=33, y=0.06, text=f"area = {area:.2f}", showarrow=False, bgcolor="white", row=1, col=1)
fig.add_trace(go.Scatter(x=x, y=d32.pdf(x), mode="lines", line=dict(color=BLUE, width=4), showlegend=False), 1, 2)
fig.add_trace(go.Scatter(x=x, y=d34.pdf(x), mode="lines", line=dict(color=GREEN, width=4, dash="dash"),
                         name="N(34, 2.5²)"), 1, 2)
for d, c, txt, pos in ((d32, BLUE, "0.12", "middle left"), (d34, GREEN, "0.16", "top right")):
    fig.add_trace(go.Scatter(x=[34], y=[d.pdf(34)], mode="markers+text", marker=dict(size=14, color=c),
                             text=[txt], textposition=pos, textfont=dict(color=c, size=22), showlegend=False), 1, 2)
fig.add_trace(go.Scatter(x=[34, 34], y=[0, 0.17], mode="lines", line=dict(color=RED, width=2, dash="dot"),
                         showlegend=False), 1, 2)
fig.add_trace(go.Scatter(x=[34], y=[0], mode="markers", marker=dict(size=13, color="black"),
                         name="the weighed mouse: 34 g"), 1, 2)
for c in (1, 2):
    fig.update_xaxes(title_text="mouse weight (grams)", row=1, col=c)
    fig.update_yaxes(range=[0, 0.19], row=1, col=c)
fig.update_yaxes(title_text="density", row=1, col=1)
fig.update_layout(template="simple_white", width=1200, height=520, font=FONT,
                  legend=dict(orientation="h", x=0, y=-0.2), margin=dict(l=70, r=20, t=50, b=140))
fig.update_annotations(font_size=21)
fig.write_image(HERE / "area_vs_height.png", scale=2)
fig.write_image(HERE / "area_vs_height.pdf")
