"""Batch size, measured on MNIST (data/batch_size.json from experiments/batch_size.py: 32-32-32 ReLU network, Adam,
10 epochs, mean of 2 seeds, one GPU). Left: seconds per epoch; right: test accuracy after the 10 epochs. Plotly."""
import json
from pathlib import Path

import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
R = {int(k): v for k, v in json.load(open(HERE.parent / "data" / "batch_size.json")).items()}
B = sorted(R)
sec = [R[b]["sec_per_epoch"] for b in B]
acc = [100 * R[b]["acc"] for b in B]
assert sec[0] > 10 * min(sec) and acc[-1] < acc[0] - 5 and max(acc[:3]) - min(acc[:3]) < 0.5
X = list(range(len(B)))
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
                    subplot_titles=("Time per epoch (seconds)", "Test accuracy after 10 epochs (%)"))
fig.add_scatter(x=X, y=sec, mode="lines+markers+text", text=[f"{v:.1f}" for v in sec], textposition="top right",
                line=dict(color="#4C78A8", width=4), marker=dict(size=12), showlegend=False, row=1, col=1)
fig.add_scatter(x=X, y=acc, mode="lines+markers+text", text=[f"{v:.1f}" for v in acc], textposition="bottom center",
                line=dict(color="#E45756", width=4), marker=dict(size=12), showlegend=False, row=1, col=2)
fig.update_xaxes(tickvals=X, ticktext=[f"{b:,}" for b in B], title_text="batch size", range=[-0.4, len(B) - 0.6])
fig.update_yaxes(range=[0, 7], row=1, col=1)
fig.update_yaxes(range=[86, 98.5], row=1, col=2)
fig.update_layout(template="simple_white", width=1250, height=540, font=dict(family="Latin Modern Roman", size=20),
                  margin=dict(l=70, r=30, t=70, b=80))
for a in fig.layout.annotations[:2]:
    a.font.size = 21
fig.write_image(HERE / "batch_size.png", scale=2)
