"""Angles between 20,000 random pairs of directions, as the dimension grows from 2 to 12,288.
Data: data/random_angles_hist.csv, data/random_angles_summary.csv (Notebook). Run: python dims_sweep.py"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from common import BLUE, GREY, RED, FONT
from gif_tools import save_gif

HERE = Path(__file__).parent
h = pd.read_csv(HERE.parent / "data" / "random_angles_hist.csv")
s = pd.read_csv(HERE.parent / "data" / "random_angles_summary.csv").set_index("d")


def frame(d):
    y = h[str(d)] * 100
    fig = go.Figure(go.Bar(x=h.angle, y=y, marker_color=BLUE, width=1.0, marker_line_width=0))
    fig.add_vrect(x0=85, x1=95, fillcolor=RED, opacity=0.12, line_width=0)
    fig.add_annotation(x=0.98, y=0.95, xref="paper", yref="paper", xanchor="right", showarrow=False, align="right",
                       text=f"<b>{s.share_85_95[d] * 100:.0f}%</b> of pairs<br>within 5° of 90°",
                       font=dict(size=24, color=RED))
    fig.update_layout(template="simple_white", width=900, height=560, font=dict(FONT, size=20), bargap=0,
                      title=dict(text=f"Random directions in <b>{d:,}</b> dimensions: angle between two of them", x=0.5),
                      xaxis=dict(title="angle (degrees)", range=[0, 180], tickvals=[0, 45, 90, 135, 180]),
                      yaxis=dict(title="share of pairs (%)", range=[0, max(y) * 1.15]),
                      margin=dict(l=80, r=30, t=70, b=70))
    return fig


DIMS = [2, 3, 10, 30, 100, 300, 1000, 12288]
figs, keys = [], []
for d in DIMS:
    if d in (3, 100, 1000, 12288):
        keys.append(len(figs))
    figs += [frame(d)] * (6 if d != 12288 else 12)
if __name__ == "__main__":
    save_gif(figs, keys, "dims_sweep", HERE, fps=3)
