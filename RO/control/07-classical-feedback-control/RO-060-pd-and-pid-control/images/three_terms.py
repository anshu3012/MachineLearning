"""Past, present and future of the error (after FBS Fig. 1.15), on the PID run with the dragging gearbox, at t = 1 s.
Present: the error now, 0.467 rad; the P part is 0.2 x 0.467 = 0.0934 N m. Past: the shaded area under the error
curve so far, the running sum 0.662 rad s; the I part is 0.05 x 0.662 = 0.0331 N m. Future: the slope of the error
now, -0.4056 rad/s (the line extends it 0.5 s ahead); the D part is 0.283 x -0.4056 = -0.1148 N m.
Run -> three_terms.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

import headkit as h
from gifkit import FONT, GREEN, GREY, PURPLE, RED

here = Path(__file__).parent
A = h.run(4, kd=h.KD, ki=h.KI, tau_d=h.TAU_DRAG)
k = int(round(1.0 / h.DT))
e, s, de = A["e"][k], A["integ"][k], A["de"][k]
assert round(e, 3) == 0.467 and round(s, 3) == 0.662
assert abs(round(A["p"][k], 4) - 0.0934) < 1e-9 and abs(round(A["i"][k], 4) - 0.0331) < 1e-9
assert abs(round(A["d"][k], 4) + 0.1148) < 1e-9 and abs(round(de, 4) + 0.4056) < 1e-9

fig = go.Figure()
fig.add_trace(go.Scatter(x=A["t"][:k + 1], y=A["e"][:k + 1], mode="lines", fill="tozeroy",
                         fillcolor="rgba(84,162,75,0.3)", line=dict(width=0), name="past: area so far → I"))
fig.add_trace(go.Scatter(x=A["t"], y=A["e"], mode="lines", line=dict(color="black", width=4), name="error e = 45° − θ (in rad)"))
fig.add_trace(go.Scatter(x=[1.0, 1.5], y=[e, e + 0.5 * de], mode="lines", line=dict(color=PURPLE, width=5, dash="dash"),
                         name="future: slope now → D"))
fig.add_trace(go.Scatter(x=[1.0], y=[e], mode="markers", marker=dict(color=RED, size=18), name="present: value now → P"))
fig.add_annotation(x=1.0, y=e, text=f"now: e = {e:.3f} rad<br>P = 0.2 × {e:.3f} = {A['p'][k]:.4f} N m", ax=80, ay=-60,
                   arrowhead=2, xanchor="left", font=dict(size=19, color=RED), bgcolor="rgba(255,255,255,0.85)")
fig.add_annotation(x=0.6, y=0.25, ax=1.1, ay=-0.1, axref="x", ayref="y", xanchor="left", arrowhead=2,
                   text=f"area = {s:.3f} rad s<br>I = 0.05 × {s:.3f} = {A['i'][k]:.4f} N m",
                   font=dict(size=19, color=GREEN), bgcolor="rgba(255,255,255,0.85)")
fig.add_annotation(x=1.5, y=e + 0.5 * de, text=f"slope = {de:.4f} rad/s<br>D = 0.283 × ({de:.4f}) = {A['d'][k]:.4f} N m",
                   ax=2.2, ay=0.45, axref="x", ayref="y", arrowhead=2, xanchor="left", font=dict(size=19, color=PURPLE),
                   bgcolor="rgba(255,255,255,0.85)")
fig.add_vline(x=1.0, line=dict(color=GREY, width=1.5, dash="dot"))
fig.update_xaxes(range=[0, 4], dtick=0.5, title="time after the corner (s)")
fig.update_yaxes(range=[-0.2, 0.9], dtick=0.1, title="error (rad)")
fig.update_layout(template="simple_white", font=FONT, width=1000, height=640, margin=dict(l=90, r=30, t=50, b=70),
                  legend=dict(x=0.55, y=0.99, font=dict(size=18), bgcolor="rgba(255,255,255,0.85)"))
fig.write_image(here / "three_terms.png", scale=2)
