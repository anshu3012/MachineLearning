"""Feature-map size through a stack of 3 x 3 convolution layers on a 28 x 28 image, without padding (Keras 'valid')
and with it ('same'). Sizes come from Keras itself. Plotly."""
import os
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
import plotly.graph_objects as go  # noqa: E402
import keras  # noqa: E402

HERE = Path(__file__).parent
LAYERS = 13
sizes = {}
for pad in ("valid", "same"):
    m = keras.Sequential([keras.Input((28, 28, 1))] + [keras.layers.Conv2D(1, 3, padding=pad) for _ in range(LAYERS)])
    sizes[pad] = [28] + [m.layers[k].output.shape[1] for k in range(LAYERS)]
assert sizes["valid"] == [28 - 2 * k for k in range(LAYERS + 1)] and set(sizes["same"]) == {28}
fig = go.Figure()
fig.add_scatter(x=list(range(LAYERS + 1)), y=sizes["valid"], mode="lines+markers+text", text=sizes["valid"],
                textposition="bottom left", line=dict(color="#E45756", width=4), marker=dict(size=10),
                name="no padding ('valid'): loses 2 pixels per layer")
fig.add_scatter(x=list(range(LAYERS + 1)), y=sizes["same"], mode="lines+markers", line=dict(color="#54A24B", width=4),
                marker=dict(size=10), name="one ring of zeros ('same'): stays 28")
fig.update_layout(template="simple_white", width=1000, height=560, font=dict(family="Latin Modern Roman", size=20),
                  title=dict(text="Width of the feature map after each 3 × 3 convolution layer (28 × 28 input)", x=0.5,
                             font=dict(size=21)),
                  xaxis=dict(title="number of convolution layers", dtick=1), yaxis=dict(title="width (pixels)", range=[0, 31]),
                  legend=dict(x=0.02, y=0.12, font=dict(size=17)), margin=dict(l=80, r=30, t=70, b=80))
fig.write_image(HERE / "layer_sizes.png", scale=2)
print(sizes)
