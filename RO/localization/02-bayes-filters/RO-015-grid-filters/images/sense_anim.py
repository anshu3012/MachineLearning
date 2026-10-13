"""The sense step of the histogram filter, animated. The robot has no idea where it is
(0.1 in every cell) and reads 'door'. 1. prior 0.1; 2. each bar is multiplied by p(door | cell), 0.6 at a door and
0.2 at a wall, and shrinks to 0.06 or 0.02; 3. the 10 products stack into one column, 3 x 0.06 + 7 x 0.02 = 0.32;
4. every product is divided by 0.32 and grows to 0.1875 (door) or 0.0625 (wall), the new belief.
Run: python sense_anim.py -> sense_anim.gif, sense_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

from gifkit import BLUE, GREEN, GREY, ORANGE, make_gif
from hallplot import BROWN, DOOR, DOORS, N, layout, likelihood

here = Path(__file__).parent
prior = np.full(N, 0.1)
lik = likelihood(1)
prod = lik * prior
post = prod / prod.sum()
assert np.allclose(prod[DOOR], 0.06) and np.allclose(prod[~DOOR], 0.02) and abs(prod.sum() - 0.32) < 1e-12
assert np.allclose(post[DOOR], 0.1875) and np.allclose(post[~DOOR], 0.0625) and abs(post.sum() - 1) < 1e-12
SUM_X, YMAX = 11, 0.36


def frame(head, line2, vals, color, labels=None, label_color="black", stack=0, hot=None, prior_line=False):
    """vals: the 10 bars; stack: how many products are already in the sum column; hot: the cell being added."""
    fig = go.Figure()
    fig.add_bar(x=list(range(N)), y=vals, width=0.7, cliponaxis=False,
                marker_color=[ORANGE if i == hot else color for i in range(N)],
                text=labels, textposition="outside", textfont=dict(size=17, color=label_color))
    for d in DOORS:
        fig.add_vrect(x0=d - 0.5, x1=d + 0.5, fillcolor=BROWN, opacity=0.13, line_width=0, layer="below")
        fig.add_annotation(x=d, y=YMAX * 0.95, text="door", showarrow=False, font=dict(size=16, color=BROWN))
    base = 0.0
    for i in range(stack):                        # the sum column, one segment per product
        fig.add_shape(type="rect", x0=SUM_X - 0.35, x1=SUM_X + 0.35, y0=base, y1=base + prod[i],
                      fillcolor=ORANGE if i == hot else GREY, opacity=1, line=dict(color="white", width=1.5))
        base += prod[i]
    if stack:
        fig.add_annotation(x=SUM_X, y=base, text=f"<b>{base:.2f}</b>", showarrow=False, yanchor="bottom", yshift=4,
                           font=dict(size=19))
    if prior_line:                                # where every bar started
        fig.add_shape(type="line", x0=-0.5, x1=N - 0.5, y0=0.1, y1=0.1, line=dict(color=GREY, width=2, dash="dash"))
        fig.add_annotation(x=N - 0.55, y=0.1, text="prior 0.1", showarrow=False, xanchor="right", yanchor="bottom",
                           yshift=3, font=dict(size=16, color=GREY))
    fig.update_xaxes(tickvals=list(range(N)) + [SUM_X], ticktext=[str(i) for i in range(N)] + ["sum"],
                     range=[-0.6, SUM_X + 0.6], title="cell")
    fig.update_yaxes(range=[0, YMAX], title="probability", dtick=0.05)
    layout(fig, 1100, 640, title=f"{head}<br><span style='font-size:19px;color:{GREY}'>{line2}</span>", top=110)
    return fig


two = lambda v: [f"{x:.2f}" for x in v]
figs, holds = [], []
figs.append(frame("1. prior: 0.1 in every cell", "the robot has no information about where it is; it reads 'door'",
                  prior, BLUE, two(prior)))
holds.append(8)
times = [f"× {x:.1f}" for x in lik]
figs.append(frame("2. times p(door | cell)", "0.6 at a door, 0.2 at a wall", prior, BLUE, times, GREEN))
holds.append(7)
for s in (1 / 3, 2 / 3):                          # the bars shrink
    figs.append(frame("2. times p(door | cell)", "0.6 at a door, 0.2 at a wall", prior + s * (prod - prior), GREY))
    holds.append(1)
products = "door cell: 0.1 × 0.6 = 0.06      wall cell: 0.1 × 0.2 = 0.02"
figs.append(frame("2. times p(door | cell)", products, prod, GREY, two(prod)))
holds.append(8)
key = [0, 1]
for i in range(N):                                # the products stack into the sum, one cell at a time
    so_far = prod[:i + 1].sum()
    figs.append(frame("3. add the 10 products", f"cells 0 to {i}: sum so far {so_far:.2f}", prod, GREY, two(prod),
                      stack=i + 1, hot=i))
    holds.append(2)
figs.append(frame("3. add the 10 products", "3 × 0.06 + 7 × 0.02 = 0.32", prod, GREY, two(prod), stack=N))
holds.append(8)
key.append(len(figs) - 1)
div = "door cell: 0.06 / 0.32 = 0.1875      wall cell: 0.02 / 0.32 = 0.0625"
for s in (1 / 3, 2 / 3):                          # the bars grow
    figs.append(frame("4. divided by 0.32: the new belief", div, prod + s * (post - prod), BLUE, stack=N))
    holds.append(1)
figs.append(frame("4. divided by 0.32: the new belief", div + "; the 10 cells add to 1", post, BLUE,
                  [f"{x:.4f}" for x in post], stack=N, prior_line=True))
holds.append(24)
key.append(len(figs) - 1)
make_gif(figs, here / "sense_anim", fps=4, holds=holds, keys=key, cols=2, width=900)
