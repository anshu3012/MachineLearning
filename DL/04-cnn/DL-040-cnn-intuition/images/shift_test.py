"""The shift test of experiments/toy_cnn.py: top, the letter X and its four one-pixel shifts; bottom, the share of
the 8 shifted letters each kind of network gets right (mean over the random starts that learned both letters).
Plotly: a small image row plus a bar chart. Data: data/toy_cnn.json.  Run: python shift_test.py -> shift_test.png"""
import json
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, GREEN, GREY, RED, FONT

HERE = Path(__file__).parent
d = json.load(open(HERE.parent / "data" / "toy_cnn.json"))
X = np.array(d["X"])
views = [("trained on", X), ("1 right", np.roll(X, 1, 1)), ("1 left", np.roll(X, -1, 1)), ("1 down", np.roll(X, 1, 0)), ("1 up", np.roll(X, -1, 0))]
fig = make_subplots(2, 5, specs=[[{}] * 5, [{"colspan": 5}, None, None, None, None]], row_heights=[0.38, 0.62],
                    subplot_titles=[v[0] for v in views] + [""], vertical_spacing=0.14, horizontal_spacing=0.03)
for c, (_, img) in enumerate(views, start=1):
    fig.add_trace(go.Heatmap(z=img, colorscale=[[0, "#E6E6E6"], [1, BLUE]], showscale=False, xgap=2, ygap=2), 1, c)
    fig.update_xaxes(visible=False, row=1, col=c)
    fig.update_yaxes(visible=False, autorange="reversed", scaleanchor=f"x{'' if c == 1 else c}", row=1, col=c)
names = list(d["summary"])
acc = [100 * d["summary"][n]["shifted_accuracy"] for n in names]
labels = ["ANN on the 36 flattened pixels", "CNN, 2 × 2 max pooling", "CNN, max pooling over the whole map"]
fig.add_trace(go.Bar(y=labels, x=acc, orientation="h", marker_color=[RED, GREEN, GREEN], text=[f"{a:.0f}%" for a in acc],
                     textposition="outside", textfont=dict(size=22)), 2, 1)
fig.add_vline(x=50, line=dict(color=GREY, dash="dash"), row=2, col=1)
fig.add_annotation(x=50, y=2.62, text="guessing: 50%", showarrow=False, font=dict(size=17, color=GREY), row=2, col=1)
fig.update_xaxes(title_text="shifted letters classified correctly (percent)", range=[0, 105], row=2, col=1)
fig.update_yaxes(autorange="reversed", row=2, col=1)
fig.update_layout(template="simple_white", width=1100, height=640, font=dict(FONT, size=20), showlegend=False,
                  margin=dict(l=20, r=20, t=50, b=70))
fig.write_image(HERE / "shift_test.png", scale=2)
