"""Figure: self-collision of a planar arm with three links, 1.0 m, 0.8 m and 0.6 m long, drawn as line segments.
Links 1 and 2, and links 2 and 3, share a joint and always touch there, so only links 1 and 3 are checked.
Left: joint angles (0, 90, 90) degrees, free. Right: (0, 150, 150) degrees, link 3 folds back across link 1.
Run -> arm.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from shapely.geometry import LineString

import collide as k
import drawkit as dk
from gifkit import BLUE, GREEN, ORANGE, PURPLE, RED

here = Path(__file__).parent
CFG = [(0, 90, 90), (0, 150, 150)]
assert not k.self_collides(np.radians(CFG[0])) and k.self_collides(np.radians(CFG[1]))
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.06,
                    subplot_titles=["joint angles (0°, 90°, 90°): free", "joint angles (0°, 150°, 150°): self-collision"])
for col, th in enumerate(CFG, 1):
    p = k.arm(np.radians(th))
    for i, lc in enumerate([BLUE, ORANGE, PURPLE]):
        fig.add_trace(go.Scatter(x=[p[i][0], p[i + 1][0]], y=[p[i][1], p[i + 1][1]], mode="lines",
                                 line=dict(color=lc, width=9), hoverinfo="skip"), row=1, col=col)
        mx, my = [[(0.5, -0.13), (1.15, 0.4), (0.7, 0.92)], [(0.25, -0.13), (0.82, 0.32), (0.22, 0.12)]][col - 1][i]
        fig.add_annotation(x=mx, y=my, text=f"link {i + 1}", showarrow=False, font=dict(size=18, color=lc),
                           row=1, col=col)
    fig.add_trace(go.Scatter(x=[q[0] for q in p[:3]], y=[q[1] for q in p[:3]], mode="markers",
                             marker=dict(size=14, color="black"), hoverinfo="skip"), row=1, col=col)
    fig.add_trace(go.Scatter(x=[-0.12, 0.12, 0.12, -0.12, -0.12], y=[-0.12, -0.12, 0, 0, -0.12], fill="toself",
                             mode="lines", fillcolor="#888888", line=dict(color="#888888"), hoverinfo="skip"),
                  row=1, col=col)
    hit = LineString(p[:2]).intersection(LineString(p[2:]))
    if not hit.is_empty:
        dk.point(fig, hit.x, hit.y, RED, None, size=16, row=1, col=col)
        fig.add_annotation(x=hit.x, y=-0.35, text=f"links 1 and 3 cross at ({hit.x:.2f}, 0)", showarrow=False,
                           font=dict(size=17, color=RED), row=1, col=col)
    else:
        fig.add_annotation(x=0.5, y=-0.35, text="links 1 and 3 do not meet", showarrow=False,
                           font=dict(size=17, color=GREEN), row=1, col=col)
    fig.update_xaxes(range=[-0.4, 1.4], dtick=0.5, title="x (m)", row=1, col=col)
    fig.update_yaxes(range=[-0.55, 1.1], dtick=0.5, scaleanchor="x" if col == 1 else "x2", row=1, col=col)
fig.update_yaxes(title="y (m)", row=1, col=1)
dk.layout(fig, 1250, 560, margin=dict(l=70, r=20, t=60, b=60))
fig.update_annotations(font_size=20, selector=dict(text="joint angles (0°, 90°, 90°): free"))
fig.update_annotations(font_size=20, selector=dict(text="joint angles (0°, 150°, 150°): self-collision"))
fig.write_image(here / "arm.png")
