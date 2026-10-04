"""Blending versus K-fold stacking on the heart data: mean test accuracy over 100 random splits per training size (Plotly).
Data: data/blend_vs_stack.csv, written by notebook.ipynb section 8."""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=20)
res = pd.read_csv(HERE.parent / "data" / "blend_vs_stack.csv")
m = res.groupby("n_train")[["blending", "stacking"]].mean()
fig = go.Figure()
for col, name, color in [("blending", "blending (80/20 hold-out)", "#E45756"),
                         ("stacking", "K-fold stacking (5 folds)", "#4C78A8")]:
    fig.add_trace(go.Scatter(x=m.index, y=m[col], name=name, mode="lines+markers+text", line=dict(color=color, width=3),
                             marker=dict(size=10), text=[f"{v:.3f}" for v in m[col]],
                             textposition="top center" if col == "stacking" else "bottom center"))
fig.update_xaxes(title="training patients", tickvals=list(m.index), range=[40, 262])
fig.update_yaxes(title="mean test accuracy (100 splits)")
fig.update_layout(template="simple_white", width=1100, height=600, font=FONT, margin=dict(l=20, r=30, t=20, b=70),
                  legend=dict(x=0.55, y=0.1))
fig.write_image(HERE / "blend_vs_stack.png", scale=2)
fig.write_image(HERE / "blend_vs_stack.pdf")
