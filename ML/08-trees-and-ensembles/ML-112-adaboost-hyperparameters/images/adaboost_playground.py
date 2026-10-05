"""Serverless twin of ../app.py: precompute the AdaBoost decision surface for a grid of (n_estimators, learning_rate,
max_depth) and write ONE Plotly HTML whose two sliders and one dropdown switch between the precomputed frames in the
browser (no Dash, no callbacks).

Run: python adaboost_playground.py -> adaboost_playground.html
"""
import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from sitecustomize import plotlyjs_src
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import COLOURS, REGION, X, X_test, X_train, y_test, y_train  # noqa: E402

# ponytail: the Dash slider allows every n in 1..1500 (37,500 combinations); 8 n values x 5 learning rates x
# 5 depths = 200 frames, one fit per (lr, depth) with staged_predict giving every n at once.
NS = [1, 5, 10, 25, 50, 150, 500, 1500]
LRS = [0.01, 0.1, 0.5, 1.0, 2.0]
DEPTHS = [1, 2, 3, 4, 5]
N = 150                                            # grid cells per axis (app.py uses 250); size grows with N**2
xs = np.linspace(X[:, 0].min() - 0.2, X[:, 0].max() + 0.2, N)
ys = np.linspace(X[:, 1].min() - 0.2, X[:, 1].max() + 0.2, N)
XX, YY = np.meshgrid(xs, ys)
GRID = np.c_[XX.ravel(), YY.ravel()]


def pick(staged):
    """The stages in NS from a staged_* generator; a fit that stopped early repeats its last stage (as app.py does)."""
    out, last = {}, None
    for i, s in enumerate(staged, start=1):
        last = s
        if i in NS:
            out[i] = s
    return [out.get(n, last) for n in NS]


def name(n, lr, d):
    return f"{n}|{lr}|{d}"


def title(n, lr, d, tr, te):
    return f"n_estimators {n}, learning_rate {lr}, max_depth {d}   |   train {tr:.2f}, test {te:.2f}"


frames, start = [], {}
for lr in LRS:
    for d in DEPTHS:
        model = AdaBoostClassifier(DecisionTreeClassifier(max_depth=d), n_estimators=max(NS), learning_rate=lr,
                                   random_state=42).fit(X_train, y_train)
        Zs = pick(model.staged_predict(GRID))
        trs = pick(model.staged_score(X_train, y_train))
        tes = pick(model.staged_score(X_test, y_test))
        for n, Z, tr, te in zip(NS, Zs, trs, tes):
            Z = Z.reshape(XX.shape).astype(np.int8)
            frames.append(go.Frame(name=name(n, lr, d), data=[go.Heatmap(z=Z)], traces=[0],
                                   layout=dict(title=title(n, lr, d, tr, te))))
            if (n, lr, d) == (50, 1.0, 1):            # the app starts here
                start = dict(Z=Z, title=title(n, lr, d, tr, te))

fig = go.Figure(
    data=[go.Heatmap(x=xs, y=ys, z=start["Z"], zmin=0, zmax=1, colorscale=REGION, showscale=False, hoverinfo="skip")]
    + [go.Scatter(x=X_train[y_train == c, 0], y=X_train[y_train == c, 1], mode="markers", name=f"class {c}",
                  marker=dict(color=COLOURS[c], size=6, line=dict(color="white", width=0.5))) for c in (0, 1)],
    frames=frames)
# Controls only record their choice (method "skip"); the script below joins the three choices into a frame name.
slider = dict(pad=dict(t=30), len=0.9, x=0.05)
fig.update_layout(
    template="simple_white", height=680, margin=dict(l=40, r=20, t=120, b=150),
    title=dict(text=start["title"], y=0.985, yanchor="top"),             # title, then dropdown, then legend
    xaxis=dict(range=[xs[0], xs[-1]], showticklabels=False), yaxis=dict(range=[ys[0], ys[-1]], showticklabels=False),
    legend=dict(orientation="h", x=0.5, xanchor="center", y=1.02, yanchor="bottom"),
    updatemenus=[dict(type="dropdown", x=0.13, xanchor="left", y=1.1, yanchor="bottom", active=LRS.index(1.0),
                      buttons=[dict(label=str(lr), method="skip") for lr in LRS])],
    annotations=[dict(text="learning_rate", x=0, xref="paper", y=1.11, yref="paper", yanchor="bottom",
                      xanchor="left", showarrow=False)],
    sliders=[dict(active=NS.index(50), currentvalue=dict(prefix="n_estimators = "), y=0, **slider,
                  steps=[dict(label=str(n), method="skip") for n in NS]),
             dict(active=DEPTHS.index(1), currentvalue=dict(prefix="max_depth of each tree = "), y=-0.3, **slider,
                  steps=[dict(label=str(d), method="skip") for d in DEPTHS])])

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
out = HERE / "adaboost_playground.html"
fig.write_html(out, include_plotlyjs=plotlyjs_src(out), full_html=True, post_script=JS, auto_play=False,
               config={"responsive": True, "displaylogo": False})
print(f"{len(frames)} frames, {N}x{N} grid, {out.stat().st_size / 1e6:.1f} MB")
