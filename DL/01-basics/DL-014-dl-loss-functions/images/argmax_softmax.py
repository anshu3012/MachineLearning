"""Argmax against softmax on three raw outputs (Plotly frames). The first raw output slides from 1.43 down to -1.0
while the others stay at -0.4 and 0.23. The argmax bars only jump (when the first output stops being the largest);
the softmax bars move with every small change, so they have a slope that training can use.
Run: python argmax_softmax.py -> argmax_softmax.gif, argmax_softmax_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, GREEN, save_gif

HERE = Path(__file__).parent
REST = np.array([-0.4, 0.23])
z1s = np.round(np.arange(1.43, -1.01, -0.09), 2)
softmax = lambda z: np.exp(z) / np.exp(z).sum()
assert np.allclose(softmax(np.r_[1.43, REST]).round(2), [0.68, 0.11, 0.21])
am = np.array([np.eye(3)[np.r_[z, REST].argmax()] for z in z1s])
sm = np.array([softmax(np.r_[z, REST]) for z in z1s])
assert (np.abs(np.diff(am[:, 0])) > 0).sum() == 1          # argmax changes exactly once along the slide
assert (np.diff(sm[:, 0]) < 0).all()                       # softmax changes at every step
COLS = [BLUE, ORANGE, GREEN]


def frame(k):
    z = np.r_[z1s[k], REST]
    fig = make_subplots(1, 3, subplot_titles=["raw outputs", "after argmax", "after softmax"], horizontal_spacing=0.08)
    for c, (vals, fmt) in enumerate(((z, "{:.2f}"), (am[k], "{:.0f}"), (sm[k], "{:.2f}")), start=1):
        fig.add_trace(go.Bar(x=["class 1", "class 2", "class 3"], y=vals, marker_color=COLS,
                             text=[fmt.format(v).replace("-", "−") for v in vals], textposition="outside", textfont=dict(size=22)), 1, c)
    fig.update_yaxes(range=[-1.3, 1.8], row=1, col=1)
    fig.update_yaxes(range=[0, 1.2], row=1, col=2)
    fig.update_yaxes(range=[0, 1.2], row=1, col=3)
    fig.update_annotations(font=dict(size=26))
    fig.update_layout(template="simple_white", width=1200, height=560, showlegend=False, font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text=f"raw output of class 1 = <b>{z1s[k]:.2f}</b>".replace("-", "−"), x=0.5, font=dict(size=28)),
                      margin=dict(l=50, r=20, t=120, b=50))
    return fig


if __name__ == "__main__":
    jump = int(np.argmax(np.abs(np.diff(am[:, 0])) > 0))
    save_gif([frame(k) for k in range(len(z1s))], "argmax_softmax", [0, jump, jump + 1, len(z1s) - 1], HERE, fps=4, hold=8)
    print("argmax jumps between z1 =", z1s[jump], "and", z1s[jump + 1], "; softmax at start", sm[0].round(2))
