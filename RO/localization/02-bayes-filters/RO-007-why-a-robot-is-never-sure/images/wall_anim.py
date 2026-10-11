"""200 readings of one wall, one at a time. A distance sensor 2.00 m from a wall: 190 readings of the wall with sensor
noise (standard deviation 3 cm, from 1.92 to 2.07 m) and, after the 100th, 10 readings taken while a person walks
through the beam (0.61 to 1.16 m; shown in increasing order as the person walks away).
Top: the beam and the reported distance (dot); bottom: the histogram so far, on the same metre axis.
Run: python wall_anim.py -> wall_anim.gif, wall_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, RED, make_gif
from plotly.subplots import make_subplots

here = Path(__file__).parent
rng = np.random.default_rng(7)
wall = rng.normal(2.0, 0.03, 190)
person = rng.uniform(0.6, 1.2, 10)
assert (round(wall.min(), 2), round(wall.max(), 2)) == (1.92, 2.07)
assert (round(person.min(), 2), round(person.max(), 2)) == (0.61, 1.16)
z = np.concatenate([wall[:100], np.sort(person), wall[100:]])
is_person = np.zeros(200, bool)
is_person[100:110] = True
EDGES = np.arange(0.5, 2.3001, 0.02)
MID = (EDGES[:-1] + EDGES[1:]) / 2
TOP = np.histogram(wall, bins=EDGES)[0].max()
R = 0.045                                          # the person's marker half-width in metres, front edge at the reading


def frame(n, title, final=False):
    k = n - 1
    fig = make_subplots(rows=2, cols=1, row_heights=[0.27, 0.73], vertical_spacing=0.06, shared_xaxes=True)
    fig.add_shape(type="line", x0=2.0, x1=2.0, y0=-0.8, y1=0.8, line=dict(color="black", width=6), opacity=1,
                  layer="below", row=1, col=1)
    fig.add_annotation(x=2.0, y=0.8, text="wall", showarrow=False, yanchor="bottom", font=dict(size=18), row=1, col=1)
    hit = z[k] if is_person[k] else 2.0
    fig.add_trace(go.Scatter(x=[0.03, hit], y=[0, 0], mode="lines", line=dict(color=GREY, width=3)), 1, 1)
    if is_person[k]:
        fig.add_trace(go.Scatter(x=[z[k] + R], y=[0], mode="markers", marker=dict(size=28, color=RED)), 1, 1)
        fig.add_annotation(x=z[k] + R, y=0.45, text="person", showarrow=False, font=dict(size=18, color=RED),
                           row=1, col=1)
    fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers", marker=dict(size=26, color=GREY, symbol="square")), 1, 1)
    fig.add_annotation(x=0, y=0.45, text="sensor", showarrow=False, font=dict(size=18, color=GREY), row=1, col=1)
    col = RED if is_person[k] else BLUE
    fig.add_trace(go.Scatter(x=[z[k]], y=[0], mode="markers", marker=dict(size=14, color=col,
                                                                          line=dict(color="white", width=1))), 1, 1)
    fig.add_annotation(x=1.0, y=-0.62, text="dot: the distance the sensor reports; noise moves it a few cm", showarrow=False,
                       font=dict(size=18, color=GREY), row=1, col=1)
    for mask, c in ((~is_person[:n], BLUE), (is_person[:n], RED)):
        fig.add_trace(go.Bar(x=MID, y=np.histogram(z[:n][mask], bins=EDGES)[0], width=0.02, marker_color=c,
                             marker_line=dict(width=0.5, color="white")), 2, 1)
    fig.add_shape(type="line", x0=2.0, x1=2.0, y0=0, y1=TOP + 9, line=dict(color=GREY, dash="dash", width=2),
                  opacity=1, row=2, col=1)
    fig.add_annotation(x=2.0, y=TOP + 7, text="true distance 2.00 m", showarrow=False, xanchor="right", xshift=-8,
                       font=dict(size=18, color=GREY), row=2, col=1)
    if not final:                                  # a marker over the bar the newest reading landed in
        b = np.searchsorted(EDGES, z[k], side="right") - 1
        h = np.histogram(z[:n], bins=EDGES)[0][b]
        fig.add_trace(go.Scatter(x=[MID[b]], y=[h + 2.5], mode="markers",
                                 marker=dict(size=13, color=col, symbol="triangle-down")), 2, 1)
    if n <= 10:
        fig.add_annotation(x=1.0, y=40, text="each reading adds 1 to the bar<br>of its distance (0.02 m wide)",
                           showarrow=False, font=dict(size=18, color=GREY), row=2, col=1)
    if final:
        fig.add_annotation(x=0.9, y=12, text="10 readings: a person walked<br>past, 0.61 to 1.16 m", showarrow=False,
                           font=dict(size=18, color=RED), row=2, col=1)
        fig.add_annotation(x=1.5, y=34, text="190 readings: the wall,<br>1.92 to 2.07 m, spread<br>by sensor noise",
                           showarrow=False, font=dict(size=18, color=BLUE), row=2, col=1)
    fig.update_yaxes(visible=False, range=[-0.9, 1.15], row=1, col=1)
    fig.update_xaxes(visible=False, row=1, col=1)
    fig.update_xaxes(range=[-0.12, 2.25], dtick=0.2, title="reading (m)", row=2, col=1)
    fig.update_yaxes(range=[0, TOP + 11], title="number of readings", row=2, col=1)
    fig.update_layout(template="simple_white", width=900, height=720, font=FONT, showlegend=False, barmode="overlay",
                      margin=dict(l=80, r=30, t=80, b=70), title=dict(text=title, x=0.5, y=0.96, font=dict(size=22)))
    return fig


def name(n):
    k = n - 1
    who = "the person" if is_person[k] else "the wall"
    return f"reading {n} ({who}): {z[k]:.2f} m"


figs, holds = [], []
for n in range(1, 11):                                     # the first ten one at a time
    figs.append(frame(n, name(n)))
    holds.append(6 if n == 1 else 2)
for n in range(20, 101, 10):                               # then ten at a time
    figs.append(frame(n, f"{n} readings of the wall so far"))
    holds.append(1)
for n in range(101, 111):                                  # a person walks through the beam
    figs.append(frame(n, name(n)))
    holds.append(3)
for n in range(120, 200, 20):                              # the person has gone; the wall again
    figs.append(frame(n, f"{n} readings so far; the person has gone"))
    holds.append(1)
figs.append(frame(200, "200 readings of one wall from one spot", final=True))
holds.append(20)
key = [0, 9, 23, len(figs) - 1]
assert figs and z[0].round(2) == 2.00 and is_person[100] and len(z) == 200
make_gif(figs, here / "wall_anim", fps=4, holds=holds, keys=key, cols=2, width=900)
