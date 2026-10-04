"""Rejection regions on the standard normal curve for the two z-test examples:
right-tailed (training program, z = 3.29) and two-tailed (chips packets, z = -1.58), alpha = 0.05."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
BLUE_FILL, RED_FILL, GREEN = "rgba(76,120,168,0.30)", "rgba(228,87,86,0.55)", "#54A24B"
z = np.linspace(-4, 4, 800)
pdf = stats.norm.pdf
cases = [  # title, rejection test, critical values, observed z
    ("training program: H₁ μ > 50 (right-tailed)", lambda x: x >= 1.645, [1.645], 3.29),
    ("chips packets: H₁ μ ≠ 50 (two-tailed)", lambda x: np.abs(x) >= 1.96, [-1.96, 1.96], -1.58),
]
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.07, subplot_titles=[c[0] for c in cases])
for i, (title, rejects, crit, zobs) in enumerate(cases, start=1):
    keep = z[~rejects(z)]
    fig.add_scatter(x=keep, y=pdf(keep), fill="tozeroy", fillcolor=BLUE_FILL, line=dict(width=0), row=1, col=i)
    for side in ([z[z >= crit[-1]]] if len(crit) == 1 else [z[z <= crit[0]], z[z >= crit[1]]]):
        fig.add_scatter(x=side, y=pdf(side), fill="tozeroy", fillcolor=RED_FILL, line=dict(width=0), row=1, col=i)
    fig.add_scatter(x=z, y=pdf(z), mode="lines", line=dict(color="black", width=3), row=1, col=i)
    fig.add_vline(x=zobs, line=dict(color=GREEN, width=4), opacity=1, row=1, col=i)
    fig.add_annotation(x=zobs, y=0.36, text=f"z = {zobs:.2f}".replace("-", "−"), showarrow=False, font=dict(size=19, color=GREEN),
                       xanchor="left" if zobs > 0 else "right", xshift=6 if zobs > 0 else -6, row=1, col=i)
    if len(crit) == 1:
        fig.add_annotation(x=2.6, y=0.09, text="α = 0.05", showarrow=False, font_size=17, row=1, col=i)
        fig.add_annotation(x=0, y=0.13, text="fail to reject H₀", showarrow=False, font_size=17, row=1, col=i)
    else:
        for s in (-1, 1):
            fig.add_annotation(x=s * 2.95, y=0.09, text="α/2 = 0.025", showarrow=False, font_size=17, row=1, col=i)
        fig.add_annotation(x=0.25, y=0.13, text="fail to reject H₀", showarrow=False, font_size=17, row=1, col=i)
    fig.update_xaxes(tickvals=[0] + crit, ticktext=["0"] + [f"{c:.4g}".replace("-", "−") for c in crit],
                     title_text="z", range=[-4, 4], row=1, col=i)
fig.update_yaxes(showticklabels=False, range=[0, 0.43])
fig.update_annotations(font_family="Latin Modern Roman")
fig.layout.annotations[0].font.size = fig.layout.annotations[1].font.size = 19
fig.update_layout(template="simple_white", width=1150, height=420, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=20, r=20, t=45, b=50))
fig.write_image(here / "rejection_regions.png", scale=2)
fig.write_image(here / "rejection_regions.pdf")
