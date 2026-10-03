"""Likelihoods of parameter values for two observed events. Coin: 5 heads in 5 tosses, likelihood p^5 for
p = 0.5 (fair) and p = 0.7. Bag: 5 green balls drawn in 5 draws (with replacement), likelihood p^5 for a bag with
2 green of 5 (p = 0.4) and 4 green of 5 (p = 0.8)."""
from pathlib import Path

import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, GREY = "#4C78A8", "#F58518", "#54A24B", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=20)
coin = {"fair coin, p = 0.5": 0.5 ** 5, "biased coin, p = 0.7": 0.7 ** 5}
bag = {"2 green of 5, p = 0.4": 0.4 ** 5, "4 green of 5, p = 0.8": 0.8 ** 5}
assert coin["biased coin, p = 0.7"] > coin["fair coin, p = 0.5"] and bag["4 green of 5, p = 0.8"] > bag["2 green of 5, p = 0.4"]
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
                    subplot_titles=("observed: 5 heads in 5 tosses", "observed: 5 green in 5 draws"))
for col, d, colour in ((1, coin, BLUE), (2, bag, GREEN)):
    fig.add_trace(go.Bar(x=list(d), y=list(d.values()), marker_color=[GREY, colour], text=[f"{v:.3f}" for v in d.values()],
                         textposition="outside", showlegend=False), 1, col)
    fig.update_yaxes(range=[0, 0.4], title_text="likelihood = p⁵" if col == 1 else None, row=1, col=col)
fig.update_layout(template="simple_white", width=1100, height=480, font=FONT, margin=dict(l=70, r=20, t=50, b=60))
fig.update_annotations(font_size=21)
fig.write_image(HERE / "coin_balls.png", scale=2)
fig.write_image(HERE / "coin_balls.pdf")
