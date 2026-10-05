"""Serverless twin of ../app.py: precompute the base-regressor curves and the voting regressor's curve for every
non-empty choice of base models, and write ONE Plotly HTML whose dropdown switches between the precomputed frames
in the browser (no Dash, no callbacks).

Run: python voting_playground.py -> voting_playground.html
"""
import sys
from itertools import combinations
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from sitecustomize import plotlyjs_src

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import COLOURS, X_line, X_test, X_train, run, y_test, y_train  # noqa: E402

NAMES = list(COLOURS)
# ponytail: the Dash checklist has 2**3 - 1 = 7 non-empty states; one dropdown entry per state, nothing coarsened.
COMBOS = [c for r in (1, 2, 3) for c in combinations(NAMES, r)]
START = ("linear regression", "SVR")                   # the app's initial ticks
ANIM = dict(mode="immediate", frame=dict(duration=0, redraw=True), transition=dict(duration=0))
x_line = X_line.ravel()


def curves(combo):
    """[(name, y on X_line, R², MAE)] for every base model (hidden if not ticked), then the voting regressor."""
    res = {n: (m, r2, mae) for n, m, r2, mae in run(list(combo))}
    out = []
    for n in NAMES:
        if n in combo:
            m, r2, mae = res[n]
            out.append(dict(y=m.predict(X_line).astype(np.float32), visible=True, name=f"{n}: R² {r2:.2f}, MAE {mae:.2f}"))
        else:
            out.append(dict(visible=False, name=n))
    m, r2, mae = res["voting regressor"]
    out.append(dict(y=m.predict(X_line).astype(np.float32), name=f"voting regressor: R² {r2:.2f}, MAE {mae:.2f}"))
    return out, f"voting regressor: R² {r2:.2f}, MAE {mae:.2f}"


label = " + ".join
frames, buttons = [], []
for combo in COMBOS:
    data, title = curves(combo)
    frames.append(go.Frame(name=label(combo), data=[go.Scatter(**d) for d in data], traces=[2, 3, 4, 5], layout=dict(title=title)))
    buttons.append(dict(label=label(combo), method="animate", args=[[label(combo)], ANIM]))

data0, title0 = curves(START)
fig = go.Figure(
    data=[go.Scatter(x=X_train.ravel(), y=y_train, mode="markers", name="training points",
                     marker=dict(color="#FFD24C", size=9, line=dict(color="black", width=1))),
          go.Scatter(x=X_test.ravel(), y=y_test, mode="markers", name="test points",
                     marker=dict(color="white", size=9, symbol="diamond", line=dict(color="black", width=1.5)))]
    + [go.Scatter(x=x_line, mode="lines", line=dict(color=COLOURS[n], width=2, dash="dashdot"), **d)
       for n, d in zip(NAMES, data0[:3])]
    + [go.Scatter(x=x_line, mode="lines", line=dict(color="#4C78A8", width=4), **data0[3])],
    frames=frames)
fig.update_layout(template="simple_white", height=560, margin=dict(l=60, r=20, t=90, b=50), title=title0,
                  xaxis_title="x", yaxis_title="y",
                  updatemenus=[dict(type="dropdown", buttons=buttons, active=COMBOS.index(START), x=1, xanchor="right",
                                    y=1.02, yanchor="bottom", pad=dict(l=0, r=0, t=0, b=0))],
                  annotations=[dict(text="base models:", x=1, xref="paper", y=1.11, yref="paper",
                                    xanchor="right", yanchor="bottom", showarrow=False, font=dict(size=12))])
out = HERE / "voting_playground.html"
fig.write_html(out, include_plotlyjs=plotlyjs_src(out), full_html=True, auto_play=False,
               config={"responsive": True, "displaylogo": False})
print(f"{len(COMBOS)} frames")
