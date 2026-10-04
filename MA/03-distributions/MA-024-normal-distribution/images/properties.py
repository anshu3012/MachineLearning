"""Properties of the normal curve on the heights N(68, 3^2): symmetric, mean = median = mode at 68, the shares
within 1, 2 and 3 standard deviations (68-95-99.7), the same tail on each side, and total area 1."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from scipy import stats

here = Path(__file__).parent
d = stats.norm(68, 3)
x = np.linspace(56, 80, 800)
share = {k: d.cdf(68 + 3 * k) - d.cdf(68 - 3 * k) for k in (1, 2, 3)}
assert [round(100 * share[k], 1) for k in (1, 2, 3)] == [68.3, 95.4, 99.7]
assert np.isclose(d.cdf(62), d.sf(74)) and abs(d.median() - 68) < 1e-9
fig = go.Figure()
for k, alpha in [(3, 0.18), (2, 0.3), (1, 0.45)]:
    xs = x[np.abs(x - 68) <= 3 * k]
    fig.add_scatter(x=xs, y=d.pdf(xs), fill="tozeroy", fillcolor=f"rgba(76,120,168,{alpha})", mode="lines",
                    line=dict(width=0), showlegend=False)
for side in (x[x <= 62], x[x >= 74]):
    fig.add_scatter(x=side, y=d.pdf(side), fill="tozeroy", fillcolor="rgba(228,87,86,0.45)", mode="lines",
                    line=dict(width=0), showlegend=False)
fig.add_scatter(x=x, y=d.pdf(x), mode="lines", line=dict(color="black", width=3.5), showlegend=False)
fig.add_vline(x=68, line=dict(color="#F58518", width=3, dash="dash"))
fig.add_annotation(x=68, y=0.148, text="mean = median = mode = 68", showarrow=False, font=dict(size=20, color="#F58518"),
                   bgcolor="white")
for k, y in [(1, 0.072), (2, 0.040), (3, 0.016)]:
    fig.add_annotation(x=68 - 3 * k, y=y, ax=68 + 3 * k, ay=y, xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowside="end+start", arrowhead=2, arrowwidth=2, text="")
    fig.add_annotation(x=68, y=y + 0.007, text=f"{100 * share[k]:.1f}% within {k} σ", showarrow=False,
                       font=dict(size=19), bgcolor="rgba(255,255,255,0.8)")
for xx, txt in [(60.2, "below 62:<br>2.3%"), (75.8, "above 74:<br>2.3%")]:
    fig.add_annotation(x=xx, y=0.03, text=txt, showarrow=False, font=dict(size=18, color="#E45756"))
fig.add_annotation(x=0.99, y=0.97, xref="paper", yref="paper", xanchor="right", showarrow=False,
                   text=f"total area = {np.trapezoid(d.pdf(np.linspace(40, 96, 4000)), np.linspace(40, 96, 4000)):.3f}",
                   font=dict(size=20))
fig.update_layout(template="simple_white", width=1000, height=560, font=dict(family="Latin Modern Roman", size=19),
                  xaxis=dict(title="height (inches)", tickvals=[59, 62, 65, 68, 71, 74, 77], range=[56, 80]),
                  yaxis=dict(title="density", range=[0, 0.16]), margin=dict(l=70, r=20, t=20, b=55))
fig.write_image(here / "properties.png", scale=2)
fig.write_image(here / "properties.pdf")
