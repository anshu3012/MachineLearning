"""Two normal curves on one axis: newborn boys' length, N(19.64, 0.745^2) inches (WHO Child Growth Standards,
length-for-age boys at day 0: median 49.88 cm, SD 1.89 cm), and adult men's height, N(68, 3^2) inches (this Note).
The narrow curve must be tall and the wide one low, because each encloses area 1.
Run: python newborn_adult.py -> newborn_adult.png, .pdf"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from scipy import stats

HERE = Path(__file__).parent
BLUE, ORANGE, GREY = "#4C78A8", "#F58518", "#6B6B6B"
CM = 2.54
baby = stats.norm(49.8842 / CM, 49.8842 * 0.03795 / CM)            # WHO: M = 49.8842 cm, S = 0.03795 (SD = M * S)
adult = stats.norm(68, 3)
x = np.linspace(10, 82, 6000)
for d in (baby, adult):
    assert abs(d.cdf(d.mean() + 2 * d.std()) - d.cdf(d.mean() - 2 * d.std()) - 0.9545) < 1e-3
print("newborn mean %.2f sd %.3f peak %.3f | adult peak %.3f | ratio %.2f"
      % (baby.mean(), baby.std(), baby.pdf(baby.mean()), adult.pdf(68), baby.pdf(baby.mean()) / adult.pdf(68)))

fig = go.Figure()
for d, c, rgba, name, (lx, ly) in [(baby, BLUE, "rgba(76,120,168,0.25)", "newborn boys", (22.5, 0.42)),
                                     (adult, ORANGE, "rgba(245,133,24,0.25)", "adult men", (40, 0.26))]:
    m, s = d.mean(), d.std()
    band = np.linspace(m - 2 * s, m + 2 * s, 400)
    fig.add_scatter(x=band, y=d.pdf(band), fill="tozeroy", mode="none", fillcolor=rgba, showlegend=False)
    fig.add_scatter(x=x, y=d.pdf(x), mode="lines", line=dict(color=c, width=4, simplify=False), showlegend=False)
    fig.add_annotation(x=lx, y=ly, xanchor="left", align="left", showarrow=False, font=dict(color=c, size=20),
                       text=f"<b>{name}</b><br>mean {m:.1f}, SD {s:.2f}<br>peak density {d.pdf(m):.3f}"
                            f"<br>95% (shaded): {m - 2 * s:.1f} to {m + 2 * s:.1f}")
fig.update_layout(template="simple_white", width=1000, height=520, font=dict(family="Latin Modern Roman", size=20),
                  xaxis=dict(title="length or height (inches)", range=[10, 82], dtick=10),
                  yaxis=dict(title="probability density", range=[0, 0.68]), margin=dict(l=80, r=20, t=20, b=60))
fig.write_image(HERE / "newborn_adult.png", scale=2)
fig.write_image(HERE / "newborn_adult.pdf")
