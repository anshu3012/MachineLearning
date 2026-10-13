"""Animation: lifecycle nodes started and stopped by Nav2's lifecycle manager. Left: the state machine of one managed
node, the controller server, its current state lit: Unconfigured, Inactive, Active, Finalized, joined by the
transitions configure, cleanup, activate, deactivate and shutdown. Right: the 17 nodes the default bring-up manages,
in its order (localization first: map_server, amcl; then the keepout-zone and speed-zone filter servers, both switched
on by default in bringup_launch.py; then the 11 navigation servers). Start-up configures every node in
order, then activates every node in order; shut-down deactivates, cleans up and shuts down in reverse order.
Run -> lifecycle.gif, lifecycle_frames.png"""
from pathlib import Path

import netdraw as nd
from gifkit import BLUE, GREEN, GREY, ORANGE, RED, make_gif

here = Path(__file__).parent
ZONES = ["keepout_filter_mask_server", "keepout_costmap_filter_info_server", "speed_filter_mask_server",
         "speed_costmap_filter_info_server"]
NODES = ["map_server", "amcl"] + ZONES + ["controller_server", "smoother_server", "planner_server", "route_server",
         "behavior_server", "velocity_smoother", "collision_monitor", "bt_navigator", "waypoint_follower",
         "docking_server", "following_server"]
assert len(NODES) == 17
POS = {"Unconfigured": (0.10, 0.70), "Inactive": (0.32, 0.70), "Active": (0.54, 0.70), "Finalized": (0.32, 0.36)}
COL = {"Unconfigured": GREY, "Inactive": ORANGE, "Active": GREEN, "Finalized": RED}
DOES = {"Unconfigured": "just created: no parameters read, nothing set up",
        "Inactive": "parameters read, publishers made; processes nothing",
        "Active": "publishes /cmd_vel 20 times a second",
        "Finalized": "about to be destroyed"}
TRANS = [("configure", "Unconfigured", "Inactive", 0.725), ("cleanup", "Inactive", "Unconfigured", 0.675),
         ("activate", "Inactive", "Active", 0.725), ("deactivate", "Active", "Inactive", 0.675)]


def frame(states, head, focus_trans=None):
    fig = nd.blank()
    cur = states["controller_server"]
    box_state = cur if cur in POS else "Unconfigured"          # "configuring" is a transition state between boxes
    for name, p in POS.items():
        nd.box(fig, *p, name, COL[name], lit=box_state == name, w=0.17, h=0.085, size=20)
    for lab, a, b, y in TRANS:
        xa = POS[a][0] + (0.085 if POS[b][0] > POS[a][0] else -0.085)
        xb = POS[b][0] + (-0.085 if POS[b][0] > POS[a][0] else 0.085)
        on = focus_trans == lab
        nd.arrow(fig, (xa, y), (xb, y), BLUE if on else "#AAAAAA", width=5 if on else 2)
        nd.text(fig, (xa + xb) / 2, y + (0.012 if y > 0.7 else -0.012), lab, size=18, color=BLUE if on else GREY,
                anchor="center", valign="bottom" if y > 0.7 else "top")
    for a in ("Unconfigured", "Inactive", "Active"):
        on = focus_trans == "shutdown" and a == "Unconfigured"     # Nav2 cleans up first, then shuts down
        p0 = (POS[a][0], POS[a][1] - 0.043)
        nd.arrow(fig, p0, (POS["Finalized"][0] + (POS[a][0] - POS["Finalized"][0]) * 0.3, 0.405),
                 BLUE if on else "#AAAAAA", width=5 if on else 2)
    nd.text(fig, 0.255, 0.53, "shutdown", size=18, color=BLUE if focus_trans == "shutdown" else GREY, anchor="center")
    nd.text(fig, 0.02, 0.97, head, size=21)
    does = DOES.get(cur, "running its configure step: reading parameters, making publishers")
    nd.text(fig, 0.02, 0.22, f"<b>controller_server now:</b> {cur}<br>{does}", size=20)
    nd.text(fig, 0.66, 0.92, "<b>the lifecycle manager's list</b>", size=19)
    for i, n in enumerate(NODES):
        s = states[n]
        y = 0.86 - i * 0.046
        nd.text(fig, 0.655, y, f"{i + 1}. {n}", size=16, color="black" if n != "controller_server" else BLUE)
        nd.text(fig, 0.99, y, s, size=16, color=COL[s.split()[-1]] if s.split()[-1] in COL else BLUE, anchor="right")
    return fig


st = {n: "Unconfigured" for n in NODES}
figs = [frame(dict(st), "<b>start</b><br>every node is created Unconfigured")]
STEPS = [["map_server"], ["amcl"], ZONES, ["controller_server"]]       # the four zone servers shown as one step
K = NODES.index("controller_server") + 1
for grp in STEPS:
    s2 = dict(st)
    for n in grp:
        s2[n] = "configuring"
    what = grp[0] if len(grp) == 1 else "the four zone-filter servers"
    figs.append(frame(s2, f"<b>start-up: configure, in order</b><br>configuring {what}",
                      "configure" if grp == ["controller_server"] else None))
    for n in grp:
        st[n] = "Inactive"
for n in NODES[K:]:
    st[n] = "Inactive"
figs.append(frame(dict(st), "<b>start-up: configure, in order</b><br>all 17 configured: Inactive", "configure"))
for grp in STEPS:
    for n in grp:
        st[n] = "Active"
    what = grp[0] if len(grp) == 1 else "the four zone-filter servers"
    figs.append(frame(dict(st), f"<b>start-up: then activate, in order</b><br>{what} active",
                      "activate" if grp == ["controller_server"] else None))
for n in NODES[K:]:
    st[n] = "Active"
figs.append(frame(dict(st), "<b>start-up done</b><br>all 17 active: the robot can navigate", "activate"))
for n in NODES:
    st[n] = "Inactive"
figs.append(frame(dict(st), "<b>shut-down, last node first</b><br>deactivate all 17", "deactivate"))
for n in NODES:
    st[n] = "Unconfigured"
figs.append(frame(dict(st), "<b>shut-down, last node first</b><br>clean up all 17", "cleanup"))
for n in NODES:
    st[n] = "Finalized"
figs.append(frame(dict(st), "<b>shut-down, last node first</b><br>shut down all 17", "shutdown"))
holds = [5] + [3] * (len(figs) - 2) + [10]
make_gif(figs, here / "lifecycle", fps=2, holds=holds, keys=[0, 4, 5, 9, 10, len(figs) - 1], cols=2, width=900)
