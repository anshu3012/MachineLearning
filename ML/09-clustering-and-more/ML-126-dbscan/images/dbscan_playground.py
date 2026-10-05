"""Serverless twin of ../app.py: precompute DBSCAN's labels for every dataset and a grid of (eps, min_samples) and
write ONE Plotly HTML whose dropdown and two sliders switch between the precomputed frames in the browser (no Dash,
no callbacks).

Run: python dbscan_playground.py -> dbscan_playground.html
"""
import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from sitecustomize import plotlyjs_src
from sklearn.cluster import DBSCAN

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import COLS, DATA  # noqa: E402

# ponytail: the Dash sliders allow eps in 0.05 steps and every min_samples in 2..20 (1,520 combinations); each frame
# is ~500 points (a few KB), so 4 datasets x 12 eps x 8 min_samples = 384 frames stay small.
EPSS = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6, 0.8, 1.0]
MINS = [2, 3, 4, 5, 7, 10, 15, 20]
NOISE = len(COLS)                                  # colour index of noise (grey), after the 8 cluster colours
SCALE = [[(i + k) / (NOISE + 1), c] for i, c in enumerate(COLS + ["#6B6B6B"]) for k in (0, 1)]   # 9 flat bands


def axes(X):
    """Axis ranges that fit this dataset (the app autoscales per dataset)."""
    lo, hi = X.min(0) - 0.2, X.max(0) + 0.2
    return dict(xaxis=dict(range=[lo[0], hi[0]]), yaxis=dict(range=[lo[1], hi[1]]))


def name(data, eps, ms):
    return f"{data}|{eps:g}|{ms}"


def run(data, eps, ms):
    """Per-point colour index, marker symbol (0 circle, 4 x), hover text and the title, as in app.figure_for."""
    labels = DBSCAN(eps=eps, min_samples=ms).fit_predict(DATA[data])
    noise = labels == -1
    colour = np.where(noise, NOISE, labels % len(COLS)).astype(np.int8)
    symbol = np.where(noise, 4, 0).astype(np.int8)
    text = ["noise" if k == -1 else f"cluster {k}" for k in labels]
    title = (f"{data}, eps {eps:g}, min_samples {ms}   |   "
             f"{len(set(labels) - {-1})} clusters, {noise.sum()} noise points")
    return colour, symbol, text, title


frames = []
for data, X in DATA.items():
    for eps in EPSS:
        for ms in MINS:
            colour, symbol, text, title = run(data, eps, ms)
            frames.append(go.Frame(name=name(data, eps, ms), traces=[0], layout=dict(title=title, **axes(X)),
                                   data=[go.Scatter(x=X[:, 0].astype(np.float32), y=X[:, 1].astype(np.float32),
                                                    text=text, marker=dict(color=colour, symbol=symbol))]))

X0 = DATA["two moons"]
colour, symbol, text, title = run("two moons", 0.3, 5)       # the app starts here
fig = go.Figure(
    data=[go.Scatter(x=X0[:, 0], y=X0[:, 1], mode="markers", text=text, hovertemplate="%{text}<extra></extra>",
                     marker=dict(color=colour, symbol=symbol, size=6, cmin=0, cmax=NOISE + 1, colorscale=SCALE,
                                 showscale=False))],
    frames=frames)
# Controls only record their choice (method "skip"); the script below joins the three choices into a frame name.
slider = dict(len=0.9, x=0.05, y=0)
fig.update_layout(
    template="simple_white", height=760, margin=dict(l=40, r=20, t=110, b=230),
    title=dict(text=title, y=0.985, yanchor="top"),                     # title, then dropdown, then the plot
    xaxis=axes(X0)["xaxis"], yaxis=dict(scaleanchor="x", **axes(X0)["yaxis"]),
    updatemenus=[dict(type="dropdown", x=0.1, xanchor="left", y=1.02, yanchor="bottom", active=0,
                      buttons=[dict(label=d, method="skip") for d in DATA])],
    annotations=[dict(text="dataset", x=0, xref="paper", y=1.03, yref="paper", yanchor="bottom", xanchor="left",
                      showarrow=False)],
    sliders=[dict(active=EPSS.index(0.3), pad=dict(t=40), **slider,
                  currentvalue=dict(prefix="eps (radius of the neighbourhood, standardized units) = "),
                  steps=[dict(label=f"{e:g}", method="skip") for e in EPSS]),
             dict(active=MINS.index(5), pad=dict(t=140), **slider,
                  currentvalue=dict(prefix="min_samples (points needed within eps, itself included) = "),
                  steps=[dict(label=str(m), method="skip") for m in MINS])])

JS = """
var gd = document.getElementById('{plot_id}');
function show(e) {
  if (e && e.interaction === false) return;      // the sliders also fire while they are first drawn
  var L = gd._fullLayout, s = L.sliders, m = L.updatemenus[0];
  var f = [m.buttons[m.active].label, s[0].steps[s[0].active].label, s[1].steps[s[1].active].label].join('|');
  Plotly.animate(gd, [f], {mode: 'immediate', frame: {duration: 0, redraw: true}, transition: {duration: 0}});
}
gd.on('plotly_sliderchange', show);
gd.on('plotly_buttonclicked', show);
"""
out = HERE / "dbscan_playground.html"
fig.write_html(out, include_plotlyjs=plotlyjs_src(out), full_html=True, post_script=JS, auto_play=False,
               config={"responsive": True, "displaylogo": False})
print(f"{len(frames)} frames, {out.stat().st_size / 1e6:.1f} MB")
