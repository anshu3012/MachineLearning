"""Nav2's goal checker and progress checker in our runs (btkit.py, with the bring-up values). Top: the end of the
blocked-door run: the robot's distance to the door pose and its heading error; the goal checker first waits for
the distance to drop under 0.25 m, then (stateful) only for the heading to come within 0.25 rad. Bottom: a run in
which a wheel is caught at 2.0 s: the distance from the progress checker's last checkpoint, which moves to the
robot each time the robot is more than 0.5 m from it; 10 s without that, FollowPath fails. Run -> checkers.png"""
from pathlib import Path

import btkit as bt
import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, ORANGE, RED
from plotly.subplots import make_subplots

here = Path(__file__).parent
RES = bt.results()
B = [r for r in RES["blocked"]["records"] if r["t"] >= 13.0]
tb = np.array([r["t"] for r in B])
d = np.array([np.hypot(*(r["robot"][:2] - bt.GOAL[:2])) for r in B])
yaw = np.abs([(bt.GOAL[2] - r["robot"][2] + np.pi) % (2 * np.pi) - np.pi for r in B])
latch = min(r["t"] for r in B if r["checkers"] and r["checkers"]["xy_reached"])
assert latch == 14.6 and round(RES["blocked"]["t"], 2) == 15.6
S = [r for r in RES["stuck"]["records"] if r["checkers"]]
ts = np.array([r["t"] for r in S])
dp = np.array([np.hypot(*(r["robot"][:2] - r["checkers"]["prog_xy"])) for r in S])
fails = [r["t"] for r in RES["stuck"]["records"] if any(l == "FollowPath" and s == bt.FAILURE for l, s, u in r["log"])]
resets = sorted(set(r["checkers"]["prog_t"] for r in S))
assert fails == [11.62, 21.63] and resets == [0.01, 1.57, 11.62, 21.63]

fig = make_subplots(rows=2, cols=1, vertical_spacing=0.2, subplot_titles=(
    "Goal checker: the end of the blocked-door run", "Progress checker: a wheel caught at 2.0 s"))
fig.add_trace(go.Scatter(x=tb, y=d, mode="lines", line=dict(color=BLUE, width=3), name="distance to the door pose (m)"),
              row=1, col=1)
fig.add_trace(go.Scatter(x=tb, y=yaw, mode="lines", line=dict(color=ORANGE, width=3),
                         name="heading error (rad)"), row=1, col=1)
fig.add_hline(y=0.25, line=dict(color=GREY, dash="dash", width=2), opacity=1, row=1, col=1)
fig.add_annotation(x=13.05, y=1.04, text="distance to the door pose (m)", showarrow=False, xanchor="left",
                   yanchor="bottom", font=dict(size=18, color=BLUE), row=1, col=1)
fig.add_annotation(x=14.1, y=0.92, text="heading error (rad)", showarrow=False, xanchor="right",
                   font=dict(size=18, color=ORANGE), row=1, col=1)
fig.add_annotation(x=13.05, y=0.25, text="tolerances: 0.25 m, 0.25 rad", showarrow=False, xanchor="left",
                   yanchor="bottom", font=dict(size=18, color=GREY), row=1, col=1)
for t, txt in ((latch, f"{latch:.2f} s: within 0.25 m"), (15.6, "15.60 s: within 0.25 rad: accepted")):
    fig.add_vline(x=t, line=dict(color=RED, width=2), opacity=1, row=1, col=1)
fig.add_annotation(x=latch, y=1.55, text=f"{latch:.2f} s: within 0.25 m,<br>position kept as reached",
                   showarrow=False, xanchor="right", font=dict(size=17, color=RED), row=1, col=1)
fig.add_annotation(x=15.6, y=1.0, text="15.60 s:<br>heading within<br>0.25 rad:<br>accepted", showarrow=False,
                   xanchor="right", font=dict(size=17, color=RED), row=1, col=1)
fig.add_trace(go.Scatter(x=ts, y=dp, mode="lines", line=dict(color=BLUE, width=3),
                         name="distance from the checkpoint (m)"), row=2, col=1)
fig.add_hline(y=0.5, line=dict(color=GREY, dash="dash", width=2), opacity=1, row=2, col=1)
fig.add_annotation(x=2.4, y=0.16, text="distance from the last checkpoint (m)", showarrow=False, xanchor="left",
                   font=dict(size=18, color=BLUE), row=2, col=1)
fig.add_annotation(x=24.8, y=0.5, text="0.5 m", showarrow=False, xanchor="right", yanchor="bottom",
                   font=dict(size=18, color=GREY), row=2, col=1)
fig.add_vline(x=2.0, line=dict(color=GREY, width=2, dash="dot"), opacity=1, row=2, col=1)
fig.add_annotation(x=2.1, y=0.62, text="wheel caught", showarrow=False, xanchor="left", font=dict(size=17),
                   row=2, col=1)
for t, txt in zip(fails, ("FollowPath fails; local costmap<br>cleared; FollowPath again",
                          "fails again: navigation fails;<br>recovery 1: clear both costmaps")):
    fig.add_vline(x=t, line=dict(color=RED, width=2), opacity=1, row=2, col=1)
    fig.add_annotation(x=t - 0.2, y=0.33, text=f"{t:.2f} s: {txt}", showarrow=False, xanchor="right",
                       align="right", font=dict(size=16, color=RED), row=2, col=1)
fig.update_xaxes(title_text="time (s)", range=[13.0, 15.75], row=1, col=1)
fig.update_xaxes(title_text="time (s)", range=[0, 25], row=2, col=1)
fig.update_yaxes(range=[0, 1.8], title_text="m or rad", row=1, col=1)
fig.update_yaxes(range=[0, 0.7], title_text="m", row=2, col=1)
fig.update_layout(template="simple_white", font=FONT, width=1000, height=900, showlegend=False,
                  margin=dict(l=70, r=20, t=50, b=60))
for title in ("Goal checker: the end of the blocked-door run", "Progress checker: a wheel caught at 2.0 s"):
    fig.update_annotations(selector=dict(text=title), font=dict(size=21))
fig.write_image(here / "checkers.png")
print("xy reached at", latch, "; accepted at", RES["blocked"]["t"], "; progress failures at", fails,
      "; checkpoints at", resets, "; final distance %.3f m, heading error %.3f rad" % (d[-1], yaw[-1]))
