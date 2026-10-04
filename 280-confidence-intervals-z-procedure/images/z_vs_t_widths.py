"""Section 5: the same 20 samples of 100 ages from the Notebook's population N(28, 15^2) (seed 42), each with a 95%
z-interval (sigma = 15 known: every interval has the same width 5.88) and a 95% t-interval (sample s: the width
changes from sample to sample)."""
from pathlib import Path

import numpy as np
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
BLUE, ORANGE = "#4C78A8", "#F58518"
X = np.random.default_rng(42).normal(28, 15, size=(20, 100))
m, s = X.mean(axis=1), X.std(axis=1, ddof=1)
ez = stats.norm.ppf(0.975) * 15 / 10
et = stats.t.ppf(0.975, 99) * s / 10
assert round(ez, 2) == 2.94
fig = make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.05,
                    subplot_titles=["z-procedure: σ = 15 known<br>every width 5.88",
                                    f"t-procedure: s from each sample<br>widths {2 * et.min():.2f} to {2 * et.max():.2f}"])
for col, e, c in [(1, np.full(20, ez), BLUE), (2, et, ORANGE)]:
    for i in range(20):
        fig.add_scatter(x=[m[i] - e[i], m[i] + e[i]], y=[i + 1, i + 1], mode="lines", line=dict(color=c, width=5),
                        showlegend=False, row=1, col=col)
    fig.add_scatter(x=m, y=np.arange(1, 21), mode="markers", marker=dict(color="black", size=7), showlegend=False,
                    row=1, col=col)
    fig.add_vline(x=28, line=dict(color="#6B6B6B", width=2, dash="dash"), row=1, col=col)
fig.update_xaxes(title_text="mean age (years)", range=[21, 35])
fig.update_yaxes(title_text="sample", row=1, col=1)
fig.update_annotations(font_size=21)
fig.update_layout(template="simple_white", width=1000, height=620, font=dict(family="Latin Modern Roman", size=19),
                  margin=dict(l=70, r=20, t=90, b=55))
fig.write_image(here / "z_vs_t_widths.png", scale=2)
fig.write_image(here / "z_vs_t_widths.pdf")
