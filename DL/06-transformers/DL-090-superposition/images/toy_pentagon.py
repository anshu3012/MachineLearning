"""Training the toy model with 5 equally important features, each non-zero only 5 percent of the time (S = 0.95),
in 2 hidden numbers: the 5 feature directions spread out into a regular pentagon.
Data: data/toy_training.csv (Notebook). Run: python toy_pentagon.py"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from common import GREY, FONT
from gif_tools import save_gif

HERE = Path(__file__).parent
tr = pd.read_csv(HERE.parent / "data" / "toy_training.csv")
C = ["#B2182B", "#EF8A62", "#4C78A8", "#54A24B", "#B279A2"]
steps = sorted(tr.step.unique())


def frame(s):
    d = tr[tr.step == s].sort_values("feature")
    ang = np.sort(np.degrees(np.arctan2(d.w2, d.w1)) % 360)
    gaps = np.diff(np.r_[ang, ang[0] + 360])
    fig = go.Figure()
    th = np.linspace(0, 2 * np.pi, 200)
    fig.add_trace(go.Scatter(x=np.cos(th), y=np.sin(th), mode="lines", line=dict(color=GREY, dash="dot", width=1),
                             showlegend=False))
    for _, r in d.iterrows():
        i = int(r.feature) - 1
        fig.add_trace(go.Scatter(x=[0, r.w1], y=[0, r.w2], mode="lines+markers", line=dict(color=C[i], width=6),
                                 marker=dict(size=[0, 16], color=C[i]), name=f"feature {i + 1}"))
    fig.update_layout(template="simple_white", width=720, height=760, font=dict(FONT, size=20),
                      title=dict(text=f"training step {s:,}<br><span style='font-size:18px'>angles between neighbours: "
                                      + ", ".join(f"{x:.0f}°" for x in np.sort(gaps)) + "</span>", x=0.5),
                      xaxis=dict(range=[-1.4, 1.4], title="hidden number 1"),
                      yaxis=dict(range=[-1.4, 1.4], title="hidden number 2", scaleanchor="x"),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.12),
                      margin=dict(l=70, r=20, t=110, b=110))
    return fig


show = steps
figs = [frame(s) for s in show] + [frame(steps[-1])] * 8
if __name__ == "__main__":
    save_gif(figs, [0, 3, 10, len(figs) - 1], "toy_pentagon", HERE, fps=4, width=560)
