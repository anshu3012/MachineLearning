"""Cost-complexity pruning on the Social Network Ads data (app.load split). The fully grown tree (49 leaves) is cut
back along cost_complexity_pruning_path: one frame per alpha. Left: the decision surface. Right: training accuracy
and 5-fold cross-validation accuracy on the training set against the pruning step. CV picks the 3-leaf tree.
Run: python ccp_sweep.py -> ccp_sweep.gif, ccp_sweep_frames.png (Plotly frames + ffmpeg)"""
import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import fit, grid, traces  # noqa: E402
from gifkit import FONT, GREY, RED, make_gif  # noqa: E402

full, X_train, _, y_train, _, axes, classes = fit("ads")
alphas = full.cost_complexity_pruning_path(X_train, y_train).ccp_alphas
trees = [fit("ads", ccp_alpha=a)[0] for a in alphas]
leaves = [t.get_n_leaves() for t in trees]
train = [t.score(X_train, y_train) for t in trees]
cv = [cross_val_score(DecisionTreeClassifier(random_state=42, ccp_alpha=a), X_train, y_train, cv=5).mean() for a in alphas]
best = int(np.argmax(cv))
assert leaves[0] == 49 and leaves[best] == 3 and round(cv[best], 3) == 0.873 and round(cv[0], 3) == 0.820
xs, ys = grid(X_train)
steps = list(range(len(alphas)))


def frame(k):
    fig = make_subplots(rows=1, cols=2, column_widths=[0.55, 0.45], horizontal_spacing=0.12,
                        subplot_titles=(f"α = {alphas[k]:.4f}: {leaves[k]} leaves", "accuracy"))
    for t in traces(trees[k], X_train, y_train, classes, show_legend=False):
        fig.add_trace(t, 1, 1)
    for vals, label, col in ((train, "training", GREY), (cv, "cross-validation", RED)):
        fig.add_trace(go.Scatter(x=steps[:k + 1], y=vals[:k + 1], mode="lines+markers", name=label,
                                 line=dict(color=col, width=4), marker=dict(size=10)), 1, 2)
    if k >= best:
        fig.add_annotation(x=best, y=cv[best], text="best: 3 leaves", ax=-80, ay=50, font=dict(color=RED), row=1, col=2)
    fig.update_xaxes(range=[xs[0], xs[-1]], title=axes[0], row=1, col=1)
    fig.update_yaxes(range=[ys[0], ys[-1]], title=axes[1], showticklabels=False, row=1, col=1)
    ticks = [0, 4, 8, 10, 12, 14, 16]
    fig.update_xaxes(range=[-0.5, len(alphas) - 0.5], tickvals=ticks, ticktext=[str(leaves[i]) for i in ticks],
                     title="leaves left (α grows →)", row=1, col=2)
    fig.update_yaxes(range=[0.6, 1.02], row=1, col=2)
    fig.update_layout(template="simple_white", width=1100, height=560, font=FONT, margin=dict(l=60, r=20, t=70, b=80),
                      legend=dict(x=0.62, xanchor="left", y=0.1, font_size=20))
    fig.update_annotations(font_size=24)
    return fig


if __name__ == "__main__":
    n = len(alphas)
    make_gif([frame(k) for k in range(n)], HERE / "ccp_sweep", fps=2, holds=[2] * (n - 1) + [6], keys=[0, best], cols=1)
