"""10,000 directions in 100 dimensions, nudged to be more perpendicular: the angle histogram at every step
(log scale, so the rare far-off pairs stay visible). Data: data/optimise_hist.csv, data/optimise_stats.csv.
Run: python angle_squeeze.py"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from common import BLUE, GREY, RED, ORANGE, FONT
from gif_tools import save_gif

HERE = Path(__file__).parent
h = pd.read_csv(HERE.parent / "data" / "optimise_hist.csv")
st = pd.read_csv(HERE.parent / "data" / "optimise_stats.csv").set_index("step")
start = h["0"].replace(0, np.nan) * 100


def frame(k):
    y = h[str(k)].replace(0, np.nan) * 100
    w = st.worst_deg_from_90[k]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=h.angle, y=start, mode="lines", line=dict(color=GREY, width=2, dash="dot"),
                             name="step 0 (random)"))
    fig.add_trace(go.Bar(x=h.angle, y=y, marker_color=BLUE, width=0.5, marker_line_width=0, name=f"step {k}"))
    for x in (90 - w, 90 + w):
        fig.add_vline(x=x, line=dict(color=RED, width=3))
    fig.add_annotation(x=0.99, y=0.97, xref="paper", yref="paper", xanchor="right", showarrow=False, align="right",
                       text=f"every pair lies between<br>the red lines: worst<br>pair {w:.1f}° from 90°",
                       font=dict(size=18, color=RED), bgcolor="rgba(255,255,255,0.85)")
    fig.add_annotation(x=0.01, y=0.97, xref="paper", yref="paper", xanchor="left", showarrow=False, align="left",
                       text=f"RMS cosine {st.rms_cos[k]:.4f}<br>floor (no arrangement<br>can go lower): 0.0995",
                       font=dict(size=18, color=ORANGE))
    fig.update_layout(template="simple_white", width=900, height=620, font=dict(FONT, size=20), bargap=0,
                      title=dict(text=f"10,000 directions in 100 dimensions, optimisation step {k}", x=0.5),
                      xaxis=dict(title="angle between two directions (degrees)", range=[55, 125]),
                      yaxis=dict(title="share of pairs (%, log scale)", type="log", range=[-6.3, 1],
                                 tickvals=[10.0 ** k for k in range(-6, 2)],
                                 ticktext=["10<sup>%d</sup>" % k if k not in (0, 1) else str(10 ** k) for k in range(-6, 2)]),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2), margin=dict(l=90, r=30, t=70, b=110))
    return fig


steps = list(range(0, 11)) + list(range(12, 61, 4))
figs = [frame(0)] * 4 + [frame(k) for k in steps] + [frame(60)] * 8
if __name__ == "__main__":
    save_gif(figs, [0, 6, 13, len(figs) - 1], "angle_squeeze", HERE, fps=4)
