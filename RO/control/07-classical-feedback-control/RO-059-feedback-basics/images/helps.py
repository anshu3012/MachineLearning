"""Why feedback helps, at steady state. Left: the settled speed against the ramp's pull d (from a 2 percent slope down,
-1.57 N, to a 2 percent slope up, +1.57 N). Right: the settled speed against the true rolling drag b, while the
controller still assumes 2 N per m/s. Open loop (red) follows every change; closed loop (blue) barely moves.
Marked: the ramp (0.108 against 0.464 m/s) and the carpet (0.333 against 0.478 m/s). Run -> helps.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import speedkit as s
from gifkit import BLUE, FONT, GREY, RED

here = Path(__file__).parent
d = np.linspace(-2 * s.D_RAMP, 2 * s.D_RAMP, 201)
b = np.linspace(1.0, 4.0, 201)
assert round(s.steady_closed(d=s.D_RAMP), 3) == 0.464 and round(s.steady_closed(b=s.B_CARPET), 3) == 0.478
assert round(s.steady_open(d=s.D_RAMP), 3) == 0.108 and round(s.steady_open(b=s.B_CARPET), 3) == 0.333

fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
                    subplot_titles=["a disturbance: the ramp's pull", "a wrong model: the true drag"])
for col, x, yo, yc in ((1, d, s.steady_open(d=d), s.steady_closed(d=d)),
                       (2, b, s.steady_open(b=b), s.steady_closed(b=b))):
    fig.add_trace(go.Scatter(x=x, y=yo, mode="lines", line=dict(color=RED, width=4, dash="dash"),
                             name="open loop", showlegend=col == 1), row=1, col=col)
    fig.add_trace(go.Scatter(x=x, y=yc, mode="lines", line=dict(color=BLUE, width=4),
                             name="closed loop", showlegend=col == 1), row=1, col=col)
    fig.add_hline(y=0.5, line=dict(color=GREY, width=1.5, dash="dot"), row=1, col=col)
marks = [(1, s.D_RAMP, s.steady_open(d=s.D_RAMP), RED, "0.108"), (1, s.D_RAMP, s.steady_closed(d=s.D_RAMP), BLUE, "0.464"),
         (2, s.B_CARPET, s.steady_open(b=s.B_CARPET), RED, "0.333"),
         (2, s.B_CARPET, s.steady_closed(b=s.B_CARPET), BLUE, "0.478")]
for col, x, y, c, txt in marks:
    fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers", marker=dict(color=c, size=14), showlegend=False),
                  row=1, col=col)
    left = col == 1 and c == RED                      # keep the label off the steep open-loop line
    fig.add_annotation(x=x, y=y, text=txt, showarrow=False, xanchor="right" if left else "left",
                       xshift=-16 if left else 16, yshift=-30 if c == RED else 18,
                       font=dict(size=19, color=c), row=1, col=col)
fig.add_annotation(x=s.D_RAMP, y=1.18, text="our ramp", showarrow=False, font=dict(size=17, color=GREY), row=1, col=1)
fig.add_annotation(x=s.B_CARPET, y=1.18, text="carpet", showarrow=False, font=dict(size=17, color=GREY), row=1, col=2)
fig.add_annotation(x=s.B, y=1.18, text="hard floor", showarrow=False, font=dict(size=17, color=GREY), row=1, col=2)
for col, x in ((1, s.D_RAMP), (2, s.B_CARPET), (2, s.B)):
    fig.add_vline(x=x, line=dict(color=GREY, width=1.5, dash="dash"), row=1, col=col)
fig.update_xaxes(title="ramp's pull d (N)", range=[-1.65, 1.65], dtick=0.785, tickformat=".3f", row=1, col=1)
fig.update_xaxes(title="true drag b (N per m/s)", range=[0.9, 4.1], dtick=1, row=1, col=2)
fig.update_yaxes(title="speed it settles at (m/s)", range=[-0.35, 1.3], dtick=0.25, row=1, col=1)
fig.update_yaxes(range=[-0.35, 1.3], dtick=0.25, row=1, col=2)
fig.update_layout(template="simple_white", font=FONT, width=1300, height=620, margin=dict(l=90, r=30, t=70, b=80),
                  legend=dict(x=0.01, y=0.02, yanchor="bottom", font=dict(size=18), bgcolor="rgba(255,255,255,0.85)"))
fig.update_annotations(selector=dict(text="a disturbance: the ramp's pull"), font_size=21)
fig.update_annotations(selector=dict(text="a wrong model: the true drag"), font_size=21)
fig.write_image(here / "helps.png", scale=2)
