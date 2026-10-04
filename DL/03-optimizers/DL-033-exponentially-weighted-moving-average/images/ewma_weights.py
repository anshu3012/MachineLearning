"""Weight (1 - beta) beta^k that the EWMA gives to the point k steps in the past, beta = 0.5 and 0.9 (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, GREY, FONT

here = Path(__file__).parent
k = np.arange(0, 31)
fig = make_subplots(rows=1, cols=2, subplot_titles=("β = 0.5", "β = 0.9"), horizontal_spacing=0.1)
for col, (beta, c) in enumerate(((0.5, ORANGE), (0.9, BLUE)), start=1):
    w = (1 - beta) * beta ** k
    fig.add_trace(go.Bar(x=k, y=w, marker_color=c, showlegend=False), row=1, col=col)
    n = 1 / (1 - beta)
    fig.add_vline(x=n, line=dict(color=GREY, dash="dash", width=2), row=1, col=col)
    fig.add_annotation(x=n, y=max(w) * 0.9, text=f"1/(1 − β) = {n:.0f}", xanchor="left", showarrow=False,
                       font=dict(color=GREY, size=16), row=1, col=col, xshift=6)
fig.update_xaxes(title_text="steps in the past (k)")
fig.update_yaxes(title_text="weight (1 − β) β<sup>k</sup>", col=1)
fig.update_layout(template="simple_white", width=1000, height=400, font=FONT, bargap=0.15,
                  margin=dict(l=80, r=20, t=40, b=60))
fig.write_image(here / "ewma_weights.png", scale=2)
fig.write_image(here / "ewma_weights.pdf")
