"""Validation accuracy of the three methods drawn epoch by epoch (mean of 3 seeds), then the test accuracy
(bars: mean; whiskers: lowest and highest of 3 seeds). Data: data/history.csv, data/test_accuracy.csv (Notebook).
Plotly frames: curves grow with the epochs. Run: python results_anim.py -> results_anim.gif, results_anim_frames.png"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import GREY, BLUE, GREEN
from frames import save

HERE = Path(__file__).parent
h = pd.read_csv(HERE.parent / "data" / "history.csv")
t = pd.read_csv(HERE.parent / "data" / "test_accuracy.csv")
NAMES = {"scratch": ("from scratch", GREY), "feature_extraction": ("feature extraction", BLUE),
         "fine_tuning": ("fine-tuning", GREEN)}
FONT = dict(family="Latin Modern Roman", size=22)
MEAN = {k: h[h.method == k].groupby("epoch").val_accuracy.mean() for k in NAMES}
assert len(MEAN["scratch"]) == 60 and len(MEAN["fine_tuning"]) == 20


def frame(e, bars=False):
    fig = make_subplots(rows=1, cols=2, column_widths=[0.64, 0.36], horizontal_spacing=0.1,
                        subplot_titles=("validation accuracy", "test accuracy"))
    for key, (name, c) in NAMES.items():
        m = MEAN[key][MEAN[key].index <= e]
        fig.add_trace(go.Scatter(x=m.index, y=m.values, mode="lines", line=dict(color=c, width=4)), row=1, col=1)
        fig.add_trace(go.Scatter(x=[m.index[-1]], y=[m.values[-1]], mode="markers+text", marker=dict(color=c, size=12),
                                 text=[f"{name} {m.values[-1]:.2f}"], textfont=dict(color=c),
                                 textposition="bottom right" if key == "feature_extraction" else "top right"), row=1, col=1)
        s = t[t.method == key].test_accuracy
        label = name.replace(" ", "<br>")
        fig.add_trace(go.Bar(x=[label], y=[s.mean() if bars else 0], marker_color=c,
                             error_y=dict(type="data", symmetric=False, array=[s.max() - s.mean()],
                                          arrayminus=[s.mean() - s.min()], visible=bars)), row=1, col=2)
        if bars:
            fig.add_annotation(x=label, y=0.6, text=f"{s.mean():.3f}", showarrow=False, font=dict(color="white", size=22),
                               xref="x2", yref="y2")
    fig.add_vline(x=10.5, line=dict(color=GREEN, width=1.5, dash="dot"), row=1, col=1)
    fig.add_annotation(x=11, y=0.84, text="block 5 unfrozen", showarrow=False, xanchor="left", font=dict(color=GREEN, size=18),
                       xref="x", yref="y")
    fig.update_xaxes(title="epoch", range=[0, 105], tickvals=[1, 10, 20, 40, 60], row=1, col=1)
    fig.update_yaxes(title="accuracy", range=[0.5, 1.06], tickvals=[0.5, 0.6, 0.7, 0.8, 0.9, 1.0], row=1, col=1)
    fig.update_yaxes(range=[0.5, 1.03], row=1, col=2)
    fig.update_xaxes(tickangle=0, row=1, col=2)
    fig.update_annotations(font_size=22, selector=dict(text="validation accuracy"))
    fig.update_annotations(font_size=22, selector=dict(text="test accuracy"))
    fig.update_layout(template="simple_white", width=1150, height=540, font=FONT, showlegend=False,
                      title=dict(text=f"epoch {e}" if not bars else "after training: the test photos, used once", x=0.5),
                      margin=dict(l=80, r=20, t=100, b=70))
    return fig


if __name__ == "__main__":
    epochs = [1, 2, 3, 4, 5, 6, 8, 10, 11, 12, 14, 16, 18, 20, 25, 30, 35, 40, 45, 50, 55, 60]
    figs = [frame(e) for e in epochs] + [frame(60, bars=True)]
    n = len(figs)
    seq = [0] * 4 + list(range(n - 1)) + [n - 1] * 10
    save("results_anim", figs, seq, [0, 7, 13, n - 1], HERE, fps=3, gif_width=820)
