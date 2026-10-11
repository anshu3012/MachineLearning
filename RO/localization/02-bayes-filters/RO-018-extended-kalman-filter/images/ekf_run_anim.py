"""The EKF on the corridor, step by step, for all 16 steps past the beacon at 6 m.
Top: the beacon distance h(x); each step the prediction (hollow blue) sits on the curve, the tangent line (purple)
touches the curve there with slope H, the reading (orange line) gives the innovation (orange bar), and the update
(blue dot) moves the estimate. Step 1 plays one move per frame with the numbers worked by hand; later steps take two
frames. Middle: truth, estimate and its band of two standard deviations, built step by step.
Bottom: the slope H at each prediction, from -0.940 through 0 at the beacon to +0.617.
Run: python ekf_run_anim.py -> ekf_run_anim.gif, ekf_run_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, ORANGE, PURPLE, RED, make_gif
from ekfsim import B, P0, X0, X_TRUE, Z, ekf, h

here = Path(__file__).parent
rows = ekf()
N = len(rows)
x = np.array([r["x"] for r in rows])
p = np.array([r["p"] for r in rows])
sd = np.sqrt(p)
H = np.array([r["H"] for r in rows])
K = np.array([r["K"] for r in rows])
r0 = rows[0]
# every number the text and the frames quote
assert N == 16 and X_TRUE[0] == 0.73 and X_TRUE[-1] == 7.86
assert abs(r0["x_pred"] - 0.5) < 1e-9 and abs(r0["p_pred"] - 1.01) < 1e-9
assert abs(r0["h_pred"] - 5.852) < 5e-4 and abs(r0["y"] + 0.242) < 5e-4 and abs(r0["S"] - 0.902) < 5e-4
assert abs(r0["K"] + 1.052) < 5e-4 and abs(r0["x"] - 0.755) < 5e-4 and abs(r0["p"] - 0.0112) < 5e-5
assert abs(r0["K"] * r0["y"] - 0.255) < 5e-4
assert np.allclose(H[[0, 5, 10, 11, 12, 15]], [-0.940, -0.825, -0.349, -0.115, 0.133, 0.617], atol=5e-4)
assert np.allclose(K[[5, 10, 11, 12, 15]], [-0.662, -0.623, -0.307, 0.459, 0.868], atol=5e-4)
assert abs(p[12] - 0.0346) < 5e-5 and p.argmax() == 12 and np.all((p[1:9] > 0.007) & (p[1:9] < 0.011))
assert abs(x[-1] - 7.749) < 5e-4 and abs(0.1 / abs(H[0]) - 0.106) < 5e-4


def m(v, f):
    """Format with a true minus sign, as in the Note."""
    return format(v, f).replace("-", "−")


G = np.linspace(-1.7, 9.0, 600)
NOTES = {(11, "b"): "near the beacon the slope is only −0.115: a reading says almost nothing about the position",
         (12, "a"): "past the beacon the slope turns positive, +0.133",
         (12, "b"): "the gain turns positive with it, K = 0.459; the variance is the largest of the run, 0.0346 m²",
         (15, "b"): "end: estimate 7.749 m, true 7.86 m; the slope is back up to +0.617"}
STEP1 = {"predict": "first guess 0 m, moved by the command 0.5 m; variance 1 + 0.01 = 1.01 m²",
         "linearise": "expected reading h(0.5) = 5.852 m; slope H = −5.5 / 5.852 = −0.940",
         "reading": "innovation 5.61 − 5.852 = −0.242 m: the robot is closer to the beacon than predicted",
         "update": "estimate 0.5 + (−1.052)(−0.242) = 0.5 + 0.255 = 0.755 m; variance 0.0112 m²"}
NAMES = {"predict": "predict", "linearise": "linearise at the prediction", "reading": "the reading and the innovation",
         "update": "update", "a": "predict, then linearise at the prediction", "b": "reading, innovation, update"}


def frame(k, stage):
    r = rows[k]
    show = {"predict": 1, "linearise": 2, "a": 2, "reading": 3, "update": 4, "b": 4}[stage]
    prev = (X0, P0) if k == 0 else (x[k - 1], p[k - 1])
    fig = make_subplots(rows=3, cols=1, row_heights=[0.44, 0.34, 0.22], vertical_spacing=0.065)
    # top: the beacon curve and this step's moves on it
    fig.add_trace(go.Scatter(x=G, y=h(G), line=dict(color="black", width=4),
                             name="beacon distance h(x), lowest (2 m) under the beacon at 6 m"), 1, 1)
    fig.add_trace(go.Scatter(x=[X_TRUE[k]] * 2, y=[1.5, 8.3], mode="lines", line=dict(color="black", width=2, dash="dot"),
                             name=f"true position {X_TRUE[k]:.2f} m"), 1, 1)
    first = "first guess" if k == 0 else "previous estimate"
    fig.add_trace(go.Scatter(x=[prev[0]], y=[h(prev[0])], mode="markers", marker=dict(color="#BBBBBB", size=13),
                             error_x=dict(type="constant", value=2 * np.sqrt(prev[1]), color="#BBBBBB", thickness=3, width=8),
                             name=f"{first} {prev[0]:.3f} m ± 2 sd"), 1, 1)
    fig.add_trace(go.Scatter(x=[r["x_pred"]], y=[r["h_pred"]], mode="markers",
                             marker=dict(color="white", size=19, line=dict(color=BLUE, width=3)),
                             error_x=dict(type="constant", value=2 * np.sqrt(r["p_pred"]), color=BLUE, thickness=2, width=8),
                             name=f"prediction {r['x_pred']:.2f} m ± 2 sd (variance {r['p_pred']:.4f} m²)"), 1, 1)
    if show >= 2:
        tx = np.linspace(r["x_pred"] - 2, r["x_pred"] + 2, 2)
        fig.add_trace(go.Scatter(x=tx, y=r["h_pred"] + r["H"] * (tx - r["x_pred"]), mode="lines",
                                 line=dict(color=PURPLE, width=4, dash="dash"),
                                 name=f"tangent at the prediction: h = {r['h_pred']:.3f} m, slope H = {m(r['H'], '.3f')}"), 1, 1)
    if show >= 3:
        fig.add_trace(go.Scatter(x=G[[0, -1]], y=[Z[k]] * 2, mode="lines", line=dict(color=ORANGE, width=3, dash="dash"),
                                 name=f"reading z = {Z[k]:.2f} m"), 1, 1)
        fig.add_trace(go.Scatter(x=[r["x_pred"]] * 2, y=[r["h_pred"], Z[k]], mode="lines", line=dict(color=ORANGE, width=7),
                                 name=f"innovation z − h = {m(r['y'], '.3f')} m"), 1, 1)
    if show >= 4:
        fig.add_trace(go.Scatter(x=[x[k]], y=[h(x[k])], mode="markers", marker=dict(color=BLUE, size=11),
                                 error_x=dict(type="constant", value=2 * sd[k], color=BLUE, thickness=4, width=10),
                                 name=f"estimate {x[k]:.3f} m ± 2 sd (variance {p[k]:.4f} m², gain K = {m(K[k], '.3f')})"), 1, 1)
    # middle: the run so far; the estimate of step k appears at its update
    t = np.arange(1, k + 2)
    n = k + 1 if show == 4 else k
    tb, xb, sb = (t[:n], x[:n], sd[:n]) if n != 1 else (np.array([0.8, 1.2]), x[[0, 0]], sd[[0, 0]])
    leg = dict(legend="legend2")
    fig.add_trace(go.Scatter(x=np.r_[tb, tb[::-1]], y=np.r_[xb + 2 * sb, (xb - 2 * sb)[::-1]], fill="toself", mode="lines",
                             fillcolor="rgba(76,120,168,0.25)", line=dict(width=0), name="estimate ± 2 sd", **leg), 2, 1)
    fig.add_trace(go.Scatter(x=t, y=X_TRUE[:k + 1], mode="lines+markers", line=dict(color="black", width=3),
                             name="true", **leg), 2, 1)
    fig.add_trace(go.Scatter(x=t[:n], y=x[:n], mode="lines+markers", line=dict(color=BLUE, width=3),
                             name="EKF estimate", **leg), 2, 1)
    if k >= 11:
        fig.add_annotation(x=12, y=B, text="passing the beacon (6 m)", showarrow=True, ax=90, ay=60,
                           font=dict(color=RED, size=16), row=2, col=1)
    # bottom: the slope H, one dot per linearisation
    nh = k + 1 if show >= 2 else k
    lab = [f"{m(v, '.3f')}" if i in (0, 5, 10, 11, 12, 15) else "" for i, v in enumerate(H[:nh])]
    fig.add_trace(go.Scatter(x=t[:nh], y=H[:nh], mode="lines+markers+text", line=dict(color=RED, width=3),
                             marker=dict(size=9), text=lab, textposition=[{0: "top right", 5: "top center"}.get(i, "top left") for i in range(nh)], textfont=dict(size=16, color=RED),
                             showlegend=False), 3, 1)
    fig.add_hline(y=0, line=dict(color="black", width=1), row=3, col=1)
    title = f"step {k + 1}: {NAMES[stage]}"
    note = STEP1.get(stage) if k == 0 else NOTES.get((k, stage))
    if note:
        title += f"<br><span style='font-size:18px'>{note}</span>"
    y2 = fig.layout.yaxis2.domain
    fig.update_xaxes(title="position x (m)", range=[-1.7, 9.0], dtick=1, row=1, col=1)
    fig.update_yaxes(title="distance (m)", range=[1.5, 8.3], row=1, col=1)
    for row in (2, 3):
        fig.update_xaxes(range=[0.5, 16.5], dtick=1, row=row, col=1)
    fig.update_xaxes(title="step", row=3, col=1)
    fig.update_yaxes(title="position (m)", range=[0, 8.6], row=2, col=1)
    fig.update_yaxes(title="slope H", range=[-1.15, 1.15], row=3, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1500, margin=dict(l=90, r=30, t=300, b=70),
                      legend=dict(x=0.0, y=1.0, yanchor="bottom", font=dict(size=17), traceorder="normal"),
                      legend2=dict(x=0.01, y=y2[1], yanchor="top", font=dict(size=17)),
                      title=dict(x=0.5, y=0.98, text=title))
    return fig


figs, holds = [], []
for stage, hold in zip(("predict", "linearise", "reading", "update"), (3, 3, 3, 4)):
    figs.append(frame(0, stage))
    holds.append(hold)
for k in range(1, N):
    for stage in ("a", "b"):
        figs.append(frame(k, stage))
        holds.append(2 if (k in (11, 12) and stage == "a") else 4 if k in (11, 12) else 1)
holds[-1] = 8
make_gif(figs, here / "ekf_run_anim", fps=1, holds=holds, keys=[1, 3, 27, 33], cols=2, width=850)
