"""What the GDRegressor class does when it runs (Plotly frames -> GIF). The Notebook's 100 points, 80 for training
(random_state 2); start m = 100, b = -120; learning rate 0.001; 50 epochs. Left: the line after each epoch closing
in on the OLS line (dashed). Right: the loss per epoch. Final m = 28.159, b = -2.300 against OLS 28.126, -2.271."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from common import X100, y100
from gifkit import BLUE, FONT, GREY, ORANGE, make_gif

here = Path(__file__).parent
X_train, X_test, y_train, y_test = train_test_split(X100, y100, test_size=0.2, random_state=2)
x, y = X_train.ravel(), y_train
ols = LinearRegression().fit(X_train, y_train)
m, b, hist = 100.0, -120.0, []
for _ in range(50):
    hist.append((m, b, float(np.sum((y - m * x - b) ** 2))))
    sb, sm = -2 * np.sum(y - m * x - b), -2 * np.sum((y - m * x - b) * x)
    b, m = b - 0.001 * sb, m - 0.001 * sm
hist.append((m, b, float(np.sum((y - m * x - b) ** 2))))
assert (round(m, 3), round(b, 3)) == (28.159, -2.300) and (round(ols.coef_[0], 3), round(ols.intercept_, 3)) == (28.126, -2.271)
xs = np.array([x.min() - 0.3, x.max() + 0.3])
assert round(hist[0][2] / 1e6, 1) == 1.5 and round(hist[-1][2], -3) == 24000
loss = np.array([h[2] for h in hist])


def frame(e):
    me, be, _ = hist[e]
    fig = make_subplots(1, 2, horizontal_spacing=0.1,
                        subplot_titles=[f"epoch {e}: m = {me:.2f}, b = {be:.2f}", "loss (sum of squared errors)"])
    fig.update_annotations(font_size=22)
    fig.add_trace(go.Scatter(x=x, y=y, mode="markers", marker=dict(size=7, color=GREY, opacity=0.6), name="80 training points"), 1, 1)
    fig.add_trace(go.Scatter(x=xs, y=ols.coef_[0] * xs + ols.intercept_, mode="lines", name="OLS (LinearRegression)",
                             line=dict(color="black", width=2, dash="dash")), 1, 1)
    fig.add_trace(go.Scatter(x=xs, y=me * xs + be, mode="lines", name="GDRegressor", line=dict(color=ORANGE, width=5)), 1, 1)
    fig.add_trace(go.Scatter(x=list(range(e + 1)), y=loss[:e + 1], mode="lines+markers", line=dict(color=BLUE, width=3),
                             marker=dict(size=6), showlegend=False), 1, 2)
    fig.update_xaxes(title="x", row=1, col=1)
    fig.update_yaxes(title="y", range=[y.min() - 120, y.max() + 120], row=1, col=1)
    fig.update_xaxes(title="epoch", range=[-1, 51], row=1, col=2)
    fig.update_yaxes(type="log", range=[np.log10(loss.min()) - 0.2, np.log10(loss.max()) + 0.2], row=1, col=2)
    fig.update_layout(template="simple_white", width=1200, height=560, font=FONT,
                      legend=dict(orientation="h", x=0.25, xanchor="center", y=-0.2), margin=dict(l=70, r=30, t=60, b=130))
    return fig


if __name__ == "__main__":
    es = [0, 1, 2, 3, 4, 5, 7, 10, 15, 20, 30, 40, 50]
    make_gif([frame(e) for e in es], here / "class_fit", fps=2, holds=[3] + [1] * (len(es) - 2) + [6],
             keys=[len(es) - 1], cols=1)
