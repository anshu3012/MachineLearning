"""The Viterbi algorithm on the three-step hallway run, drawn on a trellis (time across, cells down). Each node shows
the probability of the best path ending there; a grey line shows the best way in (the back-pointer). The last frame
follows the back-pointers (edges that wrap round the loop, such as 8 to 0, are not drawn)
from the best end (cell 5 at t = 3) back to the start: 1 -> 3 -> 5.
Run: python viterbi.py -> viterbi.gif, viterbi_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

from gifkit import BLUE, FONT, GREY, RED, make_gif
from hmmrun import BACK, M, PATH

here = Path(__file__).parent
assert PATH == [1, 3, 5] and abs(M[2][5] - 0.018432) < 1e-9
READ = ["stay, reads door", "move 2, reads door", "move 2, reads wall"]


def frame(upto, back=False):
    fig = go.Figure()
    for t in range(1, upto):                         # back-pointer edges into column t
        for j in range(10):
            i = BACK[t - 1][j]
            if abs(i - j) > 3:                       # ponytail: wrap-round edges (e.g. 8 -> 0) left out for clarity
                continue
            fig.add_trace(go.Scatter(x=[t - 1 + 0.08, t - 0.08], y=[i, j], mode="lines",
                                     line=dict(color="#c8c8c8", width=2)))
    if back:
        fig.add_trace(go.Scatter(x=[0, 1, 2], y=PATH, mode="lines", line=dict(color=RED, width=6)))
    for t in range(upto):
        v = M[t]
        best = v.argmax()
        fig.add_trace(go.Scatter(x=[t] * 10, y=list(range(10)), mode="markers+text",
                                 marker=dict(size=12 + 190 * np.sqrt(v), color=[RED if back and PATH[t] == j else BLUE
                                                                                for j in range(10)]),
                                 text=[f"{x:.4f}" for x in v], textposition="middle right",
                                 textfont=dict(size=15, color=["black" if j == best else GREY for j in range(10)])))
    fig.update_xaxes(tickvals=[0, 1, 2], ticktext=[f"t = {t + 1}<br>{r}" for t, r in enumerate(READ)],
                     range=[-0.35, 2.6])
    fig.update_yaxes(tickvals=list(range(10)), title="cell", range=[9.6, -0.6])
    title = "Viterbi: best-path probability of each cell" if not back else "Backtrack from the best end: 1 → 3 → 5"
    fig.update_layout(template="simple_white", width=1000, height=720, font=FONT, showlegend=False,
                      margin=dict(l=80, r=30, t=70, b=90), title=dict(text=title, x=0.5, font=dict(size=24)))
    return fig


figs = [frame(1), frame(2), frame(3), frame(3, back=True)]
make_gif(figs, here / "viterbi", fps=1, holds=[3, 3, 3, 6], keys=[2, 3], cols=2, width=900)
