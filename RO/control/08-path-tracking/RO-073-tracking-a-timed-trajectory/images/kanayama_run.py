"""Kanayama's tracker on the timetable, one frame per 0.25 s up to 4 s, then one per second. Left: the room, with the
reference robot (orange) driving the timetable and our robot (blue). Right: the same moment seen from our robot, which
sits at the centre facing up: the reference robot is x_e ahead (green) and y_e to the left (red, negative = right),
and heads th_e from our heading. Bottom: the three errors over time. Start: x_e = 0.2 m, y_e = -0.1 m, th_e = 0;
first command v = 0.5 m/s, w = -0.48 rad/s; within 1 cm of the timetable from 3.35 s.
Run: python kanayama_run.py -> kanayama_run.gif, kanayama_run_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from drawkit import robot, timetable_path, trail
from gifkit import BLUE, FONT, GREEN, ORANGE, PURPLE, RED, make_gif
from trackkit import DT, errors, kanayama, ref, simulate

here = Path(__file__).parent
run = simulate(kanayama)
t = run["t"]
xe, ye, the, dist = errors(run)
assert abs(run["v"][0] - 0.5) < 1e-12 and abs(run["w"][0] + 0.48) < 1e-12
assert abs(t[np.argmax(dist < 0.01)] - 3.35) < 1e-9 and not run["clipped"]

def z(v):
    """One decimal, without a minus sign on zero."""
    return f"{round(v, 1) + 0.0:.1f}"


steps = [int(round(s / DT)) for s in np.r_[np.arange(0, 4.0, 0.25), np.arange(4, 12, 1.0)]] + [len(t) - 1]


def frame(k):
    fig = make_subplots(rows=2, cols=2, row_heights=[0.6, 0.4], column_widths=[0.55, 0.45], vertical_spacing=0.13,
                        horizontal_spacing=0.12, specs=[[{}, {}], [{"colspan": 2, "secondary_y": True}, None]],
                        subplot_titles=("the room", "seen from our robot (cm)", ""))
    timetable_path(fig, 1, 1, name=None)
    trail(fig, run, k, BLUE, None, 1, 1)
    robot(fig, ref(t[k])[:3], ORANGE, "reference robot (timetable)", 1, 1)
    robot(fig, (run["x"][k], run["y"][k], run["th"][k]), BLUE, "our robot", 1, 1)
    # robot's own view: ahead = up, left = left; in cm
    X, Y = -100 * ye[k], 100 * xe[k]
    fig.add_trace(go.Scatter(x=[0, 0], y=[-24, 24], mode="lines", line=dict(color=BLUE, width=1.5, dash="dash"),
                             showlegend=False), row=1, col=2)
    fig.add_trace(go.Scatter(x=[-24, 24], y=[0, 0], mode="lines", line=dict(color=BLUE, width=1.5, dash="dash"),
                             showlegend=False), row=1, col=2)
    fig.add_trace(go.Scatter(x=[0, 0], y=[0, Y], mode="lines", line=dict(color=GREEN, width=6), showlegend=False),
                  row=1, col=2)
    fig.add_trace(go.Scatter(x=[0, X], y=[Y, Y], mode="lines", line=dict(color=RED, width=6), showlegend=False),
                  row=1, col=2)
    robot(fig, (0, 0, np.pi / 2), BLUE, None, 1, 2, r=2.5)
    robot(fig, (X, Y, np.pi / 2 + the[k]), ORANGE, None, 1, 2, r=2.5)
    fig.add_annotation(x=0, y=22.5, text="ahead", showarrow=False, font=dict(size=18, color=BLUE), xanchor="left",
                       xshift=6, row=1, col=2)
    fig.add_annotation(x=-23, y=0, text="left", showarrow=False, font=dict(size=18, color=BLUE), yshift=14,
                       xanchor="left", row=1, col=2)
    # errors over time
    tt = t[:k + 1]
    fig.add_trace(go.Scatter(x=tt, y=100 * xe[:k + 1], mode="lines", line=dict(color=GREEN, width=4),
                             name="x<sub>e</sub>, ahead (cm)"), row=2, col=1)
    fig.add_trace(go.Scatter(x=tt, y=100 * ye[:k + 1], mode="lines", line=dict(color=RED, width=4),
                             name="y<sub>e</sub>, left (cm)"), row=2, col=1)
    fig.add_trace(go.Scatter(x=tt, y=np.degrees(the[:k + 1]), mode="lines", line=dict(color=PURPLE, width=4, dash="dot"),
                             name="θ<sub>e</sub> (degrees, right axis)"), row=2, col=1, secondary_y=True)
    small = "<span style='font-size:19px'>"
    title = (f"t = {t[k]:.2f} s: x<sub>e</sub> = {z(100 * xe[k])} cm, y<sub>e</sub> = {z(100 * ye[k])} cm,"
             f" θ<sub>e</sub> = {z(np.degrees(the[k]))}°"
             f"<br>{small}command: v = {run['v'][k]:.3f} m/s, ω = {run['w'][k]:.3f} rad/s;"
             f" distance from the timetable {100 * dist[k]:.1f} cm</span>")
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1150, margin=dict(l=90, r=90, t=150, b=60),
                      title=dict(text=title, x=0.5, y=0.975, yanchor="top"),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=0.385, font=dict(size=17),
                                  bgcolor="rgba(255,255,255,0.85)"))
    fig.update_annotations(selector=dict(text="the room"), font=dict(size=20))
    fig.update_annotations(selector=dict(text="seen from our robot (cm)"), font=dict(size=20))
    fig.update_xaxes(range=[-0.4, 2.3], dtick=1, title="x (m)", constrain="domain", row=1, col=1)
    fig.update_yaxes(range=[-0.35, 2.2], dtick=1, title="y (m)", scaleanchor="x", scaleratio=1, row=1, col=1)
    fig.update_xaxes(range=[-25, 25], dtick=10, constrain="domain", row=1, col=2)
    fig.update_yaxes(range=[-25, 25], dtick=10, scaleanchor="x2", scaleratio=1, constrain="domain", row=1, col=2)
    fig.update_xaxes(range=[0, 12], title="time (s)", row=2, col=1)
    fig.update_yaxes(range=[-12, 22], title="x<sub>e</sub>, y<sub>e</sub> (cm)", row=2, col=1, secondary_y=False)
    fig.update_yaxes(range=[-12 * 0.35, 22 * 0.35], title="θ<sub>e</sub> (degrees)", row=2, col=1, secondary_y=True)
    return fig


figs = [frame(k) for k in steps]
make_gif(figs, here / "kanayama_run", fps=4, holds=[8] + [2] * (len(steps) - 2) + [16],
         keys=[0, 4, 12, len(steps) - 1], cols=2, width=800)
