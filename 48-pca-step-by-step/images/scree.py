"""Scree plot of the Note's 3-feature example (40 points, two classes, seed 23), built one component at a time:
each bar is one eigenvalue divided by the sum of all three; the line is the running total.
Plotly frames -> GIF (bars that appear one by one)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from anim import save_gif, FONT, BLUE, ORANGE

here = Path(__file__).parent
np.random.seed(23)
c1 = np.random.multivariate_normal([0, 0, 0], np.eye(3), 20)
c2 = np.random.multivariate_normal([1, 1, 1], np.eye(3), 20)
X = StandardScaler().fit_transform(np.vstack([c1, c2]))
vals, vecs = np.linalg.eigh(np.cov(X.T))
vals, vecs = vals[::-1], vecs[:, ::-1]
share = 100 * vals / vals.sum()
cum = share.cumsum()
print("eigenvalues", vals.round(3), "percent", share.round(1), "PC1 loadings", vecs[:, 0].round(3),
      "PC2 loadings", vecs[:, 1].round(3))
assert list(vals.round(3)) == [1.354, 0.946, 0.778]
names = ["PC1", "PC2", "PC3"]


def frame(k):
    fig = go.Figure()
    fig.add_bar(x=names[:k], y=share[:k], marker_color=BLUE, width=0.8, textangle=0,
                text=[f"{vals[i]:.3f} ÷ {vals.sum():.3f}<br>= <b>{share[i]:.0f}%</b>" for i in range(k)],
                textposition="inside", insidetextanchor="middle", textfont=dict(size=19, color="white"))
    if k:
        fig.add_scatter(x=names[:k], y=cum[:k], mode="lines+markers+text", line=dict(color=ORANGE, width=4),
                        marker=dict(size=14), text=[f"{c:.0f}%" for c in cum[:k]], textposition="top center",
                        textfont=dict(size=24, color=ORANGE))
    head = ("Scree plot: each eigenvalue as a share of the total" if k == 0 else
            f"PC1 alone keeps {cum[0]:.0f}% of the variance" if k == 1 else
            f"PC1 to PC{k} together keep {cum[k - 1]:.0f}%")
    fig.update_layout(template="simple_white", width=900, height=640, font=FONT, showlegend=False,
                      title=dict(text=head, x=0.5), margin=dict(l=90, r=30, t=80, b=60),
                      xaxis=dict(range=[-0.6, 2.6], categoryorder="array", categoryarray=names, type="category"),
                      yaxis=dict(range=[0, 112], title="percent of the total variance"))
    fig.add_annotation(x=-0.5, y=106, xanchor="left", showarrow=False, font=dict(size=19),
                       text=f"bars: one component   <span style='color:{ORANGE}'>line: running total</span>")
    return fig


if __name__ == "__main__":
    save_gif([frame(k) for k in range(4)], "scree", here, keys=[1, 3], fps=1, holds=[2, 2, 2, 6])
