"""Animation for the Overview: two things the earlier plans assume and the moving robot cannot do.
Left, stopping: on RO-037's straight line to the closed door the plan drives at the top speed, 0.6 m/s, to s = 3.0 m and
stops there (pale robot). Braking at 0.5 m/s^2 takes 0.36 m, so the robot meets the door at s = 3.117 m still moving
at 0.49 m/s. Right, turning: driving RO-034's A* route at 0.5 m/s, the plan turns 45 degrees at the first corner
(2.75, 1.75) at once (pale robot); turning at its limit, 1 rad/s, the robot swings 0.146 m to the right of the route.
Run -> opening.gif, opening_frames.png"""
import math
from pathlib import Path

import numpy as np
from plotly.subplots import make_subplots

import drawkit as k
import motionkit as m
from gifkit import GREEN, RED, make_gif

here = Path(__file__).parent

# left: the late stop
S0, V_PLAN, S_BRAKE = 2.4, m.V_TOP, 3.0
v_hit = math.sqrt(V_PLAN ** 2 - 2 * m.A_MAX * (m.S_DOOR - S_BRAKE))
assert round(m.S_DOOR, 3) == 3.117 and round(v_hit, 2) == 0.49 and round(m.stopping_distance(V_PLAN), 2) == 0.36


def left_state(t):
    """(s, v, hit) at time t: cruise at 0.6 m/s to s = 3.0, then brake until the door."""
    t_cruise = (S_BRAKE - S0) / V_PLAN
    if t <= t_cruise:
        return S0 + V_PLAN * t, V_PLAN, False
    tb = t - t_cruise
    t_hit = (V_PLAN - v_hit) / m.A_MAX
    tb = min(tb, t_hit)
    return S_BRAKE + V_PLAN * tb - 0.5 * m.A_MAX * tb * tb, V_PLAN - m.A_MAX * tb, tb >= t_hit - 1e-9


# right: the corner
ROUTE = [(2.25, 1.25), (2.75, 1.75), (2.75, 2.25), (2.75, 2.75), (2.75, 3.25), (3.25, 3.75), (3.75, 3.75)]
CORNER = ROUTE[1]
T_SEG = math.dist(ROUTE[0], CORNER) / m.V_CRUISE
TURN = math.pi / 4
T_TURN = TURN / m.W_MAX
swing = m.RHO * (1 - math.cos(TURN))
assert round(swing, 3) == 0.146 and round(m.W_MAX, 6) == 1 and round(m.RHO, 6) == 0.5


def right_state(t):
    """Pose of the robot on the route's first leg, then turning left at 1 rad/s from the corner."""
    th0 = math.pi / 4
    if t <= T_SEG:
        return (ROUTE[0][0] + m.V_CRUISE * t * math.cos(th0), ROUTE[0][1] + m.V_CRUISE * t * math.sin(th0), th0)
    tt = min(t - T_SEG, T_TURN + 0.9)
    turn = min(tt, T_TURN) * m.W_MAX
    x = CORNER[0] + m.RHO * (math.sin(th0 + turn) - math.sin(th0))
    y = CORNER[1] - m.RHO * (math.cos(th0 + turn) - math.cos(th0))
    if tt > T_TURN:
        y += m.V_CRUISE * (tt - T_TURN)
    return (x, y, th0 + turn)


def trail_right(t, n=60):
    return [right_state(u) for u in np.linspace(0, t, n)]


def frame(t, final=False):
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08,
                        subplot_titles=["stopping takes room", "turning takes room"])
    # left
    k.room(fig, 1, 1)
    xa, ya = m.on_line(0)
    xb, yb = m.on_line(m.LINE_LEN)
    k.line(fig, [xa, xb], [ya, yb], color="black", width=1.5, dash="dot", row=1, col=1)
    s, v, hit = left_state(t)
    xs, ys = zip(*[m.on_line(u) for u in np.linspace(S0, s, 30)])
    k.line(fig, xs, ys, color=RED if hit else GREEN, width=4, row=1, col=1)
    if t >= (S_BRAKE - S0) / V_PLAN:
        gx, gy = m.on_line(S_BRAKE)
        k.ghost(fig, gx, gy, m.LINE_HEADING, row=1, col=1)
        k.text(fig, gx - 0.42, gy - 0.05, "plan: stop<br>at 3.0 m", color="#888888", size=16, row=1, col=1,
               xanchor="right")
    px, py = m.on_line(s)
    k.disk(fig, px, py, m.LINE_HEADING, row=1, col=1, color=RED if hit else k.FOOT)
    msg = (f"hits the door at {s:.3f} m<br>still at {v:.2f} m/s" if hit else
           f"s = {s:.2f} m<br>speed {v:.2f} m/s" + (", braking" if s > S_BRAKE + 1e-9 else ""))
    k.text(fig, 1.7, 2.95, msg, color=RED if hit else "black", size=17, row=1, col=1, xanchor="left")
    # right
    k.room(fig, 1, 2)
    rx, ry = zip(*ROUTE)
    k.line(fig, rx, ry, color="black", width=2, dash="dot", mode="lines+markers", row=1, col=2)
    tr = trail_right(t)
    k.line(fig, [p[0] for p in tr], [p[1] for p in tr], color=GREEN, width=4, row=1, col=2)
    p = right_state(t)
    if t > T_SEG:
        k.ghost(fig, CORNER[0], CORNER[1], math.pi / 2, row=1, col=2)
        k.text(fig, CORNER[0] - 0.33, CORNER[1] + 0.05, "plan: turn<br>45° here", color="#888888", size=16,
               row=1, col=2, xanchor="right")
    k.disk(fig, p[0], p[1], p[2], row=1, col=2)
    if t >= T_SEG + T_TURN:
        yy = CORNER[1] + m.RHO * math.sin(TURN)
        k.line(fig, [CORNER[0], CORNER[0] + swing], [yy, yy], color=RED, width=4, row=1, col=2)
        k.text(fig, CORNER[0] - 0.05, yy + 0.02, f"{swing:.3f} m off<br>the route", color=RED, size=17, row=1, col=2,
               xanchor="right")
    else:
        k.text(fig, 1.75, 0.92, f"speed 0.5 m/s, turning at most {m.W_MAX:.0f} rad/s", size=17, row=1, col=2, xanchor="left")
    k.room_axes(fig, 1, 1, xr=(1.6, 4.6), yr=(1.9, 4.3), anchor="x")
    k.room_axes(fig, 1, 2, xr=(1.7, 3.9), yr=(0.8, 3.2), anchor="x2")
    title = ("the plans assume an instant stop and an instant turn" if not final else
             "neither happens at speed: the robot needs room to stop and room to turn")
    k.layout(fig, 1300, 640, title, margin=dict(l=70, r=20, t=100, b=60))
    fig.update_annotations(font_size=21, selector=dict(text="stopping takes room"))
    fig.update_annotations(font_size=21, selector=dict(text="turning takes room"))
    return fig


times = list(np.arange(0, 3.15, 0.1))
figs = [frame(t) for t in times] + [frame(times[-1], final=True)]
holds = [6] + [2] * (len(times) - 1) + [26]
make_gif(figs, here / "opening", fps=6, holds=holds, keys=[0, 10, 15, len(figs) - 1], cols=2, width=1000)
