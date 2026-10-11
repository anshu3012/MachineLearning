"""Sampling the odometry model, played. Part 1, left panel: the worked sample of Section 5.2, one draw done slowly. The
noise draws +0.05 rad, -0.03 m, -0.02 rad give the turn 0.550 rad, the drive 0.449 m and the turn 0.480 rad; the robot
ends at (2.214, 1.395) facing 1.554 rad. Part 2: 500 draws for each of three noise settings (seed 5, as in
the notebook) appear in batches; the mostly-turning-noise cloud bends along a circle around the start, the banana. The
last frame shows the three clouds.
Run: python banana_anim.py -> banana_anim.gif, banana_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, ORANGE, RED, make_gif
from motion import START, sample_odometry
from plotly.subplots import make_subplots
from robotdraw import robot

here = Path(__file__).parent
X0, Y0, TH0 = START
u = (0.500, 0.479, 0.500)
CASES = [("the Note's noise", (0.1, 0.1, 0.1, 0.01)), ("mostly turning noise", (0.4, 0.1, 0.02, 0.0)),
         ("mostly driving noise", (0.02, 0.0, 0.4, 0.0))]
CLOUDS = [sample_odometry(u, START, np.random.default_rng(5), 500, a) for _, a in CASES]   # the notebook's seed
R1, TR, R2 = 0.500 + 0.05, 0.479 - 0.03, 0.500 - 0.02                  # the worked sample's three draws
XE, YE, THE = X0 + TR * np.cos(TH0 + R1), Y0 + TR * np.sin(TH0 + R1), TH0 + R1 + R2
assert [round(v, 3) for v in (R1, TR, R2)] == [0.550, 0.449, 0.480]
assert round(TH0 + R1, 3) == 1.074 and (round(XE, 3), round(YE, 3), round(THE, 3)) == (2.214, 1.395, 1.554)
assert round((2.249 - XE) * 100, 1) == 3.5 and round((1.409 - YE) * 100, 1) == 1.4   # 3.5 cm left, 1.4 cm below


def base(title, sub):
    fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.05, subplot_titles=[c[0] for c in CASES])
    t = np.linspace(TH0, TH0 + 1, 50)
    for c in (1, 2, 3):
        fig.add_trace(go.Scatter(x=1.75 + 0.5 * np.sin(t), y=1.433 - 0.5 * np.cos(t), mode="lines",
                                 line=dict(color=GREY, dash="dash", width=2)), 1, c)
        fig.update_xaxes(range=[1.7, 2.6], dtick=0.2, title="x (m)", row=1, col=c)
        fig.update_yaxes(range=[0.9, 1.85], dtick=0.2, scaleanchor=f"x{c if c > 1 else ''}", row=1, col=c)
    fig.update_yaxes(title="y (m)", row=1, col=1)
    fig.update_layout(template="simple_white", width=1200, height=600, font=FONT, showlegend=False,
                      margin=dict(l=80, r=30, t=150, b=70),
                      title=dict(x=0.5, y=0.96, font=dict(size=23),
                                 text=f"{title}<br><span style='font-size:20px'>{sub}</span>"))
    fig.update_annotations(font_size=20)
    return fig


def marks(fig):  # start (black) and the model's end (red x) in every panel
    for c in (1, 2, 3):
        fig.add_trace(go.Scatter(x=[X0], y=[Y0], mode="markers", marker=dict(size=12, color="black")), 1, c)
        fig.add_trace(go.Scatter(x=[2.249], y=[1.409], mode="markers", marker=dict(size=12, color=RED, symbol="x")),
                      1, c)


LINES = [("noise drawn: +0.05 rad, −0.03 m, −0.02 rad", "black"),
         ("1. first turn: 0.500 + 0.05 = 0.550 rad", ORANGE), ("2. drive: 0.479 − 0.03 = 0.449 m", ORANGE),
         ("3. second turn: 0.500 − 0.02 = 0.480 rad", ORANGE), ("end (2.214, 1.395), heading 1.554 rad", ORANGE),
         ("3.5 cm left of and 1.4 cm below", GREY), ("the model's end (red ×)", GREY)]


def one_draw(nlines, r1=0.0, d=0.0, r2=0.0, end=False):
    """Part 1, zoomed on the left panel's scene: the robot has done r1 of the first turn, d of the drive, r2 of the
    second turn; the first nlines lines of the working are shown."""
    fig = go.Figure()
    t = np.linspace(TH0, TH0 + 1, 50)
    fig.add_trace(go.Scatter(x=1.75 + 0.5 * np.sin(t), y=1.433 - 0.5 * np.cos(t), mode="lines",
                             line=dict(color=GREY, dash="dash", width=2)))
    if d > 0:
        fig.add_trace(go.Scatter(x=[X0, X0 + d * np.cos(TH0 + R1)], y=[Y0, Y0 + d * np.sin(TH0 + R1)], mode="lines",
                                 line=dict(color=ORANGE, width=4)))
    fig.add_trace(go.Scatter(x=[X0], y=[Y0], mode="markers", marker=dict(size=13, color="black")))
    q = (X0 + d * np.cos(TH0 + R1), Y0 + d * np.sin(TH0 + R1), TH0 + r1 + r2)
    for tr in robot(q, scale=0.22, opacity=0.4 if end else 0.75):
        fig.add_trace(tr)
    fig.add_trace(go.Scatter(x=[2.249], y=[1.409], mode="markers", marker=dict(size=15, color=RED, symbol="x")))
    if end:
        fig.add_trace(go.Scatter(x=[XE], y=[YE], mode="markers", marker=dict(size=13, color=ORANGE)))
    for j, (txt, col) in enumerate(LINES[:nlines]):
        fig.add_annotation(x=0.56, y=0.93 - 0.12 * j, xref="paper", yref="paper", text=txt, showarrow=False,
                           xanchor="left", yanchor="middle",
                           font=dict(color=col, size=22 if j < 5 else 20))
    fig.update_xaxes(range=[1.9, 2.4], dtick=0.1, title="x (m)", domain=[0, 0.5], showgrid=True, gridcolor="#eee")
    fig.update_yaxes(range=[0.95, 1.47], dtick=0.1, title="y (m)", scaleanchor="x", showgrid=True, gridcolor="#eee")
    fig.update_layout(template="simple_white", width=1200, height=600, font=FONT, showlegend=False,
                      margin=dict(l=80, r=30, t=80, b=70),
                      title=dict(x=0.5, y=0.97, font=dict(size=23),
                                 text="one draw from the Note's noise: noisy turn, drive, turn"))
    return fig


def cloud(n, sub):
    """Part 2: the first n of the 500 draws in each panel."""
    fig = base("500 sampled end positions for the same odometry reading", sub)
    for c, (xs, ys, _) in enumerate(CLOUDS, start=1):
        fig.add_trace(go.Scatter(x=xs[:n], y=ys[:n], mode="markers", marker=dict(size=4, color=BLUE, opacity=0.6)),
                      1, c)
    marks(fig)
    return fig


figs, holds = [], []
add = lambda f, h: (figs.append(f), holds.append(h))
add(one_draw(1), 8)
for k in (1, 2, 3):
    add(one_draw(2, r1=R1 * k / 3), 2 if k < 3 else 4)
for k in (1, 2, 3):
    add(one_draw(3, r1=R1, d=TR * k / 3), 2 if k < 3 else 4)
for k in (1, 2, 3):
    add(one_draw(4, r1=R1, d=TR, r2=R2 * k / 3), 2 if k < 3 else 4)
add(one_draw(7, r1=R1, d=TR, r2=R2, end=True), 14)
key = [len(figs) - 1]
for n in (5, 20, 50, 100, 200, 350, 500):
    sub = (f"{n} of 500 draws in each panel" if n < 500 else
           "turning noise swings the cloud along a circle around the start: the banana")
    add(cloud(n, sub), 3 if n < 500 else 24)
key.append(len(figs) - 1)
make_gif(figs, here / "banana_anim", fps=4, holds=holds, keys=key, cols=2, width=950)
