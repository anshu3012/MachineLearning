"""A moving goal: a person P walks along the top wall from x 5.0-5.5 m towards the left, one 0.5 m cell per second.
Each cell of the person's walk, with the second the person is in it, is a goal (purple numbers: that second). The
robot R drives at 0.5 m/s, so it needs 2 s per metre of its shortest route. The first goal it can reach in time is
the cell x 2.0-2.5 m, y 3.5-4.0 m, where the person is at 6 s: the robot's route there is 2.5 m straight up, 5 s; it
waits 1 s and they meet at 6 s. One frame per second. Run -> moving_target.gif, moving_target_frames.png"""
from pathlib import Path

import plotly.graph_objects as go
from drawkit import axes, centre, layout, room, route, title_at
from gifkit import BLUE, PURPLE, make_gif
from searchkit import START, astar, dist_from

here = Path(__file__).parent
XR, YR = (1, 11), (0, 8)
V = 0.5                                                     # robot speed, m/s
walk = [(10 - k, 7) for k in range(11)]                    # person's cell at second k
d = dist_from(START)
arrive = [d[c] / V for c in walk]
meet = next(k for k, c in enumerate(walk) if arrive[k] <= k + 1e-9)
assert meet == 6 and walk[meet] == (4, 7) and round(arrive[meet], 3) == 5.0
assert [round(a, 3) for a in arrive[:7]] == [9.828, 8.828, 7.828, 6.828, 5.828, 5.414, 5.0]
R = astar(goal=walk[meet])
assert R["path"] == [(4, j) for j in range(2, 8)] and round(R["cost"], 3) == 2.5


def frame(t):
    fig = go.Figure()
    room(fig, None, {}, xr=XR, yr=YR, labels=False)
    route(fig, R["path"], colour=BLUE, width=3, dash="dot", points=[(x, y - 0.05) for x, y in map(centre, R["path"])])
    for k, c in enumerate(walk):
        if k > t and XR[0] <= c[0] < XR[1]:
            x, y = centre(c)
            fig.add_annotation(x=x, y=y + 0.175, text=f"{k} s", showarrow=False, font=dict(size=18, color=PURPLE))
    rc = R["path"][min(t, len(R["path"]) - 1)]
    pc = walk[t]
    for c, txt, col, dy in ((pc, "P", PURPLE, 0.0), (rc, "R", BLUE, -0.09 if rc == pc else 0.0)):
        x, y = centre(c)
        fig.add_trace(go.Scatter(x=[x + (0.11 if rc == pc and txt == "R" else (-0.11 if rc == pc else 0))], y=[y + dy - 0.05],
                                 mode="markers+text", text=[f"<b>{txt}</b>"], textfont=dict(size=17, color="white"),
                                 marker=dict(size=27, color=col)))
    axes(fig, None, XR, YR)
    if t < 5:
        sub = "purple: the second the person reaches each cell; dotted: the robot's route"
    elif t == 5:
        sub = "the robot is there after 2.5 m, at 5 s: it waits for the person"
    else:
        sub = "they meet: the first goal the robot can reach in time"
    title_at(fig, sub, 1.0, size=19)
    return layout(fig, f"t = {t} s", width=900, height=700, margin=dict(l=30, r=30, t=110, b=30))


figs = [frame(t) for t in range(meet + 1)]
make_gif(figs, here / "moving_target", fps=1, holds=[3, 2, 2, 2, 2, 3, 10], keys=[0, 3, 5, 6], cols=2, width=760)
