"""EWMAs of a noisy gradient (mean 1, sd 0.5, seed 0) started at 0: raw and bias-corrected, beta1 = 0.9 for the
gradient (left) and beta2 = 0.999 for the squared gradient (right), first 100 steps (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, GREY, FONT

here = Path(__file__).parent
g = np.random.default_rng(0).normal(1.0, 0.5, 100)
t = np.arange(1, 101)
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1,
                    subplot_titles=("first moment m (β₁ = 0.9)", "second moment v (β₂ = 0.999)"))
for col, (beta, values, true) in enumerate(((0.9, g, 1.0), (0.999, g ** 2, 1.25)), start=1):
    a, raw = 0.0, []
    for x in values:
        a = beta * a + (1 - beta) * x
        raw.append(a)
    raw = np.array(raw)
    fig.add_trace(go.Scatter(x=t, y=raw, name="raw EWMA (starts at 0)", line=dict(color=ORANGE, width=3),
                             showlegend=col == 1), 1, col)
    fig.add_trace(go.Scatter(x=t, y=raw / (1 - beta ** t), name="divided by 1 − βᵗ", line=dict(color=BLUE, width=3),
                             showlegend=col == 1), 1, col)
    fig.add_hline(y=true, line=dict(color=GREY, dash="dot", width=2), row=1, col=col)
fig.update_xaxes(title_text="step t")
fig.update_yaxes(range=[0, 2.2], col=1)
fig.update_yaxes(range=[0, 2.2], col=2)
fig.update_layout(template="simple_white", width=1050, height=430, font=FONT,
                  legend=dict(orientation="h", x=0, y=-0.25), margin=dict(l=60, r=20, t=40, b=110))
fig.write_image(here / "bias_correction.png", scale=2)
fig.write_image(here / "bias_correction.pdf")
