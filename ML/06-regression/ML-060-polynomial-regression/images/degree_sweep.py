"""Degree by degree (Plotly frames -> GIF): polynomial fits of degree 1 to 15 on the 25 training points of
Section 4 (pipeline PolynomialFeatures, StandardScaler, LinearRegression, as in degrees.py), scored on 200 new test
points. Left: the curve; right: training and test R2 so far. Training R2 only rises; test R2 peaks at degree 2."""
import warnings
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from data61 import X_te, X_tr, y_te, y_tr
from gifkit import BLUE, FONT, GREY, ORANGE, make_gif

warnings.simplefilter("ignore")
here = Path(__file__).parent
model = lambda d: make_pipeline(PolynomialFeatures(d, include_bias=False), StandardScaler(), LinearRegression()).fit(X_tr, y_tr)
D = list(range(1, 16))
M = {d: model(d) for d in D}
tr = [M[d].score(X_tr, y_tr) for d in D]
te = [M[d].score(X_te, y_te) for d in D]
assert [round(tr[d - 1], 2) for d in (1, 2, 6, 10, 15)] == [0.48, 0.94, 0.97, 0.98, 0.99]
assert [round(te[d - 1], 2) for d in (1, 2, 6, 10, 15)] == [0.28, 0.86, 0.81, 0.28, -9.35]
# Exact least squares can never lower the training R2 as the degree grows; the one dip (degree 14 -> 15, 0.0002)
# is rounding error, quoted in the Note's Extra on conditioning.
drops = [round(a - b, 4) for a, b in zip(tr, tr[1:]) if b < a]
assert drops == [0.0002] and tr[14] < tr[13] and int(np.argmax(te)) + 1 == 2
xs = np.linspace(-3, 3, 400).reshape(-1, 1)


def frame(d):
    fig = make_subplots(1, 2, column_widths=[0.55, 0.45], horizontal_spacing=0.1,
                        subplot_titles=[f"degree {d}: train R² {tr[d - 1]:.2f}, test R² {te[d - 1]:.2f}", "R² against degree"])
    fig.update_annotations(font_size=21)
    fig.add_trace(go.Scatter(x=X_te.ravel(), y=y_te, mode="markers", marker=dict(size=5, color="#CCCCCC"), name="test points"), 1, 1)
    fig.add_trace(go.Scatter(x=X_tr.ravel(), y=y_tr, mode="markers", marker=dict(size=9, color=BLUE), name="training points"), 1, 1)
    fig.add_trace(go.Scatter(x=xs.ravel(), y=np.clip(M[d].predict(xs), -6, 16), mode="lines", line=dict(color=ORANGE, width=4),
                             name="fitted curve"), 1, 1)
    fig.add_trace(go.Scatter(x=D[:d], y=tr[:d], mode="lines+markers", line=dict(color=BLUE, width=3), name="training R²"), 1, 2)
    fig.add_trace(go.Scatter(x=D[:d], y=np.clip(te[:d], -1, 1), mode="lines+markers", line=dict(color=ORANGE, width=3),
                             name="test R² (clipped at −1)"), 1, 2)
    fig.update_xaxes(title="x", range=[-3.1, 3.1], row=1, col=1)
    fig.update_yaxes(title="y", range=[-5, 15], row=1, col=1)
    fig.update_xaxes(title="degree", range=[0.5, 15.5], row=1, col=2)
    fig.update_yaxes(title="R²", range=[-1.05, 1.05], row=1, col=2)
    fig.update_layout(template="simple_white", width=1250, height=560, font=FONT,
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2), margin=dict(l=70, r=30, t=60, b=120))
    return fig


if __name__ == "__main__":
    make_gif([frame(d) for d in D], here / "degree_sweep", fps=2, holds=[3, 4] + [1] * 12 + [6], keys=[1, 14], cols=1, width=950)
