"""Bias squared, variance and expected test error against model complexity (polynomial degree), measured over
200 training sets (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from common import fits, decompose, NOISE

here = Path(__file__).parent
degs = list(range(1, 12))
b2, var = zip(*[decompose(fits(d)) for d in degs])
total = np.array(b2) + np.array(var) + NOISE ** 2
best = degs[int(np.argmin(total))]
fig = go.Figure()
fig.add_trace(go.Scatter(x=degs, y=b2, mode="lines+markers", name="bias²", line=dict(color="#4C78A8", width=3)))
fig.add_trace(go.Scatter(x=degs, y=var, mode="lines+markers", name="variance", line=dict(color="#F58518", width=3)))
fig.add_trace(go.Scatter(x=degs, y=total, mode="lines+markers", name="expected test error = bias² + variance + noise",
                         line=dict(color="#E45756", width=4)))
fig.add_trace(go.Scatter(x=[1, 11], y=[NOISE ** 2] * 2, mode="lines", name="noise (cannot be removed)",
                         line=dict(color="#6B6B6B", dash="dash")))
fig.add_annotation(x=best, y=float(np.log10(total.min())), ax=0, ay=-60, text=f"best: degree {best}", font=dict(size=16),
                   arrowcolor="#6B6B6B")
fig.add_annotation(x=1.6, y=1.3, text="underfitting", showarrow=False, font=dict(size=16, color="#4C78A8"))
fig.add_annotation(x=10.3, y=1.3, text="overfitting", showarrow=False, font=dict(size=16, color="#F58518"))
fig.update_layout(template="simple_white", width=950, height=520, font=dict(family="Latin Modern Roman", size=15),
                  legend=dict(orientation="h", y=-0.22, x=0.5, xanchor="center"), margin=dict(l=70, r=30, t=50, b=110),
                  title=dict(text="The bias-variance trade-off (measured)", x=0.5),
                  xaxis=dict(title="model complexity: polynomial degree"), yaxis=dict(title="squared error (log scale)", type="log", range=[-3.2, 1.8]))
for d, a, b, t in zip(degs, b2, var, total):
    print(d, round(a, 3), round(b, 3), round(t, 3))
fig.write_image(here / "tradeoff.png", scale=2)
fig.write_image(here / "tradeoff.pdf")
