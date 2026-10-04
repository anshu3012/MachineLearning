"""Section 8.2: Table 3 of Vaswani et al. (2017), English-German development BLEU when one setting of the base model
(25.8) is changed at a time. Numbers typed from the paper, as in the Note's table.
Run: python table3.py  -> table3.png (Plotly horizontal bars around the base line)"""
from pathlib import Path

import plotly.graph_objects as go

from common import BLUE, GREY, RED

HERE = Path(__file__).parent
BASE = 25.8
rows = [("(A) 1 head", 24.9), ("(A) 4 heads", 25.5), ("(A) 16 heads", 25.8), ("(A) 32 heads", 25.4),
        ("(B) d<sub>k</sub> = 16", 25.1), ("(B) d<sub>k</sub> = 32", 25.4),
        ("(C) N = 2 blocks", 23.7), ("(C) N = 4 blocks", 25.3), ("(C) N = 8 blocks", 25.5),
        ("(C) d<sub>model</sub> = 256", 24.5), ("(C) d<sub>model</sub> = 1024", 26.0),
        ("(C) d<sub>ff</sub> = 1024", 25.4), ("(C) d<sub>ff</sub> = 4096", 26.2),
        ("(D) dropout 0.0", 24.6), ("(D) dropout 0.2", 25.5), ("(D) label smoothing 0.0", 25.3),
        ("(D) label smoothing 0.2", 25.7), ("(E) learned positions", 25.7), ("big model", 26.4)]
assert round(BASE - 24.9, 1) == 0.9                          # "single-head attention is 0.9 BLEU worse"
labels, vals = [r[0] for r in rows], [r[1] for r in rows]
fig = go.Figure(go.Bar(y=labels, x=[v - BASE for v in vals], base=BASE, orientation="h",
                       marker_color=[BLUE if v >= BASE else RED for v in vals],
                       text=[f"{v}" for v in vals], textposition="outside"))
fig.add_vline(x=BASE, line=dict(color=GREY, width=3, dash="dash"))
fig.add_annotation(x=BASE, y=-1.2, text="base model 25.8", showarrow=False, font=dict(size=20, color=GREY))
fig.update_yaxes(autorange="reversed")
fig.update_layout(template="simple_white", width=1000, height=820, font=dict(family="Latin Modern Roman", size=20),
                  xaxis=dict(title="BLEU (EN–DE, development set)", range=[23.3, 27.0]),
                  margin=dict(l=20, r=30, t=50, b=60))

if __name__ == "__main__":
    fig.write_image(HERE / "table3.png", scale=2)
