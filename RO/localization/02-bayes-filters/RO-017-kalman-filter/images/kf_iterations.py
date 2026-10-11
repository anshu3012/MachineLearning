"""The Kalman filter on the corridor, one stage per frame for all ten steps.
Top: predict (the bell moves 0.5 m and widens by Q), the reading's bell arrives, update (the product: narrower,
between the two); the red line is the true position. Middle: the run so far: true position,
readings, and the estimate with its band of two standard deviations, added step by step. Bottom: the gain K, one dot
per update, falling from 0.863 and settling at 0.224. Step 6's reading is 0.90 m too high; the estimate moves 0.21 m.
Run: python kf_iterations.py -> kf_iterations.gif, kf_iterations_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, ORANGE, PURPLE, RED, make_gif
from kfsim import P0, R, X0, X_TRUE, Z, kf1d, normal

here = Path(__file__).parent
rows = kf1d()
g = np.linspace(-2.5, 6.5, 900)
STEPS = 10
x = np.array([r["x"] for r in rows])
sd = np.sqrt([r["p"] for r in rows])
K = np.array([r["K"] for r in rows])
jump, pull = Z[5] - X_TRUE[6], rows[5]["x"] - rows[5]["x_pred"]
assert np.allclose(K[[0, 1, 2, 9]], [0.863, 0.481, 0.352, 0.224], atol=5e-4)
assert abs(rows[0]["p"] - 0.138) < 5e-4 and abs(rows[5]["K"] - 0.245) < 5e-4
assert abs(jump - 0.90) < 5e-3 and abs(pull - 0.21) < 5e-3
assert np.all(np.abs(X_TRUE[1:] - x) < 2 * sd)                     # the truth stays inside the band


def frame(k, stage, prev):
    r = rows[k]
    fig = make_subplots(rows=3, cols=1, row_heights=[0.44, 0.36, 0.2], vertical_spacing=0.07)
    # top: the bells of this step
    fig.add_trace(go.Scatter(x=g, y=normal(g, *prev), line=dict(color="#BBBBBB", width=3), name="belief before"), 1, 1)
    if stage in ("predict", "reading", "update"):
        fig.add_trace(go.Scatter(x=g, y=normal(g, r["x_pred"], r["p_pred"]), line=dict(color=BLUE, width=4),
                                 name=f"prediction {r['x_pred']:.3f}, variance {r['p_pred']:.4f}"), 1, 1)
    if stage in ("reading", "update"):
        fig.add_trace(go.Scatter(x=g, y=normal(g, r["z"], R), line=dict(color=ORANGE, width=4, dash="dash"),
                                 name=f"reading {r['z']:.2f}, variance 0.16"), 1, 1)
    if stage == "update":
        fig.add_trace(go.Scatter(x=g, y=normal(g, r["x"], r["p"]), line=dict(color=PURPLE, width=5),
                                 name=f"update {r['x']:.3f}, variance {r['p']:.4f}  (K = {r['K']:.3f})"), 1, 1)
    fig.add_vline(x=X_TRUE[k + 1], line=dict(color=RED, width=2, dash="dot"), row=1, col=1)
    fig.add_annotation(x=X_TRUE[k + 1], y=2.32, text="true", showarrow=False, font=dict(color=RED, size=17),
                       xanchor="left", row=1, col=1)
    # middle: the run so far; the reading and the estimate of step k appear at their stages
    t = np.arange(1, k + 2)
    n = k + 1 if stage == "update" else k                   # estimates done
    nz = k + 1 if stage in ("reading", "update") else k     # readings arrived
    tb, xb, sb = (t[:n], x[:n], sd[:n]) if n != 1 else (np.array([0.85, 1.15]), x[[0, 0]], sd[[0, 0]])
    leg = dict(legend="legend2")
    fig.add_trace(go.Scatter(x=np.r_[tb, tb[::-1]], y=np.r_[xb + 2 * sb, (xb - 2 * sb)[::-1]], fill="toself", mode="lines",
                             fillcolor="rgba(76,120,168,0.18)", line=dict(width=0), name="estimate ± 2 sd",
                             legendrank=4, **leg), 2, 1)
    fig.add_trace(go.Scatter(x=t, y=X_TRUE[1:k + 2], mode="lines+markers", line=dict(color="black", width=3),
                             name="true", legendrank=1, **leg), 2, 1)
    fig.add_trace(go.Scatter(x=t[:nz], y=Z[:nz], mode="markers", marker=dict(color=ORANGE, size=13, symbol="x"),
                             name="readings", legendrank=2, **leg), 2, 1)
    fig.add_trace(go.Scatter(x=t[:n], y=x[:n], mode="lines+markers", line=dict(color=BLUE, width=4),
                             name="estimate", legendrank=3, **leg), 2, 1)
    # bottom: the gain, one dot per update
    fig.add_trace(go.Scatter(x=t[:n], y=K[:n], mode="lines+markers+text", line=dict(color=RED, width=4),
                             marker=dict(size=11), text=[f"{v:.3f}" for v in K[:n]], textposition="top right",
                             textfont=dict(size=16), showlegend=False), 3, 1)
    title = f"step {k + 1}: {stage}"
    if k == 5 and stage == "update":
        title += (f"<br><span style='font-size:18px'>the reading is {jump:.2f} m too high;"
                  f" the estimate moves only {pull:.2f} m</span>")
    y2 = fig.layout.yaxis2.domain
    fig.update_xaxes(title="position (m)", range=[-2.5, 6.5], row=1, col=1)
    fig.update_yaxes(title="density", range=[0, 2.45], row=1, col=1)
    for row in (2, 3):
        fig.update_xaxes(range=[0.5, 10.5], dtick=1, row=row, col=1)
    fig.update_xaxes(title="step", row=3, col=1)
    fig.update_yaxes(title="position (m)", range=[-0.3, 6.2], row=2, col=1)
    fig.update_yaxes(title="gain K", range=[0, 1.1], row=3, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1350, margin=dict(l=90, r=30, t=190, b=70),
                      legend=dict(x=0.01, y=1.0, yanchor="bottom", font=dict(size=17)),
                      legend2=dict(x=0.01, y=y2[1], yanchor="top", font=dict(size=17)),
                      title=dict(x=0.5, y=0.985, text=title))
    return fig


figs, holds, prev = [], [], (X0, P0)
for k in range(STEPS):
    for stage in ("predict", "reading", "update"):
        figs.append(frame(k, stage, prev))
    prev = (rows[k]["x"], rows[k]["p"])
    holds += [3, 2, 3] if k == 0 else [2, 2, 4] if k in (1, 5) else [1, 1, 2]
holds[-1] = 8
make_gif(figs, here / "kf_iterations", fps=1, holds=holds, keys=[0, 2, 17, 29], cols=2, width=850)
