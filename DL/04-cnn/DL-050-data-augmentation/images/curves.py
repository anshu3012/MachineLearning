"""Training vs validation accuracy without and with augmentation, 2,000 training photos, mean of 3 seeds (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, FONT

here = Path(__file__).parent
h = pd.read_csv(here.parent / "data" / "history.csv")
fig = make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.04,
                    subplot_titles=("without augmentation", "with augmentation"))
for col, aug in ((1, "without"), (2, "with")):
    g = h[h.augmentation == aug]
    for key, name, c in (("accuracy", "training", BLUE), ("val_accuracy", "validation", ORANGE)):
        for _, s in g.groupby("seed"):
            fig.add_trace(go.Scatter(x=s.epoch, y=s[key], mode="lines", opacity=0.3, line=dict(color=c, width=1.2),
                                     showlegend=False), row=1, col=col)
        m = g.groupby("epoch")[key].mean()
        fig.add_trace(go.Scatter(x=m.index, y=m.values, mode="lines", name=f"{name} (mean of 3 seeds)",
                                 line=dict(color=c, width=4), showlegend=(col == 1)), row=1, col=col)
fig.update_xaxes(title="epoch")
fig.update_yaxes(title="accuracy", range=[0.45, 1.01], row=1, col=1)
fig.update_layout(template="simple_white", width=1000, height=430, font=FONT, legend=dict(x=0.62, y=0.04, yanchor="bottom", bgcolor="rgba(255,255,255,0.85)"),
                  margin=dict(l=60, r=20, t=40, b=60))
fig.write_image(here / "curves.png", scale=2)
fig.write_image(here / "curves.pdf")
