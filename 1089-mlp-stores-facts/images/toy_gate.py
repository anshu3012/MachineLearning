"""Section 4.2: the toy neuron (row M + J, bias -1) on five inputs: its value after the bias, after ReLU and after
GELU. From data/toy_and_gate.csv (the Notebook). Only "Michael Jordan" clears the threshold.
Run: python toy_gate.py  -> toy_gate.png (Plotly grouped bars)"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

HERE = Path(__file__).parent
BLUE, ORANGE, GREY = "#4C78A8", "#F58518", "#6B6B6B"
t = pd.read_csv(HERE.parent / "data" / "toy_and_gate.csv")
assert list(t.plus_bias) == [1, 0, 0, 0, -1] and list(t.after_relu) == [1, 0, 0, 0, 0]
assert round(t.gelu[0], 2) == 0.84 and round(t.gelu[4], 2) == -0.16
fig = go.Figure()
for col, name, c in (("plus_bias", "row · e − 1 (before activation)", GREY), ("after_relu", "after ReLU", BLUE),
                     ("gelu", "after GELU (GPT-2)", ORANGE)):
    fig.add_trace(go.Bar(x=t.input, y=t[col], name=name, marker_color=c, text=[f"{v:.2f}" for v in t[col]],
                         textposition="outside"))
fig.add_hline(y=0, line=dict(color=GREY, width=1))
fig.update_layout(template="simple_white", barmode="group", width=1100, height=500,
                  font=dict(family="Latin Modern Roman", size=20), yaxis=dict(title="neuron value", range=[-1.35, 1.3]),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=1.0, yanchor="bottom"),
                  margin=dict(l=80, r=20, t=60, b=50))

if __name__ == "__main__":
    fig.write_image(HERE / "toy_gate.png", scale=2)
