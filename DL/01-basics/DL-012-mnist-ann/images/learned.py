"""What the first network (784-128-10) learned, from extras.json (written by the Notebook). Plotly stills.
hidden_weights.png : the 784 incoming weights of the first 16 hidden nodes, each drawn as a 28 x 28 picture
                     (blue positive, red negative).
noise.png          : one image of pure random noise and the 10 probabilities the network gives it.
Run: python learned.py"""
import json
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
e = json.loads((HERE / "extras.json").read_text())
FONT = dict(family="Latin Modern Roman", size=22)
RED, GREY = "#E45756", "#6B6B6B"

# 1. hidden-node weights as pictures
Wh = np.array(e["hidden_weights"])
assert Wh.shape == (16, 28, 28)
lim = float(np.abs(Wh).max())
fig = make_subplots(2, 8, horizontal_spacing=0.01, vertical_spacing=0.06, subplot_titles=[f"node {k + 1}" for k in range(16)])
for k in range(16):
    fig.add_trace(go.Heatmap(z=Wh[k], colorscale="RdBu", zmin=-lim, zmax=lim, showscale=(k == 15),
                             colorbar=dict(title="weight", len=0.9)), k // 8 + 1, k % 8 + 1)
fig.update_xaxes(visible=False, constrain="domain")
fig.update_yaxes(visible=False, autorange="reversed", constrain="domain")
for k in range(16):
    fig.update_yaxes(scaleanchor=f"x{k + 1}" if k else "x", row=k // 8 + 1, col=k % 8 + 1)
fig.update_annotations(font=dict(size=20))
fig.update_layout(template="simple_white", width=1500, height=470, font=FONT, margin=dict(l=10, r=10, t=50, b=10))
fig.write_image(HERE / "hidden_weights.png", scale=2)

# 2. noise in, confident answer out
P = np.array(e["noise_probs"])
assert np.isclose(P.sum(), 1, atol=1e-4) and P.max() > 0.99 and e["noise_median_top"] > 0.9   # confident on noise, not one lucky image
fig = make_subplots(1, 2, column_widths=[0.32, 0.68], horizontal_spacing=0.1,
                    subplot_titles=["input: random noise", "output: 10 probabilities"])
fig.add_trace(go.Heatmap(z=e["noise_image"], colorscale=[[0, "white"], [1, "black"]], zmin=0, zmax=1, showscale=False), 1, 1)
fig.add_trace(go.Bar(x=list(range(10)), y=P, marker_color=[RED if k == P.argmax() else GREY for k in range(10)],
                     text=[f"{p:.3f}" for p in P], textposition="outside", textfont=dict(size=18)), 1, 2)
fig.update_xaxes(visible=False, constrain="domain", row=1, col=1)
fig.update_yaxes(visible=False, autorange="reversed", scaleanchor="x", constrain="domain", row=1, col=1)
fig.update_xaxes(title="digit", dtick=1, row=1, col=2)
fig.update_yaxes(title="probability", range=[0, 1.12], row=1, col=2)
fig.update_annotations(font=dict(size=24))
fig.update_layout(template="simple_white", width=1200, height=480, font=FONT, showlegend=False, margin=dict(l=20, r=20, t=60, b=70))
fig.write_image(HERE / "noise.png", scale=2)
print("noise image: digit", int(P.argmax()), "p", round(float(P.max()), 3), "median top", round(e["noise_median_top"], 3))
