"""The trained embedding model reads one short test review word by word. Top: the 32 numbers of the hidden state after
each word (blue positive, red negative). Bottom: the prediction the model would give if the review stopped there.
Data: data/running_review.csv (Notebook, last section).
Run: python running_review.py  -> running_review.gif, running_review_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from common import BLUE, GREEN, GREY, ORANGE, RED

HERE = Path(__file__).parent
run = pd.read_csv(HERE.parent / "data" / "running_review.csv")
H = run[[f"h{j}" for j in range(32)]].values.T                 # (32 units, T words)
P, WORDS, T = run.p_positive.values, run.word.tolist(), len(run)
SCALE = [[0, RED], [0.5, "white"], [1, BLUE]]


def review_text(k):
    """The whole review, read words dark, the current word orange and bold, unread words light grey."""
    out, line = [], 0
    for i, w in enumerate(WORDS):
        style = f"color:{ORANGE}" if i == k else ("color:black" if i < k else "color:#C8C8C8")
        out.append(f"<b><span style='{style}'>{w}</span></b>" if i == k else f"<span style='{style}'>{w}</span>")
        line += len(w) + 1
        if line > 52 and i < T - 1:
            out.append("<br>")
            line = 0
    return " ".join(out).replace(" <br> ", "<br>")


def frame(k):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.58, 0.42], vertical_spacing=0.06)
    Z = np.full_like(H, np.nan)
    Z[:, :k + 1] = H[:, :k + 1]
    fig.add_trace(go.Heatmap(z=Z, x=list(range(T)), zmin=-1, zmax=1, colorscale=SCALE, showscale=False), 1, 1)
    fig.add_trace(go.Scatter(x=[-0.5, T - 0.5], y=[0.5, 0.5], mode="lines", line=dict(color=GREY, dash="dot", width=2),
                             showlegend=False), 2, 1)
    fig.add_trace(go.Scatter(x=list(range(k + 1)), y=P[:k + 1], mode="lines+markers", showlegend=False,
                             line=dict(color=GREEN, width=4), marker=dict(size=9, color=GREEN)), 2, 1)
    fig.add_trace(go.Scatter(x=[k], y=[P[k]], mode="markers+text", text=[f"{P[k]:.2f}"], showlegend=False,
                             textposition="top center" if P[k] < 0.8 else "bottom center",
                             textfont=dict(size=24, color=GREEN), marker=dict(size=16, color=ORANGE)), 2, 1)
    fig.update_yaxes(title_text="hidden state<br>(32 numbers)", showticklabels=False, row=1, col=1)
    fig.update_yaxes(title_text="P(positive)", range=[0, 1.05], dtick=0.5, row=2, col=1)
    fig.update_xaxes(range=[-0.5, T - 0.5], tickvals=list(range(T)), ticktext=WORDS, tickangle=-60,
                     tickfont=dict(size=19), row=2, col=1)
    fig.update_layout(template="simple_white", width=1000, height=760, font=dict(family="Latin Modern Roman", size=22),
                      margin=dict(l=110, r=25, t=150, b=110),
                      annotations=list(fig.layout.annotations) + [
                          dict(text=review_text(k), x=0.5, y=1.02, xref="paper", yref="paper", yanchor="bottom",
                               showarrow=False, font=dict(size=22), align="left")])
    return fig


if __name__ == "__main__":
    tmp = HERE / ".review_frames"
    tmp.mkdir(exist_ok=True)
    for k in range(T):
        frame(k).write_image(tmp / f"{k:03d}.png")
    for i in range(T, T + 10):                                    # hold the last frame
        shutil.copy(tmp / f"{T - 1:03d}.png", tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "running_review.gif")], check=True)
    shutil.copy(tmp / f"{T - 1:03d}.png", HERE / "running_review_frames.png")   # the last frame holds the whole story
    shutil.rmtree(tmp)
