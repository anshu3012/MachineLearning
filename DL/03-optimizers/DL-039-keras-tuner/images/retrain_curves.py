"""Validation accuracy after every epoch for the baseline and the tuned winner, each retrained with 5 seeds on the
Pima data: thin lines are the runs, thick lines their mean. The last frame marks each model's best epoch and last
epoch (means of 5 runs). Data: data/retrain_curves.csv (Notebook). Plotly frames: curves grow with the epochs.
Run: python retrain_curves.py -> retrain_curves.gif, retrain_curves_frames.png"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, RED
from frames import save

HERE = Path(__file__).parent
c = pd.read_csv(HERE.parent / "data" / "retrain_curves.csv")
FONT = dict(family="Latin Modern Roman", size=22)
MODELS = (("baseline", "hand-made baseline", RED), ("tuned", "tuned winner", BLUE))
BEST = c.groupby(["model", "seed"]).val_accuracy.max().groupby("model").mean()
LAST = c[c.epoch == 100].groupby("model").val_accuracy.mean()
assert round(LAST["baseline"], 3) == 0.751 and round(LAST["tuned"], 3) == 0.723          # the Note's table


def frame(e, final=False):
    fig = make_subplots(1, 2, shared_yaxes=True, horizontal_spacing=0.04, subplot_titles=[m[1] for m in MODELS])
    for k, (key, _, col) in enumerate(MODELS, start=1):
        d = c[(c.model == key) & (c.epoch <= e)]
        for _, run in d.groupby("seed"):
            fig.add_trace(go.Scatter(x=run.epoch, y=run.val_accuracy, mode="lines", line=dict(color=col, width=1), opacity=0.35), 1, k)
        m = d.groupby("epoch").val_accuracy.mean()
        fig.add_trace(go.Scatter(x=m.index, y=m.values, mode="lines", line=dict(color=col, width=4)), 1, k)
        if final:
            for y, text, dash in ((BEST[key], f"best epoch of each run: {BEST[key]:.3f}", "dot"),
                                  (LAST[key], f"last epoch: {LAST[key]:.3f}", "solid")):
                fig.add_hline(y=y, line=dict(color="black", width=1.5, dash=dash), row=1, col=k)
                fig.add_annotation(x=98, y=y + (0.012 if dash == "dot" else -0.014), xref=f"x{k if k > 1 else ''}", yref="y",
                                   xanchor="right", showarrow=False, text=text, font=dict(size=20))
    fig.update_xaxes(title="epoch", range=[0, 100])
    fig.update_yaxes(range=[0.62, 0.81])
    fig.update_yaxes(title="validation accuracy", col=1)
    fig.update_annotations(font=dict(size=22), selector=lambda a: a.yref == "paper")
    fig.update_layout(template="simple_white", width=1150, height=540, font=FONT, showlegend=False,
                      title=dict(text=f"epoch {e}" if not final else "a trial is scored at its best epoch; a retrained run at its last",
                                 x=0.5), margin=dict(l=90, r=20, t=100, b=70))
    return fig


if __name__ == "__main__":
    epochs = [1, 2, 4, 6, 8, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100]
    figs = [frame(e) for e in epochs] + [frame(100, final=True)]
    n = len(figs)
    save("retrain_curves", figs, [0] * 3 + list(range(n - 1)) + [n - 1] * 10, [5, 10, n - 2, n - 1], HERE, fps=3, gif_width=820)
