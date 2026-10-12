"""The opening problem, one step per frame: the true path of the robot over ten steps, the commands alone (dead
reckoning) and the beacon readings. Each frame adds one step and draws two gaps to the truth: the commands' gap (grey)
is the last gap plus the new wheel slip, so it carries over from step to step (drift); the beacon's gap (orange) is
new each step, so it swings from one side of the truth to the other (jumps). The last frame adds the Kalman filter
estimate and the average miss (RMSE) of each over the ten steps: commands 0.27 m, beacon 0.51 m, filter 0.17 m.
Run: python problem_anim.py -> problem_anim.gif, problem_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, ORANGE, make_gif
from kfsim import U, X0, X_TRUE, Z, kf1d

here = Path(__file__).parent
t = np.arange(11)
odo = X0 + U * t                                    # the commands alone: 0.5 m per step from the first guess
est = np.r_[X0, [r["x"] for r in kf1d()]]
gap = np.round(X_TRUE - odo, 2)                     # how far the commands are behind the truth
slip = np.round(np.diff(X_TRUE) - U, 2)             # each step's wheel slip
bea = np.r_[np.nan, np.round(Z - X_TRUE[1:], 2)]    # the beacon's error, + = ahead of the truth


def rmse(e):
    return np.sqrt(np.mean(np.square(e)))


rm_c, rm_b, rm_k = rmse(odo[1:] - X_TRUE[1:]), rmse(Z - X_TRUE[1:]), rmse(est[1:] - X_TRUE[1:])
assert np.allclose([rm_c, rm_b, rm_k], [0.27, 0.51, 0.17], atol=5e-3)
assert np.allclose(gap[1:], np.round(gap[:-1] + slip, 2))            # each gap = last gap + new slip, as printed
assert np.all(gap > 0)                                               # the commands stay behind the truth
assert abs(bea[5] + 0.60) < 1e-9 and abs(bea[6] - 0.90) < 1e-9       # step 5: 0.60 m behind, step 6: 0.90 m ahead


def side(e):
    return f"{abs(e):.2f} m {'ahead of' if e > 0 else 'behind'} the truth"


def frame(k, last=False):
    fig = go.Figure()
    s = t[:k + 1]
    if not last:                     # the gaps: earlier steps faint, this step bold
        for i in range(k + 1):
            w, op = (7, 1.0) if i == k else (3, 0.3)
            fig.add_trace(go.Scatter(x=[i - 0.07] * 2, y=[odo[i], X_TRUE[i]], mode="lines", showlegend=False,
                                     opacity=op, line=dict(color=GREY, width=w)))
            if i >= 1:
                fig.add_trace(go.Scatter(x=[i + 0.07] * 2, y=[X_TRUE[i], Z[i - 1]], mode="lines", showlegend=False,
                                         opacity=op, line=dict(color=ORANGE, width=w)))
    fig.add_trace(go.Scatter(x=s, y=X_TRUE[:k + 1], mode="lines+markers", line=dict(color="black", width=3),
                             name="true position"))
    fig.add_trace(go.Scatter(x=s[1:], y=Z[:k], mode="markers", marker=dict(color=ORANGE, size=13, symbol="x"),
                             name="beacon readings" + (f": miss {rm_b:.2f} m" if last else "")))
    fig.add_trace(go.Scatter(x=s, y=odo[:k + 1], mode="lines", line=dict(color=GREY, width=3, dash="dash"),
                             name="commands only (dead reckoning)" + (f": miss {rm_c:.2f} m" if last else "")))
    if last:
        fig.add_trace(go.Scatter(x=t, y=est, mode="lines+markers", line=dict(color=BLUE, width=4),
                                 name=f"Kalman filter: miss {rm_k:.2f} m"))
    grey = f"<span style='color:{GREY}'>commands</span>"
    orange = f"<span style='color:{ORANGE}'>beacon</span>"
    small = "<span style='font-size:19px'>"
    if last:
        title = (f"all ten steps, with the Kalman filter (blue)<br>{small}average miss (RMSE) over the ten steps,"
                 " in the legend</span>")
    elif k == 0:
        title = (f"step 0: the robot starts at 0.3 m<br>{small}{grey}: start from the first guess, 0 m,"
                 f" so {side(-gap[0])}</span>")
    else:
        sl = f"+ {slip[k - 1]:.2f}" if slip[k - 1] >= 0 else f"− {abs(slip[k - 1]):.2f}"
        title = (f"step {k} of 10<br>{small}{grey}: {side(-gap[k])} = {gap[k - 1]:.2f} carried over {sl} new slip"
                 f"<br>{orange}: {side(bea[k])}")
        title += f" (step {k - 1}: {side(bea[k - 1])})</span>" if k >= 2 else " (its first reading)</span>"
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=820, margin=dict(l=90, r=30, t=170, b=70),
                      legend=dict(x=0.01, y=0.99, font=dict(size=18), bgcolor="rgba(255,255,255,0.85)"),
                      title=dict(x=0.5, y=0.955, yanchor="top", text=title),
                      xaxis=dict(title="time step (1 s each)", dtick=1, range=[-0.4, 10.5]),
                      yaxis=dict(title="position along the corridor (m)", range=[-0.35, 5.5]))
    return fig


figs = [frame(k) for k in range(11)] + [frame(10, last=True)]
make_gif(figs, here / "problem_anim", fps=1, holds=[4] + [3] * 10 + [12], keys=[0, 5, 6, 11], cols=2, width=850)
