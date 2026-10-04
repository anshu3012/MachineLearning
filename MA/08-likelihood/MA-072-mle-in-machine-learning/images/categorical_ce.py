"""Categorical cross entropy (Plotly). A softmax output (0.7, 0.2, 0.1) over three classes. With one-hot targets only
the true class's probability survives in prod_k yhat_k^{y_k} (every other factor is x^0 = 1). If the first class is
true the loss is -log 0.7 = 0.357; if the third class is true, -log 0.1 = 2.303."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
yhat = np.array([0.7, 0.2, 0.1])
ce = lambda onehot: -np.sum(onehot * np.log(yhat))
assert abs(ce(np.array([1, 0, 0])) - 0.357) < 5e-4 and abs(ce(np.array([0, 0, 1])) - 2.303) < 5e-4
assert np.prod(yhat ** np.array([1, 0, 0])) == 0.7

fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1,
                    subplot_titles=(f"true class 1: loss −log 0.7 = {ce(np.array([1, 0, 0])):.3f}",
                                    f"true class 3: loss −log 0.1 = {ce(np.array([0, 0, 1])):.3f}"))
for c, true in ((1, 0), (2, 2)):
    onehot = np.eye(3)[true]
    colors = [GREEN if k == true else "#D0D0D0" for k in range(3)]
    txt = [f"{yhat[k]}<sup>{int(onehot[k])}</sup> = {yhat[k] ** onehot[k]:g}" for k in range(3)]
    fig.add_trace(go.Bar(x=["class 1", "class 2", "class 3"], y=yhat, marker_color=colors, text=txt,
                         textposition="outside", textfont=dict(size=20)), 1, c)
fig.update_yaxes(title_text="softmax output ŷ<sub>k</sub>", range=[0, 0.95], row=1, col=1)
fig.update_yaxes(range=[0, 0.95], row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=480, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=20), margin=dict(l=70, r=20, t=60, b=50))
fig.update_annotations(font_size=22)
fig.write_image(HERE / "categorical_ce.png", scale=2)
fig.write_image(HERE / "categorical_ce.pdf")
