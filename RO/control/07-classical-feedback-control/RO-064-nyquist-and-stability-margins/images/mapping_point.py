"""One point mapped through the heading loop's L(s) = 0.8 (s + 5)/s^2. Left, the s-plane: the zero of L at -5 (circle),
its double pole at 0 (cross) and the point s = -1 + j, with the arrows from the zero and from the pole to s. Right, the
w-plane: L(-1 + j) = -0.4 + 1.6j. Lengths: 0.8 x 4.123 / 1.414^2 = 1.649; angles: 14.0 - 2 x 135.0 = -256.0 degrees,
the same direction as 104.0 degrees. Run: python mapping_point.py -> mapping_point.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, RED
from loopkit import L_head

here = Path(__file__).parent
s = -1 + 1j
w = L_head(s)
lz, az = abs(s + 5), np.degrees(np.angle(s + 5))
lp, ap = abs(s), np.degrees(np.angle(s))
assert abs(w - (-0.4 + 1.6j)) < 1e-12
assert abs(lz - 4.123) < 5e-4 and abs(lp - 1.414) < 5e-4 and abs(0.8 * lz / lp ** 2 - 1.649) < 5e-4
assert abs(az - 14.0) < 0.05 and abs(ap - 135.0) < 0.05 and abs(np.degrees(np.angle(w)) - 104.0) < 0.05
assert abs(abs(w) - 1.649) < 5e-4

fig = make_subplots(rows=1, cols=2, column_widths=[0.62, 0.38], horizontal_spacing=0.08,
                    subplot_titles=["s-plane: the point s = −1 + j", "w-plane: L(s) = −0.4 + 1.6j"])
for c, (x0, x1, y0, y1) in [(1, (-5.6, 1.9, -0.8, 2.0)), (2, (-1.2, 1.0, -0.8, 2.0))]:
    fig.add_trace(go.Scatter(x=[x0, x1], y=[0, 0], mode="lines", line=dict(color=GREY, width=1)), 1, c)
    fig.add_trace(go.Scatter(x=[0, 0], y=[y0, y1], mode="lines", line=dict(color=GREY, width=1)), 1, c)
fig.add_trace(go.Scatter(x=[-5], y=[0], mode="markers", marker=dict(symbol="circle-open", size=18, color=GREEN,
                                                                      line=dict(width=3))), 1, 1)
fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers", marker=dict(symbol="x", size=18, color=ORANGE)), 1, 1)
for (x0, y0), col in [((-5, 0), GREEN), ((0, 0), ORANGE)]:
    fig.add_trace(go.Scatter(x=[x0, s.real], y=[y0, s.imag], mode="lines+markers", line=dict(color=col, width=4),
                             marker=dict(symbol="arrow", size=[0, 16], angleref="previous", color=col)), 1, 1)
fig.add_trace(go.Scatter(x=[s.real], y=[s.imag], mode="markers", marker=dict(size=14, color=BLUE)), 1, 1)
fig.add_annotation(x=-5, y=0, text="zero at −5", showarrow=False, yshift=-26, font=dict(color=GREEN, size=19), row=1,
                   col=1)
fig.add_annotation(x=0, y=0, text="double pole at 0", showarrow=False, yshift=-26, xanchor="left", xshift=-30,
                   font=dict(color=ORANGE, size=19), row=1, col=1)
fig.add_annotation(x=-3.4, y=1.05, text=f"length {lz:.3f}, angle {az:.1f}°", showarrow=False,
                   font=dict(color=GREEN, size=19), row=1, col=1)
fig.add_annotation(x=0.12, y=0.8, text=f"length {lp:.3f},<br>angle {ap:.1f}°<br>(twice)", showarrow=False,
                   xanchor="left", font=dict(color=ORANGE, size=19), row=1, col=1)
fig.add_annotation(x=s.real, y=s.imag, text="s = −1 + j", showarrow=False, yshift=22, xshift=-30,
                   font=dict(color=BLUE, size=19), row=1, col=1)
fig.add_trace(go.Scatter(x=[0, w.real], y=[0, w.imag], mode="lines+markers", line=dict(color=BLUE, width=4),
                         marker=dict(symbol="arrow", size=[0, 16], angleref="previous", color=BLUE)), 1, 2)
fig.add_annotation(x=w.real, y=w.imag, text="−0.4 + 1.6j", showarrow=False, yshift=20, font=dict(color=BLUE, size=19),
                   row=1, col=2)
fig.add_annotation(x=0.05, y=0.55, text="length 1.649<br>angle 104.0°", showarrow=False, xanchor="left",
                   font=dict(color=BLUE, size=19), row=1, col=2)
fig.update_xaxes(range=[-5.6, 1.9], title="real part", row=1, col=1)
fig.update_yaxes(range=[-0.8, 2.0], title="imaginary part", scaleanchor="x", scaleratio=1, row=1, col=1)
fig.update_xaxes(range=[-1.2, 1.0], title="real part", row=1, col=2)
fig.update_yaxes(range=[-0.8, 2.0], scaleanchor="x2", scaleratio=1, row=1, col=2)
fig.update_layout(template="simple_white", font=FONT, width=1150, height=520, showlegend=False,
                  margin=dict(l=80, r=30, t=70, b=70))
fig.update_annotations(selector=dict(xref="paper"), font_size=21)
fig.write_image(here / "mapping_point.png", scale=1)
