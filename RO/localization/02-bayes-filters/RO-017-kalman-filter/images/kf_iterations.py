"""The Kalman filter on the corridor, one stage per frame for the first five steps: predict (the bell moves 0.5 m
and widens by Q), the reading's bell arrives, update (the product: narrower, between the two). The red line is the
true position. Run: python kf_iterations.py -> kf_iterations.gif, kf_iterations_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, ORANGE, PURPLE, RED, make_gif
from kfsim import P0, R, X0, X_TRUE, Z, kf1d, normal

here = Path(__file__).parent
rows = kf1d()
g = np.linspace(-2.5, 6.5, 900)
STEPS = 5


def frame(k, stage, prev):
    fig = go.Figure()
    r = rows[k]
    fig.add_trace(go.Scatter(x=g, y=normal(g, *prev), line=dict(color="#BBBBBB", width=3), name="belief before"))
    if stage in ("predict", "reading", "update"):
        fig.add_trace(go.Scatter(x=g, y=normal(g, r["x_pred"], r["p_pred"]), line=dict(color=BLUE, width=4),
                                 name=f"prediction {r['x_pred']:.3f}, variance {r['p_pred']:.4f}"))
    if stage in ("reading", "update"):
        fig.add_trace(go.Scatter(x=g, y=normal(g, r["z"], R), line=dict(color=ORANGE, width=4, dash="dash"),
                                 name=f"reading {r['z']:.2f}, variance 0.16"))
    if stage == "update":
        fig.add_trace(go.Scatter(x=g, y=normal(g, r["x"], r["p"]), line=dict(color=PURPLE, width=5),
                                 name=f"update {r['x']:.3f}, variance {r['p']:.4f}  (K = {r['K']:.3f})"))
    fig.add_vline(x=X_TRUE[k + 1], line=dict(color=RED, width=2, dash="dot"))
    fig.add_annotation(x=X_TRUE[k + 1], y=2.05, text="true", showarrow=False, font=dict(color=RED, size=17), xanchor="left")
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=600, margin=dict(l=80, r=30, t=170, b=70),
                      legend=dict(x=0.01, y=1.0, yanchor="bottom", font=dict(size=17)),
                      title=dict(x=0.5, y=0.97, text=f"step {k + 1}: {stage}"),
                      xaxis=dict(title="position (m)", range=[-2.5, 6.5]), yaxis=dict(title="density", range=[0, 2.2]))
    return fig


figs, prev = [], (X0, P0)
for k in range(STEPS):
    for stage in ("predict", "reading", "update"):
        figs.append(frame(k, stage, prev))
    prev = (rows[k]["x"], rows[k]["p"])
make_gif(figs, here / "kf_iterations", fps=1, holds=[2, 2, 3] * STEPS, keys=[0, 1, 2, 5], cols=2, width=850)
