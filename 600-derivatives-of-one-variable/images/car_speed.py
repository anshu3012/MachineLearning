"""A car covers 100 m in 10 s: it speeds up, then slows down (Plotly frames). Top: distance s(t). Bottom: the speed,
built one point at a time the way a speedometer does it: (s(t + 0.01) - s(t)) / 0.01. Our own curve
s(t) = 100 (3u^2 - 2u^3), u = t / 10. Idea after 3Blue1Brown, "The paradox of the derivative".
Run: python car_speed.py -> car_speed.gif, car_speed_frames.png"""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, ORANGE, make_gif

here = Path(__file__).parent
DT = 0.01
s = lambda t: 100 * (3 * (t / 10) ** 2 - 2 * (t / 10) ** 3)
speed = lambda t: (s(t + DT) - s(t)) / DT
assert s(10) == 100 and abs(speed(3) - 12.6) < 0.05 and abs(speed(5) - 15) < 0.05
tt = np.linspace(0, 10, 201)


def frame(t):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1)
    fig.add_trace(go.Scatter(x=tt, y=s(tt), line=dict(color=BLUE, width=4)), row=1, col=1)
    fig.add_trace(go.Scatter(x=[t], y=[s(t)], mode="markers", marker=dict(size=16, color="black")), row=1, col=1)
    done = tt[tt <= t + 1e-9]
    fig.add_trace(go.Scatter(x=done, y=speed(done), line=dict(color=ORANGE, width=4)), row=2, col=1)
    fig.add_trace(go.Scatter(x=[t], y=[speed(t)], mode="markers", marker=dict(size=16, color=ORANGE)), row=2, col=1)
    fig.add_vline(x=t, line=dict(color=GREY, width=1.5, dash="dot"))
    fig.update_yaxes(title="distance s (m)", range=[0, 108], row=1, col=1)
    fig.update_yaxes(title="speed (m/s)", range=[0, 17], row=2, col=1)
    fig.update_xaxes(range=[0, 10.3], row=1, col=1)
    fig.update_xaxes(title="time t (s)", range=[0, 10.3], row=2, col=1)
    fig.update_layout(template="simple_white", width=900, height=760, font=FONT, showlegend=False,
                      margin=dict(l=80, r=20, t=90, b=65),
                      title=dict(x=0.5, font=dict(size=22), text=f"t = {t:.1f} s: the car moves {s(t + DT) - s(t):.3f} m in the "
                                 f"next 0.01 s<br>speed ≈ {s(t + DT) - s(t):.3f} / 0.01 = <b>{speed(t):.1f} m/s</b>"))
    return fig


ts = [round(0.5 * k, 1) for k in range(20)] + [9.9]
figs = [frame(t) for t in ts]
holds = [8 if t == 3.0 else 12 if t == 9.9 else 2 for t in ts]
make_gif(figs, here / "car_speed", fps=6, holds=holds, keys=[ts.index(1.0), ts.index(3.0), ts.index(5.0), len(ts) - 1])
