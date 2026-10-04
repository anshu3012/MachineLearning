"""One MNIST 8 shifted 0, 1, 2, 3 pixels to the right: the digit, its feature map (vertical-edge filter + ReLU)
and the 2x2 max-pooled map, with the relative change of each representation averaged over 1000 test digits.
Data: data/shift_frames.npz and data/shift_sweep.csv (Notebook). Plotly frames: the data change with the shift.
Run: python shift_anim.py -> shift_anim.gif, shift_anim_frames.png"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, GREEN, GREY
from frames import save

HERE = Path(__file__).parent
d = np.load(HERE.parent / "data" / "shift_frames.npz")
s = pd.read_csv(HERE.parent / "data" / "shift_sweep.csv").set_index("shift")
FONT = dict(family="Latin Modern Roman", size=22)
COLS = [("no_pooling", "no pooling", GREY), ("max_2x2", "2 × 2 max", BLUE), ("max_4x4", "4 × 4 max", ORANGE),
        ("global_max", "global max", GREEN)]
top = d["f"].max()
assert s.loc[1, "max_2x2"] < s.loc[1, "no_pooling"] and s.loc[0].abs().max() == 0


def frame(k):
    fig = make_subplots(1, 4, column_widths=[0.2, 0.2, 0.2, 0.4], horizontal_spacing=0.03,
                        subplot_titles=("digit", "feature map", "2 × 2 max pooled", "change against shift 0"))
    fig.add_trace(go.Heatmap(z=d["x"][k], colorscale="gray", showscale=False), 1, 1)
    fig.add_trace(go.Heatmap(z=d["f"][k], colorscale="gray_r", zmin=0, zmax=top, showscale=False), 1, 2)
    fig.add_trace(go.Heatmap(z=d["p"][k], colorscale="gray_r", zmin=0, zmax=top, showscale=False), 1, 3)
    for c, n in ((1, 28), (2, 26), (3, 13)):       # a fixed red line shows how far the picture has moved
        fig.add_vline(x=n * 0.5 - 0.5, line=dict(color="#E45756", width=2, dash="dot"), row=1, col=c)
        fig.update_xaxes(visible=False, row=1, col=c)
        fig.update_yaxes(visible=False, autorange="reversed", scaleanchor=f"x{c if c > 1 else ''}", row=1, col=c)
    vals = [s.loc[k, c] for c, _, _ in COLS]
    fig.add_trace(go.Bar(x=[lab for _, lab, _ in COLS], y=vals, marker_color=[c for _, _, c in COLS],
                         text=[f"{v:.2f}" for v in vals], textposition="outside", cliponaxis=False), 1, 4)
    fig.update_yaxes(range=[0, 1.55], title="relative change", row=1, col=4)
    fig.layout.xaxis4.domain = [0.71, 1.0]
    fig.layout.annotations[3].x = 0.855
    fig.update_annotations(font=dict(size=22))
    fig.update_layout(template="simple_white", width=1300, height=470, font=FONT, showlegend=False,
                      title=dict(text=f"digit shifted {k} pixel{'s' if k != 1 else ''} to the right", x=0.5, y=0.97),
                      margin=dict(l=10, r=20, t=110, b=50))
    return fig


if __name__ == "__main__":
    figs = [frame(k) for k in range(4)]
    seq = [0] * 3 + [1] * 4 + [2] * 3 + [3] * 3 + [2, 1] + [0] * 2 + [1] * 5
    save("shift_anim", figs, seq, [0, 1, 2, 3], HERE, fps=1.5, gif_width=900)
