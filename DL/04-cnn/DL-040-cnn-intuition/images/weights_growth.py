"""Section 4.2 drawn: weights in the first layer as a greyscale image grows, for a Dense layer of 100 nodes
(height x width x 100, plus 100 biases) and for a convolution layer of 32 filters of 3 x 3 (3 x 3 x 32 + 32,
whatever the image size). Counts checked against Keras' count_params. Plotly."""
import os
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
import numpy as np  # noqa: E402
import plotly.graph_objects as go  # noqa: E402
import keras  # noqa: E402

HERE = Path(__file__).parent
SIDES = [28, 40, 100, 224, 500, 1000]
dense = [s * s * 100 + 100 for s in SIDES]
conv = [3 * 3 * 32 + 32] * len(SIDES)
for s in (28, 40):                                      # Keras agrees with the formulas
    assert keras.Sequential([keras.Input((s * s,)), keras.layers.Dense(100)]).count_params() == s * s * 100 + 100
    assert keras.Sequential([keras.Input((s, s, 1)), keras.layers.Conv2D(32, 3)]).count_params() == 320
X = np.arange(len(SIDES))
fig = go.Figure()
fig.add_scatter(x=X, y=dense, mode="lines+markers+text", text=[f"{d:,}" for d in dense], textposition="top left",
                line=dict(color="#E45756", width=4), marker=dict(size=12), name="Dense layer, 100 nodes (flattened image)")
fig.add_scatter(x=X, y=conv, mode="lines+markers", line=dict(color="#54A24B", width=4), marker=dict(size=12),
                name="convolution layer, 32 filters of 3 × 3: always 320")
fig.update_layout(template="simple_white", width=1050, height=600, font=dict(family="Latin Modern Roman", size=20),
                  title=dict(text="Weights in the first layer, for a greyscale image of side n pixels", x=0.5),
                  xaxis=dict(title="image size (n × n pixels)", tickvals=X, ticktext=[f"{s} × {s}" for s in SIDES],
                             range=[-0.6, len(SIDES) - 0.5]),
                  yaxis=dict(title="weights and biases (log scale)", type="log", range=[2, 8.6],
                             tickvals=[1e2, 1e3, 1e4, 1e5, 1e6, 1e7, 1e8],
                             ticktext=["100", "1k", "10k", "100k", "1M", "10M", "100M"]),
                  legend=dict(x=0.02, y=0.98, font=dict(size=17)), margin=dict(l=90, r=30, t=70, b=80))
fig.write_image(HERE / "weights_growth.png", scale=2)
