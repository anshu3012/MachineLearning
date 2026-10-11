"""The hidden speed being learned. The two-variable filter (position and speed) gets the ten
position readings of the corridor one per frame, and no commands. Top: position, measured. Bottom: speed, never
measured. Bands are two standard deviations. One reading gives a speed of 0.378 m/s; the estimate swings, then
settles at 0.421 m/s (standard deviation 0.081 m/s) against the true average 0.48 m/s, while its band narrows.
Run: python cv_speed_anim.py -> cv_speed_anim.gif, cv_speed_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREEN, ORANGE, make_gif
from kfsim import X_TRUE, Z, kf2d

here = Path(__file__).parent
rows = kf2d()
pos = np.r_[0, [r["x"][0] for r in rows]]
spd = np.r_[0, [r["x"][1] for r in rows]]
sp = np.sqrt(np.r_[1, [r["P"][0, 0] for r in rows]])
ss = np.sqrt(np.r_[1, [r["P"][1, 1] for r in rows]])
true_speed = (X_TRUE[-1] - X_TRUE[0]) / 10
assert abs(spd[1] - 0.378) < 5e-4 and abs(spd[10] - 0.421) < 5e-4 and abs(ss[10] - 0.081) < 5e-4
assert abs(true_speed - 0.48) < 1e-9 and abs(true_speed - spd[10]) < ss[10]     # inside one standard deviation


def frame(t):
    s = np.arange(0, t + 1)
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.14,
                        subplot_titles=["position: measured", "speed: never measured"])
    for row, m, sd, col in ((1, pos, sp, BLUE), (2, spd, ss, GREEN)):
        sb, mb, db = (s, m[:t + 1], sd[:t + 1]) if t else (np.array([-0.15, 0.15]), m[[0, 0]], sd[[0, 0]])
        fig.add_trace(go.Scatter(x=np.r_[sb, sb[::-1]], y=np.r_[mb + 2 * db, (mb - 2 * db)[::-1]], fill="toself",
                                 mode="lines", fillcolor="rgba(120,120,120,0.15)", line=dict(width=0)), row, 1)
        fig.add_trace(go.Scatter(x=s, y=m[:t + 1], mode="lines+markers", line=dict(color=col, width=4),
                                 marker=dict(size=10)), row, 1)
    fig.add_trace(go.Scatter(x=s, y=X_TRUE[:t + 1], mode="lines", line=dict(color="black", width=2)), 1, 1)
    fig.add_trace(go.Scatter(x=s[1:], y=Z[:t], mode="markers", marker=dict(color=ORANGE, size=13, symbol="x")), 1, 1)
    fig.add_hline(y=true_speed, line=dict(color="black", width=2, dash="dash"), row=2, col=1)
    fig.add_annotation(x=10.4, y=2.15, text=f"dashed: true average {true_speed:.2f} m/s", showarrow=False,
                       xanchor="right", yanchor="top", font=dict(size=18), row=2, col=1)
    fig.add_annotation(x=-0.4, y=5.9, text="black: true    orange ×: readings", showarrow=False, xanchor="left",
                       yanchor="top", font=dict(size=18), row=1, col=1)
    if t == 0:
        title = "start: speed 0 m/s, standard deviation 1 m/s"
    elif t == 1:
        title = f"step 1: one position reading gives a speed of {spd[1]:.3f} m/s"
    else:
        title = f"step {t}: speed {spd[t]:.3f} m/s, standard deviation {ss[t]:.3f} m/s"
    fig.update_xaxes(title="step", range=[-0.5, 10.5], dtick=1)
    fig.update_yaxes(title="position (m)", range=[-2.2, 6], row=1, col=1)
    fig.update_yaxes(title="speed (m/s)", range=[-2.1, 2.2], row=2, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=900, height=1000, showlegend=False,
                      margin=dict(l=90, r=30, t=110, b=70), title=dict(x=0.5, y=0.975, text=title))
    fig.update_annotations(selector=dict(text="position: measured"), font_size=21)
    fig.update_annotations(selector=dict(text="speed: never measured"), font_size=21)
    return fig


figs = [frame(t) for t in range(11)]
make_gif(figs, here / "cv_speed_anim", fps=1, holds=[3, 4] + [2] * 8 + [8], keys=[1, 2, 5, 10], cols=2, width=850)
