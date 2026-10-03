"""The standard normal curve with the middle 1 - alpha shaded and alpha/2 in each tail: 95% gives z = 1.96,
75% gives z = 1.15."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
BLUE, RED = "#4C78A8", "#E45756"
z = np.linspace(-3.6, 3.6, 600)
levels = [0.95, 0.75]
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08,
                    subplot_titles=[f"confidence level {int(c * 100)}%" for c in levels])
for i, c in enumerate(levels, start=1):
    zc = stats.norm.ppf((1 + c) / 2)
    tail = (1 - c) / 2
    fig.add_scatter(x=z, y=stats.norm.pdf(z), mode="lines", line=dict(color="black", width=3), row=1, col=i)
    mid = z[np.abs(z) <= zc]
    fig.add_scatter(x=mid, y=stats.norm.pdf(mid), fill="tozeroy", fillcolor="rgba(76,120,168,0.35)",
                    line=dict(width=0), row=1, col=i)
    for side in (-1, 1):
        tz = z[side * z >= zc]
        fig.add_scatter(x=tz, y=stats.norm.pdf(tz), fill="tozeroy", fillcolor="rgba(228,87,86,0.45)",
                        line=dict(width=0), row=1, col=i)
        fig.add_annotation(x=side * 2.9, y=0.09, text=f"α/2 = {tail:.3f}", showarrow=False, font_size=17,
                           row=1, col=i)
    fig.add_annotation(x=0, y=0.16, text=f"1 − α = {c:.2f}", showarrow=False, font_size=19, row=1, col=i)
    fig.update_xaxes(tickvals=[-zc, 0, zc], ticktext=[f"−{zc:.2f}", "0", f"{zc:.2f}"], title_text="z",
                     row=1, col=i)
fig.update_yaxes(showticklabels=False, range=[0, 0.43])
fig.update_annotations(font_size=19)
fig.update_layout(template="simple_white", width=1100, height=400, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=20, r=20, t=40, b=50))
fig.write_image(here / "critical_values.png", scale=2)
fig.write_image(here / "critical_values.pdf")
