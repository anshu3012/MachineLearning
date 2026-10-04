"""Test accuracy of a SimpleRNN when G blank steps separate the review from the prediction (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import GREY, RED, FONT

here = Path(__file__).parent
d = pd.read_csv(here.parent / "data" / "gap_accuracy.csv")
m = d.groupby("gap").test_accuracy.mean().reset_index()
fig = go.Figure([go.Scatter(x=d.gap, y=d.test_accuracy, mode="markers", name="one run",
                            marker=dict(color=GREY, size=9, opacity=0.6)),
                 go.Scatter(x=m.gap, y=m.test_accuracy, mode="lines+markers", name="mean of 2 runs",
                            line=dict(color=RED, width=4), marker=dict(size=11))])
fig.add_hline(y=0.5, line=dict(color=GREY, dash="dash"), annotation_text="guessing (0.5)",
              annotation_position="bottom left")
fig.update_layout(template="simple_white", width=950, height=430, font=FONT,
                  xaxis=dict(title="blank steps between the review and the prediction"),
                  yaxis=dict(title="test accuracy", range=[0.45, 0.85]),
                  legend=dict(x=0.7, y=0.98), margin=dict(l=80, r=20, t=20, b=60))
fig.write_image(here / "gap_accuracy.png", scale=2)
fig.write_image(here / "gap_accuracy.pdf")
