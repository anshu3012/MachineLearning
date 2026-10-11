"""Drift vs jump, step by step. One simulated run of 60 steps from a known start. Top: the errors now, with an arrow
from each last value: the commands' error is the last error plus a small slip, so it moves a little and wanders; the
beacon's error is drawn new each step, so it lands anywhere in its band; the Kalman filter, run on the same slips and
readings, stays near zero. Bottom: the errors so far, with each band of two standard deviations.
The run (seed 1325) is one whose slips all stay under 0.19 m, so no single step of the commands looks like a jump.
Run: python drift_jump.py -> drift_jump.gif, drift_jump_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, ORANGE, make_gif
from kfsim import Q, R

T = 60
rng = np.random.default_rng(1325)
cmd = np.concatenate([[0.0], np.cumsum(rng.normal(0, np.sqrt(Q), T))])
bea = np.concatenate([[np.nan], rng.normal(0, np.sqrt(R), T)])
s = np.arange(T + 1)
# the Kalman filter on the same slips and readings, error = estimate minus true position, from a known start (p = 0)
kf, pk = [0.0], [0.0]
for t in range(1, T + 1):
    eb, pb = kf[-1] + (cmd[t] - cmd[t - 1]), pk[-1] + Q
    k = pb / (pb + R)
    kf.append((1 - k) * eb + k * bea[t])
    pk.append((1 - k) * pb)
kf, pk = np.array(kf), np.array(pk)
band_c, band_b = 2 * np.sqrt(Q * s), np.full(T + 1, 2 * np.sqrt(R))
LANE = {"commands": 2.0, "beacon": 1.0, "Kalman filter": 0.0}


def frame(t):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.4, 0.6], vertical_spacing=0.2,
                        subplot_titles=(f"step {t}: the errors now", "the errors so far"))
    # top: lanes
    fig.add_vline(x=0, line=dict(color="black", width=2), row=1, col=1)
    lo = max(1, t - 5)
    for name, e, col, sym in (("commands", cmd, GREY, "circle"), ("beacon", bea, ORANGE, "x"),
                              ("Kalman filter", kf, BLUE, "diamond")):
        y = LANE[name]
        past = range(lo, t) if name == "beacon" else range(max(0, t - 6), t)
        for j, i in enumerate(past):
            if not np.isnan(e[i]):
                fig.add_trace(go.Scatter(x=[e[i]], y=[y], mode="markers", showlegend=False,
                                         marker=dict(color=col, size=11, symbol=sym, opacity=0.15 + 0.1 * j)), 1, 1)
        if t >= 1 and not np.isnan(e[t]):
            fig.add_trace(go.Scatter(x=[e[t]], y=[y], mode="markers", showlegend=False,
                                     marker=dict(color=col, size=22, symbol=sym, line=dict(width=0))), 1, 1)
            prev = e[t - 1]
            if not np.isnan(prev) and abs(e[t] - prev) > 0.02:
                fig.add_annotation(x=e[t], y=y + 0.32, ax=prev, ay=y + 0.32, xref="x", yref="y", axref="x", ayref="y",
                                   showarrow=True, arrowhead=2, arrowsize=1.3, arrowwidth=2.5, arrowcolor=col, text="")
        elif t == 0:
            if name != "beacon":
                fig.add_trace(go.Scatter(x=[0], y=[y], mode="markers", showlegend=False,
                                         marker=dict(color=col, size=22, symbol=sym)), 1, 1)
    fig.add_annotation(x=0, y=-0.55, xref="x", yref="y", text="true position", showarrow=False, font=dict(size=17))
    fig.update_yaxes(tickvals=[2, 1, 0], ticktext=["commands:<br>drift", "beacon:<br>jumps", "Kalman<br>filter"], range=[-0.75, 2.6], row=1, col=1)
    fig.update_xaxes(title_text="error (m)", range=[-2.2, 2.2], row=1, col=1)
    # bottom: history
    for sg in (1, -1):
        fig.add_trace(go.Scatter(x=s, y=sg * band_c, mode="lines", showlegend=False,
                                 line=dict(color=GREY, width=2, dash="dash")), 2, 1)
        fig.add_trace(go.Scatter(x=s, y=sg * band_b, mode="lines", showlegend=False,
                                 line=dict(color=ORANGE, width=2, dash="dash")), 2, 1)
    for sg in (1, -1):
        fig.add_trace(go.Scatter(x=s, y=sg * 2 * np.sqrt(pk), mode="lines", showlegend=False,
                                 line=dict(color=BLUE, width=2, dash="dot")), 2, 1)
    fig.add_trace(go.Scatter(x=s[:t + 1], y=cmd[:t + 1], mode="lines", name="commands: drift",
                             line=dict(color=GREY, width=4)), 2, 1)
    fig.add_trace(go.Scatter(x=s[1:t + 1], y=bea[1:t + 1], mode="markers", name="beacon: jumps",
                             marker=dict(color=ORANGE, size=10, symbol="x")), 2, 1)
    fig.add_trace(go.Scatter(x=s[:t + 1], y=kf[:t + 1], mode="lines", name="Kalman filter",
                             line=dict(color=BLUE, width=4)), 2, 1)
    # band labels in the right margin, clear of the data
    for yv, txt, col in ((band_c[-1], "2 × 0.1 × √t", GREY), (band_b[0], "± 0.8 m", ORANGE),
                         (2 * np.sqrt(pk[-1]), "± 0.38 m", BLUE)):
        fig.add_annotation(x=1.02, y=yv, xref="x2 domain", yref="y2", text=txt, showarrow=False,
                           xanchor="left", yanchor="middle", font=dict(size=17, color=col))
    fig.update_annotations(selector=dict(text=f"step {t}: the errors now"), font=dict(size=21))
    fig.update_annotations(selector=dict(text="the errors so far"), font=dict(size=21))
    fig.update_xaxes(title_text="time step", range=[-1, T + 1], row=2, col=1)
    fig.update_yaxes(title_text="error (m)", range=[-2.2, 2.2], row=2, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=900, height=1000, margin=dict(l=110, r=140, t=60, b=60),
                      legend=dict(x=0.01, y=0.52, font=dict(size=18)))
    return fig


figs = [frame(t) for t in range(T + 1)]
holds = [6] + [2] * (T - 1) + [16]
assert np.max(np.abs(np.diff(cmd))) < 0.185 and abs(cmd[-1] - 1.39) < 0.01
assert abs(2 * np.sqrt(pk[-1]) - 0.38) < 0.01  # the Kalman filter's band settles at ±0.38 m
make_gif(figs, Path(__file__).parent / "drift_jump", fps=6, holds=holds, keys=[4, 16, 36, 60])
