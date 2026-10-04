"""Mean centring as shifting: the 150 iris flowers (sepal length, sepal width) slide, every point by the same vector,
until their mean sits at the origin. The shape of the cloud does not change. Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import load_iris
from anim import save_gif, FONT, BLUE, RED

here = Path(__file__).parent
X = load_iris().data[:, :2]
mu = X.mean(axis=0)
C = X - mu
assert np.allclose(C.mean(axis=0), 0) and np.allclose(C.std(axis=0), X.std(axis=0))


def frame(t):
    P = X - t * mu
    m = P.mean(axis=0)
    fig = go.Figure()
    fig.add_scatter(x=P[:, 0], y=P[:, 1], mode="markers", marker=dict(size=7, color=BLUE, opacity=0.6))
    fig.add_scatter(x=[m[0]], y=[m[1]], mode="markers", marker=dict(size=18, color=RED, symbol="x"))
    fig.add_annotation(x=m[0], y=m[1], text=f"mean ({m[0] + 0:.2f}, {m[1] + 0:.2f})".replace("-0.00", "0.00"), ax=60, ay=-40, font=dict(size=18, color=RED))
    fig.update_layout(template="simple_white", width=900, height=760, font=FONT, showlegend=False,
                      title=dict(text=f"subtract {t:.2f} × the mean ({mu[0]:.2f}, {mu[1]:.2f}) from every flower", x=0.5),
                      xaxis=dict(title="sepal length (cm)", range=[-3, 8.5], zeroline=True, zerolinewidth=2),
                      yaxis=dict(title="sepal width (cm)", range=[-2, 5], zeroline=True, zerolinewidth=2, scaleanchor="x"),
                      margin=dict(l=80, r=30, t=80, b=70))
    return fig


if __name__ == "__main__":
    ts = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
    save_gif([frame(t) for t in ts], "mean_centring", here, keys=[0, 5], fps=2, holds=[4, 1, 1, 1, 1, 8])
