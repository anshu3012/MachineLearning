"""Serverless twin of ../app.py: precompute the voting classifier's decision surface for every dataset, subset of
base models and voting type, and write ONE Plotly HTML whose dropdowns switch frames in the browser (no Dash).
Plotly controls are stateless, so a few lines of JS read every dropdown's active index and pick the frame.

Run: python voting_playground.py -> voting_playground.html
"""
import itertools
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sitecustomize import plotlyjs_src
from sklearn.ensemble import VotingClassifier

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import COLOURS, DATASETS, REGION, base_models, grid, load  # noqa: E402

warnings.simplefilter("ignore")
# ponytail: every control is kept (6 datasets x 2 voting types x 31 non-empty subsets of 5 models = 372 frames);
# the grid is 80x80 (app: 200x200). A base model's surface depends only on the dataset, so the 30 base surfaces
# live in the figure once and each frame only carries the voting surface plus which traces are visible.
NAMES = list(DATASETS)
MODELS = ["KNN", "logistic regression", "Gaussian naive Bayes", "SVM", "random forest"]
VOTING = ["hard", "soft"]
DEFAULT = (0, 0, 1, 0, 0, 1, 0)                     # concentric circles, hard, model i off (1) / on (0)
N = 80
ANIM = dict(mode="immediate", frame=dict(duration=0, redraw=True), transition=dict(duration=0))
POS = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3)]      # subplot of the voting classifier, then of each model


def predict(model, D):
    return model.predict(D["grid"]).reshape(N, N).astype(np.int8)


DATA = {}
for name in NAMES:
    X_train, X_test, y_train, y_test = load(name)
    xs, ys = grid(X_train, N)
    XX, YY = np.meshgrid(xs, ys)
    D = dict(X=X_train, y=y_train, test=(X_test, y_test), xs=xs, ys=ys, grid=np.c_[XX.ravel(), YY.ravel()], base={})
    for m, model in base_models(MODELS):
        model.fit(X_train, y_train)
        D["base"][m] = (predict(model, D), model.score(X_test, y_test))
    DATA[name] = D

fig = make_subplots(2, 3, subplot_titles=[" "] * 6, horizontal_spacing=0.05, vertical_spacing=0.12)
ANNOT = [a.to_plotly_json() for a in fig.layout.annotations]      # subplot-title positions, text filled per frame
D0 = DATA[NAMES[0]]
fig.add_trace(go.Heatmap(z=np.zeros((N, N), np.int8), zmin=0, zmax=1, colorscale=REGION, showscale=False,
                         hoverinfo="skip", x0=D0["xs"][0], dx=1, y0=D0["ys"][0], dy=1), 1, 1)
BASE = {}                                           # (dataset, model) -> trace index
for name in NAMES:
    D = DATA[name]
    for j, m in enumerate(MODELS):
        BASE[name, m] = len(fig.data)
        fig.add_trace(go.Heatmap(z=D["base"][m][0], zmin=0, zmax=1, colorscale=REGION, showscale=False, hoverinfo="skip",
                                 x0=D["xs"][0], dx=D["xs"][1] - D["xs"][0], y0=D["ys"][0], dy=D["ys"][1] - D["ys"][0],
                                 visible=False), *POS[j + 1])
POINTS = {}                                         # (dataset, subplot) -> trace indices of its two classes
for name in NAMES:
    D = DATA[name]
    for s in range(6):
        POINTS[name, s] = [len(fig.data), len(fig.data) + 1]
        for c in (0, 1):
            fig.add_trace(go.Scatter(x=D["X"][D["y"] == c, 0].astype(np.float32), y=D["X"][D["y"] == c, 1].astype(np.float32),
                                     mode="markers", name=f"class {c}", showlegend=(s == 0), legendgroup=str(c),
                                     visible=False, marker=dict(color=COLOURS[c], size=5, line=dict(color="white", width=0.5))),
                          *POS[s])
NT = len(fig.data)


def frame(di, vi, flags):
    """One frame: voting surface, visibility of every trace, subplot titles with accuracies, hidden empty subplots."""
    name, chosen = NAMES[di], [m for m, off in zip(MODELS, flags) if not off]
    D = DATA[name]
    visible = [False] * NT
    layout = {}
    annots = [dict(a, text="") for a in ANNOT]
    if chosen:
        vc = VotingClassifier(estimators=base_models(chosen), voting=VOTING[vi]).fit(D["X"], D["y"])
        heat = go.Heatmap(z=predict(vc, D), x0=D["xs"][0], dx=D["xs"][1] - D["xs"][0], y0=D["ys"][0],
                          dy=D["ys"][1] - D["ys"][0], visible=True)
        annots[0]["text"] = f"voting ({VOTING[vi]}): {vc.score(*D['test']):.2f}"
    else:
        heat = go.Heatmap(visible=False)
        annots[0]["text"] = "pick at least one base model"
    for j, m in enumerate(MODELS):
        on = m in chosen
        visible[BASE[name, m]] = on
        annots[j + 1]["text"] = f"{m}: {D['base'][m][1]:.2f}" if on else ""
        for ax in ("xaxis", "yaxis"):
            layout[f"{ax}{j + 2}"] = dict(visible=on)
    for s in range(6):
        if s == 0 or not flags[s - 1]:
            for t in POINTS[name, s]:
                visible[t] = bool(chosen)
    for s in range(6):
        sfx = "" if s == 0 else str(s + 1)
        layout[f"xaxis{sfx}"] = dict(layout.get(f"xaxis{sfx}", {}), range=[D["xs"][0], D["xs"][-1]])
        layout[f"yaxis{sfx}"] = dict(layout.get(f"yaxis{sfx}", {}), range=[D["ys"][0], D["ys"][-1]])
    data = [heat] + [go.Heatmap(visible=v) if i <= 5 * len(NAMES) else go.Scatter(visible=v)
                     for i, v in enumerate(visible) if i > 0]
    return go.Frame(name="|".join(map(str, (di, vi, *flags))), data=data, traces=list(range(NT)),
                    layout=dict(layout, annotations=annots))


frames = [frame(di, vi, flags) for di, vi, *flags in itertools.product(range(len(NAMES)), range(2), *[(0, 1)] * 5)]
f0 = next(f for f in frames if f.name == "|".join(map(str, DEFAULT)))
for i, t in enumerate(f0.data):                      # start the page at the app's default setting
    fig.data[i].update(t.to_plotly_json())
fig.update_layout(f0.layout.to_plotly_json())
fig.frames = frames


def menu(i, labels, active, x, y):
    return dict(type="dropdown", x=x, y=y, xanchor="left", yanchor="top", active=active, pad=dict(t=0),
                buttons=[dict(label=lab, method="relayout", args=[{f"updatemenus[{i}].active": j}])
                         for j, lab in enumerate(labels)])


fig.update_xaxes(showticklabels=False)
fig.update_yaxes(showticklabels=False)
fig.update_layout(
    template="simple_white", height=790, margin=dict(l=20, r=20, t=140, b=40),
    legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.03),
    updatemenus=[menu(0, [f"dataset: {n}" for n in NAMES], DEFAULT[0], 0, 1.24),
                 menu(1, [f"voting: {v}" for v in VOTING], DEFAULT[1], 0.3, 1.24)]
    + [menu(2 + j, [f"{m}: on", f"{m}: off"], DEFAULT[2 + j], 0.2 * j, 1.15) for j, m in enumerate(MODELS)])

JS = """
var gd = document.getElementById('{plot_id}');
function show() {
  Plotly.animate(gd, [gd._fullLayout.updatemenus.map(m => m.active).join('|')], %s);
}
gd.on('plotly_buttonclicked', show);
""" % json.dumps(ANIM)
out = HERE / "voting_playground.html"
fig.write_html(out, include_plotlyjs=plotlyjs_src(out), full_html=True, post_script=JS, auto_play=False,
               config={"responsive": True, "displaylogo": False})
print(f"{len(frames)} frames, {N}x{N} grid, {out.stat().st_size / 1e6:.1f} MB")
