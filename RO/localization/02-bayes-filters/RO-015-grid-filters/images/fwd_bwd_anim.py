"""The forward-backward algorithm on the three-step hallway run, animated.
Left: one column of the 10 cells per time step; each box shows alpha (orange, left) and beta (purple, right).
Alpha fills in from left to right (0.06 at a door and 0.02 at a wall at t = 1), beta from right to left (1 at t = 3,
beta_2(3) = 0.8, beta_1(1) = 0.4144, beta_1(3) = 0.1072). Then the column t = 1 is multiplied (alpha x beta, total
0.06896) and rescaled. Right: the belief at t = 1, filtered (blue, 0.19 at cells 1, 3, 7) and smoothed (purple,
0.36 at cell 1, 0.09 at cells 3 and 7). Lines show the moves used for the highlighted box.
Run: python fwd_bwd_anim.py -> fwd_bwd_anim.gif, fwd_bwd_anim_frames.png"""
from pathlib import Path

import numpy as np
from plotly.subplots import make_subplots

from gifkit import BLUE, FONT, GREY, ORANGE, PURPLE, make_gif
from hallplot import BROWN, DOORS, N
from hmmrun import ALPHA, BETA, FILTERED, SMOOTHED

here = Path(__file__).parent
A, B = np.array(ALPHA), np.array(BETA)
TOTAL = (A[0] * B[0]).sum()
assert np.allclose(A[0][list(DOORS)], 0.06) and abs(A[0][0] - 0.02) < 1e-12 and abs(A[1][3] - 0.0312) < 1e-12
assert np.allclose(B[2], 1) and abs(B[1][3] - 0.8) < 1e-12 and abs(B[1][2] - 0.76) < 1e-12
assert abs(B[1][5] - 0.48) < 1e-12 and abs(B[0][1] - 0.4144) < 1e-12 and abs(B[0][3] - 0.1072) < 1e-12
assert abs(TOTAL - 0.06896) < 1e-12 and all(abs((a * b).sum() - TOTAL) < 1e-12 for a, b in zip(A, B))
assert round(0.06 * 0.4144, 4) == 0.0249 and round(0.06 * 0.1072, 4) == 0.0064
assert round(0.0249 / 0.06896, 2) == round(SMOOTHED[0][1], 2) == 0.36
assert round(0.0064 / 0.06896, 2) == round(SMOOTHED[0][3], 2) == round(SMOOTHED[0][7], 2) == 0.09
assert np.allclose(FILTERED[0][list(DOORS)], 0.1875)
W, H = 0.36, 0.3                                  # half width and half height of a box (data units)
READ = ["stay, reads door", "move 2, reads door", "move 2, reads wall"]


def fmt(v):
    return f"{round(v, 4):g}"


def frame(head, line2, a=0, b=0, hot=(), edges=(), col1=False, arrow=None, smooth=False):
    """a: alpha columns shown (from the left); b: beta columns shown (from the right); hot: boxes (t, cell) in bold;
    edges: moves ((t, cell), (t + 1, cell)) drawn in colour; col1: frame the column t = 1; smooth: purple bars."""
    fig = make_subplots(rows=1, cols=2, column_widths=[0.6, 0.4], horizontal_spacing=0.05, shared_yaxes=True)
    ecol = ORANGE if b == 0 else PURPLE
    for (t0, c0), (t1, c1) in edges:
        fig.add_scatter(x=[t0 + W, t1 - W], y=[c0, c1], mode="lines", line=dict(color=ecol, width=3), row=1, col=1)
    for t in range(3):
        for j in range(N):
            is_hot = (t, j) in hot
            edge = ecol if is_hot else ("black" if col1 and t == 0 else "#c8c8c8")
            fig.add_shape(type="rect", x0=t - W, x1=t + W, y0=j - H, y1=j + H, fillcolor="white", opacity=1,
                          line=dict(color=edge, width=3 if is_hot or (col1 and t == 0) else 1.5), row=1, col=1)
            for show, x, v, colr in ((t < a, t - W / 2, A[t][j], ORANGE), (t >= 3 - b, t + W / 2, B[t][j], PURPLE)):
                if show:
                    txt = f"<b>{fmt(v)}</b>" if is_hot and colr == ecol else fmt(v)
                    fig.add_annotation(x=x, y=j, text=txt, showarrow=False, font=dict(size=18, color=colr),
                                       row=1, col=1)
    if arrow is None and a == 0:                  # the first frame says what a box is
        fig.add_annotation(x=1, y=-1.15, text="each box: one cell at one time step<br>"
                           f"<span style='color:{ORANGE}'>α</span> goes on its left, "
                           f"<span style='color:{PURPLE}'>β</span> on its right", showarrow=False,
                           font=dict(size=19, color=GREY), row=1, col=1)
    if arrow == "fwd":
        fig.add_annotation(x=2.3, y=-0.9, ax=-0.3, ay=-0.9, axref="x", ayref="y", text="", showarrow=True,
                           arrowhead=2, arrowsize=1, arrowwidth=4, arrowcolor=ORANGE, row=1, col=1)
        fig.add_annotation(x=1, y=-1.4, text="forward α (orange): readings up to t", showarrow=False,
                           font=dict(size=19, color=ORANGE), row=1, col=1)
    if arrow == "bwd":
        fig.add_annotation(x=-0.3, y=-0.9, ax=2.3, ay=-0.9, axref="x", ayref="y", text="", showarrow=True,
                           arrowhead=2, arrowsize=1, arrowwidth=4, arrowcolor=PURPLE, row=1, col=1)
        fig.add_annotation(x=1, y=-1.4, text="backward β (purple): readings after t", showarrow=False,
                           font=dict(size=19, color=PURPLE), row=1, col=1)
    cells = list(range(N))
    fig.add_bar(y=cells, x=FILTERED[0], orientation="h", marker_color=BLUE, offsetgroup="f", width=0.38,
                text=[f"{v:.2f}" for v in FILTERED[0]], textposition="outside", textfont=dict(size=17),
                cliponaxis=False, row=1, col=2)
    fig.add_bar(y=cells, x=SMOOTHED[0] if smooth else np.zeros(N), orientation="h", marker_color=PURPLE,
                offsetgroup="s", width=0.38, text=[f"{v:.2f}" for v in SMOOTHED[0]] if smooth else None,
                textposition="outside", textfont=dict(size=17), cliponaxis=False, row=1, col=2)
    fig.add_annotation(x=0.005, y=-1.4, text="filtered at t = 1: reading 1 only", showarrow=False, xanchor="left",
                       font=dict(size=18, color=BLUE), row=1, col=2)
    if smooth:
        fig.add_annotation(x=0.005, y=-0.85, text="smoothed at t = 1: all 3 readings", showarrow=False,
                           xanchor="left", font=dict(size=18, color=PURPLE), row=1, col=2)
    for c in (1, 2):                              # after the traces: Plotly skips shapes on an empty subplot
        for d in DOORS:
            fig.add_hrect(y0=d - 0.5, y1=d + 0.5, fillcolor=BROWN, opacity=0.13, line_width=0, layer="below",
                          row=1, col=c)
    fig.update_xaxes(tickvals=[0, 1, 2], ticktext=[f"t = {t + 1}<br>{r}" for t, r in enumerate(READ)],
                     range=[-0.42, 2.42], showline=False, ticks="", row=1, col=1)
    fig.update_xaxes(title="belief at t = 1", range=[0, 0.48], dtick=0.1, row=1, col=2)
    door = f" <span style='color:{BROWN}'>door</span>"
    fig.update_yaxes(tickvals=cells, ticktext=[f"{j}{door if j in DOORS else ''}" for j in cells], title="cell",
                     range=[9.6, -1.75], row=1, col=1)
    fig.update_layout(template="simple_white", width=1300, height=900, font=FONT, showlegend=False, barmode="group",
                      margin=dict(l=110, r=30, t=120, b=110),
                      title=dict(text=f"{head}<br><span style='font-size:19px;color:{GREY}'>{line2}</span>", x=0.5,
                                 font=dict(size=24)))
    return fig


figs, holds = [], []


def add(hold, **kw):
    figs.append(frame(**kw))
    holds.append(hold)


add(10, head="Where was the robot at t = 1? Readings: door, door, wall",
    line2="the filter at t = 1 knew reading 1 only: cells 1, 3 and 7 tie at 0.19 (blue bars)")
add(6, head="forward α, left to right: t = 1", a=1, arrow="fwd",
    line2="α<sub>1</sub> = 0.1 × p(door | cell): 0.06 at a door, 0.02 at a wall")
add(8, head="forward α: t = 2, cell 3 is reached from cells 0, 1 and 2", a=2, arrow="fwd", hot=[(1, 3)],
    edges=[((0, c), (1, 3)) for c in (0, 1, 2)],
    line2="α<sub>2</sub>(3) = 0.6 × (0.1 × 0.02 + 0.8 × 0.06 + 0.1 × 0.02) = 0.0312")
add(6, head="forward α: t = 3", a=3, arrow="fwd",
    line2="each cell: the α of the cells that reach it, weighted by the move, times p(wall | cell)")
add(6, head="backward β, right to left: t = 3", a=3, b=1, arrow="bwd",
    line2="no readings after t = 3, so β<sub>3</sub> = 1 in every cell")
add(8, head="backward β: t = 2, from cell 3 the robot reaches the walls 4, 5 and 6", a=3, b=2, arrow="bwd",
    hot=[(1, 3)], edges=[((1, 3), (2, c)) for c in (4, 5, 6)],
    line2="β<sub>2</sub>(3) = 0.1 × 0.8 + 0.8 × 0.8 + 0.1 × 0.8 = 0.8")
add(9, head="backward β: t = 1, from cell 1 the robot reaches 2, 3 (a door) and 4", a=3, b=3, arrow="bwd",
    hot=[(0, 1)], edges=[((0, 1), (1, c)) for c in (2, 3, 4)],
    line2="β<sub>1</sub>(1) = 0.1 × 0.2 × 0.76 + 0.8 × 0.6 × 0.8 + 0.1 × 0.2 × 0.76 = 0.4144")
add(9, head="backward β: t = 1, from cell 3 it would read 'door' at the wall of cell 5", a=3, b=3, arrow="bwd",
    hot=[(0, 3)], edges=[((0, 3), (1, c)) for c in (4, 5, 6)],
    line2="β<sub>1</sub>(3) = 0.1 × 0.2 × 0.76 + 0.8 × 0.2 × 0.48 + 0.1 × 0.2 × 0.76 = 0.1072")
add(9, head="multiply α<sub>1</sub> × β<sub>1</sub> in every cell of t = 1", a=3, b=3, col1=True,
    line2="cell 1: 0.06 × 0.4144 = 0.0249      cell 3: 0.06 × 0.1072 = 0.0064      all 10 cells: 0.06896")
add(26, head="divide by 0.06896: the smoothed belief at t = 1 (purple bars)", a=3, b=3, col1=True, smooth=True,
    line2="cell 1: 0.0249 / 0.06896 = 0.36      cell 3: 0.0064 / 0.06896 = 0.09")
make_gif(figs, here / "fwd_bwd_anim", fps=4, holds=holds, keys=[0, 2, 6, 9], cols=2, width=950)
