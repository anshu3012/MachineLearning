"""Figure 6: the prediction step on the continuous hallway, built slice by slice. Top: the old belief after one
"door" reading (0.1875 per m at a door, 0.0625 per m at a wall), cut into 50 slices of 0.2 m. Each slice's
probability (density x 0.2 m) moves 2 m on and is spread by the motion model (a Gaussian, standard deviation 0.45 m);
that green piece is stacked on the orange pile below, the predicted belief. Slices 0-2 m go one at a time, the rest
a metre at a time; pieces that pass 10 m come back at 0 m (the hallway is a loop). Last frame: the predicted belief,
three bumps moved 2 m, peak 0.154 per m instead of 0.1875, area 1, against the old belief moved 2 m without spreading.
Run -> predict_cont_anim.gif, predict_cont_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from gifkit import BLUE, FONT, GREEN, ORANGE, make_gif
from hallcont import AT_DOOR, AT_WALL, BROWN, DOORS, LOOP, SIGMA, U, X, old_belief, piece, predicted

here = Path(__file__).parent
W = 0.2                                                                     # slice width (m)
SLICES = [(round(i * W, 1), round((i + 1) * W, 1)) for i in range(int(LOOP / W))]
LIGHT_BLUE = "#B9CCE0"
pred = predicted()

# every number the text or the frames quote
assert np.isclose(AT_DOOR * W, 0.0375) and np.isclose(AT_WALL * W, 0.0125)
n_door = sum(float(old_belief((a + b) / 2)) == AT_DOOR for a, b in SLICES)
assert len(SLICES) == 50 and n_door == 15 and np.isclose(15 * 0.0375 + 35 * 0.0125, 1)
assert np.isclose(5 * 0.0125, 0.0625) and np.isclose(5 * 0.0375, 0.1875)
assert np.allclose(sum(piece(a, b) for a, b in SLICES), pred)            # the 50 pieces add up to the integral
assert abs(np.trapezoid(pred, X) - 1) < 1e-6                                # area still 1
peaks = [X[i] for i in range(1, len(X) - 1) if pred[i] >= pred[i - 1] and pred[i] > pred[i + 1]]
assert np.allclose(peaks, [3.5, 5.5, 9.5], atol=0.01), peaks                # the bumps moved from 1.5, 3.5, 7.5 m
assert round(float(np.interp(3.5, X, pred)), 3) == 0.154 and round(pred.max(), 3) == 0.154
assert U == 2.0 and SIGMA == 0.45
YMAX = 0.25


def kind(a, b):
    return "door" if float(old_belief((a + b) / 2)) == AT_DOOR else "wall"


def frame(title, sub, done, cur, arrow=None, final=False):
    """done: slices already added; cur: the slices added in this frame (green); arrow: (from, to) for the +2 m."""
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.12)
    old = old_belief(X)
    fig.add_trace(go.Scatter(x=X, y=old, mode="lines", line=dict(color=BLUE, width=2), fill="tozeroy",
                             fillcolor=BLUE), row=1, col=1)
    if done and not final:
        hi = max(b for a, b in done)
        m = X <= hi
        fig.add_trace(go.Scatter(x=X[m], y=old[m], mode="lines", line=dict(color=LIGHT_BLUE, width=2),
                                 fill="tozeroy", fillcolor=LIGHT_BLUE), row=1, col=1)
    if cur:
        a0, b1 = cur[0][0], cur[-1][1]
        m = (X >= a0) & (X <= b1)
        fig.add_trace(go.Scatter(x=X[m], y=old[m], mode="lines", line=dict(color=GREEN, width=2), fill="tozeroy",
                                 fillcolor=GREEN), row=1, col=1)
    before = sum((piece(a, b) for a, b in done), np.zeros_like(X))
    after = before + sum((piece(a, b) for a, b in cur), np.zeros_like(X))
    fig.add_trace(go.Scatter(x=X, y=before, mode="lines", line=dict(color=ORANGE, width=2), fill="tozeroy",
                             fillcolor=ORANGE), row=2, col=1)
    if cur:
        fig.add_trace(go.Scatter(x=X, y=after, mode="lines", line=dict(color=GREEN, width=2), fill="tonexty",
                                 fillcolor=GREEN), row=2, col=1)
    if arrow:
        fig.add_annotation(x=arrow[1], y=0.2, ax=arrow[0], ay=0.2, xref="x2", yref="y2", axref="x2", ayref="y2",
                           text="", showarrow=True, arrowhead=2, arrowsize=1.3, arrowwidth=3, arrowcolor=GREEN)
        fig.add_annotation(x=sum(arrow) / 2, y=0.2, yanchor="bottom", xref="x2", yref="y2", text="+2 m",
                           showarrow=False, font=dict(size=20, color=GREEN))
    if final:
        fig.add_trace(go.Scatter(x=X, y=old_belief(X - U), mode="lines", line=dict(color=BLUE, width=3, dash="dash")),
                      row=2, col=1)
        fig.add_annotation(x=3.5, y=0.11, text="0.154", showarrow=False, xref="x2", yref="y2",
                           font=dict(size=21, color="white"))
        key2 = (f"<span style='color:{ORANGE}'>orange: predicted belief</span>   "
                f"<span style='color:{BLUE}'>dashed: old belief moved 2 m, not spread</span>")
        key1 = f"<span style='color:{BLUE}'>blue: old belief</span>"
    else:
        key1 = (f"<span style='color:{BLUE}'>blue: old belief</span>   <span style='color:{GREEN}'>green: "
                f"this slice</span>   <span style='color:#7F9CBF'>light blue: slices already added</span>")
        key2 = (f"<span style='color:{ORANGE}'>orange: predicted belief so far</span>   "
                f"<span style='color:{GREEN}'>green: the piece this slice adds</span>")
    for a, b in DOORS:                   # after the traces: Plotly skips shapes on a still-empty subplot
        for r in (1, 2):
            fig.add_vrect(x0=a, x1=b, fillcolor=BROWN, opacity=0.13, line_width=0, layer="below", row=r, col=1)
        fig.add_annotation(x=(a + b) / 2, y=0.235, text="door", showarrow=False, font=dict(size=17, color=BROWN),
                           row=1, col=1)
    for r, key in ((1, key1), (2, key2)):
        fig.add_annotation(xref=f"x{'' if r == 1 else 2} domain", yref=f"y{'' if r == 1 else 2} domain", x=0,
                           y=1.02, xanchor="left", yanchor="bottom", showarrow=False, text=key, font=dict(size=17))
    fig.update_xaxes(range=[0, LOOP], dtick=1, row=1, col=1)
    fig.update_xaxes(range=[0, LOOP], dtick=1, title="position (m)", row=2, col=1)
    fig.update_yaxes(range=[0, YMAX], dtick=0.05, title="old belief (per m)", row=1, col=1)
    fig.update_yaxes(range=[0, YMAX], dtick=0.05, title="predicted (per m)", row=2, col=1)
    fig.update_layout(template="simple_white", width=1100, height=880, font=FONT, showlegend=False,
                      margin=dict(l=90, r=30, t=125, b=70),
                      title=dict(text=f"{title}<br><span style='font-size:19px'>{sub}</span>", x=0.5, y=0.98,
                                 yanchor="top", font=dict(size=24)))
    return fig


figs, holds, keys = [], [], []


def add(f, hold, key=False):
    if key:
        keys.append(len(figs))
    figs.append(f)
    holds.append(hold)


add(frame("prediction on the continuous hallway: move 2 m",
          "top: old belief after one door reading; bottom: predicted belief, built from 50 slices of 0.2 m", [], []),
    12, key=True)
done = []
for i, (a, b) in enumerate(SLICES[:10]):                         # 0-2 m, one slice at a time
    k = kind(a, b)
    lev = AT_DOOR if k == "door" else AT_WALL
    first = i in (0, 5)
    c = round((a + b) / 2 + U, 1)
    sub = (f"it moves 2 m on and spreads: its green piece, around {c:g} m, has area {lev * W:.4f}" if first else
           f"its piece lands around {c:g} m and stacks on the pile")
    if i == 5:
        sub = f"3 times a wall slice: its piece, around {c:g} m, has area {lev * W:.4f}"
    add(frame(f"slice {a:.1f}–{b:.1f} m ({k}): {lev:g} × 0.2 = {lev * W:.4f}", sub, list(done), [(a, b)],
              arrow=((a + b) / 2, (a + b) / 2 + U)), 11 if first else 4, key=first)
    done.append((a, b))
for m in range(2, int(LOOP)):                                    # 2-10 m, a metre (5 slices) at a time
    cur = [s for s in SLICES if m <= s[0] < m + 1]
    k = kind(m, m + 1)
    lev = AT_DOOR if k == "door" else AT_WALL
    c = m + 0.5 + U
    if c < LOOP:
        sub, arrow = f"their pieces land around {c:g} m", (m + 0.5, c)
    else:
        sub, arrow = f"past 10 m the loop goes on at 0 m: they land around {c - LOOP:g} m ({c:g} m)", None
    add(frame(f"slices {m}–{m + 1} m (5 {k} slices): 5 × {lev * W:.4f} = {5 * lev * W:.4f}", sub, list(done), cur,
              arrow=arrow), 9 if c >= LOOP else 6, key=m in (3, 9))
    done += cur
assert len(done) == 50
add(frame("predicted belief: moved 2 m, lower and wider",
          "all 50 slices added, area 1; peak 0.154 per m at 3.5 m (old peak 0.1875)", done, [], final=True),
    28, key=True)
make_gif(figs, here / "predict_cont_anim", fps=5, holds=holds, keys=keys, cols=2, width=900)
