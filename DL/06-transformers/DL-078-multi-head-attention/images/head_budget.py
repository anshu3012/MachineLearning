"""Section 6.1: splitting d_model = 512 among the heads keeps the cost of one full head. Left: parameters of Keras'
MultiHeadAttention for 1 head of 512, 8 heads of 64 and 2 heads of 512 (data/param_count.csv, the Notebook).
Right: translation quality against the number of heads at fixed total size (Vaswani et al. 2017, Table 3, rows A,
development-set BLEU, numbers typed from the paper).
Run: python head_budget.py  -> head_budget.png (Plotly: bars and a line)"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from common import BLUE, GREY, ORANGE, RED

HERE = Path(__file__).parent
p = pd.read_csv(HERE.parent / "data" / "param_count.csv")
d = 512
assert list(p.parameters) == [4 * d * d + 4 * d, 4 * d * d + 4 * d, 2 * (3 * d * d + 3 * d) + 2 * d * d + d]
assert list(p.parameters[:2]) == [1050624, 1050624]
heads, bleu = [1, 4, 8, 16, 32], [24.9, 25.5, 25.8, 25.8, 25.4]           # Vaswani et al. 2017, Table 3 (A)

fig = make_subplots(1, 2, column_widths=[0.45, 0.55], horizontal_spacing=0.14,
                    subplot_titles=["parameters (millions)", "BLEU at fixed total size (paper)"])
labels = [f"{h} head{'s' if h > 1 else ''} × {s}" for h, s in zip(p.heads, p.size_per_head)]
fig.add_trace(go.Bar(x=labels, y=p.parameters / 1e6, marker_color=[BLUE, ORANGE, GREY], showlegend=False,
                     text=[f"{v / 1e6:.2f}" for v in p.parameters], textposition="outside"), 1, 1)
fig.add_trace(go.Scatter(x=heads, y=bleu, mode="lines+markers+text", text=[f"{b}" for b in bleu],
                         textposition="top center", line=dict(color=RED, width=4), marker=dict(size=12),
                         showlegend=False), 1, 2)
fig.update_yaxes(range=[0, 2.5], row=1, col=1)
fig.update_xaxes(type="log", tickvals=heads, title="heads (size 512 / heads)", row=1, col=2)
fig.update_yaxes(range=[24.6, 26.2], row=1, col=2)
fig.update_layout(template="simple_white", width=1200, height=520, font=dict(family="Latin Modern Roman", size=20),
                  margin=dict(l=60, r=30, t=70, b=70))
fig.update_annotations(font_size=22)

if __name__ == "__main__":
    fig.write_image(HERE / "head_budget.png", scale=2)
