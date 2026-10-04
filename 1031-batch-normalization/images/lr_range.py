"""Batch normalisation widens the range of usable learning rates, from data/lr_range.json (experiments/lr_range.py:
the Note's circles networks, plain SGD, 100 epochs, 5 seeds per point). Dots: single runs; lines: their mean. Plotly."""
import json
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

HERE = Path(__file__).parent
R = json.load(open(HERE.parent / "data" / "lr_range.json"))
lrs = R["lrs"]
P, B = np.array(R["plain"]), np.array(R["bn"])
assert (B.mean(1) > P.mean(1)).all() and P.mean(1).max() < 0.85 and (B.mean(1)[1:5] > 0.9).all()
X = np.arange(len(lrs))
jit = np.linspace(-0.12, 0.12, 5)
fig = go.Figure()
for M, col, name, off in ((P, "#E45756", "without batch normalisation", -0.08), (B, "#54A24B", "with batch normalisation", 0.08)):
    for k in range(5):
        fig.add_scatter(x=X + off + jit[k] * 0.5, y=M[:, k], mode="markers", marker=dict(size=8, color=col, opacity=0.45),
                        showlegend=False)
    fig.add_scatter(x=X + off, y=M.mean(1), mode="lines+markers", line=dict(color=col, width=4), marker=dict(size=12),
                    name=name)
fig.add_hrect(y0=0.9, y1=1.01, fillcolor="#54A24B", opacity=0.07, line_width=0)
fig.update_layout(template="simple_white", width=1050, height=600, font=dict(family="Latin Modern Roman", size=21),
                  title=dict(text="Validation accuracy after 100 epochs of plain SGD (5 runs per point)", x=0.5,
                             font=dict(size=21)),
                  xaxis=dict(title="learning rate", tickvals=X, ticktext=[str(l) for l in lrs]),
                  yaxis=dict(title="validation accuracy", range=[0.45, 1.01]),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2), margin=dict(l=80, r=30, t=70, b=130))
fig.write_image(HERE / "lr_range.png", scale=2)
print(P.mean(1).round(3), B.mean(1).round(3))
