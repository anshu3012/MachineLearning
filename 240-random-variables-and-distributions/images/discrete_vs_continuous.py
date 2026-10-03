"""A discrete distribution has values only at separate points; a continuous one is an unbroken curve."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1,
                    subplot_titles=["Discrete: one die (values at 1, ..., 6 only)",
                                    "Continuous: CGPA (a value at every x)"])
faces = np.arange(1, 7)
for f in faces:                                   # stems
    fig.add_scatter(x=[f, f], y=[0, 1 / 6], mode="lines", line=dict(color="#4C78A8", width=4), row=1, col=1)
fig.add_scatter(x=faces, y=np.full(6, 1 / 6), mode="markers", marker=dict(size=13, color="#4C78A8"), row=1, col=1)
x = np.linspace(0, 10, 400)
fig.add_scatter(x=x, y=stats.beta(7, 3, scale=10).pdf(x), mode="lines", line=dict(color="#F58518", width=4),
                row=1, col=2)
fig.update_xaxes(title_text="face x", dtick=1, range=[0.3, 6.7], row=1, col=1)
fig.update_yaxes(title_text="probability", range=[0, 0.25], row=1, col=1)
fig.update_xaxes(title_text="CGPA x", dtick=1, row=1, col=2)
fig.update_yaxes(title_text="probability density", range=[0, 0.32], row=1, col=2)
fig.update_annotations(font_size=19)
fig.update_layout(template="simple_white", width=1050, height=440, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=18), margin=dict(l=60, r=20, t=60, b=50))
fig.write_image(here / "discrete_vs_continuous.png", scale=2)
fig.write_image(here / "discrete_vs_continuous.pdf")
