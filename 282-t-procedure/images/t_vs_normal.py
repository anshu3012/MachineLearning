"""Student's t-distribution (orange) against the standard normal (blue) for 1, 4 and 29 degrees of freedom
(sample sizes 2, 5, 30), with the 95% t critical values in the titles (z = 1.96)."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
BLUE, ORANGE = "#4C78A8", "#F58518"
x = np.linspace(-5, 5, 600)
dfs = [1, 4, 29]
fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.05,
                    subplot_titles=[f"df = {d} (n = {d + 1}): 95% t = ±{stats.t.ppf(0.975, d):.2f}" for d in dfs])
for i, d in enumerate(dfs, start=1):
    fig.add_scatter(x=x, y=stats.norm.pdf(x), mode="lines", line=dict(color=BLUE, width=3), name="standard normal",
                    showlegend=(i == 1), row=1, col=i)
    fig.add_scatter(x=x, y=stats.t.pdf(x, d), mode="lines", line=dict(color=ORANGE, width=3, dash="dash"),
                    name="Student's t", showlegend=(i == 1), row=1, col=i)
    tc = stats.t.ppf(0.975, d)
    fig.update_xaxes(range=[-5, 5], title_text="value", row=1, col=i)
fig.update_yaxes(showticklabels=False, range=[0, 0.43])
fig.update_annotations(font_size=20)
fig.update_layout(template="simple_white", width=1200, height=440,
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.32),
                  font=dict(family="Latin Modern Roman", size=19), margin=dict(l=20, r=20, t=40, b=70))
fig.write_image(here / "t_vs_normal.png", scale=2)
fig.write_image(here / "t_vs_normal.pdf")
