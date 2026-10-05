"""Serverless twin of ../app.py: precompute the SVM decision regions and support vectors for a grid of settings and
write ONE Plotly HTML whose dropdowns and sliders switch between the precomputed frames in the browser (no Dash).
Plotly controls are stateless, so a few lines of JS read every control's active index and pick the frame.

Run: python kernel_playground.py -> kernel_playground.html
"""
import itertools
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from sitecustomize import plotlyjs_src
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import COLOURS, REGION, make_data  # noqa: E402

warnings.simplefilter("ignore")

# ponytail: the Dash app allows 2 datasets x 4 kernels x 13 C x 11 gamma x 6 degrees. We keep every dataset,
# kernel and degree; C and gamma at whole powers of ten, on a 75x75 grid (app: 250x250). Settings a kernel
# ignores (gamma for linear, degree for all but poly) share one frame.
DATASETS = ["circles", "moons"]
KERNELS = ["linear", "rbf", "poly", "sigmoid"]
C_EXPS = list(range(-3, 4))
GAMMA_EXPS = list(range(-3, 3))
DEGREES = list(range(1, 7))
DEFAULT = (0, 1, 3, 3, 2)                           # circles, rbf, C = 1, gamma = 1, degree = 3
N = 75
# ponytail: libsvm has no iteration cap (the app would hang on poly with large C and gamma); a million iterations
# takes under a second, and the title says when the cap stopped the fit.
MAX_ITER = 1_000_000
ANIM = dict(mode="immediate", frame=dict(duration=0, redraw=True), transition=dict(duration=0))

DATA = {}
for name in DATASETS:
    X, y = make_data(name)
    pad = 0.4
    xs = np.linspace(X[:, 0].min() - pad, X[:, 0].max() + pad, N)
    ys = np.linspace(X[:, 1].min() - pad, X[:, 1].max() + pad, N)
    XX, YY = np.meshgrid(xs, ys)
    DATA[name] = dict(X=X, y=y, split=train_test_split(X, y, test_size=0.2, random_state=0),
                      xs=xs, ys=ys, grid=np.c_[XX.ravel(), YY.ravel()])


def canon(di, ki, ci, gi, de):
    """The frame that shows this setting: controls the kernel ignores are pinned to their default."""
    if KERNELS[ki] == "linear":
        gi = DEFAULT[3]
    if KERNELS[ki] != "poly":
        de = DEFAULT[4]
    return (di, ki, ci, gi, de)


def frame(key):
    """One frame: regions, support-vector rings, which dataset's points are visible, and the app's title."""
    di, ki, ci, gi, de = key
    D = DATA[DATASETS[di]]
    a, b, c, d = D["split"]
    model = SVC(kernel=KERNELS[ki], C=10.0 ** C_EXPS[ci], gamma=10.0 ** GAMMA_EXPS[gi], degree=DEGREES[de],
                max_iter=MAX_ITER).fit(a, c)
    capped = " (stopped at the iteration cap)" if model.n_iter_.max() >= MAX_ITER else ""
    Z = model.predict(D["grid"]).reshape(N, N).astype(np.int8)
    sv = model.support_vectors_.astype(np.float32)
    return go.Frame(
        name="|".join(map(str, key)), traces=[0, 1, 2, 3, 4, 5],
        data=[go.Heatmap(z=Z, x0=D["xs"][0], dx=D["xs"][1] - D["xs"][0], y0=D["ys"][0], dy=D["ys"][1] - D["ys"][0]),
              go.Scatter(visible=(di == 0)), go.Scatter(visible=(di == 0)),
              go.Scatter(visible=(di == 1)), go.Scatter(visible=(di == 1)), go.Scatter(x=sv[:, 0], y=sv[:, 1])],
        layout=dict(title=dict(text=f"{KERNELS[ki]}: test accuracy {model.score(b, d):.2f}, "
                                    f"{len(sv)} support vectors{capped}"),
                    xaxis=dict(range=[D["xs"][0], D["xs"][-1]]), yaxis=dict(range=[D["ys"][0], D["ys"][-1]])))


frames, MAP = {}, {}
sizes = (len(DATASETS), len(KERNELS), len(C_EXPS), len(GAMMA_EXPS), len(DEGREES))
for full in itertools.product(*map(range, sizes)):
    key = canon(*full)
    if key not in frames:
        frames[key] = frame(key)
    MAP["|".join(map(str, full))] = frames[key].name


def menu(i, labels, active, x):
    return dict(type="dropdown", x=x, y=1.3, xanchor="left", yanchor="top", active=active, pad=dict(t=0),
                buttons=[dict(label=lab, method="relayout", args=[{f"updatemenus[{i}].active": j}])
                         for j, lab in enumerate(labels)])


def slider(labels, active, x, prefix):
    return dict(x=x, len=0.28, active=active, pad=dict(t=45), currentvalue=dict(prefix=prefix, font=dict(size=13)),
                steps=[dict(label=lab, method="skip") for lab in labels])


D0 = DATA["circles"]
f0 = frames[DEFAULT]
points = [go.Scatter(x=DATA[n]["X"][DATA[n]["y"] == c, 0], y=DATA[n]["X"][DATA[n]["y"] == c, 1], mode="markers",
                     name=f"class {c}", visible=(n == "circles"),
                     marker=dict(color=COLOURS[c], size=8, line=dict(color="white", width=0.5)))
          for n in DATASETS for c in (0, 1)]
fig = go.Figure(
    data=[go.Heatmap(x0=D0["xs"][0], dx=D0["xs"][1] - D0["xs"][0], y0=D0["ys"][0], dy=D0["ys"][1] - D0["ys"][0], z=f0.data[0].z, zmin=0, zmax=1, showscale=False, hoverinfo="skip",
                     colorscale=[[0, REGION[0]], [1, REGION[1]]])] + points
    + [go.Scatter(x=f0.data[5].x, y=f0.data[5].y, mode="markers", name="support vectors",
                  marker=dict(size=14, color="rgba(0,0,0,0)", line=dict(color="black", width=1.5)))],
    frames=list(frames.values()))
fig.update_layout(
    template="simple_white", height=680, margin=dict(l=40, r=20, t=125, b=130),
    title=dict(text=f0.layout.title.text, y=0.89, yanchor="middle", font=dict(size=15)),
    xaxis=dict(range=[D0["xs"][0], D0["xs"][-1]]), yaxis=dict(range=[D0["ys"][0], D0["ys"][-1]], scaleanchor="x"),
    legend=dict(orientation="h", x=1, xanchor="right", y=1.02, yanchor="bottom"),
    updatemenus=[menu(0, [f"dataset: {d}" for d in DATASETS], DEFAULT[0], 0),
                 menu(1, [f"kernel: {k}" for k in KERNELS], DEFAULT[1], 0.3)],
    sliders=[slider([f"{10.0 ** e:g}" for e in C_EXPS], DEFAULT[2], 0, "C = "),
             slider([f"{10.0 ** e:g}" for e in GAMMA_EXPS], DEFAULT[3], 0.36, "gamma (rbf, poly, sigmoid) = "),
             slider([str(k) for k in DEGREES], DEFAULT[4], 0.72, "degree (poly only) = ")])

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
out = HERE / "kernel_playground.html"
fig.write_html(out, include_plotlyjs=plotlyjs_src(out), full_html=True, post_script=JS, auto_play=False,
               config={"responsive": True, "displaylogo": False})
print(f"{len(frames)} frames for {len(MAP)} settings, {N}x{N} grid, {out.stat().st_size / 1e6:.1f} MB")
