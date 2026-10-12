"""Animation: regulation and tracking on one run. The plan speeds the robot up from rest at 0.25 m/s^2 for 2 s to
0.5 m/s, then holds 0.5 m/s. The closed loop (open-loop force 2 x reference, plus 20 N per m/s of error) follows.
Top: the plan's position (grey outline) and the robot (blue) along the corridor. Bottom: the reference speed and the
robot's speed. While the reference rises (tracking) the robot lags by up to 0.091 m/s; once it is held (regulation) the
error dies out, but the robot stays 0.18 m behind the plan. One frame per 0.2 s for 5 s; the last frame holds.
Run -> tracking_anim.gif, tracking_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import speedkit as s
from gifkit import BLUE, FONT, GREY, ORANGE, make_gif

here = Path(__file__).parent
T = 5
R = s.run(T, closed=True, ramp=False, v0=0.0, ref=s.ramp_ref)
X_REF = np.r_[0, np.cumsum(R["r"][:-1]) * s.DT]
k2 = int(round(2 / s.DT))
assert round(R["e"][k2], 3) == 0.091 and round(s.M * 0.25 / (s.B + s.KP), 3) == 0.091
assert round(X_REF[-1] - R["x"][-1], 2) == 0.18 and abs(R["e"][-1]) < 1e-4


def box(fig, x, color, fill, dash=None):
    fig.add_trace(go.Scatter(x=[x - 0.125, x + 0.125, x + 0.125, x - 0.125, x - 0.125], y=[0.1, 0.1, 0.9, 0.9, 0.1],
                             mode="lines", fill="toself", fillcolor=fill, line=dict(color=color, width=3, dash=dash),
                             showlegend=False, hoverinfo="skip"), row=1, col=1)


def frame(t, final=False):
    k = int(round(t / s.DT))
    fig = make_subplots(rows=2, cols=1, row_heights=[0.3, 0.7], vertical_spacing=0.16,
                        subplot_titles=["along the corridor (seen from above)", "speed"])
    box(fig, X_REF[k], GREY, "rgba(0,0,0,0)", dash="dash")
    box(fig, R["x"][k], BLUE, "rgba(76,120,168,0.6)")
    gap = X_REF[k] - R["x"][k]
    fig.add_annotation(x=X_REF[k], y=1.35, text=f"plan: {X_REF[k]:.2f} m", showarrow=False,
                       font=dict(size=17, color=GREY), row=1, col=1)
    fig.add_annotation(x=R["x"][k], y=-0.35, text=f"robot: {R['x'][k]:.2f} m", showarrow=False,
                       font=dict(size=17, color=BLUE), row=1, col=1)
    fig.update_xaxes(range=[-0.3, 2.3], dtick=0.5, ticksuffix=" m", row=1, col=1)
    fig.update_yaxes(range=[-0.8, 1.8], visible=False, row=1, col=1)
    tt = R["t"][:k + 1]
    fig.add_trace(go.Scatter(x=tt, y=R["r"][:k + 1], mode="lines", line=dict(color=GREY, width=4, dash="dash"),
                             name="reference r (the plan)"), row=2, col=1)
    fig.add_trace(go.Scatter(x=tt, y=R["v"][:k + 1], mode="lines", line=dict(color=BLUE, width=4),
                             name="robot's speed v"), row=2, col=1)
    fig.add_trace(go.Scatter(x=[t, t], y=[R["v"][k], R["r"][k]], mode="lines", line=dict(color=ORANGE, width=6),
                             name="error e = r − v"), row=2, col=1)
    late = t > 4                                      # keep the label inside the plot at the end
    fig.add_annotation(x=t - 0.08 if late else t + 0.08, y=(R["v"][k] + R["r"][k]) / 2 - (0.06 if late else 0),
                       xanchor="right" if late else "left", showarrow=False,
                       text=f"e = {R['e'][k]:.3f} m/s", font=dict(size=18, color=ORANGE),
                       bgcolor="rgba(255,255,255,0.8)", row=2, col=1)
    fig.add_vline(x=2, line=dict(color=GREY, width=1.5, dash="dot"), row=2, col=1)
    fig.add_annotation(x=1.0, y=0.62, text="tracking: the reference rises", showarrow=False,
                       font=dict(size=18, color=GREY), row=2, col=1)
    fig.add_annotation(x=3.5, y=0.62, text="regulation: the reference is held", showarrow=False,
                       font=dict(size=18, color=GREY), row=2, col=1)
    fig.update_xaxes(range=[0, T + 0.05], dtick=0.5, title="time (s)", row=2, col=1)
    fig.update_yaxes(range=[0, 0.68], dtick=0.1, title="speed (m/s)", row=2, col=1)
    title = (f"the error dies out, but the robot stays {gap:.2f} m behind the plan" if final else
             f"t = {t:.1f} s: the robot is {gap:.2f} m behind the plan")
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=900, margin=dict(l=90, r=30, t=110, b=70),
                      title=dict(text=title, x=0.5, y=0.97, font=dict(size=21)),
                      legend=dict(x=0.62, y=0.04, yanchor="bottom", font=dict(size=17), bgcolor="rgba(255,255,255,0.85)"))
    for a in fig.layout.annotations[:2]:
        a.font.size = 19
    return fig


times = list(np.round(np.arange(0, T + 0.01, 0.2), 1))
figs = [frame(t) for t in times] + [frame(T, final=True)]
make_gif(figs, here / "tracking_anim", fps=4, holds=[6] + [2] * (len(times) - 1) + [24],
         keys=[0, 5, 10, len(figs) - 1], cols=2, width=900)
