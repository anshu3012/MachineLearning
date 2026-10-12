"""The opening problem and its fix, one frame per 0.5 s: the car starts 1.0 m left of the course at 2 m/s and steers by
RO-070's line rule, turn rate -0.5 e - 2 th_e from its two errors (red). It gets within 0.1 m after 7.7 m but slides
outside the arc: 0.354 m out at the arc's middle and 0.384 m at its end, the steady 0.385 m worked out by hand. The
same rule plus the turn the curve needs, v kappa, which is the steering atan(L kappa) = 14.04 degrees (purple), is
0.001 m off at the arc's middle.
Run: python opening.py -> opening.gif, opening_frames.png"""
from functools import partial
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import ffkit as fk
import trackkit as tk
from cardraw import car_traces, course_trace
from gifkit import FONT, GREY, PURPLE, RED, make_gif

here = Path(__file__).parent
fb = tk.simulate(partial(fk.line_rule, ff=False), v=tk.V_BASE)
ff = tk.simulate(partial(fk.line_rule, ff=True), v=tk.V_BASE)
m_fb, m_ff = tk.metrics(fb), tk.metrics(ff)
end_fb = fb["e"][np.argmin(np.abs(fb["s"] - tk.S2))]
assert abs(m_fb["reach"] - 7.72) < 0.01 and abs(m_fb["arc_mid"] + 0.354) < 5e-4 and abs(end_fb + 0.384) < 5e-4
assert abs(m_ff["arc_mid"] - 0.001) < 5e-4 and abs(fk.steady_offset() + 0.385) < 5e-4


def frame(i):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.66, 0.34], vertical_spacing=0.09)
    fig.add_trace(course_trace(), row=1, col=1)
    j = i + 1
    for r, col, name in ((fb, RED, "line rule: turn from the errors only"), (ff, PURPLE, "line rule plus the curve's turn")):
        k = min(i, len(r["t"]) - 1)
        fig.add_trace(go.Scatter(x=r["x"][:k + 1], y=r["y"][:k + 1], mode="lines", line=dict(color=col, width=3),
                                 showlegend=False), row=1, col=1)
        for t in car_traces(r["x"][k], r["y"][k], r["th"][k], r["delta"][k], col):
            fig.add_trace(t, row=1, col=1)
        fig.add_trace(go.Scatter(x=r["s"][:k + 1], y=r["e"][:k + 1], mode="lines", line=dict(color=col, width=4),
                                 name=name), row=2, col=1)
    for s0 in (tk.S1, tk.S2):
        fig.add_vline(x=s0, line=dict(color=GREY, dash="dot", width=1.5), row=2, col=1)
    fig.add_annotation(x=(tk.S1 + tk.S2) / 2, y=1.15, text="arc", showarrow=False, font=dict(size=18, color=GREY),
                       row=2, col=1)
    fig.add_hline(y=0, line=dict(color="black", width=1), row=2, col=1)
    k, k2 = min(i, len(fb["t"]) - 1), min(i, len(ff["t"]) - 1)
    small = "<span style='font-size:19px'>"
    same = " (one path until the arc)" if fb["s"][k] < tk.S1 else ""
    title = (f"t = {fb['t'][k]:.1f} s, course distance {fb['s'][k]:.1f} m{same}<br>{small}lateral error (+ = left): "
             f"errors only {fb['e'][k]:+.3f} m, plus the curve's turn {ff['e'][k2]:+.3f} m</span>")
    fig.update_layout(template="simple_white", font=FONT, width=900, height=1150, margin=dict(l=90, r=30, t=120, b=70),
                      title=dict(x=0.5, y=0.975, yanchor="top", text=title),
                      legend=dict(x=0.02, y=0.985, font=dict(size=18), bgcolor="rgba(255,255,255,0.85)"))
    fig.update_xaxes(title_text="x (m)", range=[-2, 24], dtick=5, row=1, col=1)
    fig.update_yaxes(title_text="y (m)", range=[-3, 24], dtick=5, scaleanchor="x", scaleratio=1, row=1, col=1)
    fig.update_xaxes(title_text="distance along the course (m)", range=[0, 36.5], dtick=5, row=2, col=1)
    fig.update_yaxes(title_text="lateral error (m)", range=[-0.8, 1.3], dtick=0.5, row=2, col=1)
    return fig


n = max(len(fb["t"]), len(ff["t"]))
idx = list(range(0, n, 50)) + [n - 1]
k_mid = int(np.argmin(np.abs(np.array([fb["s"][i] for i in idx]) - tk.S_MID)))
make_gif([frame(i) for i in idx], here / "opening", fps=4, holds=[6] + [1] * (len(idx) - 2) + [16],
         keys=[0, 9, k_mid, len(idx) - 1], cols=2, width=850)
