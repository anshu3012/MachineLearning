"""MNIST figures (Plotly) from results.json, which the Notebook writes after training.
Run: python figs.py -> digits.png, wrong.png, curves.png, confusion.png (each also .pdf)."""
import json
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
r = json.loads((here / "results.json").read_text())
font = dict(family="Latin Modern Roman", size=18)
TRAIN, VAL = "#4C78A8", "#F58518"
GREYS = [[0, "white"], [1, "black"]]


def image_row(images, titles, name, width):
    fig = make_subplots(1, len(images), horizontal_spacing=0.02, subplot_titles=titles)
    for k, im in enumerate(images):
        fig.add_trace(go.Heatmap(z=im, colorscale=GREYS, zmin=0, zmax=255, showscale=False), 1, k + 1)
    fig.update_xaxes(visible=False, constrain="domain")
    fig.update_yaxes(visible=False, autorange="reversed", scaleanchor="x", constrain="domain")
    for k in range(2, len(images) + 1):
        fig.update_yaxes(scaleanchor=f"x{k}", row=1, col=k)
    fig.update_annotations(font=dict(size=24))
    fig.update_layout(template="simple_white", width=width, height=width / len(images) + 70, font=font,
                      margin=dict(l=10, r=10, t=60, b=10))
    fig.write_image(here / f"{name}.png", scale=2)
    fig.write_image(here / f"{name}.pdf")


# the first 10 training images and their labels
image_row(r["train_images"], [f"label {y}" for y in r["train_labels"]], "digits", 1400)
# five test images the second network got wrong
image_row(r["wrong_images"], [f"true {t}, predicted {p}" for t, p in zip(r["wrong_true"], r["wrong_pred"])],
          "wrong", 1300)

# training curves of the second network
h = r["history"]
ep = list(range(1, len(h["loss"]) + 1))
fig = make_subplots(1, 2, horizontal_spacing=0.1,
                    subplot_titles=["Loss (sparse categorical cross-entropy)", "Accuracy"])
for col, key in [(1, "loss"), (2, "accuracy")]:
    fig.add_scatter(x=ep, y=h[key], name="training", line=dict(color=TRAIN, width=3), showlegend=col == 1, row=1, col=col)
    fig.add_scatter(x=ep, y=h["val_" + key], name="validation", line=dict(color=VAL, width=3), showlegend=col == 1,
                    row=1, col=col)
best = int(np.argmin(h["val_loss"]))
fig.add_scatter(x=[best + 1], y=[h["val_loss"][best]], mode="markers", marker=dict(color=VAL, size=14, symbol="circle-open",
                line=dict(width=3)), showlegend=False, row=1, col=1)
fig.update_xaxes(title="epoch")
fig.update_layout(template="simple_white", width=1100, height=430, font=font, margin=dict(l=60, r=20, t=50, b=60),
                  legend=dict(x=0.25, y=0.95))
fig.update_annotations(font=dict(size=20))
fig.write_image(here / "curves.png", scale=2)
fig.write_image(here / "curves.pdf")

# 10 x 10 confusion matrix on the 10,000 test images
cm = np.array(r["cm"])
digits = [str(d) for d in range(10)]
fig = go.Figure(go.Heatmap(z=np.log1p(cm), x=digits, y=digits, colorscale="Blues", showscale=False,
                           text=cm, texttemplate="%{text}", textfont=dict(size=15)))
fig.update_yaxes(autorange="reversed", title="actual digit")
fig.update_xaxes(title="predicted digit", side="bottom")
fig.update_layout(template="simple_white", width=720, height=680, font=font, margin=dict(l=80, r=20, t=50, b=70),
                  title=dict(text=f"Second network: accuracy {r['acc2']:.2%}", x=0.5))
fig.write_image(here / "confusion.png", scale=2)
fig.write_image(here / "confusion.pdf")
print("done")
