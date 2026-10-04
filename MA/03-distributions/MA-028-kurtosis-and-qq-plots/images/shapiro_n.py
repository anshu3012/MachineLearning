"""Normality tests flag small departures in large samples: Shapiro-Wilk p-values for samples of growing size from a
Student t distribution with 10 degrees of freedom (bell-shaped, slightly fatter tails than normal). Share of 200
seeds per size whose p-value falls below 0.05."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy import stats

here = Path(__file__).parent
NS = [20, 50, 100, 200, 500, 1000, 2000, 4000]
med, rej = [], []
for n in NS:
    p = np.array([stats.shapiro(np.random.default_rng(s).standard_t(10, n)).pvalue for s in range(200)])
    med.append(np.median(p)); rej.append(np.mean(p < 0.05))
assert med[0] > 0.3 and med[-1] < 0.05 and rej[-1] > 0.5, (med, rej)
fig = go.Figure(go.Bar(x=[str(n) for n in NS], y=[100 * r for r in rej], marker_color="#4C78A8",
                       text=[f"{100 * r:.0f}%" for r in rej], textposition="outside", textfont=dict(size=20)))
fig.update_layout(template="simple_white", width=1100, height=560, font=dict(family="Latin Modern Roman", size=19),
                  title=dict(text="Same mildly fat-tailed shape (t, 10 df): share of samples where Shapiro-Wilk rejects normality", x=0.5,
                             font=dict(size=20)),
                  xaxis=dict(title="sample size n"), yaxis=dict(title="samples rejected at 5 percent", range=[0, 112], ticksuffix="%"),
                  showlegend=False, margin=dict(l=90, r=30, t=70, b=70))
fig.write_image(here / "shapiro_n.png", scale=2)
fig.write_image(here / "shapiro_n.pdf")
print([round(m, 4) for m in med], rej)
