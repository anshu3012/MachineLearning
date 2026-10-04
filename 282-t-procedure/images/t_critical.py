"""Section 6: t critical values against degrees of freedom. The two-sided 95% value (area 0.025 in each tail) is
always above z = 1.96 and falls towards it; the one-tail 5% value is the column readers slip into by mistake."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from scipy import stats

here = Path(__file__).parent
BLUE, ORANGE, RED, GREY = "#4C78A8", "#F58518", "#E45756", "#6B6B6B"
df = np.unique(np.round(np.logspace(0, 3, 300)).astype(int))
t2, t1 = stats.t.ppf(0.975, df), stats.t.ppf(0.95, df)
table = {1: 12.706, 4: 2.776, 9: 2.262, 29: 2.045, 30: 2.042, 40: 2.021, 60: 2.000, 100: 1.984, 1000: 1.962}
assert all(round(stats.t.ppf(0.975, d), 3) == v for d, v in table.items()) and round(stats.t.ppf(0.95, 40), 3) == 1.684
assert (t2 > 1.96).all()
fig = go.Figure()
fig.add_scatter(x=df, y=t2, mode="lines", name="t, 0.025 column: two-sided 95%", line=dict(color=BLUE, width=4))
fig.add_scatter(x=df, y=t1, mode="lines", name="t, 0.05 column: one tail of 5%", line=dict(color=ORANGE, width=3, dash="dash"))
fig.add_hline(y=1.96, line=dict(color="black", width=2, dash="dot"))
fig.add_hline(y=1.645, line=dict(color=GREY, width=2, dash="dot"))
fig.add_annotation(x=np.log10(1000), y=1.96, text="z = 1.96", xanchor="right", yanchor="bottom", showarrow=False,
                   font=dict(size=18))
fig.add_annotation(x=np.log10(1000), y=1.645, text="z = 1.645", xanchor="right", yanchor="bottom", showarrow=False,
                   font=dict(size=18, color=GREY))
for d, ax_, ay_ in [(9, 40, -40), (29, 40, -40)]:
    fig.add_scatter(x=[d], y=[table[d]], mode="markers", marker=dict(color=BLUE, size=12), showlegend=False)
    fig.add_annotation(x=np.log10(d), y=table[d], text=f"df = {d}: {table[d]}", ax=ax_, ay=ay_, font=dict(size=18))
fig.add_scatter(x=[40, 40], y=[2.021, 1.684], mode="markers", marker=dict(color=[BLUE, RED], size=12), showlegend=False)
fig.add_annotation(x=np.log10(40), y=1.684, text="slip: 1.684 (wrong column)", ax=120, ay=-14,
                   font=dict(size=18, color=RED))
fig.add_annotation(x=np.log10(2.3), y=4.4, text="df = 1: 12.706 (off the chart)", xanchor="left", showarrow=False,
                   font=dict(size=18, color=BLUE))
fig.update_layout(template="simple_white", width=1000, height=600, font=dict(family="Latin Modern Roman", size=19),
                  xaxis=dict(type="log", tickvals=[1, 2, 5, 10, 20, 50, 100, 200, 500, 1000], title="degrees of freedom df = n − 1 (log scale)"),
                  yaxis=dict(title="critical value", range=[1.5, 4.5]), legend=dict(x=0.45, y=0.98),
                  margin=dict(l=70, r=20, t=20, b=60))
fig.write_image(here / "t_critical.png", scale=2)
fig.write_image(here / "t_critical.pdf")
