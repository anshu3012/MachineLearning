"""Animation: the room robot's nodes passing messages on topics from 2.30 s to 2.50 s, two frames per moment
(published, then delivered). The lidar driver publishes /scan every 0.1 s to two subscribers, the localizer and the
local planner; the base driver publishes /odom every 0.05 s; the local planner publishes /local_plan every 0.1 s;
the controller publishes /cmd_vel every 0.05 s to the base driver. At 2.40 s the scan shows the person (nearest
reading ahead 0.72 m), the local planner sends a bent plan, and the controller's next command follows. Nobody waits
for anybody: the controller at 2.35 and 2.45 s uses the latest plan it has. Run -> topics.gif, topics_frames.png"""
from pathlib import Path

import netdraw as nd
import numpy as np
import roskit as rk
from gifkit import BLUE, GREEN, GREY, ORANGE, PURPLE, RED, make_gif

here = Path(__file__).parent
NODES = {"lidar driver": (0.12, 0.72), "localizer": (0.47, 0.81), "local planner": (0.47, 0.58),
         "controller": (0.47, 0.26), "base driver": (0.12, 0.26)}
EDGES = {"scan1": ((0.21, 0.735), (0.37, 0.80), "/scan", ORANGE),
         "scan2": ((0.21, 0.705), (0.37, 0.60), "/scan", ORANGE),
         "odom1": ((0.21, 0.30), (0.37, 0.56), "/odom", GREEN),
         "odom2": ((0.21, 0.28), (0.37, 0.28), "/odom", GREEN),
         "plan": ((0.47, 0.535), (0.47, 0.305), "/local_plan", PURPLE),
         "cmd": ((0.37, 0.235), (0.21, 0.235), "/cmd_vel", BLUE)}
PUB = {"scan1": "lidar driver", "scan2": "lidar driver", "odom1": "base driver", "odom2": "base driver",
       "plan": "local planner", "cmd": "controller"}
SUB = {"scan1": "localizer", "scan2": "local planner", "odom1": "local planner", "odom2": "controller",
       "plan": "controller", "cmd": "base driver"}


def nearest(t):
    s = rk.scan(t)
    b = np.degrees(s["bearings"])
    return float(np.min(np.where(np.abs(b) < 30, s["ranges"], 99)))


assert round(nearest(2.4), 2) == 0.72 and len(rk.L[24]["P"]) == 10
v40, w40 = rk.cmd(2.40)
assert (round(v40, 3), round(w40, 3)) == (0.592, 0.079)


def cmd_line(t):
    v, w = rk.cmd(t)
    return f"{t:.2f} s /cmd_vel: {v:.3f} m/s, {w:.3f} rad/s"


def odom_line(t):
    return f"{t:.2f} s /odom: speed {rk.cmd(t)[0]:.3f} m/s"


EVENTS = [
    (2.30, "all six", ["scan1", "scan2", "odom1", "odom2", "plan", "cmd"],
     [f"2.30 s /scan: 682 readings, nearest ahead {nearest(2.3):.2f} m", odom_line(2.30),
      f"2.30 s /local_plan: {len(rk.L[23]['P'])} poses", cmd_line(2.30)]),
    (2.35, "odometry and the command", ["odom1", "odom2", "cmd"], [odom_line(2.35), cmd_line(2.35)]),
    (2.40, "the scan that shows the person", ["scan1", "scan2", "odom1", "odom2"],
     [f"<span style='color:{RED}'>2.40 s /scan: nearest ahead {nearest(2.4):.2f} m: the person</span>",
      odom_line(2.40)]),
    (2.40, "the bent plan", ["plan"], ["2.40 s /local_plan: 10 poses, bends left"]),
    (2.40, "the command from the bent plan", ["cmd"], [cmd_line(2.40)]),
    (2.45, "odometry and the command", ["odom1", "odom2", "cmd"], [odom_line(2.45), cmd_line(2.45)]),
    (2.50, "all six", ["scan1", "scan2", "odom1", "odom2", "plan", "cmd"],
     [f"2.50 s /scan: nearest ahead {nearest(2.5):.2f} m", odom_line(2.50),
      f"2.50 s /local_plan: {len(rk.L[25]['P'])} poses", cmd_line(2.50)]),
]


def frame(t, what, edges, phase, log):
    fig = nd.blank()
    lit = {PUB[e] for e in edges} if phase == 0 else {SUB[e] for e in edges}
    for name, p in NODES.items():
        nd.box(fig, *p, name, BLUE, lit=name in lit, size=22)
    for key, (p0, p1, topic, col) in EDGES.items():
        on = key in edges
        nd.arrow(fig, p0, p1, col if on else "#BBBBBB", width=5 if on else 2)
    labels = {"/scan": (0.27, 0.80), "/odom": (0.27, 0.45), "/local_plan": (0.485, 0.42), "/cmd_vel": (0.29, 0.205)}
    for topic, p in labels.items():
        col = {"/scan": ORANGE, "/odom": GREEN, "/local_plan": PURPLE, "/cmd_vel": BLUE}[topic]
        nd.text(fig, p[0], p[1], f"<b>{topic}</b>", size=21, color=col, anchor="left", valign="middle")
    for key in edges:
        p0, p1, topic, col = EDGES[key]
        nd.dot(fig, nd.lerp(p0, p1, 0.5 if phase == 0 else 0.92), col)
    head = f"<b>t = {t:.2f} s</b><br>" + (f"published: {what}" if phase == 0 else f"delivered to every subscriber: {what}")
    nd.text(fig, 0.02, 0.99, head, size=22)
    nd.text(fig, 0.02, 0.06, "no node waits: each node uses the newest message it has", size=18, color=GREY)
    nd.text(fig, 0.6, 0.97, "<b>the last messages</b> (newest at the bottom)", size=20)
    nd.text(fig, 0.6, 0.91, "<br>".join(log[-10:]), size=19)
    return fig


figs, keys, log = [], [], []
for t, what, edges, lines in EVENTS:
    figs.append(frame(t, what, edges, 0, log))
    log = log + lines
    figs.append(frame(t, what, edges, 1, log))
    if t == 2.40:
        keys.append(len(figs) - 1)
holds = [6] + [3] * (len(figs) - 2) + [14]
make_gif(figs, here / "topics", fps=3, holds=holds, keys=[1, keys[0], keys[2], len(figs) - 1], cols=2, width=900)
