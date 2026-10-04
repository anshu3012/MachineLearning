"""Three more MNIST figures (Plotly), from results.json (written by the Notebook) and the Note's own example.
scaling.png : the first training image (a 5), and an 8 x 8 patch of it as raw pixels (0 to 255) and divided by 255.
curves1.png : training and validation loss of the first network (10 epochs); lowest validation loss after epoch 4.
argmax.png  : the worked example of Section 6: P(1) = 0.03, P(2) = 0.90, P(7) = 0.05, 0.02 shared by the rest.
Run: python more_figs.py"""
import json
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
r = json.loads((HERE / "results.json").read_text())
FONT = dict(family="Latin Modern Roman", size=22)
TRAIN, VAL, RED, GREY = "#4C78A8", "#F58518", "#E45756", "#6B6B6B"
GREYS = [[0, "white"], [1, "black"]]

# 1. Scaling the pixels
img = np.array(r["train_images"][0])
assert r["train_labels"][0] == 5 and img.shape == (28, 28) and img.max() == 255 and img.min() == 0
R0, C0, K = 3, 14, 8                                            # an 8 x 8 patch with ink in it
patch = img[R0:R0 + K, C0:C0 + K]
assert patch.max() == 255 and (patch == 0).any()
fig = make_subplots(1, 3, horizontal_spacing=0.04, column_widths=[0.28, 0.36, 0.36],
                    subplot_titles=("the image (label 5)", "patch: raw pixels, 0 to 255", "patch ÷ 255: 0 to 1"))
fig.add_trace(go.Heatmap(z=img, colorscale=GREYS, zmin=0, zmax=255, showscale=False), 1, 1)
fig.add_shape(type="rect", x0=C0 - 0.5, x1=C0 + K - 0.5, y0=R0 - 0.5, y1=R0 + K - 0.5, line=dict(color=RED, width=4),
              fillcolor="rgba(0,0,0,0)", layer="above", row=1, col=1)
for col, z, fmt in ((2, patch, "%{z:.0f}"), (3, patch / 255, "%{z:.2f}")):
    fig.add_trace(go.Heatmap(z=z, colorscale=[[0, "white"], [1, "#9DB9D9"]], zmin=0, zmax=z.max(), showscale=False,
                             texttemplate=fmt, textfont=dict(size=17, color="black"), xgap=1, ygap=1), 1, col)
fig.update_xaxes(visible=False, constrain="domain")
fig.update_yaxes(visible=False, autorange="reversed", constrain="domain")
for k in (1, 2, 3):
    fig.update_yaxes(scaleanchor=f"x{k}" if k > 1 else "x", row=1, col=k)
fig.update_annotations(font=dict(size=24))
fig.update_layout(template="simple_white", width=1400, height=520, font=FONT, margin=dict(l=10, r=10, t=60, b=10))
fig.write_image(HERE / "scaling.png", scale=2)

# 2. Curves of the first network
h = r["history1"]
ep = np.arange(1, 11)
best = int(np.argmin(h["val_loss"])) + 1
assert round(h["loss"][0], 3) == 0.280 and round(h["loss"][-1], 3) == 0.014
assert best == 4 and round(h["val_loss"][3], 3) == 0.088 and round(h["val_loss"][-1], 3) == 0.099
fig = go.Figure()
fig.add_trace(go.Scatter(x=ep, y=h["loss"], mode="lines+markers", name="training loss", line=dict(color=TRAIN, width=3)))
fig.add_trace(go.Scatter(x=ep, y=h["val_loss"], mode="lines+markers", name="validation loss", line=dict(color=VAL, width=3)))
fig.add_trace(go.Scatter(x=[best], y=[h["val_loss"][best - 1]], mode="markers", marker=dict(size=20, symbol="circle-open", color=RED, line=dict(width=3)),
                         showlegend=False))
fig.add_annotation(x=best, y=h["val_loss"][best - 1], text="lowest: epoch 4, 0.088", ax=40, ay=-70,
                   font=dict(color=RED, size=22), arrowcolor=RED)
fig.update_layout(template="simple_white", width=1000, height=520, font=FONT, xaxis=dict(title="epoch", dtick=1),
                  yaxis=dict(title="loss", range=[0, 0.3]), legend=dict(x=0.6, y=0.95),
                  margin=dict(l=70, r=20, t=30, b=60))
fig.write_image(HERE / "curves1.png", scale=2)

# 3. argmax on the worked example
P = np.full(10, 0.02 / 7)
P[[1, 2, 7]] = [0.03, 0.90, 0.05]
assert np.isclose(P.sum(), 1) and P.argmax() == 2
fig = go.Figure(go.Bar(x=list(range(10)), y=P, marker_color=[RED if k == 2 else GREY for k in range(10)],
                       text=[f"{p:.2f}" if p > 0.01 else "" for p in P], textposition="outside", textfont=dict(size=24)))
fig.add_annotation(x=2, y=0.9, text="argmax = 2", showarrow=True, ax=120, ay=-10, font=dict(color=RED, size=26),
                   arrowcolor=RED)
fig.update_layout(template="simple_white", width=1000, height=500, font=FONT,
                  xaxis=dict(title="digit k", dtick=1), yaxis=dict(title="P(k)", range=[0, 1.05]),
                  margin=dict(l=70, r=20, t=30, b=60))
fig.write_image(HERE / "argmax.png", scale=2)
