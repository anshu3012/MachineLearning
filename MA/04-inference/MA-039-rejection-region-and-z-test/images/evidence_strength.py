"""Two weaknesses of the yes/no rule. Left: z = 1.95 and z = 1.97 sit either side of the two-tailed critical value
1.96, so near-identical samples get opposite decisions. Right: the chance of a z at least this large under H0
(log scale): z = 2 gives 0.023, z = 15 about 4e-51, yet both are simply "reject"."""
from pathlib import Path

import numpy as np
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
BLUE, RED = "#4C78A8", "#E45756"
assert round(stats.norm.sf(2), 3) == 0.023 and 3.5e-51 < stats.norm.sf(15) < 4.5e-51
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
                    subplot_titles=["knife edge at 1.96", "same verdict, very different evidence"])
x = np.linspace(1.7, 2.2, 300)
fig.add_scatter(x=x[x >= 1.96], y=stats.norm.pdf(x[x >= 1.96]), fill="tozeroy", fillcolor="rgba(228,87,86,0.35)",
                line=dict(width=0), row=1, col=1)
fig.add_scatter(x=x, y=stats.norm.pdf(x), mode="lines", line=dict(color="black", width=3), row=1, col=1)
fig.add_vline(x=1.96, line=dict(color=RED, dash="dash", width=2.5), opacity=1, row=1, col=1)
for z, c, t, pos in ((1.95, BLUE, "1.95: fail to reject", "top left"), (1.97, RED, "1.97: reject", "top right")):
    fig.add_scatter(x=[z], y=[stats.norm.pdf(z)], mode="markers+text", text=[t], textposition=pos,
                    marker=dict(size=16, color=c), textfont=dict(size=20, color=c), row=1, col=2 - 1)
z = np.linspace(0, 16, 400)
fig.add_scatter(x=z, y=stats.norm.sf(z), mode="lines", line=dict(color="black", width=3), row=1, col=2)
fig.add_hline(y=0.05, line=dict(color=RED, dash="dash", width=2.5), opacity=1, row=1, col=2)
fig.add_annotation(x=16, y=np.log10(0.05), xanchor="right", yanchor="bottom", text="0.05", showarrow=False,
                   font=dict(size=20, color=RED), row=1, col=2)
for zz, t, pos in ((2, "z = 2: 0.023", "top right"), (15, "z = 15: about 4 × 10⁻⁵¹  ", "middle left")):
    fig.add_scatter(x=[zz], y=[stats.norm.sf(zz)], mode="markers+text", text=[t], textposition=pos,
                    marker=dict(size=16, color=RED), textfont=dict(size=20, color=RED), row=1, col=2)
fig.update_xaxes(title_text="z", row=1, col=1)
fig.update_xaxes(title_text="z", range=[0, 16.5], row=1, col=2)
fig.update_yaxes(showticklabels=False, range=[0.03, 0.1], row=1, col=1)
fig.update_yaxes(type="log", title_text="P(Z ≥ z) if H₀ true", exponentformat="power", dtick=10, row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=480, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=20), margin=dict(l=40, r=20, t=60, b=60))
for a in fig.layout.annotations[:2]:
    a.font.size = 22
fig.write_image(here / "evidence_strength.png", scale=2)
fig.write_image(here / "evidence_strength.pdf")
