"""Animation: a route planned for the arm alone, as if the cup did not exist, from holding the cup at A (joint
angles 34.0, -144.1 degrees) to placing it at B (23.2, -67.0 degrees): the PRM of RO-052 in the arm's C-space,
150 milestones, 10 nearest, seed 0, 109.3 degrees long. The arm touches nothing along it, but the cup it carries
sinks up to 1.7 cm into the table (14.3 percent of the way) and passes through the bottle (32.2 percent of the way),
drawn red. Run -> naive.gif, naive_frames.png"""
from pathlib import Path

import numpy as np
import shapely

import armdraw as ad
import manip as m
from gifkit import BLUE, GREEN, RED, make_gif

here = Path(__file__).parent
GA = [s for s in m.ik(m.lid(m.A_X)) if not m.collide(*s, "transit A")[0]][0]
GB = [s for s in m.ik(m.lid(m.B_X)) if not m.collide(*s, "transit B")[0]][0]
assert np.allclose(np.round(GA, 1), (34.0, -144.1)) and np.allclose(np.round(GB, 1), (23.2, -67.0))
route, L, _, _ = m.prm_plan("arm", GA, GB, n=150, k=10, seed=0)
assert round(L, 1) == 109.3
P = np.array(m.densify(route, 0.05))             # configurations 0.05 degrees apart: shares are shares of length
(ex, ey), (hx, hy) = m.fk(P[:, 0], P[:, 1])
cups = shapely.box(hx - m.CUP_W / 2, hy - m.CUP_H, hx + m.CUP_W / 2, hy)
in_table = shapely.intersects(m.floor().buffer(-m.TOUCH), cups)
in_bottle = shapely.intersects(m.bottle(), cups)
depth = m.TOP - (hy - m.CUP_H)
arm_ok = ~m.collide(P[:, 0], P[:, 1], "arm")
assert arm_ok.all() and round(depth.max(), 3) == 0.017, depth.max()
assert round(in_bottle.mean(), 3) == 0.322 and round(in_table.mean(), 3) == 0.143, (in_bottle.mean(), in_table.mean())
FR = sorted(set(np.linspace(0, len(P) - 1, 21).round().astype(int)) | {int(np.argmax(depth))})
KD, KB = FR.index(int(np.argmax(depth))), int(np.argmin([abs(k - np.flatnonzero(in_bottle).mean()) for k in FR]))


def frame(i, last=False):
    fig = ad.go.Figure()
    ad.scene(fig)
    k = FR[i]
    bot = hy[:k + 1] - m.CUP_H
    fig.add_trace(ad.go.Scatter(x=hx[:k + 1], y=bot, mode="lines", line=dict(color=RED, width=2, dash="dot"),
                                hoverinfo="skip"))
    ad.arm(fig, P[k], cup=True, bad=bool(in_table[k] or in_bottle[k]))
    t = k / (len(P) - 1)
    lines = [("a route planned for the arm", "black"), ("alone, as if there were no cup,", "black"),
             ("from the grasp at A to B", "black"), ("", "black"), (f"done: {100 * t:.0f} percent", "black"),
             (f"joint 1: {P[k][0]:.1f} degrees", BLUE), (f"joint 2: {P[k][1]:.1f} degrees", "#C46A10"), ("", "black"),
             ("the arm touches nothing", GREEN),
             (f"cup in the table: {100 * max(depth[k], 0):.1f} cm" if in_table[k] else "cup clear of the table",
              RED if in_table[k] else GREEN),
             ("cup inside the bottle" if in_bottle[k] else "cup clear of the bottle", RED if in_bottle[k] else GREEN)]
    if last:
        lines += [("", "black"), ("deepest: 1.7 cm into the table", RED), ("in the bottle: 32.2 percent of the way", RED)]
    for j, (s, c) in enumerate(lines):
        fig.add_annotation(x=0.66, y=0.97 - 0.068 * j, xref="paper", yref="paper", xanchor="left", yanchor="top",
                           text=s, showarrow=False, font=dict(size=19, color=c))
    ad.scene_axes(fig)
    fig.update_xaxes(domain=[0, 0.62])
    fig.update_yaxes(scaleanchor="x")
    ad.layout(fig, 1300, 700, "Carrying the cup along a route planned for the arm alone" if not last else
              "The cup sinks into the table and passes through the bottle", margin=dict(l=80, r=20, t=80, b=60))
    return fig


figs = [frame(i) for i in range(len(FR))] + [frame(len(FR) - 1, last=True)]
holds = [4] + [2] * (len(FR) - 1) + [16]
make_gif(figs, here / "naive", fps=4, holds=holds, keys=[0, KD, KB, len(figs) - 1], cols=2, width=1000)
