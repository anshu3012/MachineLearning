"""The two-output model learns both targets at once: test-set age error and gender accuracy per epoch, 3 seeds (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, RED, FONT

here = Path(__file__).parent
c = pd.read_csv(here.parent / "data" / "two_output_curves.csv")
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
                    subplot_titles=("age output: mean absolute error (years)", "gender output: accuracy"))
for col, key, colour in ((1, "val_age_mae", BLUE), (2, "val_gender_accuracy", RED)):
    for _, s in c.groupby("seed"):
        fig.add_trace(go.Scatter(x=s.epoch, y=s[key], mode="lines", opacity=0.35, line=dict(color=colour, width=1.5),
                                 showlegend=False), row=1, col=col)
    m = c.groupby("epoch")[key].mean()
    fig.add_trace(go.Scatter(x=m.index, y=m.values, mode="lines+markers", showlegend=False,
                             line=dict(color=colour, width=4)), row=1, col=col)
fig.add_hline(y=15.03, line=dict(color="black", width=1.5, dash="dash"), row=1, col=1,
              annotation_text="guessing the median age: 15.0", annotation_position="bottom right")
fig.add_hline(y=0.525, line=dict(color="black", width=1.5, dash="dash"), row=1, col=2,
              annotation_text="guessing the commoner gender: 0.525", annotation_position="top right")
fig.update_yaxes(range=[0, 16.5], row=1, col=1)
fig.update_yaxes(range=[0.45, 0.92], row=1, col=2)
fig.update_xaxes(title="epoch")
fig.update_layout(template="simple_white", width=1000, height=400, font=FONT, margin=dict(l=60, r=20, t=40, b=60))
fig.write_image(here / "two_output_curves.png", scale=2)
fig.write_image(here / "two_output_curves.pdf")
