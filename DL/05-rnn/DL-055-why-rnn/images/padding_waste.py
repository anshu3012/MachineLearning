"""The cost of choosing one input length for an ANN, on the 25,000 IMDB training reviews: every review is padded
with zeros up to the chosen length (grey) or cut at it (red). As the length grows from 100 to 2,494 words, fewer
reviews are cut but more of the input is padding (90% at 2,494). Plotly frames -> GIF, plus a key-frame grid."""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from common import BLUE, RED, GREY, FONT
from gifkit import save_gif

HERE = Path(__file__).parent
L = np.sort(pd.read_csv(HERE.parent / "data" / "imdb_lengths.csv").query("split == 'train'").length.values)
SHOW = L[np.linspace(0, len(L) - 1, 200).round().astype(int)]          # 200 reviews spread over the sorted lengths
STEPS = [100, 200, 500, 1000, 2494]


def stats(m):
    return 100 * np.mean(1 - np.minimum(L, m) / m), 100 * np.mean(L > m)


assert round(stats(2494)[0]) == 90 and round(stats(500)[1], 1) == 8.4     # the Note's numbers


def frame(m):
    pad, cut = stats(m)
    x = np.arange(len(SHOW))
    fig = go.Figure()
    fig.add_bar(x=x, y=np.minimum(SHOW, m), marker_color=BLUE, name="words kept")
    fig.add_bar(x=x, y=np.maximum(m - SHOW, 0), marker_color="#C9C9C9", name="zero padding")
    fig.add_bar(x=x, y=np.maximum(SHOW - m, 0), marker_color=RED, name="words cut off")
    fig.add_hline(y=m, line=dict(color="black", width=2, dash="dash"))
    fig.add_annotation(x=5, y=m, text=f"input length {m:,} words", showarrow=False, yshift=16, xanchor="left",
                       font=dict(size=20))
    fig.update_layout(barmode="stack", bargap=0, template="simple_white", width=1000, height=600, font=dict(FONT, size=20),
                      title=dict(text=f"<b>{pad:.0f}%</b> of the input is padding · <b>{cut:.1f}%</b> of reviews are cut",
                                 x=0.5, y=0.95),
                      xaxis=dict(title="the 25,000 training reviews, shortest to longest (200 shown)", showticklabels=False),
                      yaxis=dict(title="words", range=[0, 2600]),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=1.08), margin=dict(l=80, r=20, t=110, b=60))
    return fig


if __name__ == "__main__":
    save_gif([frame(m) for m in STEPS], "padding_waste", HERE, keys=[0, 2, 3, 4], fps=0.7, holds=[1, 1, 2, 1, 4])
