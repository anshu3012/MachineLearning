"""Training and validation loss over 2,000 epochs: no regularisation, L2 and L1 (Plotly)."""
from pathlib import Path
import pandas as pd
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, FONT

here = Path(__file__).parent
h = pd.read_csv(here.parent / "data" / "histories.csv")
names = [("none", "No regularisation"), ("L2", "L2, λ = 0.03"), ("L1", "L1, λ = 0.001")]
fig = make_subplots(1, 3, horizontal_spacing=0.06, subplot_titles=[t for _, t in names], shared_yaxes=True)
for k, (n, _) in enumerate(names):
    fig.add_scatter(x=h.epoch + 1, y=h[f"loss {n}"], name="training loss", line=dict(color=BLUE, width=2),
                    showlegend=k == 0, row=1, col=k + 1)
    fig.add_scatter(x=h.epoch + 1, y=h[f"val_loss {n}"], name="validation loss", line=dict(color=ORANGE, width=2),
                    showlegend=k == 0, row=1, col=k + 1)
fig.update_xaxes(title="epoch")
fig.update_yaxes(title="loss", col=1)
fig.update_layout(template="simple_white", width=1200, height=430, font=FONT,
                  legend=dict(orientation="h", x=0.0, y=-0.25), margin=dict(l=60, r=20, t=50, b=60))
fig.update_annotations(font=dict(size=18))
fig.write_image(here / "curves.png", scale=2)
fig.write_image(here / "curves.pdf")
