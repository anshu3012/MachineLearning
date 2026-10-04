"""Validation accuracy per epoch (mean of 3 seeds) and test accuracy of the three methods on 2,000 training photos (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import GREY, BLUE, GREEN, FONT

here = Path(__file__).parent
h = pd.read_csv(here.parent / "data" / "history.csv")
t = pd.read_csv(here.parent / "data" / "test_accuracy.csv")
names = {"scratch": ("from scratch (with augmentation)", GREY), "feature_extraction": ("feature extraction", BLUE),
         "fine_tuning": ("fine-tuning (block 5 unfrozen after epoch 10)", GREEN)}
fig = make_subplots(rows=1, cols=2, column_widths=[0.65, 0.35], horizontal_spacing=0.1,
                    subplot_titles=("validation accuracy", "test accuracy (1,000 photos)"))
for key, (name, c) in names.items():
    m = h[h.method == key].groupby("epoch").val_accuracy.mean()
    fig.add_trace(go.Scatter(x=m.index, y=m.values, mode="lines", name=name, line=dict(color=c, width=4)), row=1, col=1)
    s = t[t.method == key].test_accuracy
    label = name.split(" (")[0].replace("feature extraction", "feature<br>extraction").replace("from scratch", "from<br>scratch")
    fig.add_trace(go.Bar(x=[label], y=[s.mean()], marker_color=c, showlegend=False,
                         error_y=dict(type="data", symmetric=False, array=[s.max() - s.mean()], arrayminus=[s.mean() - s.min()])),
                  row=1, col=2)
    fig.add_annotation(x=label, y=0.6, text=f"{s.mean():.3f}", showarrow=False, font=dict(color="white", size=20),
                       xref="x2", yref="y2")
fig.add_vline(x=10.5, line=dict(color=GREEN, width=1, dash="dot"), row=1, col=1)
fig.update_xaxes(title="epoch", row=1, col=1)
fig.update_yaxes(title="accuracy", range=[0.5, 1.0], row=1, col=1)
fig.update_yaxes(range=[0.5, 1.03], row=1, col=2)
fig.update_xaxes(tickangle=0, row=1, col=2)
fig.update_layout(template="simple_white", width=1000, height=450, font=FONT, legend=dict(x=0.2, y=0.9, yanchor="top", bgcolor="rgba(255,255,255,0.85)"),
                  margin=dict(l=60, r=20, t=40, b=60))
fig.write_image(here / "results.png", scale=2)
fig.write_image(here / "results.pdf")
