"""Single shooting with one number, on the straight drive: speed up at a for 5 s, brake at a for 5 s, and the
robot ends 25 a metres along. Each frame fires one shot (blue: position over time), measures the miss at 10 s
against the target 3.0 m (dashed), and moves a against the slope of the squared miss (gradient descent, step
0.0006). a: 0, 0.09, 0.1125, 0.1181, 0.1195; the miss shrinks to a quarter each step: 3.0, 0.75, 0.1875,
0.0469, 0.0117 m. Run -> straight_shoot.gif, straight_shoot_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import trajkit as tk
from gifkit import BLUE, FONT, GREY, RED, make_gif

here = Path(__file__).parent
steps = tk.straight_gd(steps=5)
assert [round(a, 4) for a, *_ in steps] == [0.0, 0.09, 0.1125, 0.1181, 0.1195]
assert [round(abs(m), 4) for _, _, m, _ in steps] == [3.0, 0.75, 0.1875, 0.0469, 0.0117]
t = np.linspace(0, 10, 201)


def pos(a):
    return np.where(t <= 5, a * t * t / 2, a * 12.5 + 5 * a * (t - 5) - a * (t - 5) ** 2 / 2)


def frame(k):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[0, 10.4], y=[3, 3], mode="lines", line=dict(color=GREY, dash="dash", width=2)))
    fig.add_annotation(x=0.2, y=3.12, text="target: 3.0 m at 10 s", showarrow=False, xanchor="left",
                       font=dict(size=19, color=GREY))
    for j in range(k):
        fig.add_trace(go.Scatter(x=t, y=pos(steps[j][0]), mode="lines", line=dict(color="#C9D6E8", width=2)))
    a, end, miss, grad = steps[k]
    fig.add_trace(go.Scatter(x=t, y=pos(a), mode="lines", line=dict(color=BLUE, width=4)))
    fig.add_trace(go.Scatter(x=[10, 10], y=[end, 3], mode="lines", line=dict(color=RED, width=4)))
    nxt = a - 0.0006 * grad
    txt = [f"<b>shot {k + 1}</b>: a = {a:.4f} m/s²", f"ends at 25 × a = {end:.4f} m",
           f"miss = {end:.4f} − 3 = {miss:.4f} m", f"slope of miss²: 50 × miss = {grad:.2f}",
           f"next a = {a:.4f} − 0.0006 × ({grad:.2f}) = {nxt:.4f}"]
    fig.add_annotation(x=0.2, y=2.85, text="<br>".join(txt), showarrow=False, xanchor="left", yanchor="top",
                       align="left", font=dict(size=19), bgcolor="rgba(255,255,255,0.9)")
    fig.update_xaxes(title="time (s)", range=[0, 10.4])
    fig.update_yaxes(title="distance along the line (m)", range=[-0.1, 3.4])
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=640, showlegend=False,
                      margin=dict(l=80, r=20, t=20, b=60))
    return fig


figs = [frame(k) for k in range(5)]
make_gif(figs, here / "straight_shoot", fps=1, holds=[4, 4, 4, 4, 10], keys=[0, 1, 2, 4], cols=2, width=800)
