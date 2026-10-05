"""Serverless twin of ../app.py: precompute the single model's curve and the bagging regressor's curve for a grid of
settings and write ONE Plotly HTML whose controls switch between the precomputed frames in the browser (no Dash,
no callbacks). Each control is a Plotly slider or button row with method "skip"; a few lines of JavaScript read
the position of every control, build the frame name and animate to it.

Run: python bagging_regressor_playground.py -> bagging_regressor_playground.html
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
from app import BASE, X_line, X_train, fit, y_train  # noqa: E402

BASES = list(BASE)
# ponytail: the Dash n_estimators slider allows every value in 1..500; we keep 9 of them (the rest of the grid is
# the app's own: max_samples in steps of 25, bootstrap on/off), 3 x 9 x 6 x 2 = 324 frames of two 500-point curves.
NS = [1, 2, 5, 10, 25, 50, 100, 250, 500]
ROWS = list(range(25, 151, 25))
BOOTS = ["True", "False"]
START = ("decision tree", 50, 25, "True")              # the app's initial settings
ANIM = dict(mode="immediate", frame=dict(duration=0, redraw=True), transition=dict(duration=0))
x_line = X_line.ravel()


def key(base, n, rows, boot):
    return f"{base}|{n}|{rows}|{boot}"


def compute(base, n, rows, boot):
    (single, r1), (bag, r2) = fit(base, n, rows, boot == "True")
    return key(base, n, rows, boot), (single.predict(X_line).astype(np.float32), bag.predict(X_line).astype(np.float32),
                                     f"single {base}: test R² {r1:.2f}", f"bagging: test R² {r2:.2f}")


GRID = list(product(BASES, NS, ROWS, BOOTS))
RESULTS = dict(Parallel(n_jobs=-1)(delayed(compute)(*g) for g in GRID))

ys0, yb0, t1, t2 = RESULTS[key(*START)]
fig = make_subplots(1, 2, shared_yaxes=True, horizontal_spacing=0.04, subplot_titles=[t1, t2])
for col, (yc, colour) in enumerate([(ys0, "#E45756"), (yb0, "#4C78A8")], start=1):
    fig.add_trace(go.Scatter(x=X_train.ravel(), y=y_train, mode="markers", name="training points", showlegend=(col == 1),
                             marker=dict(color="#FFD24C", size=7, line=dict(color="black", width=1))), 1, col)
    fig.add_trace(go.Scatter(x=x_line, y=yc, mode="lines", showlegend=False, line=dict(color=colour, width=3)), 1, col)
fig.update_xaxes(title="x")
fig.update_yaxes(title="y", col=1)

skip = dict(method="skip", args=[])
buttons = lambda labels: [dict(skip, label=l) for l in labels]  # noqa: E731
steps = lambda values: [dict(skip, label=str(v)) for v in values]  # noqa: E731
fig.update_layout(
    template="simple_white", height=640, margin=dict(l=60, r=20, t=130, b=150),
    updatemenus=[
        dict(type="buttons", direction="right", buttons=buttons(BASES), active=BASES.index(START[0]),
             x=0, xanchor="left", y=1.12, yanchor="bottom", showactive=True),
        dict(type="buttons", direction="right", buttons=buttons(BOOTS), active=BOOTS.index(START[3]),
             x=0.75, xanchor="center", y=1.12, yanchor="bottom", showactive=True)],
    sliders=[
        dict(steps=steps(NS), active=NS.index(START[1]), x=0, len=0.46, y=-0.18, yanchor="top", pad=dict(t=0),
             currentvalue=dict(prefix="n_estimators = ", xanchor="left")),
        dict(steps=steps(ROWS), active=ROWS.index(START[2]), x=0.54, len=0.46, y=-0.18, yanchor="top", pad=dict(t=0),
             currentvalue=dict(prefix="max_samples (rows per model) = ", xanchor="left"))],
    annotations=list(fig.layout.annotations) + [
        dict(text="base model", x=0, xref="paper", y=1.24, yref="paper", xanchor="left", yanchor="bottom",
             showarrow=False, font=dict(size=12)),
        dict(text="bootstrap (rows with replacement)", x=0.75, xref="paper", y=1.24, yref="paper", xanchor="center",
             yanchor="bottom", showarrow=False, font=dict(size=12))])

# the panel titles are annotations 0 and 1: every frame rewrites the list with its own scores
ANN = [a.to_plotly_json() for a in fig.layout.annotations]
fig.frames = [go.Frame(name=k, data=[go.Scatter(y=ys), go.Scatter(y=yb)], traces=[1, 3],
                       layout=dict(annotations=[dict(ANN[0], text=t1), dict(ANN[1], text=t2)] + ANN[2:]))
              for k, (ys, yb, t1, t2) in RESULTS.items()]

# the glue: every control fires an event; read all of them, name the frame, show it
JS = """
var gd = document.getElementById('{plot_id}');
function show() {
  var L = gd._fullLayout, m = L.updatemenus, s = L.sliders;
  var k = [m[0].buttons[m[0].active].label, s[0].steps[s[0].active].label, s[1].steps[s[1].active].label,
           m[1].buttons[m[1].active].label].join('|');
  Plotly.animate(gd, [k], %s);
}
gd.on('plotly_sliderchange', show); gd.on('plotly_buttonclicked', show);
""" % json.dumps(ANIM)
out = HERE / "bagging_regressor_playground.html"
fig.write_html(out, include_plotlyjs=plotlyjs_src(out), full_html=True, auto_play=False, post_script=JS,
               config={"responsive": True, "displaylogo": False})
print(f"{len(fig.frames)} frames")
