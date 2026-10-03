"""Left-tailed, right-tailed and two-tailed rejection regions at alpha = 0.05."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
BLUE_FILL, RED_FILL = "rgba(76,120,168,0.30)", "rgba(228,87,86,0.55)"
z = np.linspace(-3.6, 3.6, 800)
pdf = stats.norm.pdf
cases = [("H₁: μ < μ₀ (left-tailed)", [(-9, -1.645)], ["−1.645"], [-1.645]),
         ("H₁: μ ≠ μ₀ (two-tailed)", [(-9, -1.96), (1.96, 9)], ["−1.96", "1.96"], [-1.96, 1.96]),
         ("H₁: μ > μ₀ (right-tailed)", [(1.645, 9)], ["1.645"], [1.645])]
fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.05, subplot_titles=[c[0] for c in cases])
for i, (title, regions, labels, ticks) in enumerate(cases, start=1):
    fig.add_scatter(x=z, y=pdf(z), fill="tozeroy", fillcolor=BLUE_FILL, line_width=0, row=1, col=i)
    for lo, hi in regions:
        part = z[(z >= lo) & (z <= hi)]
        fig.add_scatter(x=part, y=pdf(part), fill="tozeroy", fillcolor=RED_FILL, line_width=0, row=1, col=i)
        area = 0.05 / len(regions)
        fig.add_annotation(x=np.clip((lo + hi) / 2, -2.9, 2.9), y=0.1, text=f"{area:g}", showarrow=False,
                           font_size=18, row=1, col=i)
    fig.add_scatter(x=z, y=pdf(z), mode="lines", line=dict(color="black", width=3), row=1, col=i)
    fig.update_xaxes(tickvals=[0] + ticks, ticktext=["0"] + labels, title_text="z", row=1, col=i)
fig.update_yaxes(showticklabels=False, range=[0, 0.43])
fig.update_annotations(font_family="Latin Modern Roman")
for k in range(3):
    fig.layout.annotations[k].font.size = 19
fig.update_layout(template="simple_white", width=1150, height=380, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=20, r=20, t=45, b=50))
fig.write_image(here / "tails.png", scale=2)
fig.write_image(here / "tails.pdf")
