"""Serverless twin of ../app.py: precompute the gradient-boosting ensemble curve for a grid of (number of trees,
learning rate, max_leaf_nodes) and write ONE Plotly HTML whose two sliders and one dropdown switch between the
precomputed frames in the browser (no Dash, no callbacks).

Run: python gradient_boosting_playground.py -> gradient_boosting_playground.html
"""
import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from sitecustomize import plotlyjs_src

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import BLUE, FONT, GRID, RED, X, X_test, boost, mse, predict, y, y_test  # noqa: E402

# ponytail: the Dash sliders allow every n in 0..100 and every leaf count in 2..32 (15,655 combinations); each frame
# is one 500-point curve (a few KB), so 10 tree counts x 5 learning rates x 6 leaf counts = 300 frames fit easily.
NS = [0, 1, 2, 3, 4, 5, 10, 25, 50, 100]
LRS = [0.05, 0.1, 0.3, 0.5, 1.0]
LEAVES = [2, 3, 4, 8, 16, 32]


def name(n, lr, leaves):
    return f"{n}|{lr}|{leaves}"


def curve(n, lr, leaves):
    f0, trees = boost(n, lr, leaves)
    train, test = mse(y, predict(f0, trees, lr, X)), mse(y_test, predict(f0, trees, lr, X_test))
    title = f"{n} trees, learning rate {lr}, {leaves} leaves   |   training MSE {train:.4f}, test MSE {test:.4f}"
    return predict(f0, trees, lr, GRID).astype(np.float32), title


frames = []
for lr in LRS:
    for leaves in LEAVES:
        for n in NS:
            yy, title = curve(n, lr, leaves)
            frames.append(go.Frame(name=name(n, lr, leaves), data=[go.Scatter(y=yy)], traces=[1],
                                   layout=dict(title=title)))

y0, title0 = curve(3, 1.0, 8)                       # the app starts here
fig = go.Figure(
    data=[go.Scatter(x=X[:, 0], y=y, mode="markers", name="training data", marker=dict(color=BLUE, size=7)),
          go.Scatter(x=GRID[:, 0], y=y0, mode="lines", name="ensemble", line=dict(color=RED, width=3))],
    frames=frames)
# Controls only record their choice (method "skip"); the script below joins the three choices into a frame name.
slider = dict(len=0.9, x=0.05, y=0)
fig.update_layout(
    template="simple_white", font=FONT, height=700, margin=dict(l=60, r=20, t=120, b=230),
    title=dict(text=title0, y=0.985, yanchor="top"),                     # title, then dropdown, then legend
    xaxis=dict(title="x"), yaxis=dict(title="y", range=[-0.2, 0.9]),
    legend=dict(orientation="h", x=0.5, xanchor="center", y=1.02, yanchor="bottom"),
    updatemenus=[dict(type="dropdown", x=0.15, xanchor="left", y=1.115, yanchor="bottom", active=LRS.index(1.0),
                      buttons=[dict(label=str(lr), method="skip") for lr in LRS])],
    annotations=[dict(text="learning rate", x=0, xref="paper", y=1.125, yref="paper", yanchor="bottom",
                      xanchor="left", showarrow=False)],
    sliders=[dict(active=NS.index(3), currentvalue=dict(prefix="number of trees = "), pad=dict(t=60), **slider,
                  steps=[dict(label=str(n), method="skip") for n in NS]),
             dict(active=LEAVES.index(8), currentvalue=dict(prefix="max_leaf_nodes of each tree = "),
                  pad=dict(t=160), **slider, steps=[dict(label=str(k), method="skip") for k in LEAVES])])

JS = """
var gd = document.getElementById('{plot_id}');
function show(e) {
  if (e && e.interaction === false) return;      // the sliders also fire while they are first drawn
  var L = gd._fullLayout, s = L.sliders, m = L.updatemenus[0];
  var f = [s[0].steps[s[0].active].label, m.buttons[m.active].label, s[1].steps[s[1].active].label].join('|');
  Plotly.animate(gd, [f], {mode: 'immediate', frame: {duration: 0, redraw: true}, transition: {duration: 0}});
}
gd.on('plotly_sliderchange', show);
gd.on('plotly_buttonclicked', show);
"""
out = HERE / "gradient_boosting_playground.html"
fig.write_html(out, include_plotlyjs=plotlyjs_src(out), full_html=True, post_script=JS, auto_play=False,
               config={"responsive": True, "displaylogo": False})
print(f"{len(frames)} frames, {out.stat().st_size / 1e6:.1f} MB")
