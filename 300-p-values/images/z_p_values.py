"""P-values of the two z-tests: right-tailed training program (z = 3.29, area to the right) and
two-tailed chips packets (z = -1.58, area beyond -1.58 plus area beyond +1.58)."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
GREEN, RED_FILL = "#54A24B", "rgba(228,87,86,0.65)"
z = np.linspace(-4, 4, 800)
pdf = stats.norm.pdf
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.07,
                    subplot_titles=["training program, right-tailed: p = P(Z ≥ 3.29) = 0.0005",
                                    "chips packets, two-tailed: p = 2 × P(Z ≤ −1.58) = 0.114"])
# right-tailed
tail = z[z >= 3.29]
fig.add_scatter(x=tail, y=pdf(tail), fill="tozeroy", fillcolor=RED_FILL, line_width=0, row=1, col=1)
fig.add_annotation(x=3.45, y=0.004, ax=2.2, ay=0.3, axref="x", ayref="y", text="area 0.0005<br>(too thin to see)",
                   font_size=17, arrowcolor="#E45756", arrowwidth=2, xanchor="center", row=1, col=1)
# two-tailed
for side in (z[z <= -1.58], z[z >= 1.58]):
    fig.add_scatter(x=side, y=pdf(side), fill="tozeroy", fillcolor=RED_FILL, line_width=0, row=1, col=2)
for s in (-1, 1):
    fig.add_annotation(x=s * 2.6, y=0.11, text="0.057", showarrow=False, font_size=18, row=1, col=2)
for i, obs in [(1, [3.29]), (2, [-1.58, 1.58])]:
    fig.add_scatter(x=z, y=pdf(z), mode="lines", line=dict(color="black", width=3), row=1, col=i)
    for k, o in enumerate(obs):
        fig.add_vline(x=o, line=dict(color=GREEN, width=3, dash="solid" if k == 0 else "dot"), opacity=1,
                      row=1, col=i)
    fig.update_xaxes(tickvals=[0] + obs, ticktext=["0"] + [f"{o:.2f}".replace("-", "−") for o in obs],
                     title_text="z", range=[-4, 4], row=1, col=i)
fig.update_yaxes(showticklabels=False, range=[0, 0.43])
fig.update_annotations(font_family="Latin Modern Roman")
fig.layout.annotations[0].font.size = fig.layout.annotations[1].font.size = 18
fig.update_layout(template="simple_white", width=1150, height=410, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=20, r=20, t=45, b=50))
fig.write_image(here / "z_p_values.png", scale=2)
fig.write_image(here / "z_p_values.pdf")
