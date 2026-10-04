"""Running parameter tally, matrix kind by matrix kind, for GPT-2 small (counted from the released weights) and
GPT-3 175B (Brown et al. 2020, Table 2.1 sizes; tied unembedding). Each bar is 100 percent of that model.
Data: data/param_tally.csv from the Notebook.
Run: python param_tally.py -> param_tally.gif, param_tally_frames.png (Plotly frames + ffmpeg)"""
import re
import shutil
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from PIL import Image

from common import BLUE, ORANGE, GREEN, GREY, FONT, DATA, gif, grid

HERE = Path(__file__).parent
t = pd.read_csv(DATA / "param_tally.csv")
KINDS = list(dict.fromkeys(t.kind))
SHORT = {KINDS[0]: "W<sub>E</sub>", KINDS[1]: "W<sub>P</sub>", "query W_Q": "W<sub>Q</sub>", "key W_K": "W<sub>K</sub>",
         "value W_V": "W<sub>V</sub>", "attention output W_O": "W<sub>O</sub>", "MLP up": "MLP up", "MLP down": "MLP down", "biases and layer norms": "b, LN"}
COL = {KINDS[0]: BLUE, KINDS[1]: "#9ECAE9", "query W_Q": ORANGE, "key W_K": "#FFBF79", "value W_V": ORANGE,
       "attention output W_O": "#FFBF79", "MLP up": GREEN, "MLP down": "#88D27A", "biases and layer norms": GREY}
MODELS = ["GPT-3 175B", "GPT-2 small"]                     # bottom to top
fmt = lambda n: f"{n/1e9:.1f} billion" if n >= 1e9 else f"{n/1e6:.1f} million"


def frame(k):
    fig = go.Figure()
    for kind in KINDS[:k]:
        sub = t[t.kind == kind].set_index("model").loc[MODELS]
        fig.add_trace(go.Bar(y=MODELS, x=sub.share_percent, orientation="h", marker_color=COL[kind], name=SHORT[kind],
                             marker_line=dict(color="white", width=1.5), showlegend=False,
                             text=[SHORT[kind] if s > 4.5 else "" for s in sub.share_percent], textposition="inside",
                             insidetextanchor="middle", textangle=0, textfont=dict(size=17, color="white")))
    tot = {m: t[(t.model == m) & t.kind.isin(KINDS[:k])].parameters.sum() for m in MODELS}
    full = {m: t[t.model == m].parameters.sum() for m in MODELS}
    for m in MODELS:
        fig.add_annotation(x=100, y=m, xanchor="right", yshift=50, showarrow=False, font=dict(size=19),
                           text=f"{fmt(tot[m])} of {fmt(full[m])}")
    new = KINDS[k - 1] if k else ""
    head = "+ " + re.sub(r"W_(\w)", r"W<sub>\1</sub>", new) if k else "Counting the weights, one kind of matrix at a time"
    fig.update_layout(template="simple_white", width=960, height=520, font=FONT, barmode="stack", bargap=0.6,
                      title=dict(text=head, x=0.5, y=0.95, font=dict(size=24)),
                      xaxis=dict(range=[0, 100], title="share of the model's parameters (percent)"),
                      yaxis=dict(tickfont=dict(size=21)), margin=dict(l=150, r=30, t=110, b=70))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".tally_frames"
    tmp.mkdir(exist_ok=True)
    seq = [0, 0] + [k for k in range(1, len(KINDS) + 1) for _ in range(3)] + [len(KINDS)] * 8
    for i, k in enumerate(seq):
        if i == 0 or k != seq[i - 1]:
            frame(k).write_image(tmp / f"{i:03d}.png")
        else:
            shutil.copy(tmp / f"{i-1:03d}.png", tmp / f"{i:03d}.png")
    gif(tmp / "%03d.png", HERE / "param_tally.gif", fps=3, framerate=3, width=800)
    key = [seq.index(k) for k in (2, 6, 8)] + [len(seq) - 1]
    grid([Image.open(tmp / f"{i:03d}.png") for i in key], HERE / "param_tally_frames.png")
    shutil.rmtree(tmp)
