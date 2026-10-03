"""Training and validation loss without and with dropout, for the regression and the classification problem (Plotly)."""
from pathlib import Path
import pandas as pd
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, FONT

here = Path(__file__).parent
d = here.parent / "data"
reg, cls = pd.read_csv(d / "regression_history.csv"), pd.read_csv(d / "classification_history.csv")
panels = [(reg, "0", "Regression, no dropout", "MSE"), (reg, "0.2", "Regression, p = 0.2", "MSE"),
          (cls, "0", "Classification, no dropout", "binary cross-entropy"),
          (cls, "0.5", "Classification, p = 0.5", "binary cross-entropy")]
fig = make_subplots(2, 2, subplot_titles=[p[2] for p in panels], horizontal_spacing=0.08, vertical_spacing=0.16)
for k, (h, p, _, ylab) in enumerate(panels):
    r, c = k // 2 + 1, k % 2 + 1
    fig.add_scatter(x=h.epoch + 1, y=h[f"loss p={p}"], name="training loss", line=dict(color=BLUE, width=2),
                    showlegend=k == 0, row=r, col=c)
    fig.add_scatter(x=h.epoch + 1, y=h[f"val_loss p={p}"], name="validation loss", line=dict(color=ORANGE, width=2),
                    showlegend=k == 0, row=r, col=c)
    if c == 1:
        fig.update_yaxes(title=ylab, row=r, col=c)
# same y range within a row, so the two panels compare directly
top_r = max(reg[[f"val_loss p={p}" for p in ("0", "0.2")]].max())
top_c = max(cls[[f"val_loss p={p}" for p in ("0", "0.5")]].max())
fig.update_yaxes(range=[0, top_r * 1.05], row=1)
fig.update_yaxes(range=[0, top_c * 1.05], row=2)
fig.update_xaxes(title="epoch", row=2)
fig.update_layout(template="simple_white", width=1150, height=780, font=FONT,
                  legend=dict(orientation="h", x=0.0, y=-0.1), margin=dict(l=70, r=20, t=50, b=60))
fig.update_annotations(font=dict(size=18))
fig.write_image(here / "loss_curves.png", scale=2)
fig.write_image(here / "loss_curves.pdf")
