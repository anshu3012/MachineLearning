"""The all-in-one random search of section 8, trial by trial: each trial appears as a dot at (number of hidden
layers, nodes in all hidden layers), coloured by its validation accuracy; the best so far is ringed.
Data: data/trials.csv (Notebook). Plotly frames: one trial per frame.
Run: python trial_search.py -> trial_search.gif, trial_search_frames.png"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from common import GREY, RED
from frames import save

HERE = Path(__file__).parent
t = pd.read_csv(HERE.parent / "data" / "trials.csv").sort_values("trial").reset_index(drop=True)
t["nodes"] = [sum(int(p.split()[0]) for p in s.split(", ")) for s in t.layers]
t["x"] = t.num_layers + (t.groupby("num_layers").cumcount() - t.groupby("num_layers").num_layers.transform("size") / 2) * 0.07
FONT = dict(family="Latin Modern Roman", size=22)
assert len(t) == 20 and t.val_accuracy.idxmax() == 2


def frame(k):
    """Trials 0..k-1 shown."""
    s = t.iloc[:k]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=s.x, y=s.nodes, mode="markers",
                             marker=dict(size=26, color=s.val_accuracy, cmin=0.74, cmax=0.78, colorscale="Viridis",
                                         showscale=True, line=dict(color="white", width=1),
                                         colorbar=dict(title="validation<br>accuracy", tickformat=".2f", dtick=0.01))))
    msg = "the search space: 1 to 4 layers, 8 to 128 nodes each"
    if k:
        b = s.loc[s.val_accuracy.idxmax()]
        fig.add_trace(go.Scatter(x=[b.x], y=[b.nodes], mode="markers",
                                 marker=dict(size=44, color="rgba(0,0,0,0)", line=dict(color=RED, width=4))))
        last = s.iloc[-1]
        msg = (f"trial {k - 1}: {last.num_layers} layer{'s' if last.num_layers > 1 else ''}, {last.optimizer}, "
               f"score {last.val_accuracy:.3f}  |  best so far: trial {int(b.trial)}, {b.val_accuracy:.3f}")
    fig.update_layout(template="simple_white", width=1000, height=600, font=FONT, showlegend=False,
                      title=dict(text=msg, x=0.5, font=dict(size=22)),
                      xaxis=dict(title="number of hidden layers", range=[0.5, 4.5], tickvals=[1, 2, 3, 4]),
                      yaxis=dict(title="nodes in all hidden layers", range=[0, 300]),
                      margin=dict(l=90, r=20, t=70, b=70))
    return fig


if __name__ == "__main__":
    figs = [frame(k) for k in range(21)]
    seq = [0] * 3 + [k for k in range(1, 21) for _ in range(2)] + [20] * 8
    save("trial_search", figs, seq, [1, 3, 10, 20], HERE, fps=2.5)
