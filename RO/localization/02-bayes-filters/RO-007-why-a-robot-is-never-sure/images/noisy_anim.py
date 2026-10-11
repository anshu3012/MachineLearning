"""One reading "door", played step by step for a perfect sensor (top) and the chapter's noisy sensor (bottom).
Every cell starts at 0.1. Each is multiplied by the chance of reading "door" there: 1 at a door and 0 at a wall for the
perfect sensor, 0.6 and 0.2 for the noisy one (0.06 and 0.02). The products add up to 0.3 and 0.32, and dividing by
that sum gives 0.33 at each door (walls 0) and 0.1875 at each door, 0.0625 at each wall (3 and 1 shares of 16).
Run: python noisy_anim.py -> noisy_anim.gif, noisy_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from corrdraw import DOORS
from gifkit import BLUE, FONT, ORANGE, PURPLE, make_gif
from plotly.subplots import make_subplots

here = Path(__file__).parent
door = np.array([i in DOORS for i in range(10)])
start = np.full(10, 0.1)
lik = {"perfect": np.where(door, 1.0, 0.0), "noisy": np.where(door, 0.6, 0.2)}
prod = {k: start * v for k, v in lik.items()}
total = {k: v.sum() for k, v in prod.items()}
post = {k: v / total[k] for k, v in prod.items()}
assert np.allclose(prod["noisy"][[0, 1]], [0.02, 0.06]) and np.isclose(total["noisy"], 0.32)
assert np.isclose(total["perfect"], 0.3) and np.isclose(post["perfect"][1], 1 / 3) and post["perfect"][0] == 0
assert np.allclose(post["noisy"][[1, 0]], [0.1875, 0.0625])                      # 3/16 and 1/16
TICKS = [f"{i}<br><span style='color:{ORANGE}'>door</span>" if i in DOORS else str(i) for i in range(10)]


def label(v):
    return "0.33" if np.isclose(v, 1 / 3) else f"{v:.4f}".rstrip("0").rstrip(".")


def frame(bars, title, rows, labels=True):
    """bars: (perfect, noisy) heights; rows: the two row titles."""
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.25)
    for r, (b, col) in enumerate(zip(bars, (BLUE, PURPLE)), start=1):
        fig.add_trace(go.Bar(x=np.arange(10), y=b, marker_color=col, width=0.6,
                             text=[label(v) for v in b] if labels else None, textposition="outside",
                             constraintext="none", cliponaxis=False, textfont=dict(size=18)), r, 1)
        fig.update_xaxes(tickvals=list(range(10)), ticktext=TICKS, title="cell", title_standoff=4, row=r, col=1)
        fig.update_yaxes(range=[0, 0.4], dtick=0.1, title="probability", row=r, col=1)
    for (y, text), col in zip(zip((1.03, 0.395), rows), (BLUE, PURPLE)):
        fig.add_annotation(x=0.5, y=y, xref="paper", yref="paper", text=text, showarrow=False, yanchor="bottom",
                           font=dict(size=20, color=col))
    fig.update_layout(template="simple_white", width=900, height=960, font=FONT, showlegend=False,
                      margin=dict(l=90, r=30, t=130, b=70), title=dict(text=title, x=0.5, y=0.97, font=dict(size=22)))
    return fig


def tween(a, b, k, n=3):
    s = k / (n + 1)
    return tuple((1 - s) * x + s * y for x, y in zip(a, b))


s0 = (start, start)
s1 = (prod["perfect"], prod["noisy"])
s3 = (post["perfect"], post["noisy"])
figs, holds = [frame(s0, "before the reading: no idea yet, 0.1 for each cell",
                     ["perfect sensor: 0.1 for each cell", "noisy sensor: 0.1 for each cell"])], [6]
mult = ["perfect sensor: × 1 at a door, × 0 at a wall", "noisy sensor: × 0.6 at a door, × 0.2 at a wall"]
for k in (1, 2, 3):
    figs.append(frame(tween(s0, s1, k), 'reading "door": each cell × the chance of reading "door" there', mult, False))
    holds.append(1)
figs.append(frame(s1, 'reading "door": each cell × the chance of reading "door" there', mult))
holds.append(8)
figs.append(frame(s1, "the products no longer add up to 1",
                  ["perfect sensor: sum = 3 × 0.1 = 0.3", "noisy sensor: sum = 3 × 0.06 + 7 × 0.02 = 0.32"]))
holds.append(8)
div = ["perfect sensor: each ÷ 0.3", "noisy sensor: each ÷ 0.32"]
for k in (1, 2, 3):
    figs.append(frame(tween(s1, s3, k), "divide each cell by the sum, so the ten add up to 1 again", div, False))
    holds.append(1)
figs.append(frame(s3, 'after one reading "door" (doors at cells 1, 3 and 7)',
                  ["perfect sensor: walls crossed out (each ÷ 0.3)",
                   "noisy sensor: 0.6 at a door, 0.2 at a wall (each ÷ 0.32)"]))
holds.append(20)
make_gif(figs, here / "noisy_anim", fps=4, holds=holds, keys=[0, 4, 5, len(figs) - 1], cols=2, width=900)
