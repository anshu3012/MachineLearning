"""One Gaussian holds one side, step by step. The same 16 readings fed to two EKFs, one step per frame: one started at
0 m follows the truth; one started at 11 m, the far side of the beacon, says 11.24 m at step 1, 10.5 m off with
error bars of only +-0.21 m, and moves left while the robot moves right, until the robot passes the beacon at 6 m.
The last frame shows the whole run. Run: python mirror_anim.py -> mirror_anim.gif, mirror_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, RED, make_gif
from ekfsim import B, X_TRUE, Z, ekf

here = Path(__file__).parent
t = np.arange(1, 17)
runs = []
for x0, c, name in ((0.0, BLUE, "EKF started at 0 m"), (11.0, RED, "EKF started at 11 m")):
    rows = ekf(x=x0)
    runs.append((np.array([r["x"] for r in rows]), np.sqrt([r["p"] for r in rows]), c, name))
(xa, sa, _, _), (xb, sb, _, _) = runs
assert Z[0] == 5.61 and abs(xa[0] - 0.755) < 5e-4 and abs(xb[0] - 11.24) < 5e-3
assert abs(xb[0] - X_TRUE[0] - 10.5) < 0.05 and np.all(xb - X_TRUE <= xb[0] - X_TRUE[0])   # 10.5 m off is the worst
assert abs(sb[0] - 0.106) < 5e-4 and abs(2 * sb[0] - 0.21) < 5e-3                          # about 10 cm, bars +-0.21 m
assert np.all(np.diff(xb[:13]) < 0) and np.all(np.diff(X_TRUE) > 0)                        # left while the robot goes right
assert abs(xb[-1] - 7.96) < 5e-3 and abs(xa[-1] - 7.749) < 5e-4 and X_TRUE[-1] == 7.86
assert X_TRUE[11] < B < X_TRUE[12]
TITLES = {0: ("step 1: both filters read 5.61 m",
              "started at 0 m: 0.755 m; started at 11 m: 11.24 m, 10.5 m off, with error bars of only ± 0.21 m"),
          11: ("step 12: the robot (5.67 m) nears the beacon at 6 m", ""),
          12: ("step 13: the robot (6.32 m) has passed the beacon",
               "it is now on the same side as the filter started at 11 m (7.40 m)"),
          15: ("step 16: started at 11 m: 7.96 m; started at 0 m: 7.75 m", "true position 7.86 m")}


def frame(k):
    n = k + 1
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t[:n], y=X_TRUE[:n], mode="lines+markers", line=dict(color="black", width=3), name="true"))
    for x, sd, c, name in runs:
        fig.add_trace(go.Scatter(x=t[:n], y=x[:n], mode="lines+markers", line=dict(color=c, width=3), name=name,
                                 error_y=dict(type="data", array=2 * sd[:n], color=c, thickness=1.5)))
    fig.add_hline(y=B, line=dict(color=GREY, width=2, dash="dot"))
    fig.add_annotation(x=16.45, y=B - 0.1, text="beacon at 6 m", showarrow=False, xanchor="right", yanchor="top",
                       font=dict(color=GREY, size=16))
    if k == 0:
        fig.add_shape(type="line", x0=1.3, x1=1.3, y0=X_TRUE[0], y1=xb[0], line=dict(color=GREY, width=2))
        fig.add_annotation(x=1.4, y=8.5, text="10.5 m off", showarrow=False, xanchor="left", font=dict(color=GREY, size=17))
    head, sub = TITLES.get(k, (f"step {n}: the robot moves right; the filter started at 11 m moves left", ""))
    if k in (13, 14):
        head = f"step {n}: the filter started at 11 m closes in on the truth"
    title = head + (f"<br><span style='font-size:18px'>{sub}</span>" if sub else "")
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=620, margin=dict(l=90, r=30, t=125, b=70),
                      legend=dict(x=0.65, y=0.99, font=dict(size=17)), title=dict(x=0.5, y=0.955, text=title),
                      xaxis=dict(title="step", dtick=1, range=[0.5, 16.5]), yaxis=dict(title="position (m)", range=[0, 12.5]))
    return fig


figs = [frame(k) for k in range(16)]
holds = [4] + [1] * 10 + [2, 3, 1, 1, 8]
make_gif(figs, here / "mirror_anim", fps=1, holds=holds, keys=[0, 6, 12, 15], cols=2, width=850)
