"""Standardizing: X ~ N(5, 2.5^2) (top) becomes Z ~ N(0, 1) (bottom). Each tick on the top axis lines up with
its z-score on the bottom axis: z = (x - 5) / 2.5."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
ORANGE, BLUE, GREY = "#F58518", "#4C78A8", "#6B6B6B"
mu, sd = 5, 2.5
z = np.linspace(-3.6, 3.6, 600)
fig = make_subplots(rows=2, cols=1, vertical_spacing=0.22,
                    subplot_titles=["X ~ N(5, 2.5²)", "Z ~ N(0, 1): the standard normal distribution"])
fig.add_scatter(x=mu + sd * z, y=stats.norm(mu, sd).pdf(mu + sd * z), mode="lines", line=dict(color=ORANGE, width=4),
                fill="tozeroy", fillcolor="rgba(245,133,24,0.12)", row=1, col=1)
fig.add_scatter(x=z, y=stats.norm().pdf(z), mode="lines", line=dict(color=BLUE, width=4), fill="tozeroy",
                fillcolor="rgba(76,120,168,0.12)", row=2, col=1)
for k in range(-3, 4):
    fig.add_vline(x=mu + sd * k, line=dict(color=GREY, width=1, dash="dot"), row=1, col=1)
    fig.add_vline(x=k, line=dict(color=GREY, width=1, dash="dot"), row=2, col=1)
fig.update_xaxes(range=[mu - 3.6 * sd, mu + 3.6 * sd], tickvals=[mu + sd * k for k in range(-3, 4)], title_text="x",
                 row=1, col=1)
fig.update_xaxes(range=[-3.6, 3.6], tickvals=list(range(-3, 4)), title_text="z = (x − 5) / 2.5", row=2, col=1)
fig.update_yaxes(title_text="density", row=1, col=1)
fig.update_yaxes(title_text="density", row=2, col=1)
fig.update_annotations(font_size=19)
fig.update_layout(template="simple_white", width=1000, height=620, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=70, r=20, t=40, b=50))
fig.write_image(here / "standardize.png", scale=2)
fig.write_image(here / "standardize.pdf")
