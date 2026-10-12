"""Animation: the cup moved from A to B as transit, transfer, transit. Left: the arm (side view). Right: the arm's
C-space of the current mode, coloured by what a blocked configuration hits (as in modes.png), with the path so far.
Each leg is planned by the PRM of RO-052 in that mode's free space (150 milestones, 10 nearest, seed 0): transit
from home (90, 0) to the grasp (34.0, -144.1), 169.0 degrees; transfer to the placing (23.2, -67.0), 123.2 degrees;
transit back home, 99.2 degrees. At the grasp and at the placing the mode switches and the C-space changes.
Run -> pickplace.gif, pickplace_frames.png"""
from pathlib import Path

import numpy as np
from plotly.subplots import make_subplots

import armdraw as ad
import manip as m
from gifkit import BLUE, GREEN, RED, make_gif

here = Path(__file__).parent
GA = [s for s in m.ik(m.lid(m.A_X)) if not m.collide(*s, "transit A")[0]][0]
GB = [s for s in m.ik(m.lid(m.B_X)) if not m.collide(*s, "transit B")[0]][0]
LEGS = [("transit A", m.HOME, GA, 169.0), ("transfer", GA, GB, 123.2), ("transit B", GB, m.HOME, 99.2)]
PATHS = []
for mode, s, g, length in LEGS:
    P, L, _, _ = m.prm_plan(mode, s, g, n=150, k=10, seed=0)
    assert round(L, 1) == length, (mode, L)
    D = np.array(m.densify(P, 0.5))
    assert not m.collide(D[:, 0], D[:, 1], mode).any()
    PATHS.append((P, D))
NAME = {"transit A": "transit: the cup stands at A", "transfer": "transfer: the cup is held",
        "transit B": "transit: the cup stands at B"}


def frame(leg, k, title, done=False):
    mode = LEGS[leg][0]
    P, D = PATHS[leg]
    q = D[k]
    fig = make_subplots(rows=1, cols=2, column_widths=[0.55, 0.45], horizontal_spacing=0.1,
                        subplot_titles=["the arm", "its C-space: " + NAME[mode]])
    cup_x = m.A_X if mode == "transit A" else (m.B_X if mode == "transit B" else None)
    ad.scene(fig, cup_x=cup_x, spot_b=mode != "transit B", row=1, col=1)
    ad.arm(fig, q, cup=mode == "transfer", row=1, col=1)
    ad.cspace(fig, mode, row=1, col=2)
    for j in range(leg):
        ad.cs_path(fig, PATHS[j][1], "rgba(107,107,107,0.6)", 3, row=1, col=2)
    ad.cs_path(fig, D[:k + 1], [BLUE, "#C46A10", GREEN][leg], 5, row=1, col=2)
    for p, c, t, pos in ((m.HOME, "black", "home", "top center"), (GA, BLUE, "grasp", "bottom center"),
                         (GB, RED, "place", "top center")):
        ad.point(fig, p, c, t, pos, size=11, row=1, col=2)
    ad.point(fig, q, "white", size=15, row=1, col=2)
    ad.scene_axes(fig, row=1, col=1)
    fig.update_yaxes(scaleanchor="x", row=1, col=1)
    ad.cs_axes(fig, row=1, col=2)
    fig.update_yaxes(scaleanchor="x2", row=1, col=2)
    for a in fig.layout.annotations:
        a.font = dict(size=19)
    ad.layout(fig, 1450, 640, title, margin=dict(l=80, r=30, t=110, b=70))
    return fig


figs, holds = [], []
STEPS = 10
for leg, (mode, s, g, length) in enumerate(LEGS):
    P, D = PATHS[leg]
    idx = np.linspace(0, len(D) - 1, STEPS + 1).round().astype(int)
    for n, k in enumerate(idx):
        if leg == 0:
            t = f"1. transit from home to the grasp: {length} degrees of joint motion"
        elif leg == 1:
            t = f"2. transfer: the cup moves with the hand, over the bottle, {length} degrees"
        else:
            t = f"3. transit back home: {length} degrees"
        figs.append(frame(leg, k, t))
        holds.append(4 if n == 0 else 1)
    if leg == 0:
        figs.append(frame(0, len(D) - 1, "grasp: a configuration free in both modes; the cup is held, the mode switches"))
        holds.append(10)
    if leg == 1:
        figs.append(frame(1, len(D) - 1, "place: the cup rests at B and is let go; the mode switches back"))
        holds.append(10)
holds[-1] = 16
make_gif(figs, here / "pickplace", fps=4, holds=holds, keys=[6, 11, 18, len(figs) - 1], cols=2, width=1000)
