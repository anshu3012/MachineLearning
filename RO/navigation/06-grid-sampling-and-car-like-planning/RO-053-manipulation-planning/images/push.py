"""Animation: the arm pushes the cup (no lid, so the suction gripper cannot hold it) 6 cm to the left, from A
(centre x = 0.18 m) to C (x = 0.12 m). Cup: 0.25 kg, 0.06 m wide, 0.08 m tall; friction coefficient with the
table 0.4 (assumed). Part 1: a slow push (0.05 m/s) 0.04 m above the table: the cup slides with the hand and stops
when the hand stops (it would coast 0.32 mm). Part 2: a push at the rim, 0.08 m up: the cup tips over its left
bottom corner, because the push's torque about that corner, 0.0785 N m, beats the weight's, 0.0736 N m, before the
cup can slide. Part 3: a fast push (0.5 m/s) at 0.04 m: when the hand stops at C the cup slides on 3.2 cm.
Run -> push.gif, push_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from shapely import affinity

import armdraw as ad
import manip as m
from gifkit import BLUE, GREEN, GREY, RED, make_gif

here = Path(__file__).parent
MASS, G, MU, W = 0.25, 9.81, 0.4, m.CUP_W
weight = MASS * G
friction = MU * weight
coast = lambda v: v ** 2 / (2 * MU * G)
assert round(friction, 3) == 0.981 and round(weight * W / 2, 4) == 0.0736 and round(friction * 0.08, 4) == 0.0785
assert round(coast(0.05) * 1000, 2) == 0.32 and round(coast(0.5) * 100, 1) == 3.2 and round(W / (2 * MU), 3) == 0.075
A, C = m.A_X, 0.12


def hand_q(hand):
    """The elbow-up solution: link 2 comes down to the cup's right face from above."""
    return [s for s in m.ik(hand) if s[1] < 0][0]


def frame(title, cup_geom, hand, lines, target=True):
    fig = go.Figure()
    ad.scene(fig, spot_b=False)
    if target:
        ad.poly(fig, m.cup_at(C), "rgba(0,0,0,0)", GREY, 1.5, "dash")
        fig.add_trace(go.Scatter(x=[C], y=[-0.15], mode="text", text=["C"], textfont=dict(size=16, color="#4D4D4D")))
    ad.poly(fig, cup_geom, ad.CUP_FILL, ad.CUP_LINE)
    ad.arm(fig, hand_q(hand))
    for j, (s, c) in enumerate(lines):
        fig.add_annotation(x=0.6, y=0.96 - 0.07 * j, xref="paper", yref="paper", xanchor="left", yanchor="top",
                           text=s, showarrow=False, font=dict(size=19, color=c))
    ad.scene_axes(fig, xr=(-0.05, 0.38), yr=(-0.2, 0.28))
    fig.update_xaxes(domain=[0, 0.55])
    fig.update_yaxes(scaleanchor="x")
    ad.layout(fig, 1300, 640, title, margin=dict(l=80, r=20, t=80, b=60))
    return fig


figs, holds = [], []
# part 1: slow push low
p = 0.04
for k, x in enumerate([0.26, 0.235]):
    figs.append(frame("1. slow push, 4 cm above the table: the hand reaches the cup", m.cup_at(A),
                      (x, m.TOP + p), [("push 4 cm above the table", "black"), ("at 0.05 m/s", "black")]))
    holds.append(3)
for t in np.arange(0, 1.21, 0.2):
    xc = A - 0.05 * t
    figs.append(frame(f"1. slow push: t = {t:.1f} s, the cup slides with the hand", m.cup_at(xc),
                      (xc + W / 2, m.TOP + p),
                      [("push 4 cm above the table", "black"), ("at 0.05 m/s", "black"), ("", "black"),
                       ("push = friction = 0.981 N", "black"), ("speeding up the cup takes", "black"),
                       ("only 0.025 N: forces balance", GREEN), ("", "black"), (f"cup moved: {100 * (A - xc):.0f} cm", BLUE)]))
    holds.append(2)
figs.append(frame("1. the hand stops at C, and the cup stops with it", m.cup_at(C), (C + W / 2, m.TOP + p),
                  [("hand stops: the cup coasts", "black"), ("0.32 mm and stops at C", GREEN), ("", "black"),
                   ("slow pushing is quasistatic:", "black"), ("the cup moves only while", "black"),
                   ("it is pushed", "black")]))
holds.append(10)
# part 2: push at the rim, the cup tips over its left bottom corner
p = 0.08
pivot = (A - W / 2, m.TOP)
for k, phi in enumerate([0, 10, 20, 35]):
    cup = affinity.rotate(m.cup_at(A), phi, origin=pivot)
    corner = list(cup.exterior.coords)[1]                      # the cup's top right corner, where the hand pushes
    hand = (corner[0] + 0.004, corner[1]) if phi else (A + W / 2 + 0.004, m.TOP + p)
    figs.append(frame(f"2. push at the rim, 8 cm up: the cup tips by {phi} degrees", cup, hand,
                      [("push at the rim, 8 cm up", "black"), ("", "black"),
                       ("torque about the left corner:", "black"), ("push 0.981 x 0.08 = 0.0785 N m", RED),
                       ("weight 2.4525 x 0.03 = 0.0736 N m", "black"), ("the push wins: the cup tips", RED),
                       ("before it can slide", RED)], target=False))
    holds.append(3)
fallen = affinity.rotate(m.cup_at(A), 90, origin=pivot)
figs.append(frame("2. the cup falls over", fallen, hand,
                  [("pushed above 7.5 cm,", "black"), ("the cup tips over", RED), ("", "black"),
                   ("highest push that slides:", "black"), ("0.06 / (2 x 0.4) = 0.075 m", "black")], target=False))
holds.append(10)
# part 3: fast push low: the hand stops at C, the cup coasts on 3.2 cm
p = 0.04
for xc, t in [(A, "contact"), (0.15, "pushing at 0.5 m/s"), (C, "the hand stops at C")]:
    figs.append(frame(f"3. fast push, 0.5 m/s: {t}", m.cup_at(xc), (xc + W / 2, m.TOP + p),
                      [("push 4 cm above the table", "black"), ("at 0.5 m/s", "black")]))
    holds.append(3)
end = C - coast(0.5)
for xc in np.linspace(C, end, 4)[1:]:
    figs.append(frame("3. fast push: the cup slides on after the hand stops", m.cup_at(xc), (C + W / 2, m.TOP + p),
                      [("push 4 cm above the table", "black"), ("at 0.5 m/s", "black"), ("", "black"),
                       ("hand stopped; the cup slides", "black"), ("on, slowed by friction", "black"),
                       (f"past C by {100 * (C - xc):.1f} cm", RED)]))
    holds.append(2)
holds[-1] = 16
make_gif(figs, here / "push", fps=4, holds=holds, keys=[6, 9, 13, len(figs) - 1], cols=2, width=1000)
