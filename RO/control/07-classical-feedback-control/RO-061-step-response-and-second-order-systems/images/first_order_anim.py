"""The speed loop is a first-order system. Stage 1 (time constant): the speed under P control (Kv = 6 N per m/s,
time constant T = 1 s) is drawn over time; at t = 1, 2, 3 and 4 s a dot marks 63.2, 86.5, 95.0 and 98.2 percent of the
way to its final 0.375 m/s; the dashed line is the starting slope, which would reach the final value in one time
constant. Stage 2 (raising the gain): Kv = 2, 6, 8 and 20 (the gain of feedback basics) one after another. Left: the speed; right: the force the
controller asks for, against the 4 N limit. A larger Kv is faster and ends closer to 0.5 m/s, but Kv = 20 asks for
10 N at the start. Run: python first_order_anim.py -> first_order_anim.gif, first_order_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, PURPLE, RED, make_gif
from stepkit import B, F_MAX, M, V_REF, speed_p

here = Path(__file__).parent
t = np.linspace(0, 6, 6001)
GAINS = [(2, GREY), (6, BLUE), (8, GREEN), (20, RED)]
MARKS = [(1, 0.632), (2, 0.865), (3, 0.950), (4, 0.982)]
for k, f in MARKS:
    assert abs((1 - np.exp(-k)) - f) < 5e-4
for kp, _ in GAINS:
    assert abs(speed_p(np.array([1e6]), kp)[0] - kp / (kp + B) * V_REF) < 1e-12
assert np.allclose([M / (kp + B) for kp, _ in GAINS], [2.0, 1.0, 0.8, 0.3636], atol=1e-4)
assert [kp * V_REF for kp, _ in GAINS] == [1, 3, 4, 10]


def base(title):
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1, subplot_titles=["speed v (m/s)", "drive force u (N)"])
    fig.add_trace(go.Scatter(x=[0, 6], y=[V_REF, V_REF], mode="lines", line=dict(color=GREY, width=2, dash="dash")),
                  1, 1)
    fig.add_annotation(x=0.1, y=V_REF, text="command 0.5", showarrow=False, xanchor="left", yanchor="bottom",
                       font=dict(color=GREY, size=18), row=1, col=1)
    fig.add_trace(go.Scatter(x=[0, 6], y=[F_MAX, F_MAX], mode="lines", line=dict(color=RED, width=2, dash="dash")),
                  1, 2)
    fig.add_annotation(x=5.9, y=F_MAX, text="limit 4 N", showarrow=False, xanchor="right", yanchor="bottom",
                       font=dict(color=RED, size=18), row=1, col=2)
    fig.update_xaxes(title="time t (s)", range=[0, 6])
    fig.update_yaxes(range=[0, 0.56], row=1, col=1)
    fig.update_yaxes(range=[0, 10.5], row=1, col=2)
    fig.update_layout(template="simple_white", font=FONT, width=1250, height=600, showlegend=False,
                      margin=dict(l=70, r=30, t=130, b=70), title=dict(x=0.5, y=0.95, text=title))
    fig.update_annotations(selector=dict(showarrow=False, xref="paper"), font_size=20)
    return fig


def curve(fig, kp, color, upto=6.0, width=4, opacity=1.0):
    m = t <= upto + 1e-9
    v = speed_p(t[m], kp)
    fig.add_trace(go.Scatter(x=t[m], y=v, mode="lines", line=dict(color=color, width=width), opacity=opacity), 1, 1)
    fig.add_trace(go.Scatter(x=t[m], y=kp * (V_REF - v), mode="lines", line=dict(color=color, width=width),
                             opacity=opacity), 1, 2)


def stage1(upto, nmarks):
    fig = base(f"stage 1, the time constant T = 1 s (Kv = 6):   t = {upto:.2f} s")
    curve(fig, 6, BLUE, upto)
    if nmarks:
        fig.add_trace(go.Scatter(x=[0, 1], y=[0, 0.375], mode="lines", line=dict(color=PURPLE, width=3, dash="dash")),
                      1, 1)
        fig.add_annotation(x=1, y=0.375, text="starting slope reaches<br>0.375 in one T", ax=70, ay=-60,
                           font=dict(color=PURPLE, size=17), arrowcolor=PURPLE, row=1, col=1)
    for k, f in MARKS[:nmarks]:
        fig.add_trace(go.Scatter(x=[k], y=[0.375 * f], mode="markers", marker=dict(color=ORANGE, size=14)), 1, 1)
        above = k >= 3
        fig.add_annotation(x=k, y=0.375 * f, text=f"t = {k}T: {f * 100:.1f} %", showarrow=False,
                           yanchor="bottom" if above else "top", yshift=12 if above else -12,
                           xanchor="right" if k == 3 else "left", font=dict(color=ORANGE, size=17), row=1, col=1)
    return fig


def stage2(n):
    kp, col = GAINS[n - 1]
    tau, fin = M / (kp + B), kp / (kp + B) * V_REF
    over = ", over the limit" if kp * V_REF > F_MAX else ""
    fig = base(f"stage 2, Kv = {kp}: T = {tau:.3g} s, final {fin:.3f} m/s, start force {kp * V_REF:g} N{over}")
    for j, (kq, cq) in enumerate(GAINS[:n]):
        curve(fig, kq, cq, opacity=1.0 if j == n - 1 else 0.45, width=4 if j == n - 1 else 3)
        fq = kq / (kq + B) * V_REF
        fig.add_annotation(x=5.95, y=fq, text=f"Kv = {kq}", showarrow=False, xanchor="right",
                           yanchor="top" if kq == 6 else "bottom",
                           font=dict(color=cq, size=17), row=1, col=1)
        fig.add_annotation(x=0.05, y=kq * V_REF, text=f"Kv = {kq}: {kq * V_REF:g} N", showarrow=False, xanchor="left",
                           yanchor="bottom", font=dict(color=cq, size=17), row=1, col=2)
    return fig


ups = np.round(np.linspace(0, 6, 25), 2)
figs = [stage1(u, 0) for u in ups] + [stage1(6, n) for n in (1, 2, 3, 4)] + [stage2(n) for n in (1, 2, 3, 4)]
holds = [6] + [1] * 24 + [5, 5, 5, 16] + [12, 12, 12, 30]
make_gif(figs, here / "first_order_anim", fps=6, holds=holds, keys=[28, 30, 31, 32], cols=2, width=950)
