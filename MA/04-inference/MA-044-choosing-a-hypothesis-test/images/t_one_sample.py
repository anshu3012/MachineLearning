"""The one-sample t-test on the 60 heights (Plotly): the t-distribution with 59 degrees of freedom, the sample's
t = -0.64, and the two shaded tails at least that far from 0, which hold p = 0.53 of the area. The dashed lines are
the 5% rejection region, beyond t = +-2.00."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy import stats
from gifkit import BLUE, FONT, GREY, ORANGE, RED

here = Path(__file__).parent
h = pd.read_csv(here.parent / "data" / "people.csv").height
res = stats.ttest_1samp(h, 1.55)
t, p, df = res.statistic, res.pvalue, len(h) - 1
assert (round(t, 2), round(p, 2), df, round(h.mean(), 4), round(h.std(), 3)) == (-0.64, 0.53, 59, 1.5327, 0.211)
crit = stats.t.ppf(0.975, df)
xs = np.linspace(-4, 4, 801)
fig = go.Figure(go.Scatter(x=xs, y=stats.t.pdf(xs, df), mode="lines", line=dict(color=BLUE, width=4),
                           name="t-distribution, 59 degrees of freedom (if H₀ is true)"))
for side in (-1, 1):
    tail = xs[side * xs >= abs(t)]
    fig.add_scatter(x=tail, y=stats.t.pdf(tail, df), fill="tozeroy", mode="none", fillcolor="rgba(245,133,24,0.4)",
                    showlegend=side == 1, name=f"as extreme as our sample: p = {p:.2f}")
    fig.add_vline(x=side * crit, line=dict(color=RED, dash="dash", width=2))
fig.add_annotation(x=crit, y=0.15, text="rejection region<br>beyond ±2.00", showarrow=False, xanchor="left", xshift=8,
                   font=dict(size=18, color=RED))
fig.add_annotation(x=t, y=stats.t.pdf(t, df), ax=-150, ay=-10, text=f"our sample: t = {t:.2f}", font=dict(size=22, color=ORANGE),
                   arrowcolor=ORANGE, arrowwidth=2)
fig.update_layout(template="simple_white", width=1000, height=600, font=FONT,
                  xaxis=dict(title="t = (sample mean − 1.55) / (s / √n)"), yaxis=dict(title="density", range=[0, 0.45]),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2), margin=dict(l=80, r=30, t=20, b=130))
fig.write_image(here / "t_one_sample.png", scale=2)
