"""Waypoint following on the room (our Python version of Nav2's waypoint follower and default tree, btkit.py): three
waypoints, sent one at a time as NavigateToPose goals; after each one reached, a 0.2 s pause (WaitAtWaypoint,
200 ms); stop_on_failure false, so a failed waypoint is recorded as missed and the next one is sent. The person
(pink) and the trolley (brown) are there from the start, so waypoint 2, above the table, has no path. Blue: the
path on the blackboard; dotted: the robot's track. Run -> waypoint_anim.gif, waypoint_anim_frames.png"""
import math
from pathlib import Path

import btkit as bt
import navdraw as nd
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, RED, make_gif

here = Path(__file__).parent
R = bt.results()["waypoints"]
recs = R["records"]
res = R["results"]
assert [(r["status"], r["t"]) for r in res] == [(bt.SUCCESS, 10.47), (bt.FAILURE, 21.24), (bt.SUCCESS, 34.41)]
REC_OK = [(r["t"], r["goal"]) for r in recs if (bt.SUCCESS, 21) in [(s, u) for _, s, u in r["log"]]]
assert len([t for t, g in REC_OK if g == 1]) == 6
ACTION = {31: "Spin 1.57 rad", 32: "Wait 5 s", 33: "BackUp 0.30 m", 28: "clear both costmaps"}


def state(t):
    rec = nd.at(recs, t)
    g = rec["goal"]
    used = len([1 for tt, gg in REC_OK if gg == g and tt <= t + 1e-9])
    running = [ACTION[u] for _, s, u in rec["log"] if u in ACTION and s == bt.RUNNING]
    done = {r["goal"]: r for r in res if r["t"] <= t + 1e-9}
    return rec, g, used, running, done


def frame(t):
    rec, g, used, running, done = state(t)
    fig = go.Figure()
    nd.room(fig, trolley=True, person=rec["person"])
    nd.track(fig, recs, t)
    for i, w in enumerate(bt.WAYPOINTS):
        col = GREY
        if i in done:
            col = GREEN if done[i]["status"] == bt.SUCCESS else RED
        elif i == g:
            col = ORANGE
        fig.add_trace(go.Scatter(x=[w[0]], y=[w[1]], mode="markers+text", text=[f"<b>{i + 1}</b>"],
                                 textposition="middle center", textfont=dict(size=17, color="white"),
                                 marker=dict(size=30, color=col, line=dict(color="white", width=2))))
        fig.add_annotation(x=w[0], y=w[1], ax=w[0] + 0.35 * math.cos(w[2]), ay=w[1] + 0.35 * math.sin(w[2]),
                           axref="x", ayref="y", text="", showarrow=True, arrowhead=0, arrowwidth=3, arrowcolor=col,
                           standoff=15, startstandoff=0)
    nd.path(fig, rec["path"])
    nd.robot(fig, *rec["robot"])
    lines = [f"<b>t = {t:.2f} s</b>: waypoint {g + 1} of 3 sent as a NavigateToPose goal"]
    if g in done:
        lines[0] = f"<b>t = {t:.2f} s</b>: waypoint {g + 1}: " + ("reached" if done[g]["status"] == bt.SUCCESS else
                                                               "failed after 6 recoveries: recorded as missed")
    elif rec["path"] is None and used:
        lines.append(f"no path; recoveries used: {used} of 6" + (f"; now: {running[0]}" if running else ""))
    elif rec["path"] is None and not used and t > res[0]["t"] + 0.1:
        lines.append("no path")
    else:
        lines.append("path found; following it" + (f" (after {used} recoveries)" if used else ""))
    status = ["waypoint %d: %s" % (i + 1, "reached" if done[i]["status"] == bt.SUCCESS else "missed")
              for i in sorted(done)]
    if status and g not in done:
        lines.append("so far: " + "; ".join(status))
    elif g in done and len(status) > 1:
        lines.append("so far: " + "; ".join(status))
    fig.add_annotation(x=0.0, y=1.0, xref="paper", yref="paper", text="<br>".join(lines), showarrow=False,
                       xanchor="left", yanchor="bottom", align="left", font=dict(size=19))
    fig.update_xaxes(range=[-0.05, 7.05], visible=False)
    fig.update_yaxes(range=[-0.05, 4.3], visible=False, scaleanchor="x", scaleratio=1)
    fig.update_layout(template="simple_white", font=FONT, width=900, height=680, showlegend=False,
                      margin=dict(l=8, r=8, t=95, b=8))
    return fig


T = [0.0, 2.0, 4.0, 6.0, 8.0, 10.47, 10.69, 11.5, 12.44, 15.0, 17.46, 18.5, 19.49, 20.3, 21.24, 21.25, 24.0, 27.0,
     30.0, 32.5, 34.41]
holds = [3, 1, 1, 1, 1, 5, 3, 2, 3, 2, 3, 2, 3, 2, 6, 3, 1, 1, 1, 1, 12]
figs = [frame(t) for t in T]
make_gif(figs, here / "waypoint_anim", fps=3, holds=holds, keys=[2, 5, 8, 10, 14, 20], cols=2, width=760)
print("results", [(r["goal"] + 1, r["status"], r["t0"], r["t"]) for r in res])
