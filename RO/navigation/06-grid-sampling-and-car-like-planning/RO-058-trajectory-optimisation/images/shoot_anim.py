"""Single and multiple shooting on the 8 s least-effort drive to the door pose, one solver iteration per frame
(the iterations of SciPy's least_squares, the constraint weight raised in steps; frames thin out after the first
ones). single_shoot.gif: the controls are the only unknowns; each iterate is one simulation from the start (blue),
earlier ones pale; the red line is the miss at the end. multi_shoot.gif: the 8 s are cut into 5 segments of 1.6 s,
each simulated from its own start state, also unknown, first placed on the stop-and-turn route; red lines are the
gaps (defects) between a segment's end and the next start, and the miss at the end. Both settle on the same drive.
Run -> single_shoot.gif, single_shoot_frames.png, multi_shoot.gif, multi_shoot_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import roomdraw as rd
import trajkit as tk
from gifkit import BLUE, FONT, GREEN, ORANGE, RED, make_gif

here = Path(__file__).parent
S = tk.solutions()
COLS = [BLUE, ORANGE, GREEN, "#B279A2", "#4C9FA8"]


def picks(n):
    k = list(range(min(n, 12))) + list(range(12, n, max(1, (n - 12) // 10)))
    return sorted(set(k + [n - 1]))


def gaps(segs):
    g = [np.hypot(*(segs[j][-1, :2] - segs[j + 1][0, :2])) for j in range(len(segs) - 1)]
    return g, np.hypot(*(segs[-1][-1, :2] - tk.GOAL[:2]))


def frame(sol, i, multi, title):
    segs, U = sol["hist"][i]
    fig = go.Figure()
    rd.room(fig)
    if not multi:
        for j in range(max(0, i - 4), i):
            p = sol["hist"][j][0][0]
            fig.add_trace(go.Scatter(x=p[:, 0], y=p[:, 1], mode="lines", line=dict(color="#C9D6E8", width=2)))
    for j, seg in enumerate(segs):
        fig.add_trace(go.Scatter(x=seg[:, 0], y=seg[:, 1], mode="lines",
                                 line=dict(color=COLS[j % 5] if multi else BLUE, width=5)))
        fig.add_trace(go.Scatter(x=[seg[0, 0]], y=[seg[0, 1]], mode="markers",
                                 marker=dict(size=11, color=COLS[j % 5] if multi else BLUE)))
    g, miss = gaps(segs)
    for j in range(len(segs) - 1):
        fig.add_trace(go.Scatter(x=[segs[j][-1, 0], segs[j + 1][0, 0]], y=[segs[j][-1, 1], segs[j + 1][0, 1]],
                                 mode="lines", line=dict(color=RED, width=4)))
    e = segs[-1][-1]
    fig.add_trace(go.Scatter(x=[e[0], tk.GOAL[0]], y=[e[1], tk.GOAL[1]], mode="lines", line=dict(color=RED, width=4)))
    rd.robot(fig, *tk.GOAL[:3], "#BBBBBB", width=2, fill="rgba(0,0,0,0)")
    lines = [f"<b>iteration {i}</b>", f"miss at the end: {miss:.3f} m"]
    if multi:
        lines.append(f"largest gap: {max(g):.3f} m")
    fig.add_annotation(x=1.35, y=3.85, text="<br>".join(lines), showarrow=False, xanchor="left", yanchor="top",
                       align="left", font=dict(size=21), bgcolor="rgba(255,255,255,0.9)")
    rd.axes(fig)
    fig.update_layout(template="simple_white", font=FONT, width=760, height=1000, showlegend=False,
                      title=dict(text=title, x=0.5, font_size=22), margin=dict(l=10, r=10, t=50, b=10))
    return fig, miss, (max(g) if g else 0.0)


for key, multi, name, title in (("single", False, "single_shoot", "single shooting"),
                                ("multi", True, "multi_shoot", "multiple shooting, 5 segments")):
    sol = S[key]
    n = len(sol["hist"])
    ks = picks(n)
    out = [frame(sol, i, multi, title) for i in ks]
    figs = [o[0] for o in out]
    m0, mN = out[0][1], out[-1][1]
    assert mN < 1e-3 and out[-1][2] < 1e-3
    if multi:
        assert round(out[0][2], 3) == 0.477
    else:
        assert round(m0, 3) == 1.048
    holds = [4] + [2] * (len(figs) - 2) + [12]
    make_gif(figs, here / name, fps=3, holds=holds, keys=[0, 1, 3, len(figs) - 1], cols=2, width=560)
    print(name, n - 1, "iterations; frames", len(figs))
