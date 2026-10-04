"""What H0 claims, drawn: if the new style changed nothing (mu = 6), the mean of 5 lessons would still vary by chance.
Using the five lessons' own spread (s = 3.16), the one-sample t-test's picture of that chance variation puts the
observed mean 9 at t = 2.12 with 4 degrees of freedom; 5.1 percent of the H0 curve lies at or beyond it."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy import stats

here = Path(__file__).parent
x = np.array([7, 9, 5, 11, 13.0])
se = x.std(ddof=1) / np.sqrt(5)
t = (x.mean() - 6) / se
p = stats.t(4).sf(t)
assert x.mean() == 9 and round(x.std(ddof=1), 2) == 3.16 and round(t, 2) == 2.12 and round(p, 3) == 0.051
assert np.isclose(p, stats.ttest_1samp(x, 6, alternative="greater").pvalue)
m = np.linspace(6 - 5 * se, 6 + 5 * se, 500)
dens = stats.t(4, loc=6, scale=se).pdf(m)
fig = go.Figure()
fig.add_scatter(x=m, y=dens, mode="lines", line=dict(color="#4C78A8", width=4), name="if H0 is true")
tail = m >= 9
fig.add_scatter(x=np.r_[9, m[tail], m[tail][-1]], y=np.r_[0, dens[tail], 0], fill="toself", fillcolor="rgba(245,133,24,0.6)",
                line=dict(width=0), mode="lines", name="as far as 9 or further")
fig.add_vline(x=6, line=dict(color="#6B6B6B", dash="dash", width=2))
fig.add_vline(x=9, line=dict(color="#F58518", width=3))
fig.add_annotation(x=6, y=dens.max() * 1.05, text="H<sub>0</sub>: μ = 6", showarrow=False, font=dict(size=20, color="#555"))
fig.add_annotation(x=9, y=dens.max() * 0.55, text=f"our 5 lessons: mean 9<br>{100 * p:.1f} percent of the curve<br>lies at 9 or beyond",
                   showarrow=False, xanchor="left", xshift=10, font=dict(size=19, color="#c55a00"))
fig.update_layout(template="simple_white", width=1100, height=540, font=dict(family="Latin Modern Roman", size=19),
                  showlegend=False, title=dict(text="If the new style changed nothing, how would 5-lesson means vary?", x=0.5),
                  xaxis=dict(title="mean view duration of 5 lessons (minutes)"), yaxis=dict(title="density", showticklabels=False),
                  margin=dict(l=60, r=30, t=70, b=70))
fig.write_image(here / "null_world.png", scale=2)
fig.write_image(here / "null_world.pdf")
