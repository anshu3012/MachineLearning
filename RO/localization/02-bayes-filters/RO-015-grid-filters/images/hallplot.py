"""Shared model and drawing helpers for the hallway figures (no output when run on its own).

The hallway: 10 cells of 1 m, numbered 0-9, joined into a loop (cell 9 is next to cell 0). Doors at cells 1, 3, 7.
Door sensor: p(reads door | at a door) = 0.6, p(reads door | at a wall) = 0.2 (the same numbers as the door world).
Move command "2 cells right": 0.8 exactly 2, 0.1 one cell short, 0.1 one cell too far.
"""
import numpy as np
import plotly.graph_objects as go

from gifkit import BLUE, FONT, GREEN, GREY, ORANGE

N = 10
DOORS = (1, 3, 7)
DOOR = np.isin(np.arange(N), DOORS)
P_DOOR_AT_DOOR, P_DOOR_AT_WALL = 0.6, 0.2
KERNEL = {1: 0.1, 2: 0.8, 3: 0.1}           # cells moved -> probability, for the command "move 2"
BROWN = "#9C755F"


def likelihood(z):
    """p(z | x) for every cell; z = 1 means the sensor reads 'door', 0 means 'wall'."""
    if z:
        return np.where(DOOR, P_DOOR_AT_DOOR, P_DOOR_AT_WALL)
    return np.where(DOOR, 1 - P_DOOR_AT_DOOR, 1 - P_DOOR_AT_WALL)


def predict(bel, kernel=KERNEL):
    """Predicted belief after one move: every cell's belief is spread over the cells it can reach."""
    out = np.zeros(N)
    for step, p in kernel.items():
        out += p * np.roll(bel, step)
    return out


def update(bel_bar, z):
    """Belief after a reading: multiply by p(z | x), then divide by the sum so the bars add to 1."""
    u = likelihood(z) * bel_bar
    return u / u.sum()


def story():
    """The running example: stay still and read 'door'; move 2 and read 'door'. Returns the named beliefs."""
    b0 = np.full(N, 0.1)
    b1 = update(b0, 1)
    bb2 = predict(b1)
    b2 = update(bb2, 1)
    return b0, b1, bb2, b2


def bars(fig, values, color, row=None, col=None, ymax=0.45, labels=True, name=None, width=0.7, opacity=1.0):
    """Bar chart of one belief over the 10 cells, with the doors shaded and the numbers printed on the bars."""
    kw = dict(row=row, col=col) if row else {}
    fig.add_trace(go.Bar(x=list(range(N)), y=values, marker_color=color, width=width, opacity=opacity, name=name,
                         text=[f"{v:.2f}" for v in values] if labels else None, textposition="outside",
                         textfont=dict(size=15), cliponaxis=False), **kw)
    for d in DOORS:                             # after the trace: Plotly skips shapes on a still-empty subplot
        fig.add_vrect(x0=d - 0.5, x1=d + 0.5, fillcolor=BROWN, opacity=0.13, line_width=0, layer="below", **kw)
    fig.update_xaxes(tickmode="array", tickvals=list(range(N)), range=[-0.6, N - 0.4], **kw)
    fig.update_yaxes(range=[0, ymax], **kw)


def door_labels(fig, y, row=None, col=None, size=15):
    """Write 'door' above each door column."""
    kw = dict(row=row, col=col) if row else {}
    for d in DOORS:
        fig.add_annotation(x=d, y=y, text="door", showarrow=False, font=dict(size=size, color=BROWN), **kw)


def layout(fig, width, height, title=None, top=90):
    fig.update_layout(template="simple_white", width=width, height=height, font=FONT, showlegend=False,
                      margin=dict(l=70, r=30, t=top, b=60), bargap=0.25,
                      title=dict(text=title, x=0.5, font=dict(size=24)) if title else None)
    fig.update_annotations(selector=dict(xref="paper"), font_size=21)   # subplot titles
