"""Calculus reducing the error, as motion: gradient descent on an illustrative error curve E(w) = (w - 2)^2 + 1,
starting at w = 5 with step size 0.3. Each step moves w against the slope; the steps shrink as the slope flattens
near the minimum at w = 2. Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from anim import save_gif, FONT, BLUE, RED, GREEN

here = Path(__file__).parent
E = lambda w: (w - 2) ** 2 + 1
dE = lambda w: 2 * (w - 2)
ws = [5.0]
for _ in range(7):
    ws.append(ws[-1] - 0.3 * dE(ws[-1]))
assert all(E(a) > E(b) for a, b in zip(ws, ws[1:])) and abs(ws[-1] - 2) < 0.01
g = np.linspace(-0.5, 5.5, 200)


def frame(k):
    w = ws[k]
    fig = go.Figure()
    fig.add_scatter(x=g, y=E(g), mode="lines", line=dict(color=BLUE, width=4))
    fig.add_scatter(x=[2], y=[1], mode="markers", marker=dict(size=14, color=GREEN))
    fig.add_scatter(x=ws[:k + 1], y=[E(v) for v in ws[:k + 1]], mode="lines+markers",
                    line=dict(color="#bbbbbb", dash="dot"), marker=dict(size=9, color="#bbbbbb"))
    t = np.array([w - 0.8, w + 0.8])
    fig.add_scatter(x=t, y=E(w) + dE(w) * (t - w), mode="lines", line=dict(color=RED, width=3))
    fig.add_scatter(x=[w], y=[E(w)], mode="markers", marker=dict(size=16, color=RED))
    fig.update_layout(template="simple_white", width=1000, height=560, font=FONT, showlegend=False,
                      title=dict(text=f"step {k}: w = {w:.2f}, slope {dE(w):+.2f}, error {E(w):.2f}", x=0.5),
                      xaxis=dict(title="model setting w", range=[-0.5, 5.5]),
                      yaxis=dict(title="error E(w) (illustrative)", range=[0, 12]), margin=dict(l=80, r=30, t=80, b=70))
    return fig


if __name__ == "__main__":
    save_gif([frame(k) for k in range(len(ws))], "descent_steps", here, keys=[0, 1, 3, 7], fps=2,
             holds=[3] + [2] * (len(ws) - 2) + [6])
