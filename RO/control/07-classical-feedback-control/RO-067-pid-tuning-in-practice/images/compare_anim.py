"""Three tunings of the speed PI against the same load: at t = 1 s the robot cruising at 0.5 m/s meets a 1 degree
ramp (gravity pulls back with 1.37 N). Top: the loop as built. Bottom: the same loop with the measured speed arriving
0.04 s later still (4 more samples). Gains: RO-060's kp = 20, ki = 10; the bump-test rule kp = 30.1, ki = 27.9;
Ziegler-Nichols kp = 90, ki = 270. Time runs frame by frame; the last frame holds all 8 s.
Run: python compare_anim.py -> compare_anim.gif, compare_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREEN, RED, make_gif
from tunekit import GAINS, RAMP, speed_run

here = Path(__file__).parent
T = 8.0
LOAD = lambda t: -RAMP if t >= 1.0 else 0.0
COL = {"RO-060's gains": BLUE, "bump-test rule": GREEN, "Ziegler–Nichols": RED}
nom = {k: speed_run(T, *g, d=LOAD) for k, g in GAINS.items()}
late = {k: speed_run(T, *g, d=LOAD, extra=4) for k, g in GAINS.items()}


def drop_and_recovery(run):
    t, v = run[0], run[1]
    out = np.where(abs(v - 0.5) > 0.005)[0]
    return 0.5 - v.min(), t[out[-1]] - 1.0


stats = {k: drop_and_recovery(r) for k, r in nom.items()}
want = {"RO-060's gains": (0.054, 5.2), "bump-test rule": (0.039, 2.3), "Ziegler–Nichols": (0.021, 0.8)}
for k, (d, r) in want.items():
    assert abs(stats[k][0] - d) < 0.0005 and abs(stats[k][1] - r) < 0.05, (k, stats[k])
assert abs(RAMP - 1.37) < 0.005
zl = late["Ziegler–Nichols"][1]
assert zl[-200:].max() - zl[-200:].min() > 0.05                     # Ziegler-Nichols keeps swinging
for k in ("RO-060's gains", "bump-test rule"):
    assert np.abs(late[k][1] - nom[k][1]).max() < 0.005                # the others barely change


def frame(upto, final=False):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.12,
                        subplot_titles=("as built", "speed measured 0.04 s later"))
    for row, runs in ((1, nom), (2, late)):
        for k, (t, v, y, u) in runs.items():
            n = int(round(upto / (t[1] - t[0]))) + 1
            d, r = stats[k]
            name = f"{k}: drop {d:.3f} m/s, back in {r:.1f} s"
            fig.add_trace(go.Scatter(x=t[:n], y=v[:n], mode="lines", line=dict(color=COL[k], width=3.5),
                                     name=name, showlegend=row == 1), row=row, col=1)
        fig.add_vline(x=1.0, line=dict(color="black", width=1, dash="dash"), row=row, col=1)
    title = (f"t = {upto:.1f} s: the ramp starts at t = 1 s" if not final else
             "Ziegler–Nichols reacts fastest but rings with 0.04 s more delay")
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=840,
                      margin=dict(l=110, r=30, t=230, b=80), title=dict(text=title, x=0.5, y=0.98),
                      legend=dict(x=0.5, xanchor="center", y=1.06, yanchor="bottom", font=dict(size=18)))
    fig.update_annotations(selector=dict(text="as built"), font=dict(size=19))
    fig.update_annotations(selector=dict(text="speed measured 0.04 s later"), font=dict(size=19))
    for row in (1, 2):
        fig.update_yaxes(title_text="speed (m/s)", range=[0.42, 0.545], row=row, col=1)
        fig.update_xaxes(range=[0, T], row=row, col=1)
    fig.update_xaxes(title_text="time t (s)", row=2, col=1)
    return fig


times = list(np.arange(0.6, T + 0.001, 0.4))
figs = [frame(x) for x in times] + [frame(T, final=True)]
make_gif(figs, here / "compare_anim", fps=5, holds=[3] + [1] * (len(times) - 1) + [16],
         keys=[5, len(figs) - 1], cols=1, width=850)
