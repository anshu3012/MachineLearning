"""P(A | B) against P(B | A) on the two-dice grid (Plotly). A: die 1 shows 5. B: the sum is at most 10. Left: given B,
the world is B's 33 cells, and A covers 5 of them (5/33). Right: given A, the world is A's 6 cells, and B covers 5 of
them (5/6). Cells outside the world are grey."""
from fractions import Fraction
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, RED

here = Path(__file__).parent
d1, d2 = np.meshgrid(range(1, 7), range(1, 7), indexing="ij")
A, B = d1 == 5, d1 + d2 <= 10
assert Fraction(int((A & B).sum()), int(B.sum())) == Fraction(5, 33) and Fraction(int((A & B).sum()), int(A.sum())) == Fraction(5, 6)
fig = make_subplots(1, 2, horizontal_spacing=0.1, subplot_titles=["given B: A covers 5 of 33 cells, P(A | B) = 5/33",
                                                                  "given A: B covers 5 of 6 cells, P(B | A) = 5/6"])
fig.update_annotations(font_size=21)
for col, world, target in ((1, B, A), (2, A, B)):
    z = np.where(~world, 0, np.where(target, 2, 1))
    fig.add_trace(go.Heatmap(x=list(range(1, 7)), y=list(range(1, 7)), z=z.T, zmin=0, zmax=2, showscale=False, xgap=3, ygap=3,
                             colorscale=[[0, "#E6E6E6"], [0.5, "#C9D7E8"], [1, RED]],
                             text=(d1 + d2).T, texttemplate="%{text}", textfont=dict(size=16)), 1, col)
    fig.update_xaxes(title="die 1", dtick=1, row=1, col=col)
    fig.update_yaxes(title="die 2" if col == 1 else None, dtick=1, scaleanchor=f"x{col if col > 1 else ''}", row=1, col=col)
fig.update_layout(template="simple_white", width=1200, height=600, font=FONT, margin=dict(l=70, r=20, t=60, b=70))
fig.write_image(here / "swap.png", scale=2)
