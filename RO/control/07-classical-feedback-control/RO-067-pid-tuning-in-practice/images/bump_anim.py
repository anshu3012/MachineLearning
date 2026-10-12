"""The bump test: the robot stands still, the drive force steps from 0 to 1 N at t = 0 and stays there; the measured
(averaged) speed is recorded for 30 s. Top: the whole run, with K (the final speed per newton) and T63 (63 percent of
it). Bottom: the first second, enlarged, with the steepest tangent and where it crosses the time axis (tau) and the
speed axis (-a). The last frame holds the three numbers of the model: K = 0.5 m/s per N, tau = 0.094 s, T = 4.00 s.
Run: python bump_anim.py -> bump_anim.gif, bump_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, ORANGE, RED, make_gif
from tunekit import K_FOTD, T_FOTD, TAU_FOTD, bump_test, fotd_fit

here = Path(__file__).parent
t, V, Y = bump_test()
f = fotd_fit(t, Y)
assert abs(f["K"] - K_FOTD) < 0.001 and abs(f["tau"] - TAU_FOTD) < 0.0005 and abs(f["T"] - T_FOTD) < 0.005
assert abs(f["T63"] - 4.09) < 0.005 and abs(f["slope"] - 0.122) < 0.0005 and abs(f["tj"] - 0.2) < 1e-9
assert abs(f["a"] - 0.0115) < 0.00005
K, tau, T63, s, tj, a = f["K"], f["tau"], f["T63"], f["slope"], f["tj"], f["a"]


def frame(upto, stage=0):
    n = int(round(upto / (t[1] - t[0]))) + 1
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.22, row_heights=[0.55, 0.45],
                        subplot_titles=("the whole test, 0 to 30 s", "the first second, enlarged"))
    for row in (1, 2):
        fig.add_trace(go.Scatter(x=t[:n], y=V[:n], mode="lines", line=dict(color=BLUE, width=2, dash="dot"),
                                 name="true speed", showlegend=row == 1), row=row, col=1)
        fig.add_trace(go.Scatter(x=t[:n], y=Y[:n], mode="lines", line=dict(color=ORANGE, width=4),
                                 name="measured speed", showlegend=row == 1), row=row, col=1)
    if stage >= 1:                                   # steepest tangent
        tt = np.array([0, 1.0])
        fig.add_trace(go.Scatter(x=tt, y=s * (tt - tj) + Y[int(round(tj / 0.01))], mode="lines",
                                 line=dict(color=RED, width=3), name="steepest tangent"), row=2, col=1)
        fig.add_trace(go.Scatter(x=[tj], y=[Y[int(round(tj / 0.01))]], mode="markers",
                                 marker=dict(color=RED, size=12), showlegend=False), row=2, col=1)
    if stage >= 2:                                   # tau and a
        fig.add_trace(go.Scatter(x=[tau], y=[0], mode="markers", marker=dict(color="black", size=12),
                                 showlegend=False), row=2, col=1)
        fig.add_annotation(x=tau, y=0, text=f"τ = {tau:.3f} s", ax=60, ay=-60, font=dict(size=20),
                           arrowwidth=2, row=2, col=1)
        fig.add_annotation(x=0, y=-a, text=f"−a = −{a:.4f} m/s", ax=230, ay=4, font=dict(size=20),
                           arrowwidth=2, xanchor="left", row=2, col=1)
    if stage >= 3:                                   # K
        fig.add_hline(y=K, line=dict(color=GREY, width=2, dash="dash"), row=1, col=1)
        fig.add_annotation(x=29.5, y=K, text=f"K = {K:.1f} m/s per N", showarrow=False, xanchor="right",
                           yanchor="top", font=dict(size=20), row=1, col=1)
    if stage >= 4:                                   # T63
        fig.add_trace(go.Scatter(x=[0, T63, T63], y=[0.632 * K, 0.632 * K, 0], mode="lines",
                                 line=dict(color=GREY, width=2, dash="dot"), showlegend=False), row=1, col=1)
        fig.add_annotation(x=T63, y=0.632 * K, text=f"63 percent at T63 = {T63:.2f} s", ax=120, ay=40,
                           font=dict(size=20), arrowwidth=2, xanchor="left", row=1, col=1)
    titles = {0: f"drive force 1 N from t = 0: t = {upto:.0f} s",
              1: "the steepest rise: 0.122 m/s² at t = 0.2 s",
              2: f"the tangent crosses the time axis at τ = {tau:.3f} s",
              3: f"after 30 s the speed has settled: K = {K:.1f} m/s per N",
              4: f"K = {K:.1f} m/s per N, τ = {tau:.3f} s, T = T63 − τ = {T63 - tau:.2f} s"}
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=880,
                      margin=dict(l=110, r=30, t=150, b=80), title=dict(text=titles[stage], x=0.5, y=0.97),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=1.04, yanchor="bottom",
                                  font=dict(size=18)))
    fig.update_annotations(selector=dict(text="the whole test, 0 to 30 s"), font=dict(size=19))
    fig.update_annotations(selector=dict(text="the first second, enlarged"), font=dict(size=19))
    fig.update_xaxes(title_text="time t (s)", range=[0, 30], row=1, col=1)
    fig.update_yaxes(title_text="speed (m/s)", range=[0, 0.56], row=1, col=1)
    fig.update_xaxes(title_text="time t (s)", range=[0, 1.0], row=2, col=1)
    fig.update_yaxes(title_text="speed (m/s)", range=[-0.02, 0.12], row=2, col=1)
    return fig


sweep = [1, 2, 4, 6, 10, 15, 20, 30]
figs = [frame(u) for u in sweep] + [frame(30, k) for k in (1, 2, 3, 4)]
make_gif(figs, here / "bump_anim", fps=3, holds=[3] + [1] * (len(sweep) - 2) + [3, 4, 4, 4, 14],
         keys=[3, len(figs) - 1], cols=1, width=850)
