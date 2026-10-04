"""Section 6: where a histogram comes from. The 714 known Titanic ages start as dots on one line, where they hide each
other; the range is cut into 5-year bins; the dots of each bin are stacked; each stack becomes a bar as tall as its count.
Plotly frames (dots moving into stacks) -> GIF, plus a key-frame grid for the PDF."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from gifkit import save_gif

HERE = Path(__file__).parent
BLUE = "#4C78A8"
age = pd.read_csv(HERE.parent / "data" / "titanic_train.csv")["Age"].dropna().sort_values().to_numpy()
W = 5
bins = np.minimum(age // W, 80 // W - 1).astype(int)             # age 80 goes in the last bin, as in Figure 6
rank = pd.Series(age).groupby(bins).cumcount().to_numpy() + 1   # position of each dot inside its bin's stack
counts = np.bincount(bins, minlength=80 // W)
centre = bins * W + W / 2


def frame(title, x, y, cuts=False, bars=False):
    fig = go.Figure()
    if bars:
        fig.add_bar(x=np.arange(80 // W) * W + W / 2, y=counts, width=W, marker=dict(color=BLUE, opacity=0.35, line=dict(color="white", width=1)),
                    text=counts, textposition="outside", textfont=dict(size=15))
    if cuts:
        for c in range(0, 81, W):
            fig.add_shape(type="line", x0=c, x1=c, y0=0, y1=125, line=dict(color="#BBBBBB", width=1, dash="dot"))
    fig.add_scatter(x=x, y=y, mode="markers", marker=dict(color=BLUE, size=5 if y.max() > 1 else 11, opacity=0.9 if y.max() > 1 else 0.35))
    fig.update_layout(template="simple_white", width=1000, height=600, showlegend=False, font=dict(family="Latin Modern Roman", size=19),
                      title=dict(text=title, x=0.5), xaxis=dict(title="Age (years)", range=[-1, 82], dtick=10),
                      yaxis=dict(title="Passengers", range=[-3, 130]), margin=dict(l=80, r=20, t=90, b=70))
    return fig


if __name__ == "__main__":
    flat = np.zeros(len(age))
    figs = [frame("714 ages as dots on one line: the dots hide each other", age, flat),
            frame("Cut the range into bins, each 5 years wide", age, flat, cuts=True),
            frame("Move every dot to its bin ...", centre, flat, cuts=True),
            frame("... and stack the dots of each bin: one dot = one passenger", centre, rank, cuts=True),
            frame("Draw a bar as tall as each stack: a histogram", centre, rank, cuts=True, bars=True)]
    save_gif(figs, "hist_build", HERE, keys=[0, 1, 3, 4], fps=0.7)
    print(counts)
