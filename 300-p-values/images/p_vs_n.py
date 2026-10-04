"""A small p-value does not mean a large effect: a training program that adds only 0.1 cars a day (sigma = 5, the
Note's right-tailed z-test) gives the p-value expected at the true effect, 1 - Phi(0.1 / (5 / sqrt(n))), for samples
of 10 to 100,000 employees. The p-value falls below 0.05 once n passes about 6,800, although the effect never changes."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy import stats

here = Path(__file__).parent
n = np.logspace(1, 5, 300)
p = stats.norm.sf(0.1 / (5 / np.sqrt(n)))
cross = (1.645 * 5 / 0.1) ** 2
assert 6700 < cross < 6800 and p[-1] < 1e-9
fig = go.Figure()
fig.add_scatter(x=n, y=p, mode="lines", line=dict(color="#4C78A8", width=4))
fig.add_hline(y=0.05, line=dict(color="#E45756", dash="dash", width=2))
fig.add_vline(x=cross, line=dict(color="#9a9a9a", dash="dot", width=2))
fig.add_annotation(x=np.log10(cross), y=np.log10(0.05), text=f"n ≈ {cross:,.0f}: p drops below 0.05", ax=-170, ay=60,
                   font=dict(size=19), arrowwidth=2)
fig.update_layout(template="simple_white", width=1100, height=540, font=dict(family="Latin Modern Roman", size=19),
                  title=dict(text="The same tiny effect (0.1 cars a day): bigger samples, smaller p-values", x=0.5),
                  xaxis=dict(title="employees in the sample (log scale)", type="log"),
                  yaxis=dict(title="p-value (log scale)", type="log", range=[-10, 0], exponentformat="power"),
                  showlegend=False, margin=dict(l=90, r=30, t=70, b=70))
fig.write_image(here / "p_vs_n.png", scale=2)
fig.write_image(here / "p_vs_n.pdf")
