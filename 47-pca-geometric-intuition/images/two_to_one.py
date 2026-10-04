"""Feature extraction: the Note's 30 made-up flats (rooms, washrooms) are moved onto the PC1 line, so each flat is
described by one number, its position along PC1. PC1 holds 98 percent of the variance. Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.decomposition import PCA
from flats import rooms, washrooms
from anim import save_gif, FONT, BLUE, ORANGE

here = Path(__file__).parent
P = np.c_[rooms, washrooms]
pca = PCA(n_components=1).fit(P)
assert round(pca.explained_variance_ratio_[0], 3) == 0.981
m, u = P.mean(axis=0), pca.components_[0]
s = (P - m) @ u
Q = m + np.outer(s, u)


def frame(t, last=False):
    X = (1 - t) * P + t * Q
    fig = go.Figure()
    fig.add_scatter(x=m[0] + np.array([-3.5, 3.5]) * u[0], y=m[1] + np.array([-3.5, 3.5]) * u[1], mode="lines",
                    line=dict(color=ORANGE, width=3))
    if t > 0:
        for a, b in zip(P, X):
            fig.add_scatter(x=[a[0], b[0]], y=[a[1], b[1]], mode="lines", line=dict(color="#cccccc", width=1))
    fig.add_scatter(x=X[:, 0], y=X[:, 1], mode="markers", marker=dict(size=11, color=BLUE))
    if last:
        for v in (s.min(), 0, s.max()):
            p = m + v * u
            fig.add_annotation(x=p[0], y=p[1], text=f"{v:+.1f}", ax=25, ay=25, font=dict(size=17, color="#c55a00"))
    head = ("30 flats, 2 features: rooms and washrooms" if t == 0 else
            "each flat moves onto PC1 (orange)" if not last else "1 new feature: the position along PC1 (98 percent of the variance)")
    fig.update_layout(template="simple_white", width=900, height=800, font=FONT, showlegend=False,
                      title=dict(text=head, x=0.5, font=dict(size=21)),
                      xaxis=dict(title="rooms", range=[0, 6]), yaxis=dict(title="washrooms", range=[0, 6], scaleanchor="x"),
                      margin=dict(l=80, r=30, t=80, b=70))
    return fig


if __name__ == "__main__":
    figs = [frame(0), frame(0.35), frame(0.7), frame(1), frame(1, True)]
    save_gif(figs, "two_to_one", here, keys=[0, 4], fps=2, holds=[4, 1, 1, 2, 8])
