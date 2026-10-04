"""More data, same peak, narrower curve (Plotly). The binomial likelihood of p for 4 orange answers of 7 and for 40 of
70, each divided by its maximum so both top out at 1. Both peak at p = 4/7 = 0.571; the 70-person curve is much
narrower (the range where it stays above half its maximum shrinks about threefold)."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from scipy import stats

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
p = np.linspace(0.001, 0.999, 9981)
fig = go.Figure()
widths = {}
for (n, x), col in (((7, 4), BLUE), ((70, 40), ORANGE)):
    L = stats.binom(n, p).pmf(x)
    assert abs(p[L.argmax()] - 4 / 7) < 1e-3
    half = p[L >= L.max() / 2]
    widths[n] = half[-1] - half[0]
    fig.add_trace(go.Scatter(x=p, y=L / L.max(), mode="lines", line=dict(color=col, width=4),
                             name=f"{x} of {n}: above half height for p in {half[0]:.2f} to {half[-1]:.2f}"))
assert widths[7] / widths[70] > 2.8
fig.add_vline(x=4 / 7, line=dict(color=GREEN, width=2, dash="dash"))
fig.add_annotation(x=4 / 7, y=1.06, text="p̂ = 4/7 = 0.571", showarrow=False, font=dict(color=GREEN, size=21))
fig.update_layout(template="simple_white", width=950, height=560, font=dict(family="Latin Modern Roman", size=20),
                  xaxis=dict(title="p (share preferring orange)", range=[0, 1]),
                  yaxis=dict(title="likelihood / its maximum", range=[0, 1.12]),
                  legend=dict(x=0, y=-0.2, yanchor="top"), margin=dict(l=70, r=20, t=30, b=150))
fig.write_image(HERE / "binomial_more_data.png", scale=2)
fig.write_image(HERE / "binomial_more_data.pdf")
print(widths)
