"""One step command, three step responses. The speed command steps from 0 to 0.5 m/s and the P speed loop
(Kv = 6 N per m/s) responds. Left: the speed rises to a level (0.375 m/s). Middle: the distance driven grows like a
ramp and never settles. Right: the drive force jumps to 3 N and falls to 0.75 N. All three are drawn over time.
Run: python shapes_anim.py -> shapes_anim.gif, shapes_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, ORANGE, PURPLE, make_gif
from stepkit import B, KP_V, V_REF, speed_p

here = Path(__file__).parent
t = np.linspace(0, 8, 8001)
v = speed_p(t)
x = 0.375 * (t - (1 - np.exp(-t)))                     # distance: the integral of the speed
u = KP_V * (V_REF - v)                                  # the force the P controller commands
assert abs(u[0] - 3) < 1e-12 and abs(u[-1] - 0.75) < 1e-3 and abs(B * 0.375 - 0.75) < 1e-12
assert np.allclose(np.gradient(x, t), v, atol=1e-3)
PANELS = [("speed v (m/s)", v, [0, 0.55], BLUE, "rises to a level,<br>like the command"),
          ("distance driven (m)", x, [0, 3.2], PURPLE, "a ramp: never settles,<br>no settling time"),
          ("drive force u (N)", u, [0, 3.3], ORANGE, "jumps to 3 N, falls to 0.75 N:<br>overshoot means nothing here")]


def frame(frac, last=False):
    fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.09, subplot_titles=[p[0] for p in PANELS])
    k = int(frac * (len(t) - 1))
    for c, (_, y, rng, col, note) in enumerate(PANELS, start=1):
        fig.add_trace(go.Scatter(x=t[:k + 1], y=y[:k + 1], mode="lines", line=dict(color=col, width=4)), 1, c)
        fig.add_trace(go.Scatter(x=[t[k]], y=[y[k]], mode="markers", marker=dict(color=col, size=12)), 1, c)
        if last:
            fig.add_annotation(x=7.8, y=rng[1] * (0.12 if c == 2 else 0.97), text=note, showarrow=False,
                               xanchor="right", yanchor="bottom" if c == 2 else "top", font=dict(size=18, color=col),
                               bgcolor="rgba(255,255,255,0.85)", row=1, col=c)
        fig.update_yaxes(range=rng, row=1, col=c)
    fig.update_xaxes(title="time t (s)", range=[0, 8])
    fig.update_layout(template="simple_white", font=FONT, width=1300, height=560, showlegend=False,
                      margin=dict(l=60, r=30, t=130, b=70),
                      title=dict(x=0.5, y=0.95, text=f"speed command steps 0 → 0.5 m/s at t = 0:   t = {t[k]:.1f} s"))
    fig.update_annotations(selector=dict(showarrow=False, xref="paper"), font_size=20, font_color=GREY)
    return fig


fr = np.linspace(0, 1, 25)
figs = [frame(f) for f in fr] + [frame(1, last=True)]
make_gif(figs, here / "shapes_anim", fps=6, holds=[6] + [1] * 24 + [30], keys=[6, 25], cols=1, width=950)
