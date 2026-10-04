"""What the raw-input network does: its validation accuracy only ever hits the two one-class values
(65% = 'did not buy' for everyone, 35% = 'bought' for everyone), and its loss stays in the tens to thousands
while the standardized run sits below 1 (Plotly, data from the Notebook)."""
from pathlib import Path
import pandas as pd
from plotly.subplots import make_subplots
from common import BLUE, RED, GREY, FONT

here = Path(__file__).parent
h = pd.read_csv(here.parent / "data" / "histories.csv")
assert h.raw_val_accuracy.min() == 0.3125 and h.raw_val_accuracy.max() == 0.65            # 31% to 65%
assert sorted(h.raw_val_accuracy.tail(10).unique()) == [0.35, 0.65]                      # last 10: only two values
assert round(h.raw_loss.iloc[0]) == 3618 and 17 < h.raw_loss.tail(10).min() and h.raw_loss.tail(10).max() < 175
fig = make_subplots(1, 2, horizontal_spacing=0.12,
                    subplot_titles=["Raw inputs: validation accuracy", "Training loss (log scale)"])
fig.add_scatter(x=h.epoch, y=h.raw_val_accuracy, mode="lines+markers", line=dict(color=RED, width=2),
                marker=dict(size=5), showlegend=False, row=1, col=1)
for v, txt in ((0.65, "65%: predicts 'did not buy' for everyone"), (0.35, "35%: predicts 'bought' for everyone")):
    fig.add_hline(y=v, line=dict(color=GREY, dash="dash", width=1.5), row=1, col=1)
    fig.add_annotation(x=50, y=v, text=txt, showarrow=False, yshift=14, font=dict(size=16, color=GREY),
                       bgcolor="rgba(255,255,255,0.85)", row=1, col=1)
fig.add_scatter(x=h.epoch, y=h.raw_loss, name="raw inputs", line=dict(color=RED, width=3), row=1, col=2)
fig.add_scatter(x=h.epoch, y=h.scaled_loss, name="standardized inputs", line=dict(color=BLUE, width=3), row=1, col=2)
fig.add_hline(y=0.69, line=dict(color=GREY, dash="dot", width=1.5), row=1, col=2)
fig.add_annotation(x=60, y=-0.16, text="0.69 = coin toss", showarrow=False, yshift=-12, font=dict(size=15, color=GREY),
                   row=1, col=2)
fig.update_xaxes(title="epoch")
fig.update_yaxes(range=[0.25, 0.75], tickformat=".0%", row=1, col=1)
fig.update_yaxes(type="log", tickvals=[0.3, 1, 10, 100, 1000], row=1, col=2)
fig.update_layout(template="simple_white", width=1150, height=470, font=FONT,
                  legend=dict(orientation="h", x=0.56, y=-0.2), margin=dict(l=60, r=20, t=50, b=60))
for t in ("Raw inputs: validation accuracy", "Training loss (log scale)"):
    fig.update_annotations(font_size=18, selector=dict(text=t))
fig.write_image(here / "raw_flip.png", scale=2)
fig.write_image(here / "raw_flip.pdf")
