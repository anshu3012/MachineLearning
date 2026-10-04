"""When to refuse a t-test: messages sent per day on 7 random days (illustrative values built to have the stated
mean 125 and SD 44, strongly right-skewed), beside the three conditions. Random: met. Independent (7 <= 10% of
365): met. Normal: the population is not known to be normal, n = 7 < 30, and the sample is skewed: not met.
Run: python conditions_check.py  -> conditions_check.png (Plotly)"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
RED, GREEN = "#E45756", "#54A24B"
shape = np.array([0, 1, 2, 3, 5, 12, 30], float)              # strongly right-skewed pattern
days = np.round(125 + 44 * (shape - shape.mean()) / shape.std(ddof=1))
assert abs(days.mean() - 125) < 1 and abs(days.std(ddof=1) - 44) < 1

fig = make_subplots(rows=1, cols=2, column_widths=[0.5, 0.5], horizontal_spacing=0.04)
fig.add_scatter(x=days, y=np.zeros(7), mode="markers", marker=dict(size=26, color="#4C78A8", line=dict(width=2)),
                row=1, col=1)
fig.add_vline(x=125, line=dict(color="black", dash="dash", width=2), row=1, col=1)
fig.add_annotation(x=125, y=0.8, text="mean 125", showarrow=False, xanchor="left", xshift=6, row=1, col=1)
fig.add_annotation(x=200, y=-0.55, text="long right tail", showarrow=False, font=dict(color=RED), row=1, col=1)
lines = [("Random sample of days", True), ("Independent: 7 ≤ 10% of 365", True), ("Normal:", None),
         ("  population normal? unknown", False), ("  n ≥ 30? n = 7", False), ("  sample symmetric? skewed", False)]
for i, (txt, ok) in enumerate(lines):
    mark = "" if ok is None else ("✓ " if ok else "✗ ")
    fig.add_annotation(x=0.0, y=1 - i * 0.36, xref="x2", yref="y2", xanchor="left", showarrow=False, text=mark + txt,
                       font=dict(size=24, color="black" if ok is None else (GREEN if ok else RED)))
fig.update_xaxes(title_text="messages sent in a day", range=[60, 260], row=1, col=1)
fig.update_yaxes(visible=False, range=[-1, 1], row=1, col=1)
fig.update_xaxes(visible=False, range=[0, 1], row=1, col=2)
fig.update_yaxes(visible=False, range=[-0.9, 1.2], row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=420, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=24),
                  title=dict(text="7 days, H₀: μ = 100: the normal condition fails, so no t-test", x=0.5),
                  margin=dict(l=30, r=30, t=70, b=70))
fig.write_image(HERE / "conditions_check.png", scale=2)
fig.write_image(HERE / "conditions_check.pdf")
