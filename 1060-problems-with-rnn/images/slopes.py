"""Fix 1 of section 5: the factor per step is (slope of the activation) x w_h. tanh's slope is at most 1 and
usually below it; ReLU's slope is exactly 1 for every positive input. Plotly."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from common import BLUE, RED, GREY, FONT

here = Path(__file__).parent
z = np.linspace(-4, 4, 801)
tanh_slope = 1 - np.tanh(z) ** 2
relu_slope = (z > 0).astype(float)
assert tanh_slope.max() <= 1 and abs(1 - np.tanh(0.6) ** 2 - 0.71) < 0.01
fig = go.Figure()
fig.add_scatter(x=z, y=tanh_slope, name="slope of tanh: between 0 and 1", line=dict(color=RED, width=4))
fig.add_scatter(x=z, y=relu_slope, name="slope of ReLU: 1 for every positive input", line=dict(color=BLUE, width=4, dash="dash"))
fig.add_annotation(x=-2.4, y=0.62, text="tanh: each step multiplies the gradient<br>by (slope below 1) x w<sub>h</sub>",
                   showarrow=False, font=dict(size=18, color=RED))
fig.add_annotation(x=2.4, y=1.12, text="ReLU: the factor is w<sub>h</sub> alone", showarrow=False, font=dict(size=18, color=BLUE))
fig.update_layout(template="simple_white", width=1000, height=420, font=dict(FONT, size=20),
                  xaxis=dict(title="input to the activation, x<sub>t</sub> w<sub>i</sub> + h<sub>t-1</sub> w<sub>h</sub>"),
                  yaxis=dict(title="slope", range=[-0.05, 1.25]),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.25), margin=dict(l=70, r=20, t=20, b=110))
fig.write_image(here / "slopes.png", scale=2)
fig.write_image(here / "slopes.pdf")
