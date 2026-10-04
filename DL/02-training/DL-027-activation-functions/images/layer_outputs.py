"""Zero-centred or not: the outputs of one fresh 128-node layer (Keras Dense, seed 0, the Notebook's check) for the 300
standardized circles observations, with sigmoid, tanh and ReLU. 38,400 values each. Plotly."""
import os
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import plotly.graph_objects as go  # noqa: E402
from plotly.subplots import make_subplots  # noqa: E402
import keras  # noqa: E402

from common import BLUE, GREEN, ORANGE  # noqa: E402

HERE = Path(__file__).parent
C = pd.read_csv(HERE.parent / "data" / "circles.csv")
X = C[["x1", "x2"]].values
Xs = ((X - X.mean(0)) / X.std(0)).astype("float32")
OUT = {}
for act in ("sigmoid", "tanh", "relu"):
    keras.utils.set_random_seed(0)
    OUT[act] = keras.layers.Dense(128, activation=act)(Xs).numpy().ravel()
assert len(X) == 300 and round(float(OUT["tanh"].mean()), 3) == 0.0 and round(float(OUT["sigmoid"].mean()), 1) == 0.5
assert (OUT["sigmoid"] > 0).all() and abs((OUT["tanh"] > 0).mean() - 0.5) < 0.02 and (OUT["relu"] >= 0).all()
fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.07, subplot_titles=[
    f"sigmoid: mean {OUT['sigmoid'].mean():.2f}, {100 * (OUT['sigmoid'] > 0).mean():.0f}% positive",
    f"tanh: mean {abs(OUT['tanh'].mean()):.2f}, {100 * (OUT['tanh'] > 0).mean():.0f}% positive",
    f"ReLU: mean {OUT['relu'].mean():.2f}, none negative"])
for k, (act, col) in enumerate((("sigmoid", ORANGE), ("tanh", BLUE), ("relu", GREEN)), start=1):
    fig.add_histogram(x=OUT[act], xbins=dict(start=-1, end=1.6, size=0.05), marker_color=col, showlegend=False,
                      row=1, col=k)
    fig.add_vline(x=0, line=dict(color="black", width=2, dash="dash"), opacity=1, row=1, col=k)
fig.update_xaxes(title_text="output of a node", range=[-1.05, 1.6])
fig.update_yaxes(title_text="count", row=1, col=1)
fig.update_layout(template="simple_white", width=1350, height=480, font=dict(family="Latin Modern Roman", size=19),
                  bargap=0.05, margin=dict(l=70, r=20, t=70, b=70))
for a in fig.layout.annotations[:3]:
    a.font.size = 20
fig.write_image(HERE / "layer_outputs.png", scale=2)
print({k: (round(float(v.mean()), 3), round(float((v > 0).mean()), 3)) for k, v in OUT.items()})
