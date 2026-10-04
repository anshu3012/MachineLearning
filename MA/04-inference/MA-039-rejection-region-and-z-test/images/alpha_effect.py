"""Two-tailed rejection regions for alpha = 0.30, 0.05 and 0.01: a smaller alpha pushes the critical values out
and widens the fail-to-reject region."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
BLUE_FILL, RED_FILL = "rgba(76,120,168,0.30)", "rgba(228,87,86,0.55)"
z = np.linspace(-3.6, 3.6, 800)
pdf = stats.norm.pdf
alphas = [0.30, 0.05, 0.01]
fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.05,
                    subplot_titles=[f"α = {a:.2f}" for a in alphas])
for i, a in enumerate(alphas, start=1):
    c = stats.norm.ppf(1 - a / 2)
    mid = z[np.abs(z) < c]
    fig.add_scatter(x=mid, y=pdf(mid), fill="tozeroy", fillcolor=BLUE_FILL, line=dict(width=0), row=1, col=i)
    for side in (z[z <= -c], z[z >= c]):
        fig.add_scatter(x=side, y=pdf(side), fill="tozeroy", fillcolor=RED_FILL, line=dict(width=0), row=1, col=i)
    fig.add_scatter(x=z, y=pdf(z), mode="lines", line=dict(color="black", width=3), row=1, col=i)
    fig.add_annotation(x=0, y=0.15, text=f"{1 - a:.2f}", showarrow=False, font_size=19, row=1, col=i)
    fig.update_xaxes(tickvals=[-c, 0, c], ticktext=[f"−{c:.2f}", "0", f"{c:.2f}"], title_text="z", row=1, col=i)
fig.update_yaxes(showticklabels=False, range=[0, 0.43])
fig.update_annotations(font_family="Latin Modern Roman")
for k in range(3):
    fig.layout.annotations[k].font.size = 20
fig.update_layout(template="simple_white", width=1150, height=380, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=20, r=20, t=45, b=50))
fig.write_image(here / "alpha_effect.png", scale=2)
fig.write_image(here / "alpha_effect.pdf")
