"""Two robots on a smooth floor with their motors off, played from one second ago to one second from now (titles in
words: the Note uses t for the time step). Robot A stands still at 2 m. Robot B rolls at 0.5 m/s: 1.5 m, then 2 m now, then 2.5 m. At t = 0 both
are at 2 m and look the same; only the speed tells where each will be.
Run: python coasting_anim.py -> coasting_anim.gif, coasting_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, PURPLE, make_gif

here = Path(__file__).parent
V_B = 0.5                                           # robot B's speed (m/s); robot A's is 0
YA, YB = 1.7, 0.0                                   # the two rows (robot A above, robot B below)
W, H = 0.08, 0.5                                    # half-width and height of a robot box (m, row units)


def xb(t):
    return 2.0 + V_B * t


assert (xb(-1), xb(0), xb(1)) == (1.5, 2.0, 2.5)


def box(fig, x, y, col, solid=True):
    fig.add_shape(type="rect", x0=x - W, x1=x + W, y0=y + 0.1, y1=y + 0.1 + H, opacity=1,
                  line=dict(color=col, width=3 if solid else 2, dash="solid" if solid else "dash"),
                  fillcolor="rgba(178,121,162,0.25)" if solid and col == PURPLE else
                  "rgba(76,120,168,0.25)" if solid else "rgba(0,0,0,0)")


def note(fig, x, y, text, col=GREY, size=18, anchor="center"):
    fig.add_annotation(x=x, y=y, text=text, showarrow=False, font=dict(size=size, color=col), xanchor=anchor,
                       align="left" if anchor == "left" else "center")


def frame(t, title, final=False):
    fig = go.Figure()
    for y in (YA, YB):                              # the floor of each row, with ticks every 0.5 m
        fig.add_shape(type="line", x0=0.9, x1=3.1, y0=y, y1=y, line=dict(color=GREY, width=2), opacity=1)
        for m in (1, 1.5, 2, 2.5, 3):
            fig.add_shape(type="line", x0=m, x1=m, y0=y - 0.08, y1=y + 0.08, line=dict(color=GREY, width=2), opacity=1)
            note(fig, m, y - 0.3, f"{m:g}", "black", 18)
    note(fig, 0.85, YA + 0.35, "robot A", BLUE, 22, "right")
    note(fig, 0.85, YB + 0.35, "robot B", PURPLE, 22, "right")
    box(fig, 2.0, YA, BLUE)
    note(fig, 2.0, YA + 0.85, "1 s ago, now and in 1 s" if final else "standing still", BLUE)
    if t >= 0:                                      # robot B's earlier places, dashed
        box(fig, 1.5, YB, PURPLE, solid=False)
        note(fig, 1.5, YB + 0.85, "1 s ago", PURPLE)
    if t > 0:
        box(fig, 2.0, YB, PURPLE, solid=False)
        note(fig, 2.0, YB + 0.85, "now", PURPLE)
    x = xb(t)
    box(fig, x, YB, PURPLE)
    if t == 0:
        note(fig, x, YB + 0.85, "now", PURPLE)
    if final:
        note(fig, x, YB + 0.85, "in 1 s", PURPLE)
        a0, a1 = 2.1, 2.4
    else:
        a0, a1 = x + 0.1, x + 0.3
    fig.add_annotation(x=a1, y=YB + 0.35, ax=a0, ay=YB + 0.35, axref="x", ayref="y", showarrow=True, text="",
                       arrowhead=2, arrowsize=1.2, arrowwidth=3, arrowcolor=PURPLE)
    if final:
        note(fig, 3.15, YA + 0.35, "speed 0 m/s<br>in 1 s: 2 m", BLUE, 20, "left")
        note(fig, 3.15, YB + 0.35, "speed 0.5 m/s<br>in 1 s: 2.5 m", PURPLE, 20, "left")
        note(fig, 2.0, -0.9, "both at 2 m now, no command: the speed decides where each robot will be")
        note(fig, 2.0, -1.3, "position alone is not a complete state; (position, speed) is")
    else:
        note(fig, 3.15, YA + 0.35, "position 2.00 m<br>speed 0 m/s", BLUE, 20, "left")
        note(fig, 3.15, YB + 0.35, f"position {x:.2f} m<br>speed 0.5 m/s", PURPLE, 20, "left")
        if t == 0:
            note(fig, 2.0, -0.9, "same position now; only the speed is different")
    fig.update_xaxes(visible=False, range=[0.3, 3.75])
    fig.update_yaxes(visible=False, range=[-1.5, 2.85])
    fig.update_layout(template="simple_white", width=1000, height=520, font=FONT, showlegend=False,
                      margin=dict(l=20, r=20, t=70, b=10), title=dict(text=title, x=0.5, y=0.95, font=dict(size=22)))
    return fig


ts = np.round(np.arange(-1, 1.0001, 0.125), 3)
figs, holds = [], []
for t in ts:
    if t == -1:
        figs.append(frame(t, "1 s ago: motors off; A stands at 2 m, B rolls at 0.5 m/s"))
        holds.append(8)
    elif t == 0:
        figs.append(frame(t, "now: both robots are at 2 m"))
        holds.append(14)
    elif t == 1:
        figs.append(frame(t, "in 1 s: A is still at 2 m, B is at 2.5 m", final=True))
        holds.append(24)
    else:
        figs.append(frame(t, f"{abs(t):.2f} s {'before' if t < 0 else 'after'} now"))
        holds.append(1)
i0 = int(np.flatnonzero(ts == 0)[0])
make_gif(figs, here / "coasting_anim", fps=4, holds=holds, keys=[0, i0, len(figs) - 1], cols=1, width=900)
