"""Bayes' proof on the two-dice grid (Plotly): the 5 cells of A and B together, read once inside A and once inside B.
A = die 1 shows 5, B = the sum is at most 10. P(A and B) = 5/36 = P(B|A) P(A) = P(A|B) P(B)."""
from fractions import Fraction as F
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
cells = [(d1, d2) for d1 in range(1, 7) for d2 in range(1, 7)]
A = {c for c in cells if c[0] == 5}
B = {c for c in cells if sum(c) <= 10}
AB = A & B
assert (len(A), len(B), len(AB)) == (6, 33, 5)
assert F(len(AB), len(A)) == F(5, 6) and F(len(AB), len(B)) == F(5, 33)
assert F(5, 6) * F(1, 6) == F(5, 33) * F(11, 12) == F(5, 36)   # equation (2) both ways

BLUE, ORANGE, RED, GREY = "#4C78A8", "#F58518", "#E45756", "#E8E8E8"
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08,
                    subplot_titles=("look inside A (die 1 = 5):<br>5 of its 6 cells are in B → P(B | A) = 5/6",
                                    "look inside B (sum ≤ 10):<br>5 of its 33 cells are in A → P(A | B) = 5/33"))
for col, inside in ((1, A), (2, B)):
    for (d1, d2) in cells:
        fill = RED if (d1, d2) in AB else (ORANGE if (d1, d2) in inside else GREY)
        fig.add_shape(type="rect", x0=d1 - 0.45, x1=d1 + 0.45, y0=d2 - 0.45, y1=d2 + 0.45, fillcolor=fill,
                      line=dict(width=0), opacity=1, layer="below", row=1, col=col)
    fig.add_trace(go.Scatter(x=[c[0] for c in cells], y=[c[1] for c in cells], mode="text",
                             text=[str(sum(c)) for c in cells], textfont=dict(size=17, color="black"),
                             showlegend=False), 1, col)
for name, c in (("the 5 cells of A and B", RED), ("rest of the region we look inside", ORANGE), ("outside", GREY)):
    fig.add_trace(go.Scatter(x=[None], y=[None], mode="markers", name=name,
                             marker=dict(symbol="square", size=18, color=c)))
fig.update_xaxes(title="die 1", tickvals=list(range(1, 7)), range=[0.4, 6.6], showline=False)
fig.update_yaxes(title="die 2", tickvals=list(range(1, 7)), range=[0.4, 6.6], scaleanchor="x", showline=False)
fig.update_yaxes(title=None, row=1, col=2, scaleanchor="x2")
fig.update_layout(template="simple_white", width=1100, height=680, font=dict(family="Latin Modern Roman", size=19),
                  title=dict(text="Same 5 cells, two readings:  5/6 × 6/36  =  5/33 × 33/36  =  5/36", x=0.5, y=0.97),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2),
                  margin=dict(l=60, r=20, t=130, b=140))
fig.update_annotations(font_size=19)
fig.write_image(here / "dice_two_ways.png", scale=2)
