"""Sweep k from 1 to n = 455 on the Note's two breast cancer features: the decision surface goes from islands
(overfitting) to smooth to all blue (underfitting), while test accuracy is traced on the right.
Run: python knn_k_sweep.py  -> knn_k_sweep.gif, knn_k_sweep_frames.png (Plotly frames + ffmpeg)"""
import sys
from pathlib import Path

import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import X_train, traces, xs, ys
from knn_vote import save

KS = [1, 2, 3, 5, 8, 12, 20, 30, 50, 80, 130, 200, 300, len(X_train)]
runs = [traces(k, show_legend=False) for k in KS]
acc = [a for _, a in runs]
print(dict(zip(KS, [round(a, 3) for a in acc])))
assert acc[0] < max(acc) and acc[-1] < max(acc)          # both ends worse than the middle


def frame(i):
    fig = make_subplots(rows=1, cols=2, column_widths=[0.62, 0.38], horizontal_spacing=0.12)
    for t in runs[i][0]:
        fig.add_trace(t, 1, 1)
    fig.add_trace(go.Scatter(x=KS[:i + 1], y=acc[:i + 1], mode="lines+markers", line=dict(color="black", width=3),
                             marker=dict(size=10), showlegend=False), 1, 2)
    fig.add_trace(go.Scatter(x=[KS[i]], y=[acc[i]], mode="markers", marker=dict(size=20, color="#E45756"),
                             showlegend=False), 1, 2)
    fig.update_traces(marker_size=9, selector=dict(mode="markers"), row=1, col=1)
    k = KS[i]
    tag = " (= n)" if k == len(X_train) else ""
    fig.update_xaxes(range=[xs[0], xs[-1]], title="mean radius", row=1, col=1)
    fig.update_yaxes(range=[ys[0], ys[-1]], title="mean texture", row=1, col=1)
    fig.update_xaxes(type="log", range=[-0.1, 2.75], title="k (log scale)", tickvals=[1, 3, 10, 30, 100, 455], row=1, col=2)
    fig.update_yaxes(range=[0.55, 0.95], title="test accuracy", row=1, col=2)
    fig.update_layout(template="simple_white", width=1100, height=600, font=dict(family="Latin Modern Roman", size=24),
                      title=dict(text=f"k = {k}{tag}: test accuracy {acc[i]:.2f}", x=0.5, y=0.96),
                      margin=dict(l=80, r=30, t=80, b=70))
    return fig


if __name__ == "__main__":
    save([frame(i) for i in range(len(KS))], "knn_k_sweep", keys=(0, 3, 6, len(KS) - 1), fps=2, hold=6)
