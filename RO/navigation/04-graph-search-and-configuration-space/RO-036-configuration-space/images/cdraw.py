"""Shared drawing for this Note's figures (no output when run on its own): the room seen from above in subplot (1, 1)
and the edges and the top and bottom faces of the configuration-space box in subplot (1, 2)."""
import numpy as np
import plotly.graph_objects as go
from cmodel import TWO_PI
from gifkit import BLUE, GREY, PURPLE
from roommap import POLE_R, POLES, TABLE


def room(fig):
    fig.add_trace(go.Scatter(x=[3.0, 0, 0, 7, 7, 4.2], y=[4, 4, 0, 0, 4, 4], mode="lines",
                             line=dict(color="black", width=5)), 1, 1)
    tx, ty = zip(*(TABLE + [TABLE[0]]))
    fig.add_trace(go.Scatter(x=tx, y=ty, mode="lines", fill="toself", line=dict(color=BLUE, width=2),
                             fillcolor="rgba(76,120,168,0.2)"), 1, 1)
    fig.add_trace(go.Scatter(x=[5.6, 7, 7, 6.4, 6.4, 5.6, 5.6], y=[4, 4, 2.4, 2.4, 3.4, 3.4, 4], mode="lines",
                             fill="toself", line=dict(color=PURPLE, width=2), fillcolor="rgba(178,121,162,0.2)"), 1, 1)
    for (px, py), c in zip(POLES.values(), ("#E377C2", "#54A24B")):
        a = np.linspace(0, TWO_PI, 30)
        fig.add_trace(go.Scatter(x=px + POLE_R * np.cos(a), y=py + POLE_R * np.sin(a), mode="lines", fill="toself",
                                 line=dict(color=c, width=1), fillcolor=c), 1, 1)


def box_edges(fig):
    X, Y, T = 7, 4, TWO_PI
    for a, b in [((0, 0, 0), (X, 0, 0)), ((X, 0, 0), (X, Y, 0)), ((X, Y, 0), (0, Y, 0)), ((0, Y, 0), (0, 0, 0)),
                 ((0, 0, T), (X, 0, T)), ((X, 0, T), (X, Y, T)), ((X, Y, T), (0, Y, T)), ((0, Y, T), (0, 0, T)),
                 ((0, 0, 0), (0, 0, T)), ((X, 0, 0), (X, 0, T)), ((X, Y, 0), (X, Y, T)), ((0, Y, 0), (0, Y, T))]:
        fig.add_trace(go.Scatter3d(x=[a[0], b[0]], y=[a[1], b[1]], z=[a[2], b[2]], mode="lines",
                                   line=dict(color=GREY, width=3)), 1, 2)
    for z in (0, T):
        fig.add_trace(go.Mesh3d(x=[0, X, X, 0], y=[0, 0, Y, Y], z=[z] * 4, i=[0, 0], j=[1, 2], k=[2, 3], color=BLUE,
                                opacity=0.15), 1, 2)
