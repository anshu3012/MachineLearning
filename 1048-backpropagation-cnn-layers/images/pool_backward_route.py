"""Max pooling backwards on the example of section 6: each of the four gradients of dL/dP1 goes to the cell of A1
that held its window's maximum; every other cell gets 0. Plotly frames: one window per frame.
Run: python pool_backward_route.py -> pool_backward_route.gif, pool_backward_route_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from anim import _grid, _box, _shade
from common import BLUE, ORANGE, GREEN, RED, GREY, FONT
from frames import save

A = np.array([[1, 5, 2, 3], [2, 4, 0, 1], [7, 1, 4, 2], [3, 0, 1, 3]], float)
dP = np.array([[0.1, -0.2], [0.3, 0.4]])
WINS = [(0, 0), (0, 2), (2, 0), (2, 2)]
fmt = lambda v: f"{v:g}"


def frame(k):
    """k = -1: nothing routed yet; k = 0..3: windows 0..k routed."""
    fig = go.Figure()
    dA = np.full((4, 4), np.nan)
    for j in range(k + 1):
        r, c = WINS[j]
        w = A[r:r + 2, c:c + 2]
        dA[r:r + 2, c:c + 2] = 0
        i = int(w.argmax())
        dA[r + i // 2, c + i % 2] = dP[j // 2, j % 2]
    _grid(fig, A, 0, 0, lambda v: _shade(v, 0, 7, BLUE), fmt, 24)
    _grid(fig, dP, 5.5, -1, lambda v: _shade(abs(v), 0, 0.4, ORANGE), fmt, 24)
    _grid(fig, dA, 9, 0, lambda v: "white" if v == 0 else _shade(abs(v), 0, 0.4, ORANGE), fmt, 24)
    txt = "max pooling backwards: where was each window's maximum?"
    if k >= 0:
        r, c = WINS[k]
        i = int(A[r:r + 2, c:c + 2].argmax())
        mr, mc = r + i // 2, c + i % 2
        _box(fig, 0, 0, r, c, 2, 2, RED, 5)
        _box(fig, 0, 0, mr, mc, 1, 1, GREEN, 6)
        _box(fig, 5.5, -1, k // 2, k % 2, 1, 1, RED, 5)
        _box(fig, 9, 0, r, c, 2, 2, RED, 5)
        _box(fig, 9, 0, mr, mc, 1, 1, GREEN, 6)
        txt = f"window {k + 1} of 4: maximum {fmt(A[mr, mc])} gets the gradient {fmt(dP[k // 2, k % 2])}; the other three cells get 0"
    for x, y, t in ((0, 0.25, "A<sub>1</sub> (forward)"), (5.5, -0.75, "∂L/∂P<sub>1</sub>"), (9, 0.25, "∂L/∂A<sub>1</sub>")):
        fig.add_annotation(x=x, y=y, text=t, showarrow=False, xanchor="left", yanchor="bottom",
                           font=dict(family=FONT["family"], size=22, color=GREY))
    fig.update_layout(template="simple_white", width=1100, height=470, font=FONT, showlegend=False,
                      title=dict(text=txt, x=0.5, y=0.95, font=dict(size=22)),
                      xaxis=dict(visible=False, range=[-0.3, 13.3], scaleanchor="y"),
                      yaxis=dict(visible=False, range=[-4.3, 1.2]), margin=dict(l=10, r=10, t=70, b=10))
    return fig


if __name__ == "__main__":
    figs = [frame(k) for k in range(-1, 4)]
    save("pool_backward_route", figs, [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 4, 4, 4, 4], [1, 2, 3, 4], Path(__file__).parent,
         fps=1, gif_width=900)
