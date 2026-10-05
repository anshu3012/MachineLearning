"""The latent variable, seen and unseen (Plotly): 300 draws from the mixture 0.5 N(-2, 0.5) + 0.2 N(1, 2) +
0.3 N(4, 1), made with the two-step recipe (seed 1). Top: each draw coloured by the component that produced it,
the hidden z. Bottom: the same draws as we actually observe them, all grey: z is lost."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import COLS, FONT, GREY, sample

here = Path(__file__).parent
rng = np.random.default_rng(1)
z, x = sample(300, rng)
counts = np.bincount(z, minlength=3)
assert counts.sum() == 300
jit = rng.uniform(-0.35, 0.35, 300)
fig = make_subplots(2, 1, vertical_spacing=0.2, subplot_titles=["hidden from us: the component z behind each draw",
                                                                "what we observe: only the values x"])
fig.update_annotations(font_size=22)
for k in range(3):
    m = z == k
    fig.add_trace(go.Scatter(x=x[m], y=jit[m], mode="markers", marker=dict(size=8, color=COLS[k], opacity=0.75),
                             name=f"z = {k + 1}: {counts[k]} draws"), 1, 1)
fig.add_trace(go.Scatter(x=x, y=jit, mode="markers", marker=dict(size=8, color=GREY, opacity=0.6), showlegend=False), 2, 1)
for r in (1, 2):
    fig.update_yaxes(visible=False, range=[-0.6, 0.6], row=r, col=1)
    fig.update_xaxes(title="x" if r == 2 else None, range=[-5.5, 7.5], row=r, col=1)
fig.update_layout(template="simple_white", width=1100, height=560, font=FONT,
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.25), margin=dict(l=30, r=30, t=60, b=110))
fig.write_image(here / "latent.png", scale=2)
