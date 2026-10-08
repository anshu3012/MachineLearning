"""Correlation-based map matching on 0.1 m cells. Left: the global map (grey cells: cells that touch a wall or
the box) with the local map of scan 2 (red cells: cells holding an endpoint) placed at the best candidate.
Right: the correlation between the two maps as the candidate dx moves, with dy = 0.1 m and dtheta = 5 deg fixed.
Run -> map_match.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from fieldmodel import DX, MRES, MX, MY, POSE_2, corr, global_map, local_map, scan72
from gifkit import BLUE, FONT, GREY, RED

here = Path(__file__).parent
g = global_map()
z2 = scan72(POSE_2, 12)
r = [corr(g, local_map(z2, dx, 0.1, np.radians(5))) for dx in DX]
l = local_map(z2, 0.3, 0.1, np.radians(5))
fig = make_subplots(rows=1, cols=2, column_widths=[0.52, 0.48], horizontal_spacing=0.12,
                    subplot_titles=["global map (grey) and local map (red) at the best placement",
                                    "correlation as the placement slides along x"])
for (arr, col, op) in ((g, GREY, 0.55), (l, RED, 0.9)):
    jj, ii = np.nonzero(arr)
    fig.add_trace(go.Scatter(x=MX[ii], y=MY[jj], mode="markers", marker=dict(symbol="square", size=8, color=col, opacity=op)),
                  row=1, col=1)
fig.update_xaxes(title="x (m)", range=[-0.1, 5.1], dtick=1, row=1, col=1)
fig.update_yaxes(title="y (m)", range=[-0.1, 4.1], dtick=1, scaleanchor="x", row=1, col=1)
fig.add_trace(go.Scatter(x=DX, y=r, mode="lines+markers", line=dict(color=BLUE, width=3)), row=1, col=2)
k = int(np.argmax(r))
fig.add_annotation(x=DX[k], y=r[k], ax=40, ay=40, text=f"best: dx = {DX[k]:.2f} m, r = {r[k]:.3f}", font_size=18,
                   arrowwidth=2, row=1, col=2)
fig.update_xaxes(title="candidate dx (m)", range=[-0.12, 0.72], dtick=0.1, row=1, col=2)
fig.update_yaxes(title="correlation r", range=[0.4, 1.0], row=1, col=2)
fig.update_layout(template="simple_white", width=1250, height=560, font=FONT, showlegend=False,
                  margin=dict(l=70, r=20, t=60, b=70))
fig.update_annotations(selector=dict(yref="paper"), font_size=19)
fig.write_image(here / "map_match.png")
assert abs(DX[k] - 0.3) <= 0.05
