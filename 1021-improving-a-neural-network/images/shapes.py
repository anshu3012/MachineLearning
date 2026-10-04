"""Neurons per layer, measured on MNIST (data/shapes.json from experiments/shapes.py: ReLU layers, Adam, 10 epochs,
mean test accuracy of 3 seeds). Left: a pyramid and equal layers with the same number of parameters. Right: a first
hidden layer of 1, 2 or 32 neurons, then two layers of 32. Plotly."""
import json
from pathlib import Path

import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
R = json.load(open(HERE.parent / "data" / "shapes.json"))
acc = {k: 100 * v["mean"] for k, v in R.items()}
assert abs(acc["64-32-16"] - acc["58-58-58"]) < 0.5 and acc["1-32-32"] < 50 < acc["2-32-32"] < 80 < acc["32-32-32"]
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12, column_widths=[0.42, 0.58],
                    subplot_titles=("Pyramid vs equal layers (about 53,000 weights each)",
                                    "Size of the first hidden layer"))
for col, keys, cols in ((1, ["64-32-16", "58-58-58"], ["#4C78A8", "#72B7B2"]),
                        (2, ["1-32-32", "2-32-32", "32-32-32"], ["#E45756", "#F58518", "#54A24B"])):
    fig.add_bar(x=keys, y=[acc[k] for k in keys], marker_color=cols, text=[f"{acc[k]:.1f}%" for k in keys],
                textposition="outside", showlegend=False, row=1, col=col)
fig.update_yaxes(title_text="test accuracy (%)", range=[0, 105], row=1, col=1)
fig.update_yaxes(range=[0, 105], row=1, col=2)
fig.update_xaxes(title_text="hidden layer sizes")
fig.update_layout(template="simple_white", width=1250, height=560, font=dict(family="Latin Modern Roman", size=21),
                  margin=dict(l=80, r=30, t=70, b=80))
for a in fig.layout.annotations[:2]:
    a.font.size = 21
fig.write_image(HERE / "shapes.png", scale=2)
print({k: round(v, 2) for k, v in acc.items()})
