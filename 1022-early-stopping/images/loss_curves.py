"""Training and validation loss: 3,500 epochs without early stopping (left) and the early-stopping run (right) (Plotly)."""
from pathlib import Path
import pandas as pd
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, GREY, FONT

here = Path(__file__).parent
h = pd.read_csv(here.parent / "data" / "history_3500.csv")
e = pd.read_csv(here.parent / "data" / "history_early_stopping.csv")
best, best_e, stop = h.loc[h.val_loss.idxmin()], e.loc[e.val_loss.idxmin()], e.iloc[-1]
fig = make_subplots(1, 2, column_widths=[0.6, 0.4], horizontal_spacing=0.1,
                    subplot_titles=["Without early stopping: 3,500 epochs",
                                    f"With early stopping: {len(e)} epochs"])
for col, d in ((1, h), (2, e)):
    fig.add_scatter(x=d.epoch, y=d.loss, name="training loss", line=dict(color=BLUE, width=3),
                    showlegend=col == 1, row=1, col=col)
    fig.add_scatter(x=d.epoch, y=d.val_loss, name="validation loss", line=dict(color=ORANGE, width=3),
                    showlegend=col == 1, row=1, col=col)
fig.add_vline(x=best.epoch, line=dict(color=GREY, dash="dot", width=2), row=1, col=1)
fig.add_annotation(x=best.epoch, y=0.95, text=f"lowest validation loss<br>epoch {best.epoch:.0f}", showarrow=False,
                   xanchor="left", xshift=6, row=1, col=1)
fig.add_vrect(x0=best_e.epoch, x1=stop.epoch, fillcolor=GREY, opacity=0.15, line_width=0, row=1, col=2)
fig.add_annotation(x=stop.epoch, y=0.95, text=f"best {best_e.epoch:.0f}, stop {stop.epoch:.0f}<br>(patience 50)",
                   showarrow=False, xanchor="right", xshift=-6, row=1, col=2)
fig.update_xaxes(title="epoch")
fig.update_yaxes(title="loss (binary cross-entropy)", range=[0, 1.05], row=1, col=1)
fig.update_yaxes(range=[0, 1.05], row=1, col=2)
fig.update_layout(template="simple_white", width=1150, height=470, font=FONT,
                  legend=dict(orientation="h", x=0.0, y=-0.2), margin=dict(l=70, r=20, t=50, b=60))
fig.update_annotations(font=dict(size=17))
fig.write_image(here / "loss_curves.png", scale=2)
fig.write_image(here / "loss_curves.pdf")
