"""One controller cycle in the order the navigation2 code runs it (main), followed through the person's cycle
(t = 2.4 s) of our Python version: each frame lights the next step and fills in its value. Files: nav2_controller
(controller_server.cpp, feasible_path_handler.cpp, simple_goal_checker.cpp, simple_progress_checker.cpp) and
nav2_dwb_controller/dwb_core (dwb_local_planner.cpp). Run -> codepath_anim.gif, codepath_anim_frames.png"""
import math

import dwbkit as d
import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, ORANGE, make_gif

R = d.results()
C = R["replan"]["cycles"]
o = [c for c in C if abs(c["t"] - d.T_PERSON) < 1e-9][0]
rec = o["rec"]
loc = o["local"]
assert len(loc) == 30 and round(d.path_length(loc), 2) == 1.43
assert len(rec["pairs"]) == 375 and rec["n_legal"] == 242 and round(rec["total"], 1) == 26.0
x = o["x"]
STEPS = [
    ("controller server loop", "controller_server.cpp: computeControl", "every 0.05 s (20 Hz); now t = 2.4 s"),
    ("wait for the costmap", "waitForCostmap", "local costmap updated at 2.4 s (5 Hz): the person is in it"),
    ("new plan?", "updateGlobalPath", "none this cycle; the last plan came at 2.0 s"),
    ("robot pose", "getCurrentRobotPose", f"({x[0]:.3f}, {x[1]:.3f}) m, heading {math.degrees(x[2]):.1f}°"),
    ("cut the plan", "FeasiblePathHandler: findPlanSegment, transformLocalPlan",
     "from the closest pose, up to 2.0 m, inside the costmap: 30 poses, 1.43 m"),
    ("goal reached?", "SimpleGoalChecker::isGoalReached", "plan left 1.43 m > 1.0 m: no"),
    ("progress made?", "SimpleProgressChecker::check", "moved 0.5 m within 10 s: yes"),
    ("prepare the critics", "DWBLocalPlanner: critic->prepare", "distance grids from the plan; the goal's latches"),
    ("sample the window", "coreScoringAlgorithm: startNewIteration", f"from {o['v']:.3f} m/s, {o['w']:.3f} rad/s: 375 pairs"),
    ("roll out and score", "generateTrajectory, scoreTrajectory", "133 illegal (hit a band), 242 scored"),
    ("keep the lowest", "best.total; critic->debrief",
     f"({rec['cmd'][0]:.3f} m/s, {rec['cmd'][1]:.3f} rad/s), total {rec['total']:.1f}"),
    ("send the command", "publishVelocity: cmd_vel", "the robot base brakes towards 0.158 m/s"),
]
N = len(STEPS)
H = 1.0


def frame(k):
    fig = go.Figure()
    for i, (name, fn, val) in enumerate(STEPS):
        y0 = (N - 1 - i) * 1.15
        on, done = i == k, i < k
        fill = "rgba(245,133,24,0.22)" if on else ("rgba(76,120,168,0.10)" if done else "rgba(0,0,0,0)")
        line = ORANGE if on else (BLUE if done else "#BBBBBB")
        fig.add_shape(type="rect", x0=0, x1=10, y0=y0, y1=y0 + H, line=dict(color=line, width=3 if on else 1.5),
                      fillcolor=fill)
        fig.add_annotation(x=0.15, y=y0 + 0.72, text=f"<b>{i + 1}. {name}</b>", showarrow=False, xanchor="left",
                           font=dict(size=19, color="black" if (on or done) else GREY))
        fig.add_annotation(x=9.85, y=y0 + 0.72, text=fn, showarrow=False, xanchor="right",
                           font=dict(size=14, color=GREY, family="Latin Modern Mono, monospace"))
        if on or done:
            fig.add_annotation(x=0.15, y=y0 + 0.27, text=val, showarrow=False, xanchor="left",
                               font=dict(size=17, color=ORANGE if on else BLUE))
        if i < N - 1:
            fig.add_annotation(x=5, y=y0 - 0.15, ax=5, ay=y0 - 0.02, xref="x", yref="y", axref="x", ayref="y",
                               text="", showarrow=True, arrowhead=2, arrowwidth=1.5, arrowcolor="#999999")
    fig.add_annotation(x=5, y=N * 1.15 + 0.05, text="<b>one cycle, t = 2.4 s, in the order the code runs</b>",
                       showarrow=False, font=dict(size=20))
    fig.update_xaxes(range=[-0.1, 10.1], visible=False)
    fig.update_yaxes(range=[-0.3, N * 1.15 + 0.4], visible=False)
    fig.update_layout(template="simple_white", font=FONT, width=820, height=1400, showlegend=False,
                      margin=dict(l=10, r=10, t=10, b=10))
    return fig


figs = [frame(k) for k in range(N)] + [frame(N)]
make_gif(figs, "codepath_anim", fps=1, holds=[3] + [2] * (N - 1) + [8], keys=[4, 9, N], cols=3)
