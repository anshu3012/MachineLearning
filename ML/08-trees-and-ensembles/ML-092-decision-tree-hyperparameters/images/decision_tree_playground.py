"""Serverless twin of ../app.py: precompute decision-tree surfaces and write ONE Plotly HTML (no Dash).
The app has nine controls, far too many to precompute every combination, so this page sweeps ONE hyperparameter
at a time from the app's defaults: the dropdown picks the hyperparameter, the slider moves it, everything else
stays at its default. Picking a hyperparameter jumps to a frame whose layout swaps in that hyperparameter's slider.

Run: python decision_tree_playground.py -> decision_tree_playground.html
"""
import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from sitecustomize import plotlyjs_src

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import COLOURS, REGION, fit, grid, load  # noqa: E402

# ponytail: the Dash sliders allow every integer (min_samples_split 2..375, min_samples_leaf 1..200, ...); we keep
# every value where the surface changes fast (small values) and coarsen the long flat tails. 150x150 grid (app: 300).
TAIL = [25, 30, 40, 50, 60, 80, 100, 150, 200]
SWEEPS = {                                          # hyperparameter: (slider labels, values); first value = default
    "data": (["moons", "social network ads"], ["moons", "ads"]),
    "criterion": (["gini", "entropy"], ["gini", "entropy"]),
    "splitter": (["best", "random"], ["best", "random"]),
    "max_features": (["all columns", "1", "2"], [None, 1, 2]),
    "max_depth": (["None (grow fully)"] + [str(v) for v in range(1, 21)], [None, *range(1, 21)]),
    "min_samples_split": ([str(v) for v in [*range(2, 21), *TAIL, 250, 301, 375]], [*range(2, 21), *TAIL, 250, 301, 375]),
    "min_samples_leaf": ([str(v) for v in [*range(1, 21), *TAIL]], [*range(1, 21), *TAIL]),
    "max_leaf_nodes": (["None (no limit)"] + [str(v) for v in [*range(2, 21), 25, 30, 35, 40, 45, 50]],
                       [None, *range(2, 21), 25, 30, 35, 40, 45, 50]),
    "min_impurity_decrease": ([f"{v:g}" for v in np.r_[np.arange(0, 0.051, 0.005), 0.06, 0.07, 0.08, 0.09, 0.1, 0.125, 0.15, 0.175, 0.2]],
                              list(np.r_[np.arange(0, 0.051, 0.005), 0.06, 0.07, 0.08, 0.09, 0.1, 0.125, 0.15, 0.175, 0.2])),
}
DEFAULTS = {name: values[0] for name, (_, values) in SWEEPS.items()}
N = 150
ANIM = dict(mode="immediate", frame=dict(duration=0, redraw=True), transition=dict(duration=0))
SUBTITLE = "one hyperparameter at a time: pick it in the dropdown, move the slider; the rest stay at the app's defaults"
POINTS = {name: (load(name)[0], load(name)[2]) for name in ("moons", "ads")}      # X_train, y_train


def surface(param, i):
    """Heatmap and layout for the default setting with one hyperparameter changed."""
    params = dict(DEFAULTS, **{param: SWEEPS[param][1][i]})
    name = params.pop("data")
    tree, X_train, X_test, y_train, y_test, axes, _ = fit(name, **params)
    xs, ys = grid(X_train, N)
    XX, YY = np.meshgrid(xs, ys)
    Z = tree.predict(np.c_[XX.ravel(), YY.ravel()]).reshape(N, N).astype(np.int8)
    heat = go.Heatmap(z=Z, x0=xs[0], dx=xs[1] - xs[0], y0=ys[0], dy=ys[1] - ys[0])
    points = [go.Scatter(visible=(name == "moons"))] * 2 + [go.Scatter(visible=(name == "ads"))] * 2
    layout = dict(
        title=dict(text=f"depth {tree.get_depth()}, {tree.get_n_leaves()} leaves   |   train accuracy "
                        f"{tree.score(X_train, y_train):.3f}, test accuracy {tree.score(X_test, y_test):.3f}",
                   subtitle=dict(text=SUBTITLE)),
        xaxis=dict(title=axes[0], range=[xs[0], xs[-1]]), yaxis=dict(title=axes[1], range=[ys[0], ys[-1]]))
    return [heat] + points, layout


def slider(param):
    labels = SWEEPS[param][0]
    return dict(active=0, pad=dict(t=50), currentvalue=dict(prefix=f"{param} = "),
                steps=[dict(label=lab, method="animate", args=[[f"{param}={i}"], ANIM]) for i, lab in enumerate(labels)])


frames = []
for param in SWEEPS:
    for i in range(len(SWEEPS[param][1])):
        data, layout = surface(param, i)
        frames.append(go.Frame(name=f"{param}={i}", data=data, traces=[0, 1, 2, 3, 4], layout=layout))
        if i == 0:                                  # the frame the dropdown jumps to: default surface + this slider
            frames.append(go.Frame(name=f"pick:{param}", data=data, traces=[0, 1, 2, 3, 4],
                                   layout=dict(layout, sliders=[slider(param)])))

data0, layout0 = surface("data", 0)
points = [go.Scatter(x=X[y == c, 0], y=X[y == c, 1], mode="markers", name=f"class {c} (training)",
                     visible=(name == "moons"), legendgroup=str(c),
                     marker=dict(color=COLOURS[c], size=6, line=dict(color="white", width=0.5)))
          for name, (X, y) in POINTS.items() for c in (0, 1)]
fig = go.Figure(data=[go.Heatmap(data0[0], zmin=0, zmax=1, colorscale=REGION, showscale=False, hoverinfo="skip")]
                + points, frames=frames)
fig.update_layout(
    layout0, template="simple_white", height=680, margin=dict(l=60, r=20, t=120, b=140),
    legend=dict(orientation="h", x=1, xanchor="right", y=1.02, yanchor="bottom"),
    updatemenus=[dict(type="dropdown", x=0, y=1.28, xanchor="left", yanchor="top", active=0, pad=dict(t=0),
                      buttons=[dict(label=f"sweep: {p}", method="animate", args=[[f"pick:{p}"], ANIM]) for p in SWEEPS])],
    sliders=[slider("data")])
fig.layout.title.update(y=0.9, yanchor="middle", font=dict(size=15))
out = HERE / "decision_tree_playground.html"
fig.write_html(out, include_plotlyjs=plotlyjs_src(out), full_html=True, auto_play=False,
               config={"responsive": True, "displaylogo": False})
print(f"{len(frames)} frames, {N}x{N} grid, {out.stat().st_size / 1e6:.1f} MB")
