"""The sum and product rules as vector additions (Plotly), at x = (1, 1). Left, sum rule: the gradient of
f(x) + a^T x is grad f = [3, 5] plus a^T = [1, 2], which is [4, 7]. Right, product rule for (a^T x)(b^T x) with
a = [1, 2], b = [3, -1]: the gradient is (b^T x) a^T + (a^T x) b^T = 2 [1, 2] + 3 [3, -1] = [11, 1]."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREEN, ORANGE, RED

here = Path(__file__).parent
a, b, x = np.array([1, 2]), np.array([3, -1]), np.array([1, 1])
gf = np.array([2 * x[0] + x[1], x[0] + 4 * x[1]])
prod = (b @ x) * a + (a @ x) * b
assert list(gf) == [3, 5] and list(gf + a) == [4, 7] and list(prod) == [11, 1]
fig = make_subplots(1, 2, horizontal_spacing=0.1, subplot_titles=["sum rule: ∇(f + aᵀx) = ∇f + aᵀ",
                                                                   "product rule: (bᵀx) aᵀ + (aᵀx) bᵀ"])
fig.update_annotations(font_size=21)


def arrow(col, start, end, color, text, pos):
    ax, ay = ("x", "y") if col == 1 else ("x2", "y2")
    fig.add_annotation(x=end[0], y=end[1], ax=start[0], ay=start[1], xref=ax, yref=ay, axref=ax, ayref=ay, arrowhead=3,
                       arrowsize=1.3, arrowwidth=4, arrowcolor=color, showarrow=True)
    mid = (np.array(start) + np.array(end)) / 2
    fig.add_annotation(x=mid[0], y=mid[1], xref=ax, yref=ay, text=text, showarrow=False, font=dict(size=19, color=color),
                       xshift=pos[0], yshift=pos[1])


arrow(1, (0, 0), gf, BLUE, "∇f = [3, 5]", (-55, 0))
arrow(1, gf, gf + a, ORANGE, "aᵀ = [1, 2]", (55, -5))
arrow(1, (0, 0), gf + a, GREEN, "sum [4, 7]", (50, -15))
arrow(2, (0, 0), 2 * a, BLUE, "2 × [1, 2]", (-45, 10))
arrow(2, 2 * a, 2 * a + 3 * b, ORANGE, "3 × [3, −1]", (10, 22))
arrow(2, (0, 0), prod, GREEN, "∇ = [11, 1]", (0, -20))
fig.update_xaxes(range=[-1, 6], zeroline=True, row=1, col=1)
fig.update_yaxes(range=[-1, 8], zeroline=True, scaleanchor="x", row=1, col=1)
fig.update_xaxes(range=[-1, 12], zeroline=True, row=1, col=2)
fig.update_yaxes(range=[-1.5, 5.5], zeroline=True, scaleanchor="x2", row=1, col=2)
fig.update_layout(template="simple_white", width=1250, height=560, font=FONT, showlegend=False,
                  margin=dict(l=50, r=20, t=60, b=50))
fig.write_image(here / "rule_arrows.png", scale=2)
