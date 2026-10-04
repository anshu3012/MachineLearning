"""The 4x4 map of section 4.3 pooled two ways at once: the same 2x2 window (stride 2) fills a max-pooled map
(top) and an average-pooled map (bottom). Plotly frames: the window moves and the outputs fill in.
Run: python max_avg_slide.py -> max_avg_slide.gif, max_avg_slide_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from anim import _grid, _box, _shade
from common import BLUE, ORANGE, GREEN, GREY, FONT
from frames import save

A = np.array([[1, 5, 2, 3], [2, 4, 0, 1], [7, 1, 4, 2], [3, 0, 1, 3]], float)
WINS = [(0, 0), (0, 2), (2, 0), (2, 2)]
MAX = [A[r:r + 2, c:c + 2].max() for r, c in WINS]
AVG = [A[r:r + 2, c:c + 2].mean() for r, c in WINS]
assert MAX == [5, 3, 7, 4] and AVG == [3, 1.5, 2.75, 2.5]
fmt = lambda v: f"{v:g}"


def frame(k):
    fig = go.Figure()
    pm, pa = np.full((2, 2), np.nan), np.full((2, 2), np.nan)
    for j in range(k + 1):
        pm[j // 2, j % 2], pa[j // 2, j % 2] = MAX[j], AVG[j]
    _grid(fig, A, 0, 0, lambda v: _shade(v, 0, 7, BLUE), fmt, 26)
    _grid(fig, pm, 6.2, 0.3, lambda v: _shade(v, 0, 7, GREEN), fmt, 26)
    _grid(fig, pa, 6.2, -2.3, lambda v: _shade(v, 0, 7, ORANGE), fmt, 26)
    r, c = WINS[k]
    _box(fig, 0, 0, r, c, 2, 2, "#E45756")
    _box(fig, 6.2, 0.3, k // 2, k % 2, 1, 1, "#E45756", 5)
    _box(fig, 6.2, -2.3, k // 2, k % 2, 1, 1, "#E45756", 5)
    for x, y, t in ((0, 0.25, "feature map"), (6.2, 0.55, "max pooled"), (6.2, -2.05, "average pooled")):
        fig.add_annotation(x=x, y=y, text=t, showarrow=False, xanchor="left", yanchor="bottom",
                           font=dict(family=FONT["family"], size=22, color=GREY))
    w = ", ".join(fmt(v) for v in A[r:r + 2, c:c + 2].ravel())
    fig.update_layout(template="simple_white", width=900, height=560, font=FONT, showlegend=False,
                      title=dict(text=f"window {k + 1} of 4: {w}  →  max {fmt(MAX[k])},  average {fmt(AVG[k])}",
                                 x=0.5, y=0.96, font=dict(size=24)),
                      xaxis=dict(visible=False, range=[-0.3, 8.6], scaleanchor="y"),
                      yaxis=dict(visible=False, range=[-4.6, 1.3]), margin=dict(l=10, r=10, t=70, b=10))
    return fig


if __name__ == "__main__":
    figs = [frame(k) for k in range(4)]
    save("max_avg_slide", figs, [0, 0, 1, 1, 2, 2, 3, 3, 3, 3, 3, 3], [0, 1, 2, 3], Path(__file__).parent, fps=1)
