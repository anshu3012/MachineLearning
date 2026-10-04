"""PMF of one die and of the average of two dice: same expected value 3.5, different variance (Plotly)."""
from pathlib import Path
from collections import Counter
import itertools
import numpy as np
from plotly.subplots import make_subplots

here = Path(__file__).parent
one_x, one_p = np.arange(1, 7), np.full(6, 1 / 6)
avg = Counter((a + b) / 2 for a, b in itertools.product(range(1, 7), repeat=2))
avg_x = np.array(sorted(avg)); avg_p = np.array([avg[v] / 36 for v in avg_x])
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08,
                    subplot_titles=["One die: Var 2.92, SD 1.71", "Average of two dice: Var 1.46, SD 1.21"])
for a in fig.layout.annotations:
    a.font.size = 24
for col, (x, p, w) in enumerate([(one_x, one_p, 0.6), (avg_x, avg_p, 0.3)], start=1):
    mean = (x * p).sum(); sd = np.sqrt(((x - mean) ** 2 * p).sum())
    print(col, mean, sd ** 2)
    fig.add_bar(x=x, y=p, width=w, marker_color="#4C78A8", showlegend=False, row=1, col=col)
    fig.add_scatter(x=[mean, mean], y=[0, 0.24], mode="lines", line=dict(color="#F58518", width=3), showlegend=False,
                    row=1, col=col)
    fig.add_scatter(x=[mean - sd, mean + sd], y=[0.205, 0.205], mode="lines", line=dict(color="#E45756", width=4),
                    showlegend=False, row=1, col=col)
    fig.add_annotation(x=mean + 0.08, y=0.232, text="E[X] = 3.5", xanchor="left", showarrow=False,
                       font=dict(size=22, color="#F58518"), row=1, col=col)
    fig.add_annotation(x=mean + sd + 0.08, y=0.205, text="± 1 SD", xanchor="left", showarrow=False,
                       font=dict(size=22, color="#E45756"), row=1, col=col)
fig.update_xaxes(range=[0.5, 6.5], dtick=1, title_text="value")
fig.update_yaxes(range=[0, 0.24], title_text="probability", row=1, col=1)
fig.update_yaxes(range=[0, 0.24], row=1, col=2)

fig.update_layout(template="simple_white", width=1000, height=470, font=dict(family="Latin Modern Roman", size=22),
                  margin=dict(l=70, r=20, t=50, b=60))
fig.write_image(here / "spread.png", scale=2)
fig.write_image(here / "spread.pdf")
