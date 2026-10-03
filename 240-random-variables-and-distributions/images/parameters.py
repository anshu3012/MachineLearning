"""Parameters are tuning knobs: the mean moves the normal curve, the standard deviation widens it."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
x = np.linspace(-8, 12, 500)
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08,
                    subplot_titles=["Change μ (σ = 1.5): the curve moves", "Change σ (μ = 2): the curve widens"])
for mu, c in [(0, "#4C78A8"), (2, "#F58518"), (5, "#54A24B")]:
    fig.add_scatter(x=x, y=stats.norm(mu, 1.5).pdf(x), mode="lines", line=dict(color=c, width=3.5),
                    name=f"μ = {mu}", legend="legend", row=1, col=1)
for s, c in [(1, "#4C78A8"), (2, "#F58518"), (3.5, "#54A24B")]:
    fig.add_scatter(x=x, y=stats.norm(2, s).pdf(x), mode="lines", line=dict(color=c, width=3.5, dash="dot"),
                    name=f"σ = {s}", legend="legend2", row=1, col=2)
fig.update_xaxes(title_text="x", range=[-6, 10])
fig.update_yaxes(title_text="density", range=[0, 0.42])
fig.update_annotations(font_size=19)
fig.update_layout(template="simple_white", width=1100, height=520,
                  legend=dict(x=0.36, y=0.98), legend2=dict(x=0.9, y=0.98),
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=60, r=20, t=60, b=40))
fig.write_image(here / "parameters.png", scale=2)
fig.write_image(here / "parameters.pdf")
