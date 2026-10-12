"""A moving goal: a person P walks along the top wall from x 5.0-5.5 m towards the left, one 0.5 m cell per second,
so the person is in the k-th cell of the walk from second k to second k + 1 (purple: that second). The robot R drives
at 0.5 m/s. A* over states (cell, time), with moves of 1 s (straight), 1.414 s (diagonal) or a 1 s wait, finds the
earliest meeting: four cells straight up, then one diagonal into the cell x 2.5-3.0 m, y 3.5-4.0 m at 5.414 s, while
the person is in it (5 to 6 s). 8 states come off the open list before V. Frames at t = 0, 1, ..., 5 s and 5.414 s.
Run -> moving_target.gif, moving_target_frames.png"""
from pathlib import Path

import plotly.graph_objects as go
from drawkit import axes, centre, layout, room, route, title_at
from gifkit import BLUE, PURPLE, make_gif
from searchkit import START, dist_from, moving_goal, path_cost

here = Path(__file__).parent
r3 = lambda x: round(x, 3)
XR, YR = (1, 11), (0, 8)
V = 0.5                                                     # robot speed, m/s
walk = [(10 - k, 7) for k in range(11)]                    # the person's cell from second k to k + 1
R = moving_goal(walk, speed=V)
cells, times = [s[0] for s in R["path"][:-1]], [s[1] for s in R["path"][:-1]]
assert cells == [(4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (5, 7)] and [r3(t) for t in times] == [0, 1, 2, 3, 4, 5.414]
assert r3(R["cost"]) == 5.414 and r3(path_cost(cells)) == 2.707 and len(R["order"]) == 9 and R["order"][-1] == "V"
assert walk[5] == (5, 7) and r3(4 + 1.414) == 5.414 and r3(4 * 0.5 + 0.707) == 2.707 and r3(2.707 / 0.5) == 5.414
d = dist_from(START)                                        # the check: earliest arrival in each cell of the walk
assert [r3(d[walk[k]] / V) for k in (3, 4, 5, 6)] == [6.828, 5.828, 5.414, 5.0]


def robot_at(t):
    """The robot's position at time t, moving along its route at 0.5 m/s."""
    for (a, ta), (b, tb) in zip(zip(cells, times), zip(cells[1:], times[1:])):
        if ta <= t <= tb:
            (xa, ya), (xb, yb) = centre(a), centre(b)
            u = (t - ta) / (tb - ta)
            return xa + u * (xb - xa), ya + u * (yb - ya)
    return centre(cells[-1])


def frame(t, meet=False):
    fig = go.Figure()
    room(fig, None, {}, xr=XR, yr=YR, labels=False)
    route(fig, cells, colour=BLUE, width=3, dash="dot", points=[(x, y - 0.05) for x, y in map(centre, cells)])
    for k, c in enumerate(walk):
        if k + 1 > t and XR[0] <= c[0] < XR[1]:
            x, y = centre(c)
            fig.add_annotation(x=x, y=y + 0.175, text=f"{k}–{k + 1} s", showarrow=False,
                               font=dict(size=16, color=PURPLE))
    px, py = centre(walk[int(t)])
    rx, ry = robot_at(t)
    if meet:
        px, rx = px - 0.11, rx + 0.11
    for x, y, txt, col in ((px, py - 0.05, "P", PURPLE), (rx, ry - 0.05, "R", BLUE)):
        fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers+text", text=[f"<b>{txt}</b>"],
                                 textfont=dict(size=17, color="white"), marker=dict(size=27, color=col)))
    axes(fig, None, XR, YR)
    if t < 5:
        sub = "purple: when the person is in each cell; dotted: the route A* finds over (cell, time)"
    elif not meet:
        sub = "the person steps into x 2.5 to 3.0 m; the robot is on its last move, a diagonal"
    else:
        sub = "they meet in x 2.5 to 3.0 m at 5.414 s: the person is there until 6 s"
    title_at(fig, sub, 1.0, size=19)
    return layout(fig, f"t = {r3(t):g} s", width=900, height=700, margin=dict(l=30, r=30, t=110, b=30))


figs = [frame(t) for t in range(6)] + [frame(R["cost"], meet=True)]
make_gif(figs, here / "moving_target", fps=1, holds=[3, 2, 2, 2, 2, 3, 10], keys=[0, 3, 5, 6], cols=2, width=760)
