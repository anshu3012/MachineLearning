"""Area between the mean and one standard deviation, from two z-table readings: Phi(1) - Phi(0) = 0.8413 - 0.5."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
BLUE, ORANGE = "#4C78A8", "#F58518"
z = np.linspace(-3.5, 3.5, 600)
panels = [(1, "Φ(1) = 0.8413", -3.5, 1, BLUE), (0, "Φ(0) = 0.5", -3.5, 0, BLUE), (None, "0.8413 − 0.5 = 0.3413", 0, 1, ORANGE)]
fig = make_subplots(rows=1, cols=3, subplot_titles=[p[1] for p in panels], horizontal_spacing=0.05)
for col, (_, _, lo, hi, colour) in enumerate(panels, start=1):
    fig.add_scatter(x=z, y=stats.norm.pdf(z), mode="lines", line=dict(color="#6B6B6B", width=3), row=1, col=col)
    s = np.linspace(lo, hi, 300)
    rgba = "rgba(76,120,168,0.4)" if colour == BLUE else "rgba(245,133,24,0.45)"
    fig.add_scatter(x=np.r_[lo, s, hi], y=np.r_[0, stats.norm.pdf(s), 0], fill="toself", fillcolor=rgba, mode="lines",
                    line=dict(width=0), row=1, col=col)
    fig.update_xaxes(title_text="z", dtick=1, row=1, col=col)
    fig.update_yaxes(showticklabels=col == 1, row=1, col=col)
fig.update_yaxes(title_text="density", row=1, col=1)
fig.update_annotations(font_size=19)
fig.update_layout(template="simple_white", width=1200, height=360, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=70, r=20, t=50, b=50))
fig.write_image(here / "one_sd_area.png", scale=2)
fig.write_image(here / "one_sd_area.pdf")
