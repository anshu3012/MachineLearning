"""The zero-order hold, step by step: the force the continuous PI formula asks for during the speed step (grey) and
what a D/A converter with a zero-order hold sends out at 2 Hz (orange): at each tick it takes the newest value (dot)
and holds it flat for 0.5 s. The last frames add the grey curve shifted 0.25 s later (dashed): it runs through the
middle of every step, so the staircase is the smooth force delayed by about half a sample.
Run: python zoh_anim.py -> zoh_anim.gif, zoh_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from digikit import continuous_loop
from gifkit import FONT, GREY, ORANGE, make_gif

here = Path(__file__).parent
T, T_END = 0.5, 6.0
c = continuous_loop(T_END)
t, u = c["t"], c["u"]
tk = np.arange(0, T_END - 1e-9, T)
uk = np.interp(tk, t, u)
assert abs(uk[0] - 2.8) < 1e-9
# the staircase sits closer to the curve moved 0.25 s later than to the curve itself 
stair = np.interp(np.floor(t / T) * T, t, u)
assert np.mean(np.abs(stair - np.interp(t - T / 2, t, u))) < 0.5 * np.mean(np.abs(stair - u))


def frame(k, shift=False):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=u, mode="lines", line=dict(color=GREY, width=3), name="force the formula asks for"))
    xs, ys = [], []
    for j in range(k + 1):
        xs += [tk[j], tk[j] + T]
        ys += [uk[j], uk[j]]
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=ORANGE, width=5),
                             name="force the D/A sends: each value held 0.5 s"))
    fig.add_trace(go.Scatter(x=tk[:k + 1], y=uk[:k + 1], mode="markers", showlegend=False,
                             marker=dict(color=ORANGE, size=14, line=dict(color="white", width=2))))
    if shift:
        fig.add_trace(go.Scatter(x=t + T / 2, y=u, mode="lines", line=dict(color="black", width=2, dash="dash"),
                                 name="grey curve moved 0.25 s later"))
        fig.add_annotation(x=1.0 + T / 2, y=np.interp(1.0, t, u), ax=90, ay=-70, arrowhead=2, arrowwidth=2,
                           text="middle of a step", font=dict(size=20))
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=640,
                      margin=dict(l=100, r=30, t=170, b=80),
                      title=dict(x=0.5, y=0.96, text=(f"tick {k}: t = {tk[k]:.1f} s, the D/A holds {uk[k]:.2f} N"
                                                      if not shift else "the staircase lags the curve by half a sample, 0.25 s")),
                      legend=dict(x=0.5, xanchor="center", y=1.02, yanchor="bottom", font=dict(size=18)),
                      xaxis=dict(title="time since the command (s)", range=[-0.1, T_END + 0.05]),
                      yaxis=dict(title="force (N)", range=[0.85, 2.9]))
    return fig


figs = [frame(k) for k in range(len(tk))] + [frame(len(tk) - 1, shift=True)]
make_gif(figs, here / "zoh_anim", fps=3, holds=[4] + [1] * (len(tk) - 1) + [12], keys=[3, len(figs) - 1],
         cols=1, width=800)
