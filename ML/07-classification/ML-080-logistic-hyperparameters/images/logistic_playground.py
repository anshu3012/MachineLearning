"""Serverless twin of ../app.py: precompute the logistic-regression decision regions for a grid of settings and write
ONE Plotly HTML whose dropdowns and sliders switch between the precomputed frames in the browser (no Dash).
Plotly controls are stateless, so a few lines of JS read every control's active index and pick the frame.

Run: python logistic_playground.py -> logistic_playground.html
"""
import itertools
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from sitecustomize import plotlyjs_src
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import COLOURS, REGION, make_data  # noqa: E402

warnings.simplefilter("ignore")
# ponytail: the Dash app allows 2 datasets x 4 penalties x 13 C x 6 solvers x 11 l1_ratio x 100 max_iter settings.
# We keep every dataset, penalty and solver; C at whole powers of ten, l1_ratio at 0.1 .. 0.9 in steps of 0.2 and
# max_iter at 10 / 100 / 1000, on a 90x90 grid (app: 250x250). Settings a model ignores share one frame.
DATASETS = ["binary", "three"]
PENALTIES = ["none", "l2", "l1", "elasticnet"]
SOLVERS = ["lbfgs", "newton-cg", "newton-cholesky", "liblinear", "sag", "saga"]
C_EXPS = list(range(-3, 4))
L1_RATIOS = [0.1, 0.3, 0.5, 0.7, 0.9]
MAX_ITERS = [10, 100, 1000]
DEFAULT = (0, 1, 0, 3, 2, 1)                        # binary, l2, lbfgs, C = 1, l1_ratio = 0.5, max_iter = 100
N = 90
ANIM = dict(mode="immediate", frame=dict(duration=0, redraw=True), transition=dict(duration=0))

DATA = {}
for name in DATASETS:
    X, y = make_data(name)
    xs = np.linspace(X[:, 0].min() - 1, X[:, 0].max() + 1, N)
    ys = np.linspace(X[:, 1].min() - 1, X[:, 1].max() + 1, N)
    XX, YY = np.meshgrid(xs, ys)
    DATA[name] = dict(X=X, y=y, split=train_test_split(X, y, test_size=0.3, random_state=0),
                      xs=xs, ys=ys, grid=np.c_[XX.ravel(), YY.ravel()])


def fit(di, pi, si, ci, li, mi):
    """Decision regions and title for one setting, exactly as app.figure_for builds the model."""
    D = DATA[DATASETS[di]]
    ratio = {"none": 0.0, "l2": 0.0, "l1": 1.0, "elasticnet": L1_RATIOS[li]}[PENALTIES[pi]]
    C = np.inf if pi == 0 else 10.0 ** C_EXPS[ci]
    a, b, c, d = D["split"]
    model = LogisticRegression(C=C, l1_ratio=ratio, solver=SOLVERS[si], max_iter=MAX_ITERS[mi]).fit(a, c)
    Z = model.predict(D["grid"]).reshape(N, N).astype(np.int8)
    coefs = ", ".join(f"{v:.2f}" for v in np.ravel(model.coef_))
    return Z, f"test accuracy {model.score(b, d):.3f} | C = {C:g} | coefficients: {coefs}"


BAD = set()                                         # (dataset, penalty, solver) triples sklearn refuses
for di, pi, si in itertools.product(range(2), range(4), range(6)):
    try:
        fit(di, pi, si, *DEFAULT[3:])
    except ValueError:
        BAD.add((di, pi, si))


def canon(di, pi, si, ci, li, mi):
    """The frame that shows this setting: controls the model ignores are pinned to their default."""
    if pi == 0 or (di, pi, si) in BAD:              # no penalty (C, l1_ratio do nothing) or a refused pair
        ci, li, mi = DEFAULT[3], DEFAULT[4], mi if pi == 0 else DEFAULT[5]
    elif pi != 3:                                   # l1_ratio is Elastic Net only
        li = DEFAULT[4]
    return (di, pi, si, ci, li, mi)


def frame(key):
    """One frame: heatmap (or hidden when the solver / penalty pair is not allowed), point visibility, title."""
    di = key[0]
    D = DATA[DATASETS[di]]
    points = [go.Scatter(visible=(di == 0))] * 2 + [go.Scatter(visible=(di == 1))] * 3
    try:
        Z, title = fit(*key)
        heat = go.Heatmap(z=Z, x0=D["xs"][0], dx=D["xs"][1] - D["xs"][0], y0=D["ys"][0], dy=D["ys"][1] - D["ys"][0],
                          visible=True)
    except ValueError as err:                       # some solver / penalty pairs are not allowed (as in the app)
        heat, title = go.Heatmap(visible=False), f"Not allowed: {err}"
    return go.Frame(name="|".join(map(str, key)), data=[heat] + points, traces=list(range(6)),
                    layout=dict(title=dict(text=title), xaxis=dict(range=[D["xs"][0], D["xs"][-1]]),
                                yaxis=dict(range=[D["ys"][0], D["ys"][-1]])))


frames, MAP = {}, {}
sizes = (len(DATASETS), len(PENALTIES), len(SOLVERS), len(C_EXPS), len(L1_RATIOS), len(MAX_ITERS))
for full in itertools.product(*map(range, sizes)):
    key = canon(*full)
    if key not in frames:
        frames[key] = frame(key)
    MAP["|".join(map(str, full))] = frames[key].name


def menu(i, labels, active, x):
    return dict(type="dropdown", x=x, y=1.32, xanchor="left", yanchor="top", active=active, pad=dict(t=0),
                buttons=[dict(label=lab, method="relayout", args=[{f"updatemenus[{i}].active": j}])
                         for j, lab in enumerate(labels)])


def slider(labels, active, x, prefix):
    return dict(x=x, len=0.28, active=active, pad=dict(t=45), currentvalue=dict(prefix=prefix, font=dict(size=13)),
                steps=[dict(label=lab, method="skip") for lab in labels])


D0 = DATA["binary"]
Z0, title0 = fit(*DEFAULT)
points = [go.Scatter(x=DATA[n]["X"][DATA[n]["y"] == c, 0], y=DATA[n]["X"][DATA[n]["y"] == c, 1], mode="markers",
                     name=f"class {c}", visible=(n == "binary"),
                     marker=dict(color=COLOURS[c], size=7, line=dict(color="white", width=0.5)))
          for n, k in (("binary", 2), ("three", 3)) for c in range(k)]
fig = go.Figure(
    data=[go.Heatmap(x0=D0["xs"][0], dx=D0["xs"][1] - D0["xs"][0], y0=D0["ys"][0], dy=D0["ys"][1] - D0["ys"][0], z=Z0, zmin=0, zmax=2, showscale=False, hoverinfo="skip",
                     colorscale=[[0, REGION[0]], [0.5, REGION[1]], [1, REGION[2]]])] + points,
    frames=list(frames.values()))
fig.update_layout(
    template="simple_white", height=640, margin=dict(l=40, r=20, t=125, b=130),
    title=dict(text=title0, y=0.885, yanchor="middle", font=dict(size=15)),
    xaxis=dict(range=[D0["xs"][0], D0["xs"][-1]]), yaxis=dict(range=[D0["ys"][0], D0["ys"][-1]]),
    legend=dict(orientation="h", x=1, xanchor="right", y=1.02, yanchor="bottom"),
    updatemenus=[menu(0, ["dataset: binary", "dataset: three classes"], DEFAULT[0], 0),
                 menu(1, [f"penalty: {p}" for p in PENALTIES], DEFAULT[1], 0.26),
                 menu(2, [f"solver: {s}" for s in SOLVERS], DEFAULT[2], 0.5)],
    sliders=[slider([f"{10.0 ** e:g}" for e in C_EXPS], DEFAULT[3], 0, "C = "),
             slider([str(r) for r in L1_RATIOS], DEFAULT[4], 0.36, "l1_ratio (Elastic Net only) = "),
             slider([str(m) for m in MAX_ITERS], DEFAULT[5], 0.72, "max_iter = ")])

JS = """
var gd = document.getElementById('{plot_id}');
var MAP = %s;
function show() {
  var key = gd._fullLayout.updatemenus.map(m => m.active).concat(gd._fullLayout.sliders.map(s => s.active)).join('|');
  Plotly.animate(gd, [MAP[key]], %s);
}
gd.on('plotly_buttonclicked', show);
gd.on('plotly_sliderchange', show);
""" % (json.dumps(MAP, separators=(",", ":")), json.dumps(ANIM))
out = HERE / "logistic_playground.html"
fig.write_html(out, include_plotlyjs=plotlyjs_src(out), full_html=True, post_script=JS, auto_play=False,
               config={"responsive": True, "displaylogo": False})
print(f"{len(frames)} frames for {len(MAP)} settings, {N}x{N} grid, {out.stat().st_size / 1e6:.1f} MB")
