"""Why each particle gets its own slip. After resampling, particle 2 exists twice at 1.6 m (copies a and b). Three
moves of 2.5 m follow; each move is drawn in two steps, the command and then the slip (normal, sd 0.15 m). Top: one
slip shared by both copies, so they stay one point (gap 0.00 m). Bottom: each copy draws its own slip, so they
spread apart (gap 0.21, 0.28, 0.41 m). Copy a gets the same slips in both rows. The two copies are drawn in two lanes
so both show; only left to right is position. Readings and resampling between the moves are left out.
Run: python slip_anim.py -> slip_anim.gif, slip_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, ORANGE, PURPLE, make_gif
from pfsim import DOORS, LOOP, SIGMA_U, U

here = Path(__file__).parent
X0, MOVES = 1.6, 3
rng = np.random.default_rng(10)
sa = rng.normal(0, SIGMA_U, MOVES)                         # copy a's slips (and the shared slips of the top row)
sb = rng.normal(0, SIGMA_U, MOVES)                         # copy b's own slips (bottom row)
A = X0 + np.cumsum(U + sa)                                 # copy a after each move (m)
B = X0 + np.cumsum(U + sb)                                 # copy b, own slips (m)
GAPS = np.abs(A - B)
assert np.allclose(GAPS.round(2), [0.21, 0.28, 0.41]) and A.max() < LOOP and B.max() < LOOP
LANE = {"a": 0.68, "b": 0.32}
COL = {"a": BLUE, "b": PURPLE}


def frame(title, pos, slips=None, cmd=None):
    """pos[row] = (x of copy a, x of copy b); slips[row] = (slip a, slip b) just added; cmd = x before the command."""
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.2,
                        subplot_titles=["<b>same slip for both copies</b>", "<b>each copy its own slip</b>"])
    for r in (1, 2):
        ax = "" if r == 1 else str(r)
        for a, b in DOORS:
            fig.add_shape(type="rect", x0=a, x1=b, y0=0, y1=1, xref=f"x{ax}", yref=f"y{ax} domain", fillcolor=ORANGE, opacity=0.18, line_width=0,
                          layer="below")
        xa, xb = pos[r - 1]
        if cmd is not None:
            for c, x in (("a", xa), ("b", xb)):
                fig.add_annotation(x=x, y=LANE[c] + 0.15, ax=cmd[r - 1][c == "b"], ay=LANE[c] + 0.15, xref=f"x{ax}",
                                   yref=f"y{ax}", axref=f"x{ax}", ayref=f"y{ax}", text="", showarrow=True,
                                   arrowhead=2, arrowsize=1, arrowwidth=2.5, arrowcolor=GREY)
        for c, x in (("a", xa), ("b", xb)):
            fig.add_trace(go.Scatter(x=[x], y=[LANE[c]], mode="markers+text", text=[f"copy {c}"],
                                     textposition="middle left", textfont=dict(size=18, color=COL[c]),
                                     marker=dict(size=22, color=COL[c])), row=r, col=1)
            if slips is not None:
                s_ = slips[r - 1][c == "b"]
                fig.add_annotation(x=x + 0.15, y=LANE[c], xanchor="left", text=f"slip {s_:+.2f} m".replace("-", "−"),
                                   showarrow=False, font=dict(size=17, color=COL[c]), xref=f"x{ax}", yref=f"y{ax}")
        fig.add_annotation(x=1.0, y=1.02, xref=f"x{ax} domain", yref=f"y{ax} domain", xanchor="right", yanchor="bottom",
                           text=f"gap between the copies: {abs(xa - xb):.2f} m", showarrow=False,
                           font=dict(size=19))
    fig.update_xaxes(range=[0, LOOP], dtick=1, title=None)
    fig.update_xaxes(title="position x (m)", row=2, col=1)
    fig.update_yaxes(visible=False, range=[-0.05, 1.0])
    fig.add_annotation(xref="paper", yref="paper", x=0.5, y=-0.2, yanchor="top", showarrow=False, font=dict(size=16, color=GREY),
                       text="orange: doors. The copies are drawn in two lanes so both show; position is left to right only.<br>"
                            "Readings and resampling between the moves are left out.")
    fig.update_annotations(selector=dict(text="<b>same slip for both copies</b>"), font_size=21, x=0, xanchor="left")
    fig.update_annotations(selector=dict(text="<b>each copy its own slip</b>"), font_size=21, x=0, xanchor="left")
    fig.update_layout(template="simple_white", font=FONT, width=1100, height=640, showlegend=False,
                      margin=dict(l=40, r=110, t=100, b=150), title=dict(x=0.5, y=0.97, font=dict(size=23), text=title))
    return fig


figs, holds = [], []
pos = [(X0, X0), (X0, X0)]
figs.append(frame("1. after resampling, particle 2 exists twice, both copies at 1.6 m", pos))
holds.append(6)
for k in range(MOVES):
    before = pos
    pos = [(before[0][0] + U, before[0][1] + U), (before[1][0] + U, before[1][1] + U)]
    figs.append(frame(f"move {k + 1}: both copies move by the command, 2.5 m", pos, cmd=before))
    holds.append(3)
    slips = [(sa[k], sa[k]), (sa[k], sb[k])]
    pos = [(A[k], A[k]), (A[k], B[k])]
    figs.append(frame(f"move {k + 1}: add the slip (top: one slip for both; bottom: one slip each)", pos, slips))
    holds.append(5)
figs.append(frame(f"after 3 moves: the shared slip keeps one point; own slips put the copies {GAPS[-1]:.2f} m apart",
                  pos))
holds.append(14)
keys = [0, 1, 2, len(figs) - 1]                           # start, move 1 (command, then slip), the end
make_gif(figs, here / "slip_anim", fps=2, holds=holds, keys=keys, cols=2, width=900)
