"""The Bayes filter on the door world, two time steps. Start 0.5/0.5. t = 1: do nothing (predicted 0.5/0.5), sense
open (0.75/0.25). t = 2: push (predicted 0.95/0.05), sense open (0.983/0.017). Orange: predicted belief; blue: belief.
Run: python door_filter.py -> door_filter.gif, door_filter_frames.png"""
from pathlib import Path

import plotly.graph_objects as go

from doorplot import door_bars, predict, update
from gifkit import BLUE, FONT, ORANGE, make_gif

here = Path(__file__).parent
b0 = {"open": 0.5, "closed": 0.5}
bb1 = predict(b0, "do nothing")
b1 = update(bb1, "open")
bb2 = predict(b1, "push")
b2 = update(bb2, "open")
assert abs(bb2["open"] - 0.95) < 1e-12 and abs(b2["open"] - 0.57 / 0.58) < 1e-12

STAGES = [("start: no idea", "belief at t = 0", b0, BLUE),
          ("t = 1, predict: u<sub>1</sub> = do nothing", "predicted belief: nothing changed", bb1, ORANGE),
          ("t = 1, correct: z<sub>1</sub> = sense open", "belief: open is more likely", b1, BLUE),
          ("t = 2, predict: u<sub>2</sub> = push", "predicted belief: a push opens a closed door", bb2, ORANGE),
          ("t = 2, correct: z<sub>2</sub> = sense open", "belief: almost sure it is open", b2, BLUE)]


def frame(title, sub, bel, color):
    fig = go.Figure()
    door_bars(fig, bel, color)
    fig.update_yaxes(title="probability")
    fig.update_layout(template="simple_white", width=760, height=520, font=FONT, showlegend=False,
                      margin=dict(l=80, r=30, t=110, b=50),
                      title=dict(text=f"{title}<br><span style='font-size:19px'>{sub}</span>", x=0.5,
                                 font=dict(size=24)))
    return fig


figs, holds, keys, prev = [], [], [], None
for title, sub, bel, color in STAGES:
    if prev is not None:
        for a in (0.33, 0.67):
            mix = {k: (1 - a) * prev[k] + a * bel[k] for k in bel}
            figs.append(frame(title, sub, mix, color))
            holds.append(1)
    keys.append(len(figs))
    figs.append(frame(title, sub, bel, color))
    holds.append(10)
    prev = bel
holds[-1] = 18
make_gif(figs, here / "door_filter", fps=5, holds=holds, keys=keys[1:], cols=2, width=700)
