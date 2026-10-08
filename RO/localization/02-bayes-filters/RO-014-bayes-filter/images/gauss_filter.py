"""The two Bayes-filter steps on a continuous position along a hallway, computed on a 1 cm grid.
Belief before: Gaussian, mean 0 m, sd 0.6 m. Predict with 'drive 3 m' (sd 0.9 m): the curve slides to 3 m and widens
to sd 1.08 m. Correct with the reading 3.6 m (sd 0.7 m): multiply and normalise -> mean 3.42 m, sd 0.59 m, narrower
than both inputs. Run: python gauss_filter.py -> gauss_filter.gif, gauss_filter_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, make_gif

here = Path(__file__).parent
x = np.arange(-3, 8, 0.01)
dx = 0.01


def gauss(m, s):
    return np.exp(-0.5 * ((x - m) / s) ** 2) / (s * np.sqrt(2 * np.pi))


def mean_sd(p):
    m = (x * p).sum() * dx
    return m, np.sqrt(((x - m) ** 2 * p).sum() * dx)


prior = gauss(0, 0.6)
MOTION = np.exp(-0.5 * ((x[:, None] - x[None, :] - 3) / 0.9) ** 2) / (0.9 * np.sqrt(2 * np.pi))
predicted = MOTION @ prior * dx                              # sum over every previous position
reading = gauss(3.6, 0.7)
post = reading * predicted
post /= post.sum() * dx
mp, sp = mean_sd(predicted)
mq, sq = mean_sd(post)
assert abs(sp - 1.0817) < 1e-3 and abs(sq - 0.5877) < 1e-3 and abs(mq - 3.423) < 1e-3


def frame(title, curves):
    fig = go.Figure()
    for y, color, name, dash in curves:
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(color=color, width=4, dash=dash), name=name))
    fig.update_xaxes(title="position along the hallway (m)", range=[-3, 7.5], dtick=1)
    fig.update_yaxes(title="probability density (per m)", range=[0, 0.75])
    fig.update_layout(template="simple_white", width=1000, height=540, font=FONT,
                      legend=dict(x=0.99, xanchor="right", y=0.99, font=dict(size=19)), margin=dict(l=80, r=30, t=80, b=60),
                      title=dict(text=title, x=0.5, font=dict(size=23)))
    return fig


before = (prior, BLUE, "belief before: sd 0.60 m", "solid")
figs, holds, keys = [frame("Belief before the move: mean 0 m, sd 0.60 m", [before])], [8], [0]
for a in np.linspace(0.2, 1, 5):                             # slide and widen
    mid = np.exp(-0.5 * ((x - 3 * a) / np.hypot(0.6, 0.9 * np.sqrt(a))) ** 2) / (np.hypot(0.6, 0.9 * np.sqrt(a)) * np.sqrt(2 * np.pi))
    y = predicted if a == 1 else mid
    figs.append(frame("Predict: drive 3 m (sd 0.9 m). The belief slides and widens",
                      [(prior, GREY, "belief before: sd 0.60 m", "dot"), (y, ORANGE, "predicted", "solid")]))
    holds.append(2)
holds[-1] = 8
keys.append(len(figs) - 1)
pred = (predicted, ORANGE, f"predicted: sd {sp:.2f} m", "solid")
read = (reading, GREEN, "reading 3.6 m alone: sd 0.70 m", "dash")
figs.append(frame("A reading arrives: 3.6 m (sd 0.7 m)", [pred, read]))
holds.append(8)
for a in np.linspace(0.25, 1, 4):                            # blend towards the normalised product
    y = (1 - a) * predicted + a * post
    figs.append(frame("Correct: multiply the two curves, then rescale to area 1", [pred, read, (y, BLUE, "after the reading", "solid")]))
    holds.append(2)
figs.append(frame(f"After the reading: mean {mq:.2f} m, sd {sq:.2f} m, narrower than both",
                  [pred, read, (post, BLUE, f"after the reading: sd {sq:.2f} m", "solid")]))
holds.append(20)
keys.append(len(figs) - 1)
make_gif(figs, here / "gauss_filter", fps=5, holds=holds, keys=[0, keys[1], len(figs) - 6, len(figs) - 1], cols=2, width=850)
