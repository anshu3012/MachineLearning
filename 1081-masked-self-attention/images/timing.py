"""Time of one masked pass vs n one-word steps, batch of 64 on the GPU (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import BLUE, ORANGE, FONT

here = Path(__file__).parent
t = pd.read_csv(here.parent / "data" / "timing.csv")
fig = go.Figure()
fig.add_trace(go.Scatter(x=t.length, y=t.step_by_step_ms, name="step by step: n passes, one word each",
                         mode="lines+markers", line=dict(color=ORANGE, width=4), marker=dict(size=9)))
fig.add_trace(go.Scatter(x=t.length, y=t.parallel_ms, name="parallel: one masked pass",
                         mode="lines+markers", line=dict(color=BLUE, width=4), marker=dict(size=9)))
fig.update_layout(template="simple_white", width=950, height=450, font=FONT,
                  xaxis=dict(title="sequence length n (words)", type="log", tickvals=list(t.length)),
                  yaxis=dict(title="time for a batch of 64 (ms)"), legend=dict(x=0.02, y=0.98),
                  margin=dict(l=80, r=20, t=20, b=60))
fig.write_image(here / "timing.png", scale=2)
fig.write_image(here / "timing.pdf")
