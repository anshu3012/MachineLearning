"""Keras Applications models from section 6: parameters against top-1 accuracy, marker area ~ file size.
Checks the Note's rule size ~ 4 bytes x parameters (Plotly)."""
from pathlib import Path
import plotly.graph_objects as go
from common import BLUE, ORANGE, GREEN, RED, PURPLE, GREY, FONT

here = Path(__file__).parent
# model: (size MB, top-1 %, parameters in millions)  -- Keras Applications table, as in the Note
M = {"VGG16": (528, 71.3, 138.4), "VGG19": (549, 71.3, 143.7), "ResNet50": (98, 74.9, 25.6),
     "InceptionV3": (92, 77.9, 23.9), "Xception": (88, 79.0, 22.9), "MobileNetV2": (14, 71.3, 3.5)}
for name, (mb, _, p) in M.items():
    est = 4 * p * 1e6 / 1_048_576
    assert abs(est - mb) / mb < 0.06, (name, est, mb)            # size ~ 4 bytes per parameter
assert round(4 * 138.4e6 / 1_048_576) == 528
colours = dict(zip(M, [BLUE, BLUE, ORANGE, GREEN, PURPLE, RED]))
pos = {"VGG16": "bottom center", "VGG19": "top center", "ResNet50": "bottom right", "InceptionV3": "middle left",
       "Xception": "top center", "MobileNetV2": "top center"}
fig = go.Figure()
for name, (mb, acc, p) in M.items():
    fig.add_trace(go.Scatter(x=[p], y=[acc], mode="markers+text", text=[f"{name} ({mb} MB)"], textposition=pos[name],
                             marker=dict(size=12 + 0.11 * mb, color=colours[name], opacity=0.75,
                                         line=dict(color="white", width=1)),
                             textfont=dict(size=17), showlegend=False))
fig.update_layout(template="simple_white", width=900, height=540, font=dict(FONT, size=18),
                  xaxis=dict(type="log", title="parameters (millions, log scale)", range=[0.2, 2.45],
                             tickvals=[3, 10, 30, 100]),
                  yaxis=dict(title="top-1 accuracy on ImageNet (%)", range=[69.5, 80.5]),
                  margin=dict(l=70, r=30, t=20, b=60))
fig.write_image(here / "keras_models.png", scale=2)
fig.write_image(here / "keras_models.pdf")
