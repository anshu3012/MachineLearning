"""Same start (b = 100), three learning rates: too small (slow), good, too large (jumps across and grows) (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import loss_b, descend_b, BLUE, ORANGE, RED, GREEN, FONT

here = Path(__file__).parent
cases = [(0.01, 10, "learning rate 0.01: tiny steps, 10 steps not enough"),
         (0.1, 10, "learning rate 0.1: reaches the bottom"),
         (0.26, 6, "learning rate 0.26: overshoots, moves away")]
fig = make_subplots(1, 3, horizontal_spacing=0.06, subplot_titles=[c[2] for c in cases])
bgrid = np.linspace(-120, 170, 300)
for col, (lr, n, _) in enumerate(cases, start=1):
    bs = descend_b(100, lr, n)
    fig.add_trace(go.Scatter(x=bgrid, y=[loss_b(b) for b in bgrid], mode="lines", line=dict(color=BLUE, width=3)), 1, col)
    fig.add_trace(go.Scatter(x=bs, y=[loss_b(b) for b in bs], mode="lines+markers",
                             line=dict(color=ORANGE, width=2), marker=dict(size=8, color=ORANGE)), 1, col)
    fig.add_trace(go.Scatter(x=[bs[0]], y=[loss_b(bs[0])], mode="markers", marker=dict(size=12, color=RED)), 1, col)
    fig.update_xaxes(title="b", range=[-130, 180], row=1, col=col)
    fig.update_yaxes(range=[0, 90000], row=1, col=col)
    print(lr, bs.round(1))
fig.update_yaxes(title="loss L(b)", row=1, col=1)
fig.update_layout(template="simple_white", width=1150, height=400, showlegend=False, font=FONT,
                  margin=dict(l=70, r=20, t=50, b=60))
fig.update_annotations(font_size=15)
fig.write_image(here / "learning_rates.png", scale=2)
fig.write_image(here / "learning_rates.pdf")
