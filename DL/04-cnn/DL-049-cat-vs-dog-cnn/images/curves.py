"""Training vs validation accuracy and loss of the plain CNN: 3 seeds (thin) and their mean (thick) (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, FONT

here = Path(__file__).parent
h = pd.read_csv(here.parent / "data" / "history.csv")
h = h[h.model == "plain"]
fig = make_subplots(rows=1, cols=2, subplot_titles=("accuracy", "loss (binary cross-entropy)"), horizontal_spacing=0.1)
for col, metric in ((1, "accuracy"), (2, "loss")):
    for key, name, c in ((metric, "training", BLUE), ("val_" + metric, "validation", ORANGE)):
        for _, g in h.groupby("seed"):
            fig.add_trace(go.Scatter(x=g.epoch, y=g[key], mode="lines", opacity=0.35, line=dict(color=c, width=1.5),
                                     showlegend=False), row=1, col=col)
        m = h.groupby("epoch")[key].mean()
        fig.add_trace(go.Scatter(x=m.index, y=m.values, mode="lines+markers", name=f"{name} (mean of 3 seeds)",
                                 line=dict(color=c, width=4), showlegend=(col == 1)), row=1, col=col)
fig.update_xaxes(title="epoch", dtick=1)
fig.update_layout(template="simple_white", width=1000, height=430, font=FONT, legend=dict(x=0.2, y=0.04, yanchor="bottom", bgcolor="rgba(255,255,255,0.85)"),
                  margin=dict(l=60, r=20, t=40, b=60))
fig.write_image(here / "curves.png", scale=2)
fig.write_image(here / "curves.pdf")
