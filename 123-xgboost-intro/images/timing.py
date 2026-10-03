"""Training time of five gradient boosting implementations on 10,000 x 200 synthetic rows, 100 trees of depth 3
(Plotly). Reads ../data/timings.csv, written by notebook.ipynb."""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=20)
t = pd.read_csv(HERE.parent / "data" / "timings.csv").iloc[::-1]
colours = {"sklearn GradientBoosting": "#6B6B6B", "XGBoost (CPU)": "#E45756", "XGBoost (GPU)": "#E45756"}
fig = go.Figure(go.Bar(y=t["model"], x=t["seconds"], orientation="h",
                       marker_color=[colours.get(m, "#4C78A8") for m in t["model"]],
                       text=[f"{s:.2f} s, accuracy {a:.3f}" for s, a in zip(t["seconds"], t["test accuracy"])],
                       textposition="outside"))
fig.update_xaxes(title="training time in seconds (log scale)", type="log", range=[-0.8, 2.6], tickvals=[0.2, 0.5, 1, 2, 5, 10, 20, 50, 100], ticktext=["0.2", "0.5", "1", "2", "5", "10", "20", "50", "100"])
fig.update_layout(template="simple_white", width=1100, height=520, font=FONT, margin=dict(l=20, r=20, t=20, b=70))
fig.write_image(HERE / "timing.png", scale=2)
fig.write_image(HERE / "timing.pdf")
