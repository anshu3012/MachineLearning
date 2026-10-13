"""Animation: recording a bag on the robot, then playing it back at a desk. Recording: ros2 bag record subscribes to
/scan, /odom and /cmd_vel and writes each message with its time into the bag file (shown from 2.30 to 2.50 s; the
2.40 s scan holds the person, 0.72 m ahead). Playing: ros2 bag play publishes the stored messages on the same topics
at the same times, where RViz and a local planner under test subscribe, so the person steps in at 2.4 s on every
replay. Run -> bag_anim.gif, bag_anim_frames.png"""
from pathlib import Path

import netdraw as nd
import numpy as np
import roskit as rk
from gifkit import BLUE, GREEN, GREY, ORANGE, PURPLE, make_gif

here = Path(__file__).parent
TOP = {"/scan": (0.10, 0.80, ORANGE), "/odom": (0.10, 0.66, GREEN), "/cmd_vel": (0.10, 0.52, BLUE)}


def nearest(t):
    s = rk.scan(t)
    b = np.degrees(s["bearings"])
    return float(np.min(np.where(np.abs(b) < 30, s["ranges"], 99)))


assert round(nearest(2.4), 2) == 0.72


def line(t, topic):
    if topic == "/scan":
        return f"{t:.2f} s /scan: nearest ahead {nearest(t):.2f} m"
    v, w = rk.cmd(t)
    if topic == "/odom":
        return f"{t:.2f} s /odom: speed {v:.3f} m/s"
    return f"{t:.2f} s /cmd_vel: {v:.3f} m/s, {w:.3f} rad/s"


def pubs(t):
    return ["/scan", "/odom", "/cmd_vel"] if abs(t * 10 - round(t * 10)) < 1e-6 else ["/odom", "/cmd_vel"]


def frame(phase, t, stored, sending):
    fig = nd.blank()
    rec = phase == "record"
    for name, (x, y, c) in TOP.items():
        nd.box(fig, x if rec else 0.52, y, name, c, lit=name in sending, w=0.13, h=0.08, size=21)
    if rec:
        nd.box(fig, 0.36, 0.66, "ros2 bag record", PURPLE, lit=bool(sending), w=0.2, h=0.1, size=20, sub="a subscriber")
        for name in sending:
            x, y, c = TOP[name]
            nd.arrow(fig, (x + 0.065, y), (0.26, 0.66), c, width=4)
        nd.arrow(fig, (0.46, 0.66), (0.56, 0.66), PURPLE if sending else "#BBBBBB", width=4)
    else:
        nd.box(fig, 0.18, 0.66, "ros2 bag play", PURPLE, lit=bool(sending), w=0.2, h=0.1, size=20, sub="a publisher")
        for name in sending:
            nd.arrow(fig, (0.28, 0.66), (0.455, TOP[name][1]), TOP[name][2], width=4)
        nd.box(fig, 0.83, 0.76, "RViz", BLUE, lit="/scan" in sending, w=0.15, h=0.09, size=21)
        nd.box(fig, 0.83, 0.56, "local planner", BLUE, lit="/scan" in sending or "/odom" in sending, w=0.15,
               h=0.09, size=21, sub="under test")
        if "/scan" in sending:
            nd.arrow(fig, (0.585, 0.80), (0.755, 0.76), ORANGE, width=4)
            nd.arrow(fig, (0.585, 0.795), (0.755, 0.575), ORANGE, width=4)
        if "/odom" in sending:
            nd.arrow(fig, (0.585, 0.66), (0.755, 0.55), GREEN, width=4)
    if rec:
        nd.text(fig, 0.58, 0.72, "<b>the bag file</b>", size=20, color=PURPLE)
        nd.text(fig, 0.58, 0.67, "<br>".join(stored[-9:]), size=18)
    else:
        nd.text(fig, 0.02, 0.40, "<b>the bag file</b>", size=20, color=PURPLE)
        nd.text(fig, 0.02, 0.35, "<br>".join(stored[-9:]), size=18)
        nd.arrow(fig, (0.12, 0.42), (0.16, 0.605), PURPLE if sending else "#BBBBBB", width=4)
    head = ("<b>recording, on the robot</b>" if rec else "<b>playing, later, at a desk</b>") + f": t = {t:.2f} s"
    nd.text(fig, 0.02, 0.98, head, size=22)
    if not rec and "/scan" in sending and abs(t - 2.4) < 1e-6:
        nd.text(fig, 0.52, 0.42, "the person steps in at 2.4 s again", size=20, color=ORANGE, anchor="center")
    return fig


figs, keys, stored = [], [], []
for t in (2.30, 2.35, 2.40, 2.45, 2.50):
    stored = stored + [line(t, p) for p in pubs(t)]
    figs.append(frame("record", t, stored, pubs(t)))
keys.append(2)
for t in (2.30, 2.35, 2.40, 2.45, 2.50):
    figs.append(frame("play", t, stored, pubs(t)))
keys += [7, len(figs) - 1]
holds = [4] + [3] * (len(figs) - 2) + [12]
holds[7] = 6
make_gif(figs, here / "bag_anim", fps=2, holds=holds, keys=[2, 4, 7, len(figs) - 1], cols=2, width=900)
