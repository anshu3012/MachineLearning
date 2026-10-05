"""Serverless twin of ../app.py: precompute the single model's and the bagging classifier's decision surfaces for a
grid of settings and write ONE Plotly HTML whose controls switch between the precomputed frames in the browser
(no Dash, no callbacks). Each control is a Plotly slider or button row with method "skip"; a few lines of
JavaScript read the position of every control, build the frame names and animate to them.

Run: python bagging_classifier_playground.py -> bagging_classifier_playground.html
"""
import json
import sys
from itertools import product
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from joblib import Parallel, delayed
from plotly.subplots import make_subplots
from sitecustomize import plotlyjs_src

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import BASE, COLOURS, REGION, X_train, fit, y_train  # noqa: E402
from app import xs as XS, ys as YS  # noqa: E402

BASES = list(BASE)
# ponytail: six controls multiply up fast (the app allows 3 x 500 x 15 x 2 x 2 x 2 states). We keep every button
# and coarsen the two sliders: n_estimators to 5 values, max_samples to 4 of its 15 stops, giving
# 3 x 5 x 4 x 2 x 2 x 2 = 480 bagging frames of one N x N surface each, plus 3 single-model frames.
NS = [1, 10, 50, 100, 500]
ROWS = [25, 100, 200, 375]
BOOTS = ["True", "False"]
MFS = ["1", "2"]
BFS = ["False", "True"]
START = ("decision tree", 100, 375, "True", "2", "False")        # the app's initial settings
N = 100                                                # grid cells per axis (app.py uses 250); size grows with N**2
xs, ys = np.linspace(XS[0], XS[-1], N), np.linspace(YS[0], YS[-1], N)
XX, YY = np.meshgrid(xs, ys)
GRID = np.c_[XX.ravel(), YY.ravel()]
ANIM = dict(mode="immediate", frame=dict(duration=0, redraw=True), transition=dict(duration=0))


def key(base, n, rows, boot, mf, bf):
    return f"bag|{base}|{n}|{rows}|{boot}|{mf}|{bf}"


def surface(model):
    return model.predict(GRID).reshape(XX.shape).astype(np.int8)


def compute(base, n, rows, boot, mf, bf):
    (single, a1), (bag, a2) = fit(base, n, rows, boot == "True", int(mf), bf == "True")
    return key(base, n, rows, boot, mf, bf), (surface(bag), f"single {base}: test accuracy {a1:.2f}",
                                             f"bagging: test accuracy {a2:.2f}")


GRID_SETTINGS = list(product(BASES, NS, ROWS, BOOTS, MFS, BFS))
RESULTS = dict(Parallel(n_jobs=-1)(delayed(compute)(*g) for g in GRID_SETTINGS))
SINGLE = {base: surface(BASE[base]().fit(X_train, y_train)) for base in BASES}

Zb0, t1, t2 = RESULTS[key(*START)]
fig = make_subplots(1, 2, subplot_titles=[t1, t2], horizontal_spacing=0.05)
for col, Z in enumerate([SINGLE[START[0]], Zb0], start=1):
    fig.add_trace(go.Heatmap(x=xs, y=ys, z=Z, zmin=0, zmax=1, colorscale=REGION, showscale=False, hoverinfo="skip"),
                  1, col)
    for cls in (0, 1):
        m = y_train == cls
        fig.add_trace(go.Scatter(x=X_train[m, 0], y=X_train[m, 1], mode="markers", name=f"class {cls}",
                                 showlegend=(col == 1), legendgroup=str(cls),
                                 marker=dict(color=COLOURS[cls], size=5, line=dict(color="white", width=0.5))), 1, col)
fig.update_xaxes(range=[xs[0], xs[-1]], showticklabels=False)
fig.update_yaxes(range=[ys[0], ys[-1]], showticklabels=False)

skip = dict(method="skip", args=[])
buttons = lambda labels: [dict(skip, label=l) for l in labels]  # noqa: E731
steps = lambda values: [dict(skip, label=str(v)) for v in values]  # noqa: E731
menu = dict(type="buttons", direction="right", yanchor="bottom", showactive=True)
label = dict(xref="paper", yref="paper", yanchor="bottom", showarrow=False, font=dict(size=12))
fig.update_layout(
    template="simple_white", height=720, margin=dict(l=20, r=20, t=200, b=170),
    legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.02, yanchor="top"),
    updatemenus=[
        dict(menu, buttons=buttons(BASES), active=BASES.index(START[0]), x=0, xanchor="left", y=1.3),
        dict(menu, buttons=buttons(BOOTS), active=BOOTS.index(START[3]), x=0.75, xanchor="center", y=1.3),
        dict(menu, buttons=buttons(MFS), active=MFS.index(START[4]), x=0, xanchor="left", y=1.08),
        dict(menu, buttons=buttons(BFS), active=BFS.index(START[5]), x=0.75, xanchor="center", y=1.08)],
    sliders=[
        dict(steps=steps(NS), active=NS.index(START[1]), x=0, len=0.46, y=-0.1, yanchor="top", pad=dict(t=0),
             currentvalue=dict(prefix="n_estimators = ", xanchor="left")),
        dict(steps=steps(ROWS), active=ROWS.index(START[2]), x=0.54, len=0.46, y=-0.1, yanchor="top", pad=dict(t=0),
             currentvalue=dict(prefix="max_samples (rows per model) = ", xanchor="left"))],
    annotations=list(fig.layout.annotations) + [
        dict(label, text="base model", x=0, xanchor="left", y=1.41),
        dict(label, text="bootstrap (rows with replacement)", x=0.75, xanchor="center", y=1.41),
        dict(label, text="max_features (columns per model)", x=0, xanchor="left", y=1.19),
        dict(label, text="bootstrap_features", x=0.75, xanchor="center", y=1.19)])

# the panel titles are annotations 0 and 1: every bagging frame rewrites the list with its own scores; the single
# model depends on the base model only, so its surface lives in 3 frames of its own (traces 0..2 are panel 1)
ANN = [a.to_plotly_json() for a in fig.layout.annotations]
fig.frames = [go.Frame(name=f"single|{b}", data=[go.Heatmap(z=Z)], traces=[0]) for b, Z in SINGLE.items()] + [
    go.Frame(name=k, data=[go.Heatmap(z=Z)], traces=[3],
             layout=dict(annotations=[dict(ANN[0], text=t1), dict(ANN[1], text=t2)] + ANN[2:]))
    for k, (Z, t1, t2) in RESULTS.items()]

# the glue: every control fires an event; read all of them, name the two frames, show them
JS = """
var gd = document.getElementById('{plot_id}');
function show() {
  var L = gd._fullLayout, m = L.updatemenus, s = L.sliders;
  var pick = function(i) { return m[i].buttons[m[i].active].label; };
  var base = pick(0);
  var k = ['bag', base, s[0].steps[s[0].active].label, s[1].steps[s[1].active].label, pick(1), pick(2), pick(3)].join('|');
  Plotly.animate(gd, ['single|' + base, k], %s);
}
gd.on('plotly_sliderchange', show); gd.on('plotly_buttonclicked', show);
""" % json.dumps(ANIM)
out = HERE / "bagging_classifier_playground.html"
fig.write_html(out, include_plotlyjs=plotlyjs_src(out), full_html=True, auto_play=False, post_script=JS,
               config={"responsive": True, "displaylogo": False})
print(f"{len(fig.frames)} frames, {N}x{N} grid")
