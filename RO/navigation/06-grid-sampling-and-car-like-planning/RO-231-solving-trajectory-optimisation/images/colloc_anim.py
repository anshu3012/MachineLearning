"""Direct collocation of the 8 s least-effort drive, one solver iteration per frame (thinning out after the first
ones). The unknowns are the state and the controls at 31 knot points (dots), 0.267 s apart; nothing is simulated.
The line joins the knots. The first guess puts the knots on the A* route, driven at a steady speed, with the heading turning evenly from 30 to 90 degrees. Red
lines show each knot's defect: where the trapezoid rule, from the previous knot, says it should be, against where
it is. Run -> colloc.gif, colloc_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import roomdraw as rd
import trajkit as tk
from gifkit import BLUE, FONT, RED, make_gif

here = Path(__file__).parent
sol = tk.solutions()["colloc"]
N = 30
h = 8.0 / N


def defects(X, U):
    F = tk.f(X, U)
    pred = X[:-1] + h / 2 * (F[:-1] + F[1:])
    return pred, np.hypot(*(pred[:, :2] - X[1:, :2]).T)


def frame(i):
    X, U, T = sol["hist"][i]
    fig = go.Figure()
    rd.room(fig)
    pred, d = defects(X, U)
    for k in range(N):
        fig.add_trace(go.Scatter(x=[pred[k, 0], X[k + 1, 0]], y=[pred[k, 1], X[k + 1, 1]], mode="lines",
                                 line=dict(color=RED, width=4)))
    fig.add_trace(go.Scatter(x=X[:, 0], y=X[:, 1], mode="lines+markers", line=dict(color=BLUE, width=2),
                             marker=dict(size=10, color=BLUE)))
    rd.robot(fig, *tk.GOAL[:3], "#BBBBBB", width=2, fill="rgba(0,0,0,0)")
    lines = [f"<b>iteration {i}</b>", f"largest defect: {d.max():.3f} m",
             f"start misses by {np.hypot(*(X[0, :2] - tk.START[:2])):.3f} m",
             f"end misses by {np.hypot(*(X[-1, :2] - tk.GOAL[:2])):.3f} m"]
    fig.add_annotation(x=1.35, y=3.85, text="<br>".join(lines), showarrow=False, xanchor="left", yanchor="top",
                       align="left", font=dict(size=21), bgcolor="rgba(255,255,255,0.9)")
    rd.axes(fig)
    fig.update_layout(template="simple_white", font=FONT, width=760, height=1000, showlegend=False,
                      title=dict(text="direct collocation, 31 knot points", x=0.5, font_size=22),
                      margin=dict(l=10, r=10, t=50, b=10))
    return fig, d.max()


n = len(sol["hist"])
ks = sorted(set(list(range(min(n, 12))) + list(range(12, n, max(1, (n - 12) // 10))) + [n - 1]))
out = [frame(i) for i in ks]
assert out[-1][1] < 1e-3 and round(out[0][1], 3) == 0.218
print("first largest defect", round(out[0][1], 3), "iterations", n - 1)
make_gif([o[0] for o in out], here / "colloc", fps=3, holds=[4] + [2] * (len(out) - 2) + [12],
         keys=[0, 1, 3, len(out) - 1], cols=2, width=560)
