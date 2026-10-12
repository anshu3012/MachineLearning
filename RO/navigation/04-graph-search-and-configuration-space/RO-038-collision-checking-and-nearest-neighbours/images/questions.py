"""Figure 1: the three questions a planner asks. Left, the room: is the configuration with centre (3.5, 3.2) free
(no: 0.2 m from the table)? Is the straight segment from (2, 2) to (4, 3.6) free? Its ends and its middle are, but the
point (3.5, 3.2) on it is not. Right: which stored configuration is nearest to the query at x = 3.55 m, heading 350
degrees? The one at 15 degrees is 25 degrees away round the circle; plain subtraction says 335.
Run -> questions.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import collide as k
import cspace as c
import drawkit as dk
from gifkit import GREEN, GREY, ORANGE, RED

here = Path(__file__).parent
a, b = np.array([2.0, 2.0]), np.array([4.0, 3.6])
assert k.free(a) and k.free(b) and k.free((a + b) / 2) and not k.free(c.TEST)
fig = make_subplots(rows=1, cols=2, column_widths=[0.66, 0.34], horizontal_spacing=0.06,
                    subplot_titles=["is it free? is the segment free?", "which stored heading is nearest?"])
dk.room(fig, 1, 1)
fig.add_trace(go.Scatter(x=[a[0], b[0]], y=[a[1], b[1]], mode="lines", line=dict(color="black", width=3)),
              row=1, col=1)
for p, col in [(a, GREEN), (b, GREEN), ((a + b) / 2, GREEN), (np.array(c.TEST), RED)]:
    dk.point(fig, p[0], p[1], col, None, row=1, col=1, size=13)
dk.disk(fig, *c.TEST, 0.0, row=1, col=1, body=False, color=RED)
for txt, x, y, col, anc in [("a = (2, 2)", 1.85, 2.0, GREEN, "right"), ("b = (4, 3.6)", 4.15, 3.55, GREEN, "left"),
                            ("middle (3, 2.8)", 2.9, 2.95, GREEN, "right"), ("(3.5, 3.2): hits the table", 3.15, 3.55, RED, "right")]:
    fig.add_annotation(x=x, y=y, text=txt, xanchor=anc, showarrow=False, font=dict(size=17, color=col), bgcolor="white",
                       row=1, col=1)
# heading dial
t = np.linspace(0, 2 * np.pi, 200)
fig.add_trace(go.Scatter(x=np.cos(t), y=np.sin(t), mode="lines", line=dict(color=GREY, width=2)), row=1, col=2)
for deg, col, lab in [(350, RED, "query 350°"), (15, GREEN, "stored 15°"), (320, ORANGE, "stored 320°")]:
    r = np.radians(deg)
    fig.add_trace(go.Scatter(x=[0, np.cos(r)], y=[0, np.sin(r)], mode="lines+markers", line=dict(color=col, width=4),
                             marker=dict(size=[0, 12], color=col)), row=1, col=2)
    lx, ly = {350: (1.12, -0.32), 15: (1.12, 0.42), 320: (0.86, -0.88)}[deg]
    fig.add_annotation(x=lx, y=ly, text=lab, xanchor="left", showarrow=False, font=dict(size=17, color=col),
                       row=1, col=2)
arc = np.radians(np.linspace(350, 375, 30))
fig.add_trace(go.Scatter(x=0.6 * np.cos(arc), y=0.6 * np.sin(arc), mode="lines", line=dict(color=GREEN, width=5)),
              row=1, col=2)
arc = np.radians(np.linspace(15, 350, 120))
fig.add_trace(go.Scatter(x=0.35 * np.cos(arc), y=0.35 * np.sin(arc), mode="lines", line=dict(color=RED, width=2,
              dash="dot")), row=1, col=2)
fig.add_annotation(x=0.5, y=-1.45, text="round the circle: 25°; plain 350 − 15 = 335°", showarrow=False,
                   font=dict(size=17), row=1, col=2)
fig.update_xaxes(range=[-0.2, 7.2], dtick=1, title="x (m)", row=1, col=1)
fig.update_yaxes(range=[-0.2, 4.4], dtick=1, title="y (m)", scaleanchor="x", row=1, col=1)
fig.update_xaxes(range=[-1.3, 2.3], visible=False, row=1, col=2)
fig.add_annotation(x=1.08, y=0.0, text="0°", xanchor="left", showarrow=False, font=dict(size=15, color=GREY), row=1, col=2)
fig.update_yaxes(range=[-1.7, 1.6], visible=False, scaleanchor="x2", row=1, col=2)
dk.layout(fig, 1350, 560, margin=dict(l=70, r=20, t=60, b=60))
fig.update_annotations(font_size=20, selector=dict(text="is it free? is the segment free?"))
fig.update_annotations(font_size=20, selector=dict(text="which stored heading is nearest?"))
fig.write_image(here / "questions.png")
