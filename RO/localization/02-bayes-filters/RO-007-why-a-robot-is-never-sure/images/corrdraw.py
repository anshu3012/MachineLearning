"""Shared helper for this Note's Plotly figures: the hallway of the chapter (10 cells of 1 m in a loop, doors at cells
1, 3 and 7) drawn above a bar chart of the robot's probability for each cell, and the move and sensor models of the
chapter (no output when run on its own)."""
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from gifkit import BLUE, FONT, GREY, ORANGE, PURPLE, RED

DOORS = [1, 3, 7]
MOVE = {1: 0.1, 2: 0.8, 3: 0.1}          # "move 2": 1 cell 10 %, 2 cells 80 %, 3 cells 10 % (Labbe ch.2)
SENSE_DOOR = {True: 0.6, False: 0.2}     # P(reading "door" | door cell), P(reading "door" | wall cell)


def predict(b):
    """Belief after one noisy "move 2" in the loop: every cell spreads to +1, +2, +3 cells (cell 9 + 1 = cell 0)."""
    out = np.zeros(len(b))
    for i, p in enumerate(b):
        for d, q in MOVE.items():
            out[(i + d) % len(b)] += p * q
    return out


def panel(b, title, truth=None, n=10, ymax=1.05, bar_color=BLUE, labels=True, guess=None, guess_text="best guess"):
    """Corridor on top, belief bars below. truth: the robot's true position (red robot), or None.
    guess: the position a one-guess robot believes in (purple triangle), or None."""
    fig = make_subplots(rows=2, cols=1, row_heights=[0.32, 0.68], vertical_spacing=0.08, shared_xaxes=True)
    for y in (0, 1):
        fig.add_trace(go.Scatter(x=[-0.5, n - 0.5], y=[y, y], mode="lines", line=dict(color="black", width=4)), 1, 1)
    for d in DOORS:
        if d < n:
            fig.add_trace(go.Scatter(x=[d - 0.3, d + 0.3], y=[1, 1], mode="lines", line=dict(color=ORANGE, width=12)), 1, 1)
            fig.add_annotation(x=d, y=1.32, text="door", showarrow=False, font=dict(color=ORANGE, size=18), row=1, col=1)
    if truth is not None:
        fig.add_trace(go.Scatter(x=[truth], y=[0.5], mode="markers", marker=dict(symbol="square", size=26, color=RED)), 1, 1)
        fig.add_annotation(x=truth, y=-0.35, text="true cell", showarrow=False, font=dict(color=RED, size=16),
                           row=1, col=1)
    if guess is not None:
        fig.add_trace(go.Scatter(x=[guess], y=[0.5], mode="markers",
                                 marker=dict(symbol="triangle-up", size=26, color=PURPLE)), 1, 1)
        fig.add_annotation(x=guess, y=-0.35, text=guess_text, showarrow=False, font=dict(color=PURPLE, size=16),
                           row=1, col=1)
    xs = np.arange(n)
    fig.add_trace(go.Bar(x=xs, y=b[:n], marker_color=bar_color, width=0.6,
                         text=[f"{v:.3f}".rstrip("0").rstrip(".") if v >= 0.005 and labels else "" for v in b[:n]],
                         textposition="outside", constraintext="none", cliponaxis=False, textfont=dict(size=18)), 2, 1)
    fig.update_yaxes(visible=False, range=[-0.6, 1.6], row=1, col=1)
    fig.update_yaxes(range=[0, ymax], title="probability", row=2, col=1)
    fig.update_xaxes(tickvals=list(xs), range=[-0.6, n - 0.4], row=2, col=1, title="cell (1 m each; right of cell 9 is cell 0)")
    fig.update_xaxes(visible=False, row=1, col=1)
    fig.update_layout(template="simple_white", width=900, height=640, font=FONT, showlegend=False,
                      margin=dict(l=90, r=30, t=110, b=70), title=dict(text=title, x=0.5, y=0.95, font=dict(size=22)))
    return fig
