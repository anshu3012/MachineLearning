"""Training and validation accuracy of the next-word LSTM (seed 0), with the epoch early stopping keeps (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import BLUE, ORANGE, GREY, FONT

here = Path(__file__).parent
h = pd.read_csv(here.parent / "data" / "history.csv")
h = h[h.seed == 0]
best = int(h.epoch[h.val_loss.idxmin()])
fig = go.Figure()
fig.add_trace(go.Scatter(x=h.epoch, y=h.accuracy, name="training stories", mode="lines+markers", line=dict(color=BLUE, width=4)))
fig.add_trace(go.Scatter(x=h.epoch, y=h.val_accuracy, name="validation stories", mode="lines+markers", line=dict(color=ORANGE, width=4)))
fig.add_vline(x=best, line=dict(color=GREY, dash="dot", width=2))
fig.add_annotation(x=best, y=0.235, text=f"kept: epoch {best} (lowest validation loss)", showarrow=False, xanchor="left", xshift=6, font=FONT)
fig.update_layout(template="simple_white", width=950, height=450, font=FONT, xaxis=dict(title="epoch", dtick=1),
                  yaxis=dict(title="next-word accuracy", range=[0, 0.25]),
                  legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.8)"), margin=dict(l=70, r=20, t=20, b=60))
fig.write_image(here / "accuracy_curves.png", scale=2)
fig.write_image(here / "accuracy_curves.pdf")
