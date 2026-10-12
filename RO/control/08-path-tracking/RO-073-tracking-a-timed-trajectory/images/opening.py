"""The opening problem, one frame per 0.5 s: the reference robot (orange) drives the timetable, 1 m straight, a 90 degree
left arc of radius 1 m and 1 m straight at 0.3 m/s. The room robot starts 0.2 m behind and 0.1 m to the left.
Replaying the timetable's speeds (grey) keeps the error: 0.219 m at 11.90 s. A path follower (purple) gets onto the line
but stays behind: 0.205 m behind at 11.90 s, so it reaches the end 0.69 s late. The last frame adds Kanayama's tracker
(blue): within 1 cm of the timetable from 3.35 s.
Run: python opening.py -> opening.gif, opening_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from drawkit import robot, timetable_path, trail
from gifkit import BLUE, FONT, GREY, ORANGE, PURPLE, make_gif
from trackkit import DT, START, T_END, errors, kanayama, path_follower, ref, replay, simulate

here = Path(__file__).parent
runs = {"replay": simulate(replay), "follow": simulate(path_follower), "kan": simulate(kanayama)}
dist = {k: errors(r)[3] for k, r in runs.items()}
t = runs["kan"]["t"]
first = t[np.argmax(dist["kan"] < 0.01)]
late = simulate(path_follower, T=T_END + 2)
t_end_follow = late["t"][np.argmax(late["y"] >= 2.0)]
assert abs(dist["replay"][0] - 0.2236) < 1e-4 and abs(dist["replay"][-1] - 0.219) < 5e-4
assert abs(dist["follow"][-1] - 0.205) < 5e-4 and abs(t_end_follow - T_END - 0.69) < 0.005
assert abs(first - 3.35) < 1e-9 and dist["kan"][-1] < 2e-4
assert not any(r["clipped"] for r in runs.values())

steps = list(range(0, len(t), 50)) + [len(t) - 1]


def frame(k, last=False):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.66, 0.34], vertical_spacing=0.09)
    timetable_path(fig, 1, 1)
    trail(fig, runs["replay"], k, GREY, None, 1, 1)
    trail(fig, runs["follow"], k, PURPLE, None, 1, 1)
    if last:
        trail(fig, runs["kan"], k, BLUE, None, 1, 1)
    xr, yr, thr, _, _ = ref(t[k])
    robot(fig, (xr, yr, thr), ORANGE, "timetable: where the robot should be", 1, 1)
    robot(fig, [runs["replay"][q][k] for q in ("x", "y", "th")], GREY, "replay the timetable's speeds", 1, 1)
    robot(fig, [runs["follow"][q][k] for q in ("x", "y", "th")], PURPLE, "follow the path, no clock", 1, 1)
    if last:
        robot(fig, [runs["kan"][q][k] for q in ("x", "y", "th")], BLUE, "Kanayama's tracker", 1, 1)
    fig.add_annotation(x=START[0], y=START[1] + 0.13, text="start", showarrow=False, font=dict(size=19, color=GREY),
                       row=1, col=1)
    # distance to the timetable
    for key, col, name in (("replay", GREY, "replay"), ("follow", PURPLE, "path follower"),
                           ("kan", BLUE, "Kanayama")):
        if key == "kan" and not last:
            continue
        fig.add_trace(go.Scatter(x=t[:k + 1], y=dist[key][:k + 1], mode="lines", line=dict(color=col, width=4, simplify=False),
                                 showlegend=False), row=2, col=1)
        fig.add_trace(go.Scatter(x=[t[k]], y=[dist[key][k]], mode="markers", marker=dict(color=col, size=12),
                                 showlegend=False), row=2, col=1)
    small = "<span style='font-size:19px'>"
    if last:
        title = (f"t = {t[k]:.1f} s, with Kanayama's tracker (blue)<br>{small}from the timetable: replay "
                 f"{dist['replay'][k]:.3f} m, path follower {dist['follow'][k]:.3f} m, Kanayama "
                 f"{dist['kan'][k]:.4f} m</span>")
    else:
        title = (f"t = {t[k]:.1f} s<br>{small}from the timetable: replay {dist['replay'][k]:.3f} m,"
                 f" path follower {dist['follow'][k]:.3f} m</span>")
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1250, margin=dict(l=90, r=30, t=130, b=70),
                      title=dict(text=title, x=0.5, y=0.975, yanchor="top"),
                      legend=dict(x=0.01, y=0.985, font=dict(size=18), bgcolor="rgba(255,255,255,0.85)"))
    fig.update_xaxes(range=[-0.45, 2.45], title="x (m)", dtick=0.5, constrain="domain", row=1, col=1)
    fig.update_yaxes(range=[-0.35, 2.25], title="y (m)", dtick=0.5, scaleanchor="x", scaleratio=1, row=1, col=1)
    fig.update_xaxes(range=[0, 12.2], title="time (s)", row=2, col=1)
    fig.update_yaxes(range=[0, 0.26], title="distance from<br>the timetable (m)", row=2, col=1)
    return fig


figs = [frame(k) for k in steps] + [frame(steps[-1], last=True)]
make_gif(figs, here / "opening", fps=4, holds=[6] + [2] * (len(steps) - 1) + [16],
         keys=[0, 8, len(steps) - 1, len(steps)], cols=2, width=800)
