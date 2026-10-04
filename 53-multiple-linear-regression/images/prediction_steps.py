"""Building one prediction from the equation y-hat = b0 + b1 x1 + b2 x2, with the fitted values b0 = -1.9,
b1 = 58.6, b2 = 29.1 and the point x1 = 1, x2 = 0.5 (Plotly waterfall frames -> GIF). Start at the intercept, add
58.6 x 1, add 29.1 x 0.5: the prediction is 71.3."""
from pathlib import Path
import plotly.graph_objects as go
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from gifkit import BLUE, FONT, GREEN, ORANGE, RED, make_gif

here = Path(__file__).parent
X, y = make_regression(n_samples=100, n_features=2, n_informative=2, noise=50, random_state=7)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=3)
lr = LinearRegression().fit(X_train, y_train)
b0, (b1, b2) = lr.intercept_, lr.coef_
x1, x2 = 1.0, 0.5
total = b0 + b1 * x1 + b2 * x2
assert (round(b0, 1), round(b1, 1), round(b2, 1), round(total, 1)) == (-1.9, 58.6, 29.1, 71.3)
labels = ["start: intercept β₀", "+ β₁ × x₁", "+ β₂ × x₂", "prediction ŷ"]
vals = [b0, b1 * x1, b2 * x2, total]
texts = [f"{b0:.1f}", f"+{b1:.1f} × 1 = +{b1 * x1:.1f}", f"+{b2:.1f} × 0.5 = +{b2 * x2:.1f}", f"{total:.1f}"]


def frame(k):
    measure = ["absolute", "relative", "relative", "total"][:k]
    fig = go.Figure(go.Waterfall(x=labels[:k], y=vals[:k], measure=measure, text=texts[:k], textposition="outside",
                                 textfont=dict(size=24), connector=dict(line=dict(color="#999", dash="dot")),
                                 increasing=dict(marker=dict(color=ORANGE)), decreasing=dict(marker=dict(color=RED)),
                                 totals=dict(marker=dict(color=GREEN))))
    fig.update_layout(template="simple_white", width=1000, height=560, font=FONT, showlegend=False,
                      title=dict(text="ŷ = β₀ + β₁x₁ + β₂x₂   at   x₁ = 1, x₂ = 0.5", x=0.5),
                      xaxis=dict(categoryorder="array", categoryarray=labels, range=[-0.5, 3.5]),
                      yaxis=dict(title="value", range=[-10, 85]), margin=dict(l=80, r=30, t=80, b=60))
    return fig


if __name__ == "__main__":
    make_gif([frame(k) for k in (1, 2, 3, 4)], here / "prediction_steps", fps=1, holds=[2, 2, 2, 5], keys=[3], cols=1)
