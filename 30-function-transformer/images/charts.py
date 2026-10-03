"""Plotly charts for Note 30: Q-Q plots (scipy.stats.probplot data drawn in Plotly) and before/after distributions."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import FunctionTransformer

here = Path(__file__).parent
BLUE, GREEN, RED, GREY = "#4C78A8", "#54A24B", "#E45756", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=20)


def qq(fig, x, row, col, colour=BLUE):
    """Q-Q plot: probplot gives (normal quantiles, sorted data) and the best straight line through them."""
    (osm, osr), (slope, intercept, _) = stats.probplot(x, dist="norm")
    fig.add_trace(go.Scatter(x=osm, y=osr, mode="markers", marker=dict(color=colour, size=5, opacity=0.6)), row, col)
    fig.add_trace(go.Scatter(x=osm[[0, -1]], y=slope * osm[[0, -1]] + intercept, mode="lines",
                             line=dict(color=RED, width=2.5)), row, col)
    fig.update_xaxes(title="normal quantiles", row=row, col=col)
    fig.update_yaxes(title="data quantiles" if col == 1 else None, row=row, col=col)


def hist(fig, x, row, col, colour=BLUE, xtitle="value"):
    """Histogram scaled to density, with a KDE curve on top."""
    fig.add_trace(go.Histogram(x=x, histnorm="probability density", nbinsx=40, marker_color=colour, opacity=0.45), row, col)
    grid = np.linspace(x.min(), x.max(), 300)
    fig.add_trace(go.Scatter(x=grid, y=stats.gaussian_kde(x)(grid), mode="lines", line=dict(color=colour, width=3)), row, col)
    fig.update_xaxes(title=xtitle, row=row, col=col)
    fig.update_yaxes(title="density" if col == 1 else None, row=row, col=col)


def save(fig, name, width, height):
    fig.update_layout(template="simple_white", width=width, height=height, showlegend=False, font=FONT,
                      bargap=0.02, margin=dict(l=70, r=20, t=70, b=60))
    fig.update_annotations(font_size=21)
    fig.write_image(here / f"{name}.png", scale=2)
    fig.write_image(here / f"{name}.pdf")


# 1. how to read a Q-Q plot: four made-up shapes, histogram on top, Q-Q plot below
rng = np.random.default_rng(0)
shapes = {"Normal": rng.normal(0, 1, 500),
          "Right skew": rng.lognormal(0, 0.7, 500),
          "Left skew": 10 - rng.lognormal(0, 0.7, 500),
          "Fat tails": rng.standard_t(3, 500)}
fig = make_subplots(2, 4, subplot_titles=list(shapes), vertical_spacing=0.2, horizontal_spacing=0.07)
for i, x in enumerate(shapes.values(), start=1):
    hist(fig, x, 1, i)
    qq(fig, x, 2, i)
fig.update_xaxes(showticklabels=False)
fig.update_yaxes(showticklabels=False)
save(fig, "qq_shapes", 1300, 640)

# 2. building a Q-Q plot by hand: five values against the normal quantiles of 5 equal slices
vals = np.array([1, 2, 3, 4, 10])
z = stats.norm.ppf((np.arange(1, 6) - 0.5) / 5)
slope, intercept = np.polyfit(z, vals, 1)
fig = go.Figure()
fig.add_trace(go.Scatter(x=z[[0, -1]], y=slope * z[[0, -1]] + intercept, mode="lines", line=dict(color=RED, width=2.5)))
fig.add_trace(go.Scatter(x=z, y=vals, mode="markers+text", marker=dict(color=BLUE, size=14),
                         text=[f"({a:.2f}, {b})" for a, b in zip(z, vals)], textposition="middle right",
                         textfont=dict(size=19)))
fig.update_xaxes(title="normal quantile z", range=[-1.7, 2.1])
fig.update_yaxes(title="sorted value", range=[-1, 11.5])
save(fig, "qq_build", 760, 460)

# Titanic training set, exactly as in the Notebook
df = pd.read_csv(here.parent / "data" / "titanic_train.csv", usecols=["Age", "Fare", "Survived"])
df["Age"] = df["Age"].fillna(df["Age"].mean())
X, y = df[["Age", "Fare"]], df["Survived"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. one figure per column: distribution and Q-Q plot, before and after log(1 + x)
for col in ["Fare", "Age"]:
    before, after = X_train[col], np.log1p(X_train[col])
    fig = make_subplots(2, 2, vertical_spacing=0.2, horizontal_spacing=0.1, subplot_titles=[
        f"{col} before: skewness {before.skew():.2f}", f"{col} after log(1 + x): skewness {after.skew():.2f}",
        f"{col} before: Q-Q plot", f"{col} after log(1 + x): Q-Q plot"])
    hist(fig, before.values, 1, 1, BLUE, col)
    hist(fig, after.values, 1, 2, GREEN, f"log(1 + {col})")
    qq(fig, before.values, 2, 1, BLUE)
    qq(fig, after.values, 2, 2, GREEN)
    save(fig, f"{col.lower()}_log", 1100, 760)

# 4. every transform on Fare only (whole data, 10-fold cross-validation of logistic regression)
transforms = {"No transform": lambda x: x, "Log: log(1 + x)": np.log1p,
              "Reciprocal: 1 / (x + 0.1)": lambda x: 1 / (x + 0.1), "Square: x²": np.square,
              "Square root: √x": np.sqrt, "Sine: sin(x)": np.sin}
titles, columns = [], []
for name, f in transforms.items():
    ct = ColumnTransformer([("t", FunctionTransformer(f), ["Fare"])], remainder="passthrough")
    Xt = ct.fit_transform(X)
    acc = cross_val_score(LogisticRegression(max_iter=1000), Xt, y, scoring="accuracy", cv=10).mean()
    titles.append(f"{name}<br>skew {pd.Series(Xt[:, 0]).skew():.2f}, accuracy {acc:.1%}")
    columns.append(Xt[:, 0])
fig = make_subplots(2, 3, subplot_titles=titles, vertical_spacing=0.24, horizontal_spacing=0.08)
for i, x in enumerate(columns):
    qq(fig, x, i // 3 + 1, i % 3 + 1, BLUE if i == 0 else GREEN)
fig.update_xaxes(showticklabels=False)
save(fig, "transforms_compare", 1200, 800)
