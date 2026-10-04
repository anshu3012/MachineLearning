"""Why a soft margin, in one dimension (Plotly frames -> GIF). Iris petal lengths of setosa and versicolor, plus one
made-up outlier: a flower labelled setosa with a 2.9 cm petal, next to the versicolor flowers. A linear SVC is fitted
for C = 1000, 100, 30, 10 and 1. With a large C no mistake is allowed and the threshold is squeezed between the outlier
and versicolor (2.95 cm, margin 0.1). As C falls, the SVC gives up the outlier and the threshold moves back between the
two main groups (2.60 cm, margin 1.4)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import load_iris
from sklearn.svm import SVC
from gifkit import BLUE, FONT, GREY, ORANGE, RED, make_gif

here = Path(__file__).parent
iris = load_iris()
pl = iris.data[:, 2]
se, ve, OUT, NEW = pl[iris.target == 0], pl[iris.target == 1], 2.9, 2.8
X, y = np.r_[se, OUT, ve][:, None], np.r_[-np.ones(51), np.ones(50)]
rng = np.random.default_rng(0)
js, jv = rng.uniform(-0.25, 0.25, 50), rng.uniform(-0.25, 0.25, 50)               # vertical jitter, display only


def fit(C):
    m = SVC(kernel="linear", C=C).fit(X, y)
    w, b = m.coef_[0, 0], m.intercept_[0]
    return -b / w, 2 / abs(w), int((m.predict(X) != y).sum())


res = {C: fit(C) for C in (1000, 100, 30, 10, 1)}
assert [round(v, 2) for v in res[1000][:2]] == [2.95, 0.1] and res[1000][2] == 0
assert [round(v, 2) for v in res[1][:2]] == [2.6, 1.4] and res[1][2] == 1


def frame(C):
    t, d, err = res[C]
    fig = go.Figure()
    fig.add_vrect(x0=t - d / 2, x1=t + d / 2, fillcolor=GREY, opacity=0.15, line_width=0)
    fig.add_trace(go.Scatter(x=se, y=js, mode="markers", marker=dict(size=12, color=BLUE, opacity=0.7), name="setosa"))
    fig.add_trace(go.Scatter(x=ve, y=jv, mode="markers", marker=dict(size=12, color=ORANGE, opacity=0.7), name="versicolor"))
    fig.add_trace(go.Scatter(x=[OUT], y=[0], mode="markers", marker=dict(size=17, color=BLUE, symbol="diamond", line=dict(color="black", width=2)), name="outlier (labelled setosa)"))
    fig.add_trace(go.Scatter(x=[NEW], y=[-0.42], mode="markers+text", text=["new flower"], textposition="bottom right", textfont=dict(size=20),
                             marker=dict(size=18, symbol="star", color=BLUE if NEW < t else ORANGE, line=dict(color="black", width=2)), showlegend=False))
    fig.add_trace(go.Scatter(x=[t, t], y=[-0.62, 0.62], mode="lines", line=dict(color="black", width=4), showlegend=False))
    fig.update_yaxes(visible=False, range=[-0.75, 0.7])
    fig.update_xaxes(range=[0.8, 5.3], title="petal length (cm)")
    fig.update_layout(template="simple_white", width=1100, height=520, font=FONT, margin=dict(l=30, r=30, t=110, b=70),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=1.0, yanchor="bottom"),
                      title=dict(text=f"C = {C}: threshold {t:.2f} cm, margin {d:.1f} cm, training mistakes {err}", x=0.5, font=dict(size=25)))
    return fig


if __name__ == "__main__":
    Cs = [1000, 100, 30, 10, 1]
    make_gif([frame(C) for C in Cs], here / "outlier_1d", fps=1, holds=[4, 1, 2, 2, 5], keys=[0, 4], cols=1)
