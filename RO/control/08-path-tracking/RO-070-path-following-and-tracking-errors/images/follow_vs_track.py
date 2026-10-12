"""Path following against trajectory tracking, one frame per 0.5 s. Both cars stand still for the first 1.5 s
(held at the start); the orange dot is the timetable, a point moving along the course at 2 m/s from t = 0. Blue,
path following: drives at 2 m/s once free and ignores the dot; its lateral error along the course is the same as
without the hold, and it reaches the end at 19.65 s. Purple, trajectory tracking: speed 2 m/s plus 1 per s times the
along-track error (the dot's distance along the course minus its own), at most 5 m/s; the along-track error falls
from 3.0 m to within 0.1 m by 4.89 s and the car reaches the end at 17.90 s. Lower panel: each car's along-track
error. Run -> follow_vs_track.gif, follow_vs_track_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from coursedraw import axes, car, course, label, minus, trail
from gifkit import BLUE, FONT, ORANGE, PURPLE, make_gif
from plotly.subplots import make_subplots
from trackkit import HOLD, S_END, course_point, line_rule, run, timetable_s, tracker

here = Path(__file__).parent
PF = run(lambda q, t: line_rule(q), hold=HOLD)
TR = run(tracker, hold=HOLD)
BASE = run(lambda q, t: line_rule(q))
AT_PF = np.array([timetable_s(t) for t in PF["t"]]) - PF["s"]
AT_TR = np.array([timetable_s(t) for t in TR["t"]]) - TR["s"]
k_in = np.where(np.abs(AT_TR) > 0.1)[0][-1] + 1
assert round(PF["t"][-1], 2) == 19.65 and round(TR["t"][-1], 2) == 17.90 and round(TR["t"][k_in], 2) == 4.89
assert np.max(np.abs(PF["e"][150:150 + len(BASE["e"]) - 1] - BASE["e"][:-1])) == 0.0
assert round(AT_TR[150], 2) == 3.00 and round(TR["v"].max(), 1) == 5.0
assert round(S_END / 2.0, 2) == 17.85 and round(AT_TR[-1], 2) == 0.09 and round(AT_PF[-1], 2) == 3.59


def frame(t):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.72, 0.28], vertical_spacing=0.08)
    course(fig, (1, 1))
    ps = course_point(timetable_s(t))
    for r, col in ((PF, BLUE), (TR, PURPLE)):
        k = min(int(round(t / 0.01)), len(r["t"]) - 1)
        trail(fig, r["x"][:k + 1], r["y"][:k + 1], col, (1, 1))
        car(fig, (r["x"][k], r["y"][k], r["th"][k]), r["delta"][k], col, (1, 1),
            fill="rgba(76,120,168,0.2)" if col == BLUE else "rgba(178,121,162,0.2)")
    fig.add_trace(go.Scatter(x=[ps[0]], y=[ps[1]], mode="markers", marker=dict(color=ORANGE, size=18,
                             line=dict(color="black", width=1.5)), showlegend=False), row=1, col=1)
    for r, at, col in ((PF, AT_PF, BLUE), (TR, AT_TR, PURPLE)):
        k = min(int(round(t / 0.01)), len(r["t"]) - 1)
        fig.add_trace(go.Scatter(x=r["t"][:k + 1], y=at[:k + 1], mode="lines", line=dict(color=col, width=3),
                                 showlegend=False), row=2, col=1)
    label(fig, -1.5, 22.3, "orange dot: the timetable, 2 m/s from t = 0", ORANGE, (1, 1), size=17, anchor="left")
    label(fig, -1.5, 20.6, "blue: path following, 2 m/s, no clock", BLUE, (1, 1), size=17, anchor="left")
    label(fig, -1.5, 18.9, "purple: trajectory tracking, up to 5 m/s", PURPLE, (1, 1), size=17, anchor="left")
    if t >= PF["t"][-1]:
        title = ("tracking: at the end at 17.90 s, 0.09 m behind the timetable<br><span style='font-size:19px'>"
                 "following: at the end at 19.65 s, the same path, no clock</span>")
    elif t < HOLD:
        title = f"t = {t:.1f} s: both cars held at the start<br><span style='font-size:19px'>the timetable has left</span>"
    else:
        title = (f"t = {t:.1f} s<br><span style='font-size:19px'>along-track error: following "
                 f"{AT_PF[min(int(round(t / 0.01)), len(PF['t']) - 1)]:.2f} m, tracking "
                 f"{AT_TR[min(int(round(t / 0.01)), len(TR['t']) - 1)]:.2f} m</span>")
    axes(fig, (1, 1))
    fig.update_xaxes(title=dict(text="time (s)", standoff=2), range=[0, 20], dtick=2, row=2, col=1)
    fig.update_yaxes(title=dict(text="along-track<br>error (m)", standoff=2), range=[-0.3, 4.0], dtick=1, row=2, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1250, showlegend=False,
                      margin=dict(l=100, r=30, t=120, b=60), title=dict(x=0.5, y=0.975, yanchor="top", text=minus(title)))
    return fig


ts = list(np.arange(0, 19.65, 0.5)) + [19.65]
figs = [frame(t) for t in ts]
holds = [3] + [1] * (len(ts) - 2) + [14]
make_gif(figs, here / "follow_vs_track", fps=4, holds=holds, keys=[0, 4, 12, len(ts) - 1], cols=2, width=800)
