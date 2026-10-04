"""The warm-up learning-rate schedule of Vaswani et al. (2017, eq. 3) for d_model = 512, warmup_steps = 4000 (Plotly line chart)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from common import BLUE, ORANGE, GREY, FONT

here = Path(__file__).parent
d_model, warmup = 512, 4000
step = np.arange(1, 100_001)
lr = d_model ** -0.5 * np.minimum(step ** -0.5, step * warmup ** -1.5)
peak = lr.max()
assert step[lr.argmax()] == warmup and abs(peak - (d_model * warmup) ** -0.5) < 1e-12

fig = go.Figure()
fig.add_vrect(x0=0, x1=warmup, fillcolor=ORANGE, opacity=0.12, line_width=0)
fig.add_trace(go.Scatter(x=step, y=lr * 1e4, mode="lines", line=dict(color=BLUE, width=4), showlegend=False))
fig.add_trace(go.Scatter(x=[warmup], y=[peak * 1e4], mode="markers", marker=dict(color=ORANGE, size=12), showlegend=False))
fig.add_annotation(x=warmup, y=peak * 1e4, text=f"peak at step 4,000: {peak * 1e4:.2f} × 10⁻⁴", showarrow=True,
                   ax=120, ay=-10, xanchor="left", font=FONT)
fig.add_annotation(x=warmup, y=1.2, text="warm-up (steps 1 to 4,000): linear rise", showarrow=True, ax=60, ay=0,
                   xanchor="left", font=dict(FONT, color=ORANGE), arrowcolor=ORANGE)
fig.add_annotation(x=60_000, y=2.6, text="decay: ∝ 1/√step", showarrow=False, font=dict(FONT, color=BLUE))
fig.add_annotation(x=100_000, y=lr[-1] * 1e4, text=f"step 100,000: {lr[-1] * 1e4:.2f} × 10⁻⁴", showarrow=True,
                   ax=-20, ay=-45, xanchor="right", font=dict(FONT, color=GREY))
fig.update_layout(template="simple_white", width=900, height=430, font=FONT, margin=dict(l=80, r=30, t=20, b=60),
                  xaxis=dict(title="training step", tickformat=",", range=[0, 102_000]),
                  yaxis=dict(title="learning rate (× 10⁻⁴)", range=[0, 7.8]))
fig.write_image(here / "warmup.png", scale=2)
fig.write_image(here / "warmup.pdf")
