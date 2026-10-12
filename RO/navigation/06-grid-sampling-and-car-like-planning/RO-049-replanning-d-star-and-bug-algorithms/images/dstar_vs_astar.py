"""The same drive on the room cut into 0.1 m cells, where the robot sees the box piece by piece (it sees 0.5 m round
itself), one frame per move. Top: D* Lite, which keeps its numbers and repairs them; bottom: A* from scratch, run from
the robot's cell at the same moments. Light red: the cells each method takes off its queue at this replan; brown: box
cells the robot has seen; dashed: the box. The first plan costs D* Lite 134 cells and A* 117; the 7 replans then cost
D* Lite 387 cells and A* 596, and twice, when the new box cells lie behind the robot, D* Lite takes off none while A*
searches again. Run -> dstar_vs_astar.gif, dstar_vs_astar_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from drawkit import axes, box_outline, furniture, layout, robot, sg, title_at
from gifkit import BLUE, make_gif
from plotly.subplots import make_subplots
from replan import drive

here = Path(__file__).parent
R = drive(5)
GR, EV = R["grid"], R["events"]
H = GR.h
assert R["first"] == (134, 117) and len(EV) == 7 and len(R["truth"]) == 50
assert sum(e["dstar"] for e in EV) == 387 and sum(len(e["astar"]) for e in EV) == 596
assert [e["dstar"] for e in EV][-2:] == [0, 0] and round(R["length"], 3) == 4.087
AT = {e["step"]: e for e in EV}
COL = {"free": "#FFFFFF", "blocked": "#8A8A8A", "box": "#8C6D4F", "work": "#F6B8B8"}
CODES = list(COL)
SCALE = [x for k, n in enumerate(CODES) for x in ([k / 4, COL[n]], [(k + 1) / 4, COL[n]])]


def grid_z(seen, work):
    z = np.where(GR.base, 0, 1).astype(float)
    for (i, j) in work:
        z[j, i] = 3
    for (i, j) in seen:
        z[j, i] = 2
    return z + 0.5


def panel(fig, r, seen, work):
    fig.add_trace(go.Heatmap(z=grid_z(seen, work), x0=H / 2, dx=H, y0=H / 2, dy=H, zmin=0, zmax=4, colorscale=SCALE,
                             showscale=False, hoverinfo="skip"), row=r, col=1)
    furniture(fig, (r, 1))
    box_outline(fig, (r, 1), width=2)


def xy(c):
    return ((c[0] + 0.5) * H, (c[1] + 0.5) * H)


def frame(step):
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.08)
    seen = set()
    for e in EV:
        if e["step"] <= step:
            seen = e["seen"]
    e = AT.get(step)
    dwork = {c for c, *_ in e["dlog"]} if e else set()
    awork = set(e["astar"]) if e else set()
    if step == 0:
        dwork, awork = set(), set()
    panel(fig, 1, seen, dwork)
    panel(fig, 2, seen, awork)
    done = R["route"][:step + 1]
    for r in (1, 2):
        if len(done) > 1:
            fig.add_trace(go.Scatter(x=[xy(c)[0] for c in done], y=[xy(c)[1] for c in done], mode="lines",
                                     line=dict(color=BLUE, width=4), hoverinfo="skip"), row=r, col=1)
        robot(fig, xy(done[-1]), (r, 1), size=13)
        sg(fig, (r, 1), dy=-0.15, size=16)
        axes(fig, (r, 1))
    past = [x for x in EV if x["step"] <= step]
    dtot, atot = sum(x["dstar"] for x in past), sum(len(x["astar"]) for x in past)
    if e:
        t1 = f"D* Lite repairs: {e['dstar']} cells now; replans so far {dtot}"
        t2 = f"A* from scratch: {len(e['astar'])} cells now; replans so far {atot}"
    else:
        t1 = f"D* Lite: first plan 134 cells; replans so far {dtot}"
        t2 = f"A* from scratch: first plan 117 cells; replans so far {atot}"
    title_at(fig, t1, 1.0, size=20)
    title_at(fig, t2, 0.47, size=20)
    head = (f"move {step}: new box cells seen" if e else f"move {step}" if step else
            "0.1 m cells; the robot sees 0.5 m round itself")
    if step == len(R["route"]) - 1:
        head = f"at the door: replans cost D* Lite {dtot} cells, A* {atot}"
    return layout(fig, head, width=900, height=1080, margin=dict(l=30, r=30, t=110, b=30))


steps = list(range(len(R["route"])))
figs = [frame(s) for s in steps]
holds = [12] + [14 if s in AT else 2 for s in steps[1:-1]] + [30]
make_gif(figs, here / "dstar_vs_astar", fps=5, holds=holds, keys=[3, 4, 18, steps[-1]], cols=2, width=700)
