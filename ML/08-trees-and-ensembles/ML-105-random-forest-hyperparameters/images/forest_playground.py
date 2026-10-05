"""Serverless twin of ../app.py: precompute the random forest's decision surface for a grid of the four forest-level
settings and write ONE Plotly HTML whose controls switch between the precomputed frames in the browser (no Dash,
no callbacks). Each control is a Plotly slider or button row with method "skip"; a few lines of JavaScript read
the position of every control, build the frame name and animate to it.

Run: python forest_playground.py -> forest_playground.html
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
from app import COLOURS, REGION, X_train, fit, y_train  # noqa: E402
from app import xs as XS, ys as YS  # noqa: E402

# ponytail: the Dash n_estimators slider allows every value in 1..300; we keep 8 of them. max_samples keeps 9 of the
# app's 15 stops and only counts with bootstrap=True (the app ignores it otherwise), so 8 x 2 x (9 + 1) = 160 frames.
NS = [1, 5, 10, 25, 50, 100, 200, 300]
MFS = ["sqrt", "log2", "1", "2"]
# with two features sqrt(2), log2(2) and 1 all round to one column per split, so three buttons share one surface
MF_COLS = {"sqrt": 1, "log2": 1, "1": 1, "2": 2}
BOOTS = ["True", "False"]
ROWS = [25, 50, 75, 100, 150, 200, 250, 300, 375]
START = (100, "sqrt", "True", 375)                     # the app's initial settings
N = 125                                                # grid cells per axis (app.py uses 250); size grows with N**2
xs, ys = np.linspace(XS[0], XS[-1], N), np.linspace(YS[0], YS[-1], N)
XX, YY = np.meshgrid(xs, ys)
GRID = np.c_[XX.ravel(), YY.ravel()]
ANIM = dict(mode="immediate", frame=dict(duration=0, redraw=True), transition=dict(duration=0))


def key(n, mf, boot, rows):
    return f"{n}|{MF_COLS[mf]}|{boot}|{rows if boot == 'True' else '-'}"


def compute(n, cols, boot, rows):
    rf, acc = fit(n, cols, boot == "True", rows)
    return (rf.predict(GRID).reshape(XX.shape).astype(np.int8), f"random forest: test accuracy {acc:.3f}")


COMBOS = {key(n, mf, boot, rows): (n, MF_COLS[mf], boot, rows)
          for n, mf, boot, rows in product(NS, MFS, BOOTS, ROWS)}          # one entry per distinct frame
RESULTS = dict(zip(COMBOS, Parallel(n_jobs=-1)(delayed(compute)(*c) for c in COMBOS.values())))

Z0, t0 = RESULTS[key(*START)]
fig = make_subplots(1, 1, subplot_titles=[t0])
fig.add_trace(go.Heatmap(x=xs, y=ys, z=Z0, zmin=0, zmax=1, colorscale=REGION, showscale=False, hoverinfo="skip"))
for cls in (0, 1):
    m = y_train == cls
    fig.add_trace(go.Scatter(x=X_train[m, 0], y=X_train[m, 1], mode="markers", name=f"class {cls}",
                             marker=dict(color=COLOURS[cls], size=5, line=dict(color="white", width=0.5))))
fig.update_xaxes(range=[xs[0], xs[-1]], showticklabels=False)
fig.update_yaxes(range=[ys[0], ys[-1]], showticklabels=False)

skip = dict(method="skip", args=[])
buttons = lambda labels: [dict(skip, label=l) for l in labels]  # noqa: E731
steps = lambda values: [dict(skip, label=str(v)) for v in values]  # noqa: E731
fig.update_layout(
    template="simple_white", height=740, margin=dict(l=20, r=20, t=130, b=170),
    legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.02, yanchor="top"),
    updatemenus=[
        dict(type="buttons", direction="right", buttons=buttons(MFS), active=MFS.index(START[1]),
             x=0, xanchor="left", y=1.08, yanchor="bottom", showactive=True),
        dict(type="buttons", direction="right", buttons=buttons(BOOTS), active=BOOTS.index(START[2]),
             x=0.75, xanchor="center", y=1.08, yanchor="bottom", showactive=True)],
    sliders=[
        dict(steps=steps(NS), active=NS.index(START[0]), x=0, len=0.46, y=-0.1, yanchor="top", pad=dict(t=0),
             currentvalue=dict(prefix="n_estimators (trees) = ", xanchor="left")),
        dict(steps=steps(ROWS), active=ROWS.index(START[3]), x=0.54, len=0.46, y=-0.1, yanchor="top", pad=dict(t=0),
             currentvalue=dict(prefix="max_samples (rows per tree, only with bootstrap) = ", xanchor="left"))],
    annotations=list(fig.layout.annotations) + [
        dict(text="max_features (columns per split)", x=0, xref="paper", y=1.19, yref="paper", xanchor="left",
             yanchor="bottom", showarrow=False, font=dict(size=12)),
        dict(text="bootstrap", x=0.75, xref="paper", y=1.19, yref="paper", xanchor="center", yanchor="bottom",
             showarrow=False, font=dict(size=12))])

# the panel title is annotation 0: every frame rewrites the list with its own score
ANN = [a.to_plotly_json() for a in fig.layout.annotations]
fig.frames = [go.Frame(name=k, data=[go.Heatmap(z=Z)], traces=[0], layout=dict(annotations=[dict(ANN[0], text=t)] + ANN[1:]))
              for k, (Z, t) in RESULTS.items()]

# the glue: every control fires an event; read all of them, name the frame, show it
JS = """
var gd = document.getElementById('{plot_id}');
var MF_COLS = %s;
function show() {
  var L = gd._fullLayout, m = L.updatemenus, s = L.sliders;
  var boot = m[1].buttons[m[1].active].label;
  var k = [s[0].steps[s[0].active].label, MF_COLS[m[0].buttons[m[0].active].label], boot,
           boot == 'True' ? s[1].steps[s[1].active].label : '-'].join('|');
  Plotly.animate(gd, [k], %s);
}
gd.on('plotly_sliderchange', show); gd.on('plotly_buttonclicked', show);
""" % (json.dumps(MF_COLS), json.dumps(ANIM))
out = HERE / "forest_playground.html"
fig.write_html(out, include_plotlyjs=plotlyjs_src(out), full_html=True, auto_play=False, post_script=JS,
               config={"responsive": True, "displaylogo": False})
print(f"{len(fig.frames)} frames, {N}x{N} grid")
