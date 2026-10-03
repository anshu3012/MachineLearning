"""Margin of error E = z * sigma / sqrt(n) as each factor changes, the other two fixed at 95%, sigma = 15,
n = 50."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
BLUE, GREY = "#4C78A8", "#6B6B6B"
z95 = stats.norm.ppf(0.975)
fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.08,
                    subplot_titles=["confidence level (σ = 15, n = 50)", "population std σ (95%, n = 50)",
                                    "sample size n (95%, σ = 15)"])
level = np.linspace(0.5, 0.999, 400)
fig.add_scatter(x=level * 100, y=stats.norm.ppf((1 + level) / 2) * 15 / np.sqrt(50), row=1, col=1)
sigma = np.linspace(1, 50, 100)
fig.add_scatter(x=sigma, y=z95 * sigma / np.sqrt(50), row=1, col=2)
n = np.arange(2, 501)
fig.add_scatter(x=n, y=z95 * 15 / np.sqrt(n), row=1, col=3)
fig.update_traces(mode="lines", line=dict(color=BLUE, width=3.5))
for col, x, y, label in [(1, 95, z95 * 15 / np.sqrt(50), "95%: 4.16"), (2, 15, z95 * 15 / np.sqrt(50), "σ = 15: 4.16"),
                         (3, 30, z95 * 15 / np.sqrt(30), "n = 30: 5.37"), (3, 120, z95 * 15 / np.sqrt(120), "n = 120: 2.68")]:
    fig.add_scatter(x=[x], y=[y], mode="markers", marker=dict(color="black", size=10), row=1, col=col)
    fig.add_annotation(x=x, y=y, text=label, showarrow=True, ax=-60 if col == 1 else 40, ay=45 if col == 2 else -35, font_size=16,
                       row=1, col=col)
fig.update_xaxes(title_text="confidence level (%)", row=1, col=1)
fig.update_xaxes(title_text="σ", row=1, col=2)
fig.update_xaxes(title_text="n", row=1, col=3)
fig.update_yaxes(title_text="margin of error", row=1, col=1)
fig.update_yaxes(range=[0, 15])
fig.update_annotations(font_size=17)
fig.update_layout(template="simple_white", width=1200, height=420, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=16), margin=dict(l=70, r=20, t=50, b=50))
fig.write_image(here / "margin_factors.png", scale=2)
fig.write_image(here / "margin_factors.pdf")
