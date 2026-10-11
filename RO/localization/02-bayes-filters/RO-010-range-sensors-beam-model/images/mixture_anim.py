"""The beam model built up as an animation: for the beam whose expected range is
3 m, the four weighted parts are stacked one at a time, each on top of the ones before: random readings
(0.08 x p_rand), unexpected objects (0.12 x p_short), measurement noise (0.75 x p_hit), failures (0.05 x p_max).
The last frame draws the top edge in black: the mixture, 0.049 per m at 1.00 m and 0.016 per m at 4.00 m. The
Gaussian peak (6.00 per m) and the failure spike (5.0 per m) are cut off at the top. Run -> mixture_anim.gif"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from beammodel import W, ZSTAR, mixture, p_hit, p_max, p_rand, p_short
from gifkit import BLUE, FONT, GREEN, ORANGE, PURPLE, make_gif

here = Path(__file__).parent
z = np.concatenate([np.linspace(0, 4.99, 6000), [4.9949, 4.995, 5.0]])
LAYERS = [("random readings", "rand", W["rand"] * p_rand(z), GREEN),
          ("unexpected objects", "short", W["short"] * p_short(z, ZSTAR), ORANGE),
          ("measurement noise", "hit", W["hit"] * p_hit(z, ZSTAR), BLUE),
          ("failures", "max", W["max"] * p_max(z), PURPLE)]
PEAK = float(mixture(ZSTAR, ZSTAR))


def frame(k, final=False):
    """The first k layers stacked."""
    fig = go.Figure()
    acc = np.zeros_like(z)
    for i, (name, key, y, c) in enumerate(LAYERS[:k]):
        acc = acc + y
        fig.add_trace(go.Scatter(x=z, y=acc.copy(), mode="lines", line=dict(color=c, width=2.5),
                                 fill="tozeroy" if i == 0 else "tonexty", fillcolor=c if key == "max" else None,
                                 name=f"{name}: {W[key]:.2f} × p<sub>{key}</sub>"))
    if final:
        fig.add_trace(go.Scatter(x=z, y=acc, mode="lines", line=dict(color="black", width=3),
                                 name="black top edge: the mixture"))
        for x, t in ((1.0, "1.00 m: 0.049"), (4.0, "4.00 m: 0.016")):
            fig.add_annotation(x=x, y=float(mixture(x, ZSTAR)), ax=0, ay=-90, text=t, font=dict(size=19), arrowwidth=2)
    if k == 1:
        fig.add_annotation(x=4.0, y=0.016, ax=0, ay=-90, text="0.08 × 0.2 = 0.016 per m", font=dict(size=19),
                           arrowwidth=2)
    if k >= 3:
        fig.add_annotation(x=2.85, y=0.97, text=f"peak {PEAK:.2f} at 3 m (cut off)", showarrow=False,
                           xanchor="right", yanchor="top", font_size=19)
    if k >= 4:
        fig.add_annotation(x=4.97, y=0.97, text="spike 5.0 at 5 m (cut off)", showarrow=False, xanchor="right",
                           yanchor="top", font_size=19)
    name, key, _, _ = LAYERS[k - 1]
    title = ("the beam model: the black top edge is the mixture" if final else
             f"step {k}: add {name}, weight {W[key]:.2f}")
    fig.update_layout(template="simple_white", width=1000, height=600, font=FONT, title=dict(text=title, x=0.5),
                      margin=dict(l=80, r=30, t=70, b=70), showlegend=True,
                      legend=dict(x=0.02, y=0.82, bgcolor="rgba(255,255,255,0.85)", font_size=19))
    fig.update_xaxes(title="reading z (m)", range=[0, 5.08], dtick=0.5)
    fig.update_yaxes(title="density (per m)", range=[0, 1.0])
    return fig


figs = [frame(k) for k in (1, 2, 3, 4)] + [frame(4, final=True)]
make_gif(figs, here / "mixture_anim", fps=2, holds=[5, 5, 5, 5, 14], keys=[1, 4], cols=2, width=900)
assert round(float(mixture(1.0, ZSTAR)), 3) == 0.049 and round(float(mixture(4.0, ZSTAR)), 3) == 0.016
assert round(W["rand"] * 0.2, 3) == 0.016 and round(W["max"] * float(p_max(5.0)), 1) == 5.0 and round(PEAK, 2) == 6.00
