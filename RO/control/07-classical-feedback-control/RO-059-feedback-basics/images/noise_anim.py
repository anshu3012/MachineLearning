"""Animation: the price of feedback. The closed loop on the ramp, now with sensor noise: each 10 ms speed reading is the
true speed plus a random error of typical size 0.02 m/s (seed 1). Two seconds after the loop has settled (t = 10 to
12 s), ten readings per frame. Top: readings (orange dots) and true speed (blue). Bottom: the force the controller asks
for (blue) against 1.713 N, its value without noise (grey). The last frame gives the jitter over t = 10 to 30 s:
readings 0.020 m/s, force 0.40 N, true speed 0.002 m/s. Run -> noise_anim.gif, noise_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import speedkit as s
from gifkit import BLUE, FONT, GREY, ORANGE, make_gif

here = Path(__file__).parent
R = s.run(30, closed=True, noise=s.SIGMA_N, seed=1)
k0 = int(round(10 / s.DT))
sd_read = (R["y_m"][k0:] - R["v"][k0:]).std()
sd_u, sd_v = R["u"][k0:].std(), R["v"][k0:].std()
U_CLEAN = s.run(30, closed=True)["u"][-1]
assert round(sd_read, 3) == 0.020 and round(sd_u, 2) == 0.40 and round(sd_v, 3) == 0.002
assert round(U_CLEAN, 3) == 1.713


def frame(i, final=False):
    k1 = k0 + 10 * i
    t, v, y, u = (R[n][k0:k1 + 1] for n in ("t", "v", "y_m", "u"))
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.14,
                        subplot_titles=["what the sensor reads, and the true speed", "the force the controller asks for"])
    fig.add_trace(go.Scatter(x=t, y=y, mode="markers", marker=dict(color=ORANGE, size=7), name="readings: true + noise"),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=t, y=v, mode="lines", line=dict(color=BLUE, width=4), name="true speed"), row=1, col=1)
    fig.add_trace(go.Scatter(x=[10, 12], y=[U_CLEAN] * 2, mode="lines", line=dict(color=GREY, width=3, dash="dash"),
                             name="force without noise, 1.713 N"), row=2, col=1)
    fig.add_trace(go.Scatter(x=t, y=u, mode="lines", line=dict(color=BLUE, width=2.5), name="force with noise"),
                  row=2, col=1)
    if final:
        fig.add_annotation(x=11.98, y=0.555, xanchor="right", showarrow=False, font=dict(size=19, color=ORANGE),
                           text=f"readings jitter by {sd_read:.3f} m/s; true speed by only {sd_v:.3f} m/s",
                           bgcolor="rgba(255,255,255,0.85)", row=1, col=1)
        fig.add_annotation(x=11.98, y=3.05, xanchor="right", showarrow=False, font=dict(size=19, color=BLUE),
                           text=f"force jitters by {sd_u:.2f} N = 20 × 0.02", bgcolor="rgba(255,255,255,0.85)",
                           row=2, col=1)
    fig.update_xaxes(range=[10, 12.02], dtick=0.5, title="time (s)", row=2, col=1)
    fig.update_xaxes(range=[10, 12.02], dtick=0.5, row=1, col=1)
    fig.update_yaxes(range=[0.38, 0.58], dtick=0.04, title="speed (m/s)", row=1, col=1)
    fig.update_yaxes(range=[0.3, 3.2], dtick=0.5, title="force (N)", row=2, col=1)
    title = ("jitter over 20 s: sensor 0.020 m/s, force 0.40 N, true speed 0.002 m/s" if final else
             f"closed loop on the ramp, t = {t[-1]:.1f} s")
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=900, margin=dict(l=90, r=30, t=110, b=70),
                      title=dict(text=title, x=0.5, y=0.97, font=dict(size=21)),
                      legend=dict(orientation="h", x=0.0, y=-0.13, font=dict(size=17)))
    for a in fig.layout.annotations[:2]:
        a.font.size = 19
    return fig


n = 20
figs = [frame(i) for i in range(1, n + 1)] + [frame(n, final=True)]
make_gif(figs, here / "noise_anim", fps=4, holds=[6] + [2] * (n - 1) + [24], keys=[0, n // 2, len(figs) - 1, ],
         cols=2, width=900)
