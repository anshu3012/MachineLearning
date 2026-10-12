"""The problem of the Note, on the room grid. The robot follows the door's numbers (the cost-to-go of RO-048) from S
along its 3.414 m route. A box, 1.0 m x 0.5 m at x 2.0 to 3.0 m, y 2.0 to 2.5 m (dashed), stands on the route; the
map shows free floor there. After one move the robot is within 0.5 m of the box and sees its two cells (brown): the
route is blocked, and its cell's number, 2.707 m, is wrong: the way round is 4.414 m. A* from scratch searches 11
cells for the new route; the robot drives 5.121 m in all. Run -> opening.gif, opening_frames.png"""
from pathlib import Path

import plotly.graph_objects as go
from drawkit import axes, box_outline, centre, label, layout, robot, room, route, sg
from gifkit import BLUE, RED, make_gif
from replan import GOAL, START, Grid, astar, dijkstra_from_goal, drive

here = Path(__file__).parent
R = drive(1, from_full=True)
E = R["events"][0]
V0 = dijkstra_from_goal(Grid(1))
PLAN = [START]
while PLAN[-1] != GOAL:
    PLAN.append(min([ns for ns in Grid(1).nbrs(PLAN[-1]) if ns[1] < 1e9], key=lambda ns: (round(ns[1] + V0[ns[0]], 9), V0[ns[0]], ns[0]))[0])
POS = E["pos"]
assert POS == (5, 3) and PLAN[1] == POS and set(E["new"]) == {(4, 4), (5, 4)}
assert round(V0[POS], 3) == 2.707 and round(E["g"], 3) == 4.414 and len(E["astar"]) == 11
assert round(R["length"], 3) == 5.121 and round(sum(0.5 * ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5
                                                    for a, b in zip(PLAN, PLAN[1:])), 3) == 3.414
NEW = E["a_path"]                                      # A*'s new route, from the robot's cell to G
assert NEW[0] == POS and NEW[-1] == GOAL and round(E["a_cost"], 3) == 4.414


def frame(k):
    fig = go.Figure()
    seen = k >= 2
    st = {c: "box" for c in E["new"]} if seen else {}
    if k == 4:
        st.update({c: "closed" for c in E["astar"]})
    room(fig, None, st, labels=False)
    if not seen:
        box_outline(fig)
        label(fig, (2, 4), "box, not<br>on the map", size=17, color="#6B4F33", dx=0.2)
    if k < 4:
        route(fig, PLAN, BLUE, width=6, dash="dot" if seen else None)
    if k >= 4:
        route(fig, [START] + NEW, BLUE, width=6)
    if k == 0:
        robot(fig, centre(START))
        t = "the robot follows the door's numbers from S: 3.414 m"
    elif k == 1:
        robot(fig, centre(POS))
        t = "one move on: the box is now 0.5 m away"
    elif k == 2:
        robot(fig, centre(POS), colour=RED)
        t = "it sees the box: the route through it is blocked"
    elif k == 3:
        robot(fig, centre(POS), colour=RED)
        label(fig, POS, "2.707", size=17, dx=0.0, dy=0.17)
        t = "this cell's number, 2.707 m, is wrong: the way round is 4.414 m"
    elif k == 4:
        robot(fig, centre(POS))
        t = "A* from scratch: 11 cells for the new route, 4.414 m"
    else:
        n = min(k - 4, len(NEW) - 1)
        robot(fig, centre(NEW[n]))
        t = ("driving round the box" if NEW[n] != GOAL else
             "at the door after 5.121 m, against the 3.414 m planned")
    sg(fig, dy=-0.15, size=16)
    axes(fig)
    return layout(fig, t, width=900, height=620)


figs = [frame(k) for k in range(4 + len(NEW))]
holds = [12, 8, 10, 12, 12] + [3] * (len(NEW) - 2) + [30]
make_gif(figs, here / "opening", fps=4, holds=holds, keys=[0, 2, 4, len(figs) - 1], cols=2, width=760)
