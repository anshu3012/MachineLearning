"""Time of one training step, LSTM vs self-attention, by sequence length (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import BLUE, ORANGE, FONT

here = Path(__file__).parent
t = pd.read_csv(here.parent / "data" / "timing.csv")
fig = go.Figure()
for col, c in (("LSTM", BLUE), ("self-attention", ORANGE)):
    fig.add_trace(go.Scatter(x=t.length, y=t[col], name=col, mode="lines+markers", line=dict(color=c, width=4), marker=dict(size=9)))
fig.update_layout(template="simple_white", width=950, height=450, font=FONT,
                  xaxis=dict(title="sequence length (words)", type="log", tickvals=list(t.length)),
                  yaxis=dict(title="time of one training step (ms)"), legend=dict(x=0.03, y=0.97),
                  margin=dict(l=70, r=20, t=20, b=60))
fig.write_image(here / "timing.png", scale=2)
fig.write_image(here / "timing.pdf")
