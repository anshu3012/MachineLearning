"""The order of events, built one event at a time on the hallway run: start in x0 = cell 1; control u1 = stay gives
x1 = cell 1, where z1 = door is read; u2 = move 2 gives x2 = cell 3, z2 = door; u3 = move 2 gives x3 = cell 5,
z3 = wall. Controls point into the states (green arrows), measurements out of them (orange arrows). Below, the
hallway (doors at cells 1, 3 and 7) with the robot's true cell.
Run: python timeline_anim.py -> timeline_anim.gif, timeline_anim_frames.png"""
from pathlib import Path

import plotly.graph_objects as go
from corrdraw import DOORS
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, RED, make_gif

here = Path(__file__).parent
RUN = [(None, 1, None), ("stay", 1, "door"), ("move 2", 3, "door"), ("move 2", 5, "wall")]   # (u_t, x_t, z_t)
for (u, c, z), (_, c0, _) in zip(RUN[1:], RUN[:-1]):
    assert c == (c0 + {"stay": 0, "move 2": 2}[u]) % 10 and z == ("door" if c in DOORS else "wall")
SX, UY, ZY = 3.2, 1.6, -1.8                         # spacing of the states; heights of the control and reading boxes
HY = -6.2                                           # middle of the hallway strip


def X(cell):
    return 0.15 + 1.1 * cell


def node(fig, x, y, text, col, fill, symbol, size):
    fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers+text", text=[text], textposition="middle center",
                             textfont=dict(size=24, color="black"),
                             marker=dict(size=size, symbol=symbol, color=fill, line=dict(color=col, width=3))))


def arrow(fig, x0, y0, x1, y1, col, start, end):
    fig.add_annotation(x=x1, y=y1, ax=x0, ay=y0, axref="x", ayref="y", showarrow=True, text="", arrowhead=2,
                       arrowsize=1.1, arrowwidth=3, arrowcolor=col, startstandoff=start, standoff=end)


def text(fig, x, y, s, col="black", size=20, anchor="center"):
    fig.add_annotation(x=x, y=y, text=s, showarrow=False, font=dict(size=size, color=col), xanchor=anchor,
                       align="left" if anchor == "left" else "center")


def frame(k, robot, title, hall=None, final=False):
    """k: how many events are shown (1 = x0 only; then u1, z1, u2, z2, u3, z3). robot: the robot's cell (may be
    between cells while it moves). hall: (text, colour) written beside the robot."""
    fig = go.Figure()
    for t in range(4):
        if t > 0 and k < 2 * t:                     # u_t appears at event 2t, z_t at event 2t + 1
            break
        x = SX * t
        if t > 0:
            arrow(fig, x - SX, 0, x, 0, GREY, 33, 33)
            node(fig, x - SX / 2, UY, f"u<sub>{t}</sub>", GREEN, "rgba(84,162,75,0.12)", "square", 52)
            arrow(fig, x - SX / 2, UY, x, 0, GREEN, 28, 33)
        node(fig, x, 0, f"x<sub>{t}</sub>", BLUE, "rgba(76,120,168,0.12)", "circle", 64)
        u, c, z = RUN[t]
        text(fig, x, -3.0, f"x<sub>{t}</sub> = cell {c}")
        if u:
            text(fig, x, -3.55, u, GREEN)
        if t > 0 and k >= 2 * t + 1:
            arrow(fig, x, 0, x, ZY, ORANGE, 33, 28)
            node(fig, x, ZY, f"z<sub>{t}</sub>", ORANGE, "rgba(245,133,24,0.12)", "square", 52)
            text(fig, x, -4.1, z, ORANGE)
    text(fig, 0, -0.85, "start", BLUE, 18)
    text(fig, 0, -2.45, "hallway run:", GREY, 18)
    if final:
        text(fig, 11.0, 0, "⋯", "black", 26)
        text(fig, SX * 1.5, 2.55, "controls change the state", GREEN, 20)
        text(fig, 10.3, ZY, "measurements<br>report on<br>the state", ORANGE, 20, "left")
    # the hallway: walls, doors, cell numbers, the robot's true cell
    for y in (HY - 0.6, HY + 0.6):
        fig.add_shape(type="line", x0=X(-0.5), x1=X(9.5), y0=y, y1=y, line=dict(color="black", width=4), opacity=1)
    for d in DOORS:
        fig.add_shape(type="line", x0=X(d) - 0.33, x1=X(d) + 0.33, y0=HY + 0.6, y1=HY + 0.6,
                      line=dict(color=ORANGE, width=12), opacity=1)
        text(fig, X(d), HY + 0.95, "door", ORANGE, 18)
    for c in range(10):
        text(fig, X(c), HY - 0.95, str(c), "black", 18)
    text(fig, X(4.5), HY - 1.55, "the hallway: the red square is the robot's true cell, which the robot never sees",
         GREY, 18)
    fig.add_trace(go.Scatter(x=[X(robot)], y=[HY], mode="markers", marker=dict(size=28, symbol="square", color=RED)))
    if hall:
        text(fig, X(robot) + 0.45, HY, hall[0], hall[1], 20, "left")
    fig.update_xaxes(visible=False, range=[-1.3, 12.4])
    fig.update_yaxes(visible=False, range=[-8.0, 2.95])
    fig.update_layout(template="simple_white", width=1000, height=820, font=FONT, showlegend=False,
                      margin=dict(l=10, r=10, t=70, b=10), title=dict(text=title, x=0.5, y=0.97, font=dict(size=22)))
    return fig


figs, holds = [frame(1, 1, "start: the robot is in state x<sub>0</sub> = cell 1")], [10]
for t in (1, 2, 3):
    u, c, z = RUN[t]
    c0 = RUN[t - 1][1]
    title = f"control u<sub>{t}</sub> = {u}: the state becomes x<sub>{t}</sub> = cell {c}"
    for s in (0.25, 0.5, 0.75) if c != c0 else ():   # the robot slides from its old cell to the new one
        figs.append(frame(2 * t, c0 + s * (c - c0), title, (u, GREEN)))
        holds.append(1)
    figs.append(frame(2 * t, c, title, (u, GREEN)))
    holds.append(10)
    figs.append(frame(2 * t + 1, c, f"measurement z<sub>{t}</sub> = {z}, read in state x<sub>{t}</sub>",
                      (f'reads "{z}"', ORANGE)))
    holds.append(10)
figs.append(frame(7, 5, "each step: a control changes the state, then a measurement reports on it",
                  ('reads "wall"', ORANGE), final=True))
holds.append(24)
make_gif(figs, here / "timeline_anim", fps=4, holds=holds, keys=[0, 2, 7, len(figs) - 1], cols=2, width=950)
