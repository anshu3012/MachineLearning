"""Why a regression output node is linear: the numbers each activation can output, for a weighted sum z from -6 to 6.
Linear returns z itself (any number); sigmoid stays between 0 and 1; ReLU never goes below 0. Curves from the three
formulas, no data. Plotly, because the picture is three function graphs."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
z = np.linspace(-6, 6, 241)
ACTS = [("<b>Linear</b>: f(z) = z<br>can output any number", z, "#54A24B", (-6, 6)),
        ("<b>Sigmoid</b><br>only between 0 and 1", 1 / (1 + np.exp(-z)), "#F58518", (0, 1)),
        ("<b>ReLU</b>: max(0, z)<br>never below 0", np.maximum(0, z), "#4C78A8", (0, 6))]
fig = make_subplots(rows=1, cols=3, subplot_titles=[a[0] for a in ACTS], horizontal_spacing=0.07)
for k, (_, f, col, (lo, hi)) in enumerate(ACTS, start=1):
    fig.add_shape(type="rect", x0=-6, x1=6, y0=lo, y1=hi, fillcolor=col, opacity=0.18, line_width=0, layer="below",
                  row=1, col=k)
    fig.add_scatter(x=z, y=f, mode="lines", line=dict(color=col, width=5, simplify=False), row=1, col=k)
    fig.update_xaxes(title_text="weighted sum z", range=[-6, 6], zeroline=True, zerolinecolor="#BBB", row=1, col=k)
    fig.update_yaxes(range=[-6.3, 6.3], zeroline=True, zerolinecolor="#BBB", row=1, col=k)
fig.update_yaxes(title_text="output of the node", row=1, col=1)
fig.update_annotations(font=dict(size=22))
fig.update_layout(template="simple_white", width=1300, height=520, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=21), margin=dict(l=80, r=20, t=90, b=70))
fig.write_image(HERE / "output_range.png", scale=2)
