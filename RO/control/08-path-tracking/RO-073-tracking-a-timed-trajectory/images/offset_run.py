"""Feedback linearisation of an offset point P, one frame per 0.25 s up to 4 s, then one per second. Left: P 0.2 m ahead
of the axle; the body follows P. Right: P 0.2 m behind the axle; the body turns round within about 3 s and drives the
whole timetable backwards. Both P's (green) chase the reference robot's P (orange ring) with the same law, gain 1 per s.
Bottom: the distance from P to its reference: 0.224 m at the start, 0.080 m (P ahead) and 0.082 m (P behind) at 1 s,
next to the curve 0.224 x 0.95^(t / 0.05) of a gap that shrinks by 5 percent every 0.05 s cycle.
Run: python offset_run.py -> offset_run.gif, offset_run_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from drawkit import robot, timetable_path, trail
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, make_gif
from trackkit import CTRL_DT, D_P, DT, K_P, errors, feedback_lin, p_point, p_ref, simulate

here = Path(__file__).parent
runs, gaps, pts = {}, {}, {}
for d in (D_P, -D_P):
    r = simulate(lambda t, p, d=d: feedback_lin(t, p, d=d))
    assert not r["clipped"]
    P = np.array([p_point((x, y, th), d) for x, y, th in zip(r["x"], r["y"], r["th"])])
    PR = np.array([p_ref(t, d)[0] for t in r["t"]])
    runs[d], pts[d], gaps[d] = r, (P, PR), np.hypot(*(PR - P).T)
t = runs[D_P]["t"]
model = gaps[D_P][0] * (1 - K_P * CTRL_DT) ** (t / CTRL_DT)
i1 = int(round(1 / DT))
assert abs(gaps[D_P][0] - 0.2236) < 1e-4 and abs(gaps[D_P][i1] - 0.0800) < 5e-5 and abs(gaps[-D_P][i1] - 0.0820) < 5e-5
assert abs(model[i1] - 0.0802) < 5e-5 and gaps[-D_P][-1] < 2e-4
back = np.degrees(runs[-D_P]["th"][-1])
assert abs(back - 270) < 0.5 and abs(runs[-D_P]["v"][-1] + 0.3) < 1e-3          # facing -90 deg, driving backwards
mid_back = errors(runs[-D_P])[3]                                                   # axle midpoint to the timetable
assert abs(mid_back[-1] - 0.40) < 5e-4 and errors(runs[D_P])[3][-1] < 2e-4
the_back = np.degrees(np.abs(errors(runs[-D_P])[2]))

steps = [int(round(s / DT)) for s in np.r_[np.arange(0, 4.0, 0.25), np.arange(4, 12, 1.0)]] + [len(t) - 1]
names = {D_P: "P 0.2 m ahead of the axle", -D_P: "P 0.2 m behind the axle"}


def frame(k):
    fig = make_subplots(rows=2, cols=2, row_heights=[0.6, 0.4], vertical_spacing=0.13, horizontal_spacing=0.08,
                        specs=[[{}, {}], [{"colspan": 2}, None]], subplot_titles=(names[D_P], names[-D_P], ""))
    for c, d in ((1, D_P), (2, -D_P)):
        r = runs[d]
        P, PR = pts[d]
        timetable_path(fig, 1, c, name=None)
        trail(fig, r, k, BLUE, None, 1, c)
        fig.add_trace(go.Scatter(x=P[:k + 1, 0], y=P[:k + 1, 1], mode="lines", line=dict(color=GREEN, width=2, dash="dot"),
                                 showlegend=False), row=1, col=c)
        pose = (r["x"][k], r["y"][k], r["th"][k])
        robot(fig, pose, BLUE, "robot body (line: its heading)" if c == 1 else None, 1, c)
        fig.add_trace(go.Scatter(x=[pose[0], P[k, 0]], y=[pose[1], P[k, 1]], mode="lines",
                                 line=dict(color=GREEN, width=3), showlegend=False), row=1, col=c)
        fig.add_trace(go.Scatter(x=[PR[k, 0]], y=[PR[k, 1]], mode="markers",
                                 marker=dict(color="white", size=20, line=dict(color=ORANGE, width=4)),
                                 name="the reference robot's P" if c == 1 else "", showlegend=c == 1), row=1, col=c)
        fig.add_trace(go.Scatter(x=[P[k, 0]], y=[P[k, 1]], mode="markers", marker=dict(color=GREEN, size=13),
                                 name="P" if c == 1 else "", showlegend=c == 1), row=1, col=c)
        fig.add_annotation(x=1.0, y=2.05, text=f"v = {r['v'][k]:+.2f} m/s", showarrow=False, font=dict(size=19),
                           row=1, col=c)
        if d < 0 and t[k] >= 4 - 1e-9:
            assert the_back[k] > 90
            fig.add_annotation(x=pose[0], y=pose[1], ax=1.2, ay=0.95, axref="x2", ayref="y2",
                               text=f"faces backwards;<br>axle {mid_back[k]:.2f} m from<br>the timetable",
                               font=dict(size=18, color=BLUE), arrowcolor=BLUE, row=1, col=c)
        fig.update_xaxes(range=[-0.45, 2.35], dtick=1, title="x (m)", constrain="domain", row=1, col=c)
        fig.update_yaxes(range=[-0.35, 2.3], dtick=1, scaleanchor="x" if c == 1 else "x2", scaleratio=1, row=1, col=c)
    fig.add_trace(go.Scatter(x=t, y=model, mode="lines", line=dict(color=GREY, width=8), opacity=0.35,
                             name="5 percent smaller every 0.05 s"), row=2, col=1)
    for d, dash in ((D_P, None), (-D_P, "dash")):
        fig.add_trace(go.Scatter(x=t[:k + 1], y=gaps[d][:k + 1], mode="lines", line=dict(color=GREEN, width=4, dash=dash),
                                 name=("P to its reference, " + ("ahead" if d > 0 else "behind") + " (m)")),
                      row=2, col=1)
    title = (f"t = {t[k]:.2f} s: P to its reference: {gaps[D_P][k]:.3f} m (ahead), {gaps[-D_P][k]:.3f} m (behind)"
             "<br><span style='font-size:19px'>same law for both: P's velocity = reference P's velocity"
             " + 1 per s × gap</span>")
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1150, margin=dict(l=80, r=30, t=150, b=60),
                      title=dict(text=title, x=0.5, y=0.975, yanchor="top"),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=0.385, font=dict(size=17),
                                  bgcolor="rgba(255,255,255,0.85)"))
    fig.update_annotations(font=dict(size=20), selector=dict(text=names[D_P]))
    fig.update_annotations(font=dict(size=20), selector=dict(text=names[-D_P]))
    fig.update_xaxes(range=[0, 12], title="time (s)", row=2, col=1)
    fig.update_yaxes(range=[0, 0.24], title="gap (m)", row=2, col=1)
    return fig


figs = [frame(k) for k in steps]
make_gif(figs, here / "offset_run", fps=4, holds=[8] + [2] * (len(steps) - 2) + [16],
         keys=[0, 4, 12, len(steps) - 1], cols=2, width=800)
