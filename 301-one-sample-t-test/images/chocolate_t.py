"""Two-tailed p-value of the chocolate-bar one-sample t-test: t = -1.25 on Student's t with 24 degrees of freedom."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy import stats

here = Path(__file__).parent
GREEN, RED_FILL = "#54A24B", "rgba(228,87,86,0.65)"
df, tobs = 24, -1.25
t = np.linspace(-4, 4, 800)
pdf = stats.t.pdf(t, df)
fig = go.Figure()
for side in (t <= tobs, t >= -tobs):
    fig.add_scatter(x=t[side], y=pdf[side], fill="tozeroy", fillcolor=RED_FILL, line_width=0)
fig.add_scatter(x=t, y=stats.norm.pdf(t), mode="lines", line=dict(color="#6B6B6B", width=2, dash="dash"))
fig.add_scatter(x=t, y=pdf, mode="lines", line=dict(color="black", width=3))
for k, x in enumerate([tobs, -tobs]):
    fig.add_vline(x=x, line=dict(color=GREEN, width=3, dash="solid" if k == 0 else "dot"), opacity=1)
for s in (-1, 1):
    fig.add_annotation(x=s * 2.4, y=0.12, text=f"{stats.t.cdf(tobs, df):.3f}", showarrow=False, font_size=19)
fig.add_annotation(x=2.6, y=0.33, text="t, df = 24 (solid)<br>standard normal (dashed)", showarrow=False,
                   font_size=16, align="left")
fig.update_xaxes(tickvals=[tobs, 0, -tobs], ticktext=["−1.25", "0", "1.25"], title_text="t", range=[-4, 4])
fig.update_yaxes(showticklabels=False, range=[0, 0.43])
fig.update_layout(template="simple_white", width=800, height=400, showlegend=False,
                  title=dict(text="p = 0.112 + 0.112 = 0.223", x=0.5, font_size=20),
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=20, r=20, t=50, b=50))
fig.write_image(here / "chocolate_t.png", scale=2)
fig.write_image(here / "chocolate_t.pdf")
