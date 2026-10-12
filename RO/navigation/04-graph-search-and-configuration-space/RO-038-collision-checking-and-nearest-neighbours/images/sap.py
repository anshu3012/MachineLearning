"""Animation: sweep and prune on the room's five bodies (the robot with its centre at (3.5, 3.2), the table, the
cabinet and the two poles), each inside its box with sides along x and y. The boxes are sorted by left edge; a sweep line moves
right; a box joins the active list at its left edge and leaves at its right edge. Each box that joins is compared
only with the active boxes, which overlap it along x; the full box test then checks y. Two pairs reach the box test,
one passes (robot and table); the narrow phase then finds the robot 0.2 m from the table: a collision.
Run -> sap.gif, sap_frames.png"""
from pathlib import Path

import plotly.graph_objects as go

import collide as k
import cspace as c
import drawkit as dk
from gifkit import BLUE, GREEN, GREY, ORANGE, PURPLE, RED, make_gif

here = Path(__file__).parent
q = c.TEST
bodies = {**k.furniture(), "robot": k.robot(q)}
boxes = {n: k.aabb(g) for n, g in bodies.items()}
order, xpairs, looks = k.sweep_and_prune(boxes)
assert order == ["pink pole", "table", "robot", "cabinet", "green pole"]
assert xpairs == [("table", "robot", True), ("cabinet", "green pole", False)]
COL = {"table": BLUE, "cabinet": PURPLE, "pink pole": dk.PINK, "green pole": GREEN, "robot": RED}
events = sorted([(b[0], 0, n) for n, b in boxes.items()] + [(b[2], 1, n) for n, b in boxes.items()])


def frame(title, x=None, active=(), flagged=(), tested=(), note=None, lines=()):
    fig = go.Figure()
    dk.room(fig, walls=False)
    dk.disk(fig, *q, 0.0, body=False, color=RED)
    for n, (x0, y0, x1, y1) in boxes.items():
        w = 5 if n in active else 2
        fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, line=dict(color=COL[n], width=w, dash="dash"),
                      fillcolor="rgba(0,0,0,0)", opacity=1, layer="above")
    if x is not None:
        fig.add_shape(type="line", x0=x, x1=x, y0=-0.3, y1=4.3, line=dict(color=ORANGE, width=4), opacity=1)
    for i, (s, col) in enumerate(lines):
        fig.add_annotation(x=0.67, y=0.98 - 0.075 * i, xref="paper", yref="paper", xanchor="left", yanchor="top", text=s,
                           showarrow=False, font=dict(size=18, color=col), align="left")
    dk.axes(fig, [-0.2, 7.3], [-0.3, 4.3])
    fig.update_layout(xaxis_domain=[0, 0.64])
    dk.layout(fig, 1350, 600, title, margin=dict(l=70, r=20, t=80, b=60))
    return fig


def status(active, tests, flag, extra=()):
    s = [("active boxes (overlap the line):", "black")] + [("  " + n, COL[n]) for n in active] + [("", "black")]
    s += [(f"box tests so far: {tests} (all pairs: 10)", "black")]
    s += [("flagged pairs: " + (", ".join(f"{a}–{b}" for a, b in flag) if flag else "none"), RED if flag else GREY)]
    return s + list(extra)


figs = [frame("5 bodies, 10 pairs: draw a box round each body",
              lines=[("brute force: test all 10 pairs", "black"), ("(walls left out here; Section 3)", GREY)]),
        frame("sort the boxes by their left edge", lines=[("sorted by left edge:", "black")] +
              [(f"  {n}: {boxes[n][0]:g} m", COL[n]) for n in order])]
holds = [6, 6]
active, tests, flag = [], 0, []
for x, kind, n in events:
    if kind == 0:
        msg = []
        for m in active:
            tests += 1
            ok = k.overlap(boxes[m], boxes[n])
            msg += [(f"{m} and {n} overlap along x;", RED if ok else GREY),
                    ("box test on y: " + ("they overlap: flag the pair" if ok else "no overlap"), RED if ok else GREY)]
            if ok:
                flag.append((m, n))
        active.append(n)
        title = f"x = {x:g} m: the {n} joins" + (", compared with the active boxes" if msg else "")
    else:
        active.remove(n)
        msg = []
        title = f"x = {x:g} m: the {n} leaves"
    figs.append(frame(title, x, active, lines=status(active, tests, flag, [("", "black")] + msg)))
    holds.append(5 if msg else 2)
assert tests == 2 and flag == [("table", "robot")]
d = bodies["table"].distance(k.Point(*q))
figs.append(frame("narrow phase on the one flagged pair: robot and table", lines=[
    ("2 box tests instead of 10 pairs", "black"), ("1 pair flagged: table and robot", RED), ("", "black"),
    ("narrow phase: centre (3.5, 3.2) is", "black"), (f"{d:.1f} m from the table, less than 0.25 m:", "black"),
    ("collision", RED)]))
holds.append(14)
make_gif(figs, here / "sap", fps=2, holds=holds, keys=[1, 5, 9, len(figs) - 1], cols=2, width=1000)
