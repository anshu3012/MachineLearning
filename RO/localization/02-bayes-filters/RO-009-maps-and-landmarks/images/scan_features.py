"""A simulated laser scan from the robot at (2, 1, 30 deg): 360 beams, 1 degree apart, range noise 1 cm (seeded).
Feature extraction finds the two poles as short groups of beams that are nearer than their neighbours.
Run: python scan_features.py -> scan_features.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import FONT, GREEN, GREY, RED
from roommap import CAB, DOOR, H, POLES, ROBOT, TABLE, W, extract_poles, scan

here = Path(__file__).parent
PINK = "#E377C2"
b, r = scan(ROBOT, noise=0.01, rng=np.random.default_rng(0))
found = extract_poles(b, r)
x, y, th = ROBOT
fig = go.Figure()
for seg in [[(0, 0), (W, 0), (W, H), (DOOR[1], H)], [(DOOR[0], H), (0, H), (0, 0)]]:
    sx, sy = zip(*seg)
    fig.add_trace(go.Scatter(x=sx, y=sy, mode="lines", line=dict(color="#bbb", width=3)))
px, py = zip(*(TABLE + [TABLE[0]]))
fig.add_trace(go.Scatter(x=px, y=py, mode="lines", line=dict(color="#bbb", width=2)))
fig.add_trace(go.Scatter(x=[5.6, 7, 7, 6.4, 6.4, 5.6, 5.6], y=[4, 4, 2.4, 2.4, 3.4, 3.4, 4], mode="lines",
                         line=dict(color="#bbb", width=2)))
hx, hy = x + r * np.cos(th + b), y + r * np.sin(th + b)
fig.add_trace(go.Scatter(x=hx, y=hy, mode="markers", marker=dict(size=4, color=GREY)))
for rng_, bear, n in found:
    lx, ly = x + rng_ * np.cos(th + bear), y + rng_ * np.sin(th + bear)
    col = PINK if lx < 3 else GREEN
    fig.add_trace(go.Scatter(x=[x, lx], y=[y, ly], mode="lines", line=dict(color=col, width=2, dash="dash")))
    fig.add_trace(go.Scatter(x=[lx], y=[ly], mode="markers", marker=dict(size=16, color=col, symbol="circle-open",
                                                                            line=dict(width=3))))
    fig.add_annotation(x=lx, y=ly, text=f"r = {rng_:.2f} m, φ = {np.degrees(bear):.0f}°".replace("-", "−") + f"<br>{n} beams",
                       showarrow=False, yshift=-38 if lx > 3 else 34, xshift=0 if lx > 3 else 30,
                       font=dict(size=17, color=col))
fig.add_trace(go.Scatter(x=[x, x + 0.4 * np.cos(th)], y=[y, y + 0.4 * np.sin(th)], mode="lines+markers",
                         line=dict(color=RED, width=4), marker=dict(size=[10, 0], color=RED)))
fig.update_xaxes(range=[-0.3, 7.3], dtick=1, title="x (m)")
fig.update_yaxes(range=[-0.3, 4.3], dtick=1, title="y (m)", scaleanchor="x")
fig.update_layout(template="simple_white", width=1000, height=660, font=FONT, showlegend=False,
                  margin=dict(l=80, r=30, t=90, b=70),
                  title=dict(text="360 scan points (grey) and the two poles extracted from them", x=0.5,
                             font=dict(size=22)))
fig.write_image(here / "scan_features.png")
print([(round(a, 3), round(float(np.degrees(c)), 1), n) for a, c, n in found])
