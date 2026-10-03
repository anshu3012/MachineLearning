"""Plotly versions of the dtreeviz visuals, built from the fitted trees' own arrays (no matplotlib):
iris_viz        - the depth-2 iris tree with the training data at every node (histograms) and leaf pies
boston_split    - a regression split drawn as a scatter plot with the two leaf means
importance      - feature importance of the fully grown iris tree
cars_univar     - a regression tree on one input drawn over the data (all cuts on one axis)
cars_bivar      - a regression tree on two inputs drawn as a 3D step surface"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

HERE = Path(__file__).parent
DATA = HERE.parent / "data"
COLS = ["#4C78A8", "#F58518", "#54A24B"]                  # setosa, versicolor, virginica
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=17, color="black")


def save(fig, name, w, h):
    fig.update_layout(template="simple_white", font=FONT, width=w, height=h)
    fig.write_image(HERE / f"{name}.png", scale=2)
    fig.write_image(HERE / f"{name}.pdf")


iris = load_iris()
X, y = iris.data, iris.target
names = list(iris.target_names)

# 1. The depth-2 iris tree, drawn the dtreeviz way: hand-placed panels, one per node
tree = DecisionTreeClassifier(max_depth=2, random_state=0).fit(X, y)
t = tree.tree_
rows_at = tree.decision_path(X).toarray().astype(bool)   # rows_at[i, n]: does flower i pass through node n?
# Position of each node on the page (paper coordinates): x range, y range
box = {0: ([0.30, 0.72], [0.74, 0.97]), 1: ([0.06, 0.24], [0.40, 0.58]), 2: ([0.52, 0.96], [0.40, 0.62]),
       3: ([0.47, 0.63], [0.05, 0.21]), 4: ([0.80, 0.96], [0.05, 0.21])}
fig = go.Figure()
axis = 0
for n, (bx, by) in box.items():
    mask = rows_at[:, n]
    if t.children_left[n] != -1:                            # decision node: histogram of its split column, by class
        axis += 1
        xa, ya = ("x", "y") if axis == 1 else (f"x{axis}", f"y{axis}")
        f, thr = t.feature[n], t.threshold[n]
        lo = 0 if n == 0 else 0.9
        for k in range(3):
            fig.add_trace(go.Histogram(x=X[mask & (y == k), f], xbins=dict(start=0, end=2.6, size=0.1), name=names[k],
                                       marker_color=COLS[k], showlegend=n == 0, xaxis=xa, yaxis=ya))
        fig.add_trace(go.Scatter(x=[thr], y=[0], mode="markers+text", marker=dict(symbol="triangle-up", size=18, color="black"),
                                 text=[f"{thr:.2f}"], textposition="bottom center", showlegend=False, cliponaxis=False,
                                 xaxis=xa, yaxis=ya))
        suffix = "" if axis == 1 else str(axis)
        fig.layout[f"xaxis{suffix}"] = dict(domain=bx, anchor=ya, range=[lo, 2.6],
                                            title=dict(text=iris.feature_names[f].replace(" (cm)", ""), standoff=4))
        fig.layout[f"yaxis{suffix}"] = dict(domain=by, anchor=xa, title="flowers")
    else:                                                   # leaf: pie of the classes that reached it
        counts = [int(np.sum(mask & (y == k))) for k in range(3)]
        fig.add_trace(go.Pie(values=counts, labels=names, marker=dict(colors=COLS), sort=False, textinfo="none",
                             showlegend=False, domain=dict(x=bx, y=by)))
        top = int(np.argmax(counts))
        fig.add_annotation(text=f"{names[top]}, n = {sum(counts)}<br>({counts[0]}/{counts[1]}/{counts[2]})", showarrow=False,
                           x=sum(bx) / 2, y=by[0] - 0.01, xref="paper", yref="paper", xanchor="center", yanchor="top", font=dict(size=17))
fig.update_layout(barmode="stack", legend=dict(orientation="h", x=0.02, y=1.0, traceorder="normal"),
                  margin=dict(l=60, r=20, t=20, b=60))
# Lines from each decision node down to its children, labelled like dtreeviz (< and >=)
lines = [((0.44, 0.66), (0.15, 0.60), "< 0.80"), ((0.60, 0.66), (0.74, 0.64), "≥ 0.80"),
         ((0.68, 0.32), (0.55, 0.23), "< 1.75"), ((0.82, 0.32), (0.88, 0.23), "≥ 1.75")]
for (x0, y0), (x1, y1), label in lines:
    fig.add_shape(type="line", x0=x0, y0=y0, x1=x1, y1=y1, xref="paper", yref="paper", line=dict(color=GREY, width=2))
    fig.add_annotation(x=(x0 + x1) / 2, y=(y0 + y1) / 2, xref="paper", yref="paper", text=label, showarrow=False,
                       bgcolor="white", font=dict(size=16))
save(fig, "iris_viz", 1100, 950)
print("iris depth 2:", [(int(t.feature[n]), round(float(t.threshold[n]), 2), int(t.n_node_samples[n])) for n in range(t.node_count)])

# 2. A regression split drawn as a scatter plot: Boston, depth 1, all 506 districts
boston = pd.read_csv(DATA / "boston.csv")
Xb, yb = boston.drop(columns="MEDV"), boston["MEDV"]
reg = DecisionTreeRegressor(max_depth=1, random_state=0).fit(Xb, yb)
r = reg.tree_
col, thr = Xb.columns[r.feature[0]], r.threshold[0]
fig = go.Figure(go.Scatter(x=boston[col], y=yb, mode="markers", marker=dict(color=BLUE, size=6, opacity=0.6), showlegend=False))
fig.add_vline(x=thr, line=dict(color="black", dash="dash", width=2))
for child, x0, x1 in [(1, boston[col].min(), thr), (2, thr, boston[col].max())]:
    mean, n = float(r.value[child].ravel()[0]), int(r.n_node_samples[child])
    fig.add_trace(go.Scatter(x=[x0, x1], y=[mean, mean], mode="lines", line=dict(color=RED, width=4), showlegend=False))
    fig.add_annotation(x=(x0 + x1) / 2, y=mean, text=f"mean {mean:.2f}, n = {n}", showarrow=False, yshift=16,
                       bgcolor="white", font=dict(size=17))
fig.add_annotation(x=thr, y=52, text=f"{col} ≤ {thr:.2f}", showarrow=False, xanchor="left", xshift=6)
fig.update_xaxes(title=f"{col}: average rooms per home")
fig.update_yaxes(title="MEDV: median value (thousand dollars)")
fig.update_layout(margin=dict(l=70, r=20, t=20, b=60))
save(fig, "boston_split", 1000, 500)
print("boston depth 1:", col, round(thr, 2), r.value[1:].ravel().round(2), r.n_node_samples)

# 3. Feature importance of the fully grown iris tree
full = DecisionTreeClassifier(random_state=0).fit(X, y)
imp = pd.Series(full.feature_importances_, [s.replace(" (cm)", "") for s in iris.feature_names]).sort_values()
fig = go.Figure(go.Bar(x=imp.values, y=imp.index, orientation="h", marker_color=BLUE,
                       text=[f"{v:.3f}" for v in imp.values], textposition="outside"))
fig.update_xaxes(title="feature importance", range=[0, 1.1])
fig.update_layout(margin=dict(l=120, r=20, t=20, b=60))
save(fig, "importance", 900, 380)
print("iris importance", imp.round(3).to_dict())

# 4. One input: every cut lies on the same axis
cars = pd.read_csv(DATA / "cars.csv")
uni = DecisionTreeRegressor(max_depth=3, random_state=0).fit(cars[["WGT"]], cars["MPG"])
grid = pd.DataFrame({"WGT": np.linspace(cars.WGT.min(), cars.WGT.max(), 2000)})
fig = go.Figure([go.Scatter(x=cars.WGT, y=cars.MPG, mode="markers", name="cars", marker=dict(color=BLUE, size=6, opacity=0.6)),
                 go.Scatter(x=grid.WGT, y=uni.predict(grid), mode="lines", name="tree prediction (leaf means)",
                            line=dict(color=RED, width=4))])
for thr_ in sorted(uni.tree_.threshold[uni.tree_.children_left != -1]):
    fig.add_vline(x=thr_, line=dict(color=GREY, dash="dot", width=1.5))
fig.update_xaxes(title="WGT: weight (pounds)")
fig.update_yaxes(title="MPG: miles per gallon")
fig.update_layout(legend=dict(x=0.99, xanchor="right", y=0.98), margin=dict(l=70, r=20, t=20, b=60))
save(fig, "cars_univar", 1000, 480)
print("cars univar cuts", sorted(uni.tree_.threshold[uni.tree_.children_left != -1].round(1)))

# 5. Two inputs: the tree's prediction is a surface made of flat steps
bi = DecisionTreeRegressor(max_depth=3, random_state=0).fit(cars[["WGT", "ENG"]], cars["MPG"])
wg = np.linspace(cars.WGT.min(), cars.WGT.max(), 120)
eg = np.linspace(cars.ENG.min(), cars.ENG.max(), 120)
WW, EE = np.meshgrid(wg, eg)
Z = bi.predict(pd.DataFrame({"WGT": WW.ravel(), "ENG": EE.ravel()})).reshape(WW.shape)
fig = go.Figure([go.Surface(x=wg, y=eg, z=Z, colorscale="Blues", opacity=0.85, showscale=False),
                 go.Scatter3d(x=cars.WGT, y=cars.ENG, z=cars.MPG, mode="markers",
                              marker=dict(size=2.5, color="black"), showlegend=False)])
ax3 = dict(tickfont=dict(size=12), title_font=dict(size=17))
fig.update_layout(scene=dict(xaxis=dict(title="WGT (pounds)", **ax3), yaxis=dict(title="ENG (cubic inches)", **ax3),
                             zaxis=dict(title="MPG", **ax3), aspectratio=dict(x=1.2, y=1.2, z=0.9),
                             camera=dict(eye=dict(x=1.5, y=-1.6, z=0.75), center=dict(x=0, y=0, z=-0.15))),
                  margin=dict(l=0, r=0, t=0, b=0))
save(fig, "cars_bivar", 900, 650)
print("cars bivar root:", ["WGT", "ENG"][bi.tree_.feature[0]], round(bi.tree_.threshold[0], 1))
