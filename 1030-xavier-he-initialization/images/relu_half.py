"""Why He initialisation doubles the variance: 100,000 weighted sums z drawn symmetric around 0 (standard normal,
seed 0) and the same values after ReLU. ReLU keeps the positive half and sets the negative half to 0, so the mean
square E[a^2] is half of E[z^2]. Plotly."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from common import BLUE, GREEN

HERE = Path(__file__).parent
z = np.random.default_rng(0).standard_normal(100_000)
a = np.maximum(z, 0)
mz, ma = (z ** 2).mean(), (a ** 2).mean()
assert abs(mz - 1) < 0.01 and abs(ma / mz - 0.5) < 0.01 and abs((a == 0).mean() - 0.5) < 0.01
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1, subplot_titles=(
    f"Weighted sums z: mean square {mz:.2f}", f"After ReLU: mean square {ma:.2f} ({100 * (a == 0).mean():.0f}% are 0)"))
fig.add_histogram(x=z, xbins=dict(start=-4, end=4, size=0.1), marker_color=BLUE, showlegend=False, row=1, col=1)
fig.add_histogram(x=a, xbins=dict(start=-4, end=4, size=0.1), marker_color=GREEN, showlegend=False, row=1, col=2)
fig.update_xaxes(range=[-4, 4], title_text="value")
fig.update_yaxes(title_text="count", row=1, col=1)
fig.update_yaxes(range=[0, 4300], row=1, col=2)
fig.add_annotation(x=0.05, y=4250, ax=-3.6, ay=3000, axref="x2", ayref="y2", xref="x2", yref="y2", showarrow=True,
                   arrowwidth=2, text=f"{int((a == 0).sum()):,} values at exactly 0<br>(bar cut off)", align="left",
                   xanchor="left", font=dict(size=17))
fig.update_layout(template="simple_white", width=1200, height=480, font=dict(family="Latin Modern Roman", size=20),
                  margin=dict(l=80, r=30, t=70, b=70))
for t in fig.layout.annotations:
    t.font.size = 21
fig.write_image(HERE / "relu_half.png", scale=2)
