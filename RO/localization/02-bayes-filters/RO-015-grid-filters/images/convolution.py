"""The move step as a sliding kernel (a convolution). For each new cell j, the predicted belief adds three old cells:
0.1 x old(j - 1) + 0.8 x old(j - 2) + 0.1 x old(j - 3) (one cell short, exact, one cell too far), wrapping round
the loop. Top: the old belief with the three cells used (green weights). Bottom: the new belief, filled cell by cell.
Run: python convolution.py -> convolution.gif, convolution_frames.png"""
from pathlib import Path

import numpy as np
from plotly.subplots import make_subplots

from gifkit import BLUE, GREEN, GREY, ORANGE, make_gif
from hallplot import N, layout, predict, story

here = Path(__file__).parent
b0, b1, bb2, b2 = story()
assert np.allclose(predict(b1), bb2)
W = {1: 0.1, 2: 0.8, 3: 0.1}


def frame(j):
    src = {(j - s) % N: w for s, w in W.items()}
    terms = " + ".join(f"{w} × {b1[i]:.4f}" for i, w in sorted(src.items(), key=lambda kv: -((j - kv[0]) % N)))
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.2,
                        subplot_titles=[f"old belief: the three cells that can reach cell {j}",
                                        f"new cell {j} = {terms} = {bb2[j]:.4f}"])
    colors = [GREEN if i in src else GREY for i in range(N)]
    fig.add_bar(x=list(range(N)), y=b1, marker_color=colors, width=0.7, row=1, col=1,
                text=[f"×{src[i]}" if i in src else "" for i in range(N)], textposition="outside",
                textfont=dict(size=20, color=GREEN), cliponaxis=False)
    new = [bb2[i] if i <= j else 0 for i in range(N)]
    fig.add_bar(x=list(range(N)), y=new, marker_color=[ORANGE if i == j else BLUE for i in range(N)], width=0.7,
                row=2, col=1, text=[f"{bb2[i]:.4f}" if i <= j else "" for i in range(N)], textposition="outside",
                textfont=dict(size=15), cliponaxis=False)
    for r in (1, 2):
        fig.update_xaxes(tickvals=list(range(N)), range=[-0.6, N - 0.4], title="cell", row=r, col=1)
        fig.update_yaxes(range=[0, 0.25], title="probability", row=r, col=1)
    layout(fig, 1000, 760, top=70)
    fig.update_annotations(font_size=20)
    return fig


figs = [frame(j) for j in range(N)]
holds = [6] * (N - 1) + [16]
make_gif(figs, here / "convolution", fps=4, holds=holds, keys=[3, 9], cols=2, width=850)
