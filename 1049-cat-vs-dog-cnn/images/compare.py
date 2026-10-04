"""Plain CNN vs the same CNN with batch normalisation and dropout: validation accuracy and the
training-validation accuracy gap, mean of 3 seeds (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import GREY, GREEN, FONT

here = Path(__file__).parent
h = pd.read_csv(here.parent / "data" / "history.csv")
m = h.groupby(["model", "epoch"])[["accuracy", "val_accuracy"]].mean().reset_index()
m["gap"] = m.accuracy - m.val_accuracy
fig = make_subplots(rows=1, cols=2, subplot_titles=("validation accuracy", "gap: training minus validation accuracy"),
                    horizontal_spacing=0.1)
for key, name, c in (("plain", "plain CNN", GREY), ("bn_dropout", "batch normalisation + dropout", GREEN)):
    g = m[m.model == key]
    fig.add_trace(go.Scatter(x=g.epoch, y=g.val_accuracy, mode="lines+markers", name=name, line=dict(color=c, width=4)),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=g.epoch, y=g.gap, mode="lines+markers", showlegend=False, line=dict(color=c, width=4)),
                  row=1, col=2)
fig.add_hline(y=0, line=dict(color="black", width=1), row=1, col=2)
fig.update_xaxes(title="epoch", dtick=1)
fig.update_layout(template="simple_white", width=1000, height=430, font=FONT, legend=dict(x=0.17, y=0.04, yanchor="bottom", bgcolor="rgba(255,255,255,0.85)"),
                  margin=dict(l=60, r=20, t=40, b=60))
fig.write_image(here / "compare.png", scale=2)
fig.write_image(here / "compare.pdf")
