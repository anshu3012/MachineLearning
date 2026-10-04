"""Training and validation accuracy of the next-word LSTM over 100 epochs (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import BLUE, ORANGE, FONT

here = Path(__file__).parent
h = pd.read_csv(here.parent / "data" / "history.csv")
fig = go.Figure()
fig.add_trace(go.Scatter(x=h.epoch, y=h.accuracy, name="training fables (1-40)", line=dict(color=BLUE, width=4)))
fig.add_trace(go.Scatter(x=h.epoch, y=h.val_accuracy, name="held-out fables (41-48)", line=dict(color=ORANGE, width=4)))
fig.update_layout(template="simple_white", width=950, height=450, font=FONT, xaxis=dict(title="epoch"),
                  yaxis=dict(title="next-word accuracy", range=[0, 1.02]),
                  legend=dict(x=0.55, y=0.5, bgcolor="rgba(255,255,255,0.8)"), margin=dict(l=70, r=20, t=20, b=60))
fig.write_image(here / "accuracy_curves.png", scale=2)
fig.write_image(here / "accuracy_curves.pdf")
