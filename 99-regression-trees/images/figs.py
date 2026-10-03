"""Plotly figures for the regression trees Note."""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

HERE = Path(__file__).parent
DATA = HERE.parent / "data"
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=18, color="black")


def save(fig, name, w, h):
    fig.update_layout(template="simple_white", font=FONT, width=w, height=h)
    fig.write_image(HERE / f"{name}.png", scale=2)
    fig.write_image(HERE / f"{name}.pdf")


def points(x, y, name="students", show=True):
    return go.Scatter(x=x, y=y, mode="markers", name=name, showlegend=show,
                      marker=dict(symbol="x", size=10, color=BLUE, line=dict(width=1)))


sem = pd.read_csv(DATA / "semester.csv")
day = pd.read_csv(DATA / "exam_day.csv")

# 1. A straight line fits semester hours, not hours on the day before the exam
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1,
                    subplot_titles=["hours studied in the semester", "hours studied the day before the exam"])
for col, df, q in [(1, sem, 75), (2, day, 5)]:
    lr = LinearRegression().fit(df[["hours"]], df["marks"])
    xs = np.linspace(df.hours.min(), df.hours.max(), 2)
    fig.add_trace(points(df.hours, df.marks, show=col == 1), 1, col)
    fig.add_trace(go.Scatter(x=xs, y=lr.predict(pd.DataFrame({"hours": xs})), mode="lines", name="best-fit line",
                             line=dict(color=RED, width=3), showlegend=col == 1), 1, col)
    pred = float(lr.predict(pd.DataFrame({"hours": [q]}))[0])
    fig.add_trace(go.Scatter(x=[q], y=[pred], mode="markers+text", text=[f"{q} h → {pred:.0f} marks"],
                             textposition="top center" if col == 2 else "bottom right",
                             marker=dict(color="black", size=12, symbol="diamond"),
                             showlegend=False), 1, col)
    print("line predicts", q, "hours ->", round(pred, 1), "R2", round(lr.score(df[["hours"]], df["marks"]), 3))
fig.update_xaxes(title="hours")
fig.update_annotations(font_size=20)
fig.update_yaxes(title="marks", col=1)
fig.update_yaxes(range=[0, 105])
fig.update_layout(legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2), margin=dict(l=70, r=20, t=50, b=110))
save(fig, "linear_vs_nonlinear", 1200, 520)

# 2. The three-leaf tree as a step function
tree = DecisionTreeRegressor(max_leaf_nodes=3, random_state=0).fit(day[["hours"]], day["marks"])
xs = np.linspace(0, 10, 1001)
fig = go.Figure([points(day.hours, day.marks),
                 go.Scatter(x=xs, y=tree.predict(pd.DataFrame({"hours": xs})), mode="lines", name="regression tree",
                            line=dict(color=GREEN, width=4, shape="hv"))])
for t in sorted(tree.tree_.threshold[tree.tree_.threshold > 0]):
    fig.add_vline(x=t, line=dict(color=GREY, dash="dash", width=2))
    fig.add_annotation(x=t, y=103, text=f"cut at {t:.2f}", showarrow=False, xanchor="left", xshift=4)
pred = float(tree.predict(pd.DataFrame({"hours": [5]}))[0])
fig.add_trace(go.Scatter(x=[5], y=[pred], mode="markers", marker=dict(color="black", size=13, symbol="diamond"),
                         showlegend=False))
fig.add_annotation(x=5, y=pred, ax=-40, ay=250, text=f"new student: 5 h → {pred:.1f} marks", arrowwidth=2,
                   bgcolor="white", font=dict(size=18))
fig.update_xaxes(title="hours studied the day before the exam", range=[0, 10])
fig.update_yaxes(title="marks", range=[0, 108])
fig.update_layout(legend=dict(x=0.99, xanchor="right", y=0.25), margin=dict(l=70, r=20, t=20, b=60))
save(fig, "tree_fit", 1000, 480)
print("tree thresholds", tree.tree_.threshold[tree.tree_.threshold > 0].round(2), "5 h ->", round(pred, 1))

# 3. Two inputs: the tree cuts the hours-CGPA plane into boxes, one mean each
two = pd.read_csv(DATA / "exam_cgpa.csv")
t2 = DecisionTreeRegressor(max_depth=3, min_samples_leaf=4, random_state=0).fit(two[["hours", "cgpa"]], two["marks"])
hx, cy = np.linspace(0.3, 9.7, 300), np.linspace(4.9, 10.1, 300)
HH, CC = np.meshgrid(hx, cy)
Z = t2.predict(pd.DataFrame({"hours": HH.ravel(), "cgpa": CC.ravel()})).reshape(HH.shape)
fig = go.Figure([go.Heatmap(x=hx, y=cy, z=Z, colorscale="Blues", zmin=30, zmax=100, opacity=0.75,
                            colorbar=dict(title="predicted<br>marks")),
                 go.Scatter(x=two.hours, y=two.cgpa, mode="markers", showlegend=False,
                            marker=dict(color="black", size=7, symbol="x"))])
fig.update_xaxes(title="hours studied the day before the exam")
fig.update_yaxes(title="CGPA")
fig.update_layout(margin=dict(l=70, r=20, t=20, b=60))
save(fig, "two_inputs", 1000, 560)
print("two inputs: root on", ["hours", "cgpa"][t2.tree_.feature[0]], "at", round(t2.tree_.threshold[0], 2))

# 4. max_depth on a noisy nonlinear curve (200 rows, 150 for training)
rng = np.random.default_rng(42)
x = rng.uniform(-3, 3, 200)
y = np.sin(1.5 * x) * 3 + 0.5 * x + rng.normal(0, 0.6, 200)
X_tr, X_te, y_tr, y_te = train_test_split(x[:, None], y, random_state=42)
grid = np.linspace(-3, 3, 1200)[:, None]
depths = [1, 2, 5, 15]
fits = [DecisionTreeRegressor(max_depth=d, random_state=42).fit(X_tr, y_tr) for d in depths]
titles = [f"max_depth = {d}: {m.get_n_leaves()} leaves, test R² = {r2_score(y_te, m.predict(X_te)):.2f}"
          for d, m in zip(depths, fits)]
fig = make_subplots(rows=2, cols=2, subplot_titles=titles, horizontal_spacing=0.08, vertical_spacing=0.14)
for i, m in enumerate(fits):
    r, c = i // 2 + 1, i % 2 + 1
    fig.add_trace(go.Scatter(x=X_tr[:, 0], y=y_tr, mode="markers", name="training rows", showlegend=i == 0,
                             marker=dict(color=BLUE, size=6, opacity=0.7)), r, c)
    fig.add_trace(go.Scatter(x=grid[:, 0], y=m.predict(grid), mode="lines", name="tree prediction", showlegend=i == 0,
                             line=dict(color=ORANGE, width=3)), r, c)
    print(titles[i])
fig.update_xaxes(title="x", row=2)
fig.update_yaxes(title="y", col=1)
fig.update_annotations(font_size=18)
fig.update_layout(legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.1), margin=dict(l=70, r=20, t=50, b=90))
save(fig, "depth_fits", 1100, 820)
print("depth 1 threshold", round(fits[0].tree_.threshold[0], 2))

# 5. Feature importance of a tuned tree on the Boston housing data (same settings as the Notebook)
boston = pd.read_csv(DATA / "boston.csv")
X, y = boston.drop(columns="MEDV"), boston["MEDV"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
best = DecisionTreeRegressor(criterion="absolute_error", max_depth=6, random_state=42).fit(X_train, y_train)
imp = pd.Series(best.feature_importances_, X.columns).sort_values()
fig = go.Figure(go.Bar(x=imp.values, y=imp.index, orientation="h", marker_color=BLUE,
                       text=[f"{v:.3f}" for v in imp.values], textposition="outside"))
fig.update_xaxes(title="feature importance (sums to 1)", range=[0, 0.55])
fig.update_layout(margin=dict(l=100, r=20, t=20, b=60))
save(fig, "feature_importance", 900, 560)
print(imp.sort_values(ascending=False).round(3).to_dict())
