"""Animation: the collision monitor's approach zone at 2.55 s of the main run (our Python version of
nav2_collision_monitor with the bring-up's FootprintApproach; not Nav2 running). Robot frame, x forward. Dots: the
scan's returns. The robot's footprint (16 points on a circle of 0.25 m) is moved forward with the smoothed command,
(0.4684 m/s, 0.2632 rad/s), in steps of 0.1 s; at the step whose footprint holds 6 or more returns, the loop time is
1.1 s, so the command is scaled by 1.1 / 1.2 = 0.917 to (0.4294 m/s, 0.2412 rad/s).
Run -> monitor.gif, monitor_frames.png"""
import math
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

import nav2sim as N
from gifkit import BLUE, FONT, GREY, RED, make_gif

here = Path(__file__).parent
R = N.results()
L = R["main"]["log"]
x = [y for y in L if y["zone"]][0]
assert round(x["t"], 2) == 2.55 and round(x["tc"], 1) == 1.1
pts = x["scan_base"]
steps = x["csteps"]
cmd, out = x["cmd_smooth"], x["cmd_out"]
assert np.allclose(np.round(cmd, 4), (0.4684, 0.2632)) and np.allclose(np.round(out, 4), (0.4294, 0.2412))
poly = N.MONITOR_BRINGUP[0]["poly"]


def inside(pose):
    c, s = math.cos(pose[2]), math.sin(pose[2])
    dx, dy = pts[:, 0] - pose[0], pts[:, 1] - pose[1]
    return N.points_inside(poly, np.column_stack([dx * c + dy * s, -dx * s + dy * c]))


counts = [inside(p) for p in steps]
assert counts[-1] >= 6 and all(c < 6 for c in counts[:-1]) and len(steps) == 12


def foot(fig, pose, color, width=2, dash=None):
    c, s = math.cos(pose[2]), math.sin(pose[2])
    P = np.vstack([poly, poly[:1]])
    X = pose[0] + c * P[:, 0] - s * P[:, 1]
    Y = pose[1] + s * P[:, 0] + c * P[:, 1]
    fig.add_trace(go.Scatter(x=X, y=Y, mode="lines", line=dict(color=color, width=width, dash=dash), hoverinfo="skip"))


def frame(k, title, note=""):
    fig = go.Figure()
    near = pts[(np.abs(pts[:, 0]) < 2.2) & (np.abs(pts[:, 1]) < 1.6)]
    fig.add_trace(go.Scatter(x=near[:, 0], y=near[:, 1], mode="markers", marker=dict(size=6, color="black"),
                             hoverinfo="skip"))
    foot(fig, (0.0, 0.0, 0.0), BLUE, 3)
    fig.add_trace(go.Scatter(x=[0, 0.25], y=[0, 0], mode="lines", line=dict(color=BLUE, width=3), hoverinfo="skip"))
    for j in range(k):
        last = j == len(steps) - 1
        foot(fig, steps[j], RED if last else GREY, 3 if last else 1.5, None if last else "dot")
    fig.add_annotation(x=0.02, y=0.02, xref="paper", yref="paper", xanchor="left", yanchor="bottom", align="left",
                       text=note, showarrow=False, font=dict(size=19), bgcolor="rgba(255,255,255,0.85)")
    fig.update_xaxes(range=[-0.6, 2.0], title="x, forward (m)", dtick=0.5)
    fig.update_yaxes(range=[-1.0, 1.4], title="y, left (m)", dtick=0.5, scaleanchor="x")
    fig.update_layout(template="simple_white", width=900, height=840, font=FONT, showlegend=False,
                      margin=dict(l=80, r=20, t=80, b=70), title=dict(text=title, x=0.5, y=0.97, font=dict(size=20)))
    return fig


figs, holds = [frame(0, "2.55 s, robot frame: the scan's returns (dots) and the footprint (blue)",
                     "command in: 0.4684 m/s, 0.2632 rad/s")], [6]
for k in range(1, len(steps) + 1):
    t_loop = round(0.1 * (k - 1), 1)
    hit = counts[k - 1] >= 6
    title = (f"step {k}: loop time {t_loop:.1f} s, {counts[k - 1]} returns inside"
             + (": collision" if hit else ""))
    figs.append(frame(k, title, "footprint moved 0.1 s at a time<br>with the command in"))
    holds.append(2)
figs.append(frame(len(steps), "time to collision 1.1 s: the command is scaled by 1.1 / 1.2 = 0.917",
                  "command out: 0.4294 m/s, 0.2412 rad/s"))
holds.append(18)
make_gif(figs, here / "monitor", fps=3, holds=holds, keys=[0, 6, len(figs) - 2, len(figs) - 1], cols=2, width=760)
