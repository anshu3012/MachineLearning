"""Animation: one NavigateToPose goal through Nav2's servers, one message lit per frame, with the numbers of the main
run (our Python version of Nav2's servers, written from their code and the bring-up parameters; not Nav2 running).
Boxes are the bring-up's nodes; arrows are actions (goal, ComputePathToPose, FollowPath), topics (/scan, /map,
cmd_vel_nav, cmd_vel_smoothed, cmd_vel, /odom), a service (IsPathValid) and the map -> odom transform.
Run -> goal_flow.gif, goal_flow_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

import nav2sim as N
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, RED, make_gif

here = Path(__file__).parent
R = N.results()
m = R["main"]
L = m["log"]
c1 = [x for x in L if abs(x["t"] - 1.0) < 1e-6][0]
mon = [x for x in L if x["zone"]][0]
ev = m["events"]
P0, P1 = m["plans"][0][1], m["plans"][1][1]
assert np.allclose(np.round(c1["cmd_nav"], 4), (0.5684, 0.2632)) and round(c1["cmd_smooth"][0], 3) == 0.525
assert round(mon["t"], 2) == 2.55 and round(mon["tc"], 1) == 1.1
assert ev[3]["blocked_index"] == 68 and round(N.D.path_length(P1), 3) == 2.986 and len(P0) == 130
assert round(L[-1]["t"], 2) == 11.50 and round(m["t_final"], 2) == 11.51

BOX = {"client": (1.2, 7.0, "client (RViz)"), "bt": (5.0, 7.0, "bt_navigator"),
       "planner": (8.8, 7.0, "planner_server<br>+ global costmap"), "lifecycle": (1.2, 5.0, "lifecycle_manager"),
       "controller": (5.0, 5.0, "controller_server<br>+ local costmap"), "behavior": (8.8, 5.0, "behavior_server"),
       "smoother": (5.0, 3.0, "velocity_smoother"), "map": (8.8, 3.0, "map_server"),
       "monitor": (5.0, 1.0, "collision_monitor"), "amcl": (8.8, 1.0, "amcl"), "base": (1.2, 1.0, "robot base"),
       "laser": (1.2, 3.0, "laser")}
HW, HH = 0.95, 0.5


def edge(a, b):
    """Arrow from box a to box b, starting and ending on the boxes' borders."""
    (xa, ya, _), (xb, yb, _) = BOX[a], BOX[b]
    d = np.array([xb - xa, yb - ya], float)
    def border(t):
        sx = HW / abs(t[0]) if t[0] else np.inf
        sy = HH / abs(t[1]) if t[1] else np.inf
        return min(sx, sy)
    u = d / np.linalg.norm(d)
    s0, s1 = border(u), border(-u)
    return (xa + u[0] * s0, ya + u[1] * s0), (xb - u[0] * s1, yb - u[1] * s1)


def frame(title, lit_edges=(), lit_boxes=(), note="", active=None, note_color="black"):
    fig = go.Figure()
    for k, (x, y, label) in BOX.items():
        on = k in lit_boxes
        state = active.get(k) if active else None
        fill = "#FAD4D4" if on else {"active": "#DDEFD8", "inactive": "#FCE3C4"}.get(state, "white")
        fig.add_shape(type="rect", x0=x - HW, x1=x + HW, y0=y - HH, y1=y + HH, line=dict(
            color=RED if on else GREY, width=5 if on else 2), fillcolor=fill, layer="below", opacity=1)
        fig.add_annotation(x=x, y=y, text=label, showarrow=False, font=dict(size=21 if "<br>" in label else 23))
    for a, b, lab in lit_edges:
        (x0, y0), (x1, y1) = edge(a, b)
        fig.add_annotation(x=x1, y=y1, ax=x0, ay=y0, xref="x", yref="y", axref="x", ayref="y", text="",
                           showarrow=True, arrowhead=2, arrowwidth=4.5, arrowcolor=RED)
        if lab:
            mx, my = (x0 + x1) / 2, (y0 + y1) / 2
            if abs(y1 - y0) < 1e-6:                      # horizontal: in the band above the row
                kw = dict(x=mx, y=my + 0.78)
            elif abs(x1 - x0) < 1e-6:                    # vertical: beside the arrow, on the side with room
                kw = dict(x=mx + 0.12, y=my, xanchor="left") if mx < 7 else dict(x=mx - 0.12, y=my, xanchor="right")
            else:
                kw = dict(x=mx, y=my)
            fig.add_annotation(text=lab, showarrow=False, font=dict(size=21, color=RED),
                               bgcolor="rgba(255,255,255,0.92)", **kw)
    fig.add_annotation(x=5.0, y=8.1, text=note, showarrow=False, font=dict(size=22, color=note_color))
    fig.update_xaxes(range=[0, 10], visible=False)
    fig.update_yaxes(range=[0.3, 8.5], visible=False, scaleanchor="x", scaleratio=1)
    fig.update_layout(template="simple_white", width=1200, height=1030, font=FONT, showlegend=False,
                      margin=dict(l=10, r=10, t=70, b=10), title=dict(text=title, x=0.5, y=0.985, font=dict(size=24)))
    return fig


ALL = {k: "active" for k in BOX if k not in ("client", "base", "laser", "lifecycle")}
F = [
    frame("Nav2 in the bring-up, as our Python version runs it", note="one goal, followed message by message"),
    frame("bring-up: the lifecycle manager configures 17 nodes in order, then activates them",
          lit_boxes=("lifecycle",), active=ALL, note="every server is active before the first goal"),
    frame("sensors: the laser's /scan and the map_server's /map",
          lit_edges=[("laser", "amcl", ""), ("laser", "controller", "/scan: 241 beams, 10 a second"),
                     ("laser", "monitor", ""), ("map", "amcl", "/map: 160 x 100 cells")],
          lit_boxes=("laser", "map"), active=ALL, note="/scan also reaches the global costmap in planner_server"),
    frame("localisation: amcl publishes the map -> odom transform; the base publishes /odom",
          lit_edges=[("amcl", "controller", "map -> odom"), ("base", "controller", "/odom")],
          lit_boxes=("amcl", "base"), active=ALL, note="every server can now look up where the robot is on the map"),
    frame("0.00 s: the goal arrives as a NavigateToPose action",
          lit_edges=[("client", "bt", "goal (3.6, 3.5), 90 degrees")], lit_boxes=("bt",), active=ALL,
          note="bt_navigator starts ticking its behaviour tree every 10 ms"),
    frame("0.00 s: the tree asks for a path", lit_edges=[("bt", "planner", "ComputePathToPose")],
          lit_boxes=("planner",), active=ALL, note="NavFn on the global costmap"),
    frame("0.00 s: the path comes back", lit_edges=[("planner", "bt", "path: 3.26 m, 130 poses")],
          lit_boxes=("bt",), active=ALL),
    frame("0.00 s: the tree hands the path to the controller", lit_edges=[("bt", "controller", "FollowPath")],
          lit_boxes=("controller",), active=ALL, note="controller_server runs DWB 20 times a second"),
    frame("1.00 s: DWB's command", lit_edges=[("controller", "smoother", "cmd_vel_nav: 0.5684 m/s, 0.2632 rad/s")],
          lit_boxes=("smoother",), active=ALL),
    frame("1.00 s: the smoother limits the change", lit_edges=[("smoother", "monitor", "cmd_vel_smoothed: 0.525 m/s")],
          lit_boxes=("monitor",), active=ALL, note="0.5 + 0.025: at most 0.5 m/s^2 for 0.05 s"),
    frame("1.00 s: no collision within 1.2 s, so the command passes", lit_edges=[("monitor", "base", "cmd_vel: 0.525 m/s")],
          lit_boxes=("base",), active=ALL),
    frame("2.55 s: the person 1.1 s ahead: the monitor scales the command",
          lit_edges=[("monitor", "base", "x 0.917: 0.4684 -> 0.4294 m/s")], lit_boxes=("monitor", "base"),
          active=ALL, note="1.1 / 1.2 = 0.917", note_color=RED),
    frame("3.00 s: the 1 Hz path check fails", lit_edges=[("bt", "planner", "IsPathValid: blocked at pose 68")],
          lit_boxes=("planner",), active=ALL, note="the global costmap now holds the person", note_color=RED),
    frame("3.00 s: a new path", lit_edges=[("planner", "bt", "path: 2.986 m"), ("bt", "controller", "FollowPath: new path")],
          lit_boxes=("bt", "controller"), active=ALL),
    frame("11.50 s: the goal checker accepts", lit_edges=[("controller", "bt", "FollowPath: succeeded")],
          lit_boxes=("bt",), active=ALL, note="within 0.25 m and 0.25 rad of the goal, by AMCL's estimate"),
    frame("11.51 s: the navigator reports success", lit_edges=[("bt", "client", "result: succeeded")],
          lit_boxes=("client",), active=ALL),
]
holds = [5] + [7] * (len(F) - 2) + [16]
make_gif(F, here / "goal_flow", fps=2, holds=holds, keys=[2, 5, 8, 11, 12, 14], cols=2, width=900)
