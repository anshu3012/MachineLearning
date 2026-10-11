"""Figure 11 as an animation: correlation-based map matching on 0.1 m cells. Left: the global map (grey cells: cells
that touch a wall or the box) and the local map of scan 2 (red cells: cells holding an endpoint), placed at a
candidate shift dx along x, with dy = 0.1 m and dtheta = 5 deg fixed. Right: the correlation r of the two maps,
drawn point by point as dx slides from -0.1 to 0.7 m in steps of 0.02 m: about 0.6 at both ends, a flat top of
0.86 to 0.875 between 0.24 and 0.36 m. The last frame keeps the best placement, dx = 0.28 m, r = 0.875.
local_map (fieldmodel.py) puts end points that fall beyond the map's edge into its edge cells (np.clip), and the
frames draw them there; a note under the map says so.
Run -> map_match_anim.gif"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from fieldmodel import DX, MX, MY, POSE_2, corr, global_map, local_map, scan72
from gifkit import BLUE, FONT, GREY, RED, make_gif

here = Path(__file__).parent
g = global_map()
z2 = scan72(POSE_2, 12)
R = np.array([corr(g, local_map(z2, dx, 0.1, np.radians(5))) for dx in DX])
K = int(np.argmax(R))


def frame(k, title, best=False):
    fig = make_subplots(rows=1, cols=2, column_widths=[0.52, 0.48], horizontal_spacing=0.12,
                        subplot_titles=["global map (grey) and local map (red)",
                                        "correlation r as the placement slides along x"])
    jj, ii = np.nonzero(g)
    fig.add_trace(go.Scatter(x=MX[ii], y=MY[jj], mode="markers",
                             marker=dict(symbol="square", size=8, color=GREY, opacity=0.55)), row=1, col=1)
    jj, ii = np.nonzero(local_map(z2, DX[k], 0.1, np.radians(5)))
    fig.add_trace(go.Scatter(x=MX[ii], y=MY[jj], mode="markers",
                             marker=dict(symbol="square", size=8, color=RED, opacity=0.9)), row=1, col=1)
    fig.update_xaxes(title="x (m)", range=[-0.1, 5.1], dtick=1, row=1, col=1)
    fig.update_yaxes(title="y (m)", range=[-0.1, 4.1], dtick=1, scaleanchor="x", row=1, col=1)
    upto = len(DX) if best else k + 1
    fig.add_trace(go.Scatter(x=DX[:upto], y=R[:upto], mode="lines+markers", line=dict(color=BLUE, width=3)),
                  row=1, col=2)
    fig.add_trace(go.Scatter(x=[DX[k]], y=[R[k]], mode="markers", marker=dict(color=RED, size=15),
                             cliponaxis=False), row=1, col=2)
    if best:
        fig.add_annotation(x=DX[k], y=R[k], ax=0, ay=-45, text=f"best: dx = {DX[k]:.2f} m, r = {R[k]:.3f}",
                           font_size=18, arrowwidth=2, row=1, col=2)
    fig.update_xaxes(title="candidate dx (m)", range=[-0.12, 0.72], dtick=0.1, row=1, col=2)
    fig.update_yaxes(title="correlation r", range=[0.4, 1.0], row=1, col=2)
    fig.add_annotation(x=0.23, y=-0.25, xref="paper", yref="paper", showarrow=False, font=dict(color=GREY, size=17),
                       text="end points that fall beyond the map's edge are counted in its edge cells")
    fig.update_layout(template="simple_white", width=1250, height=670, font=FONT, showlegend=False,
                      margin=dict(l=70, r=20, t=130, b=105), title=dict(text=title, x=0.5, font_size=21))
    fig.update_annotations(selector=dict(yref="paper"), font_size=19)
    return fig


def title(k):
    return (f"local map shifted by dx = {DX[k]:.2f} m".replace("-", "−") + f" (dy = 0.1 m and dθ = 5° fixed)<br>"
            f"correlation with the global map: r = {R[k]:.3f}")


figs = [frame(k, title(k)) for k in range(len(DX))]
holds = [6] + [1] * (len(DX) - 2) + [3]
figs.append(frame(K, f"keep the best placement: dx = {DX[K]:.2f} m, r = {R[K]:.3f}<br>"
                     "the flat top from 0.24 to 0.36 m: 0.1 m cells cannot tell these shifts apart", best=True))
holds.append(24)
make_gif(figs, here / "map_match_anim", fps=5, holds=holds, keys=[0, len(figs) - 1], cols=2, width=950)

# the numbers the Note quotes (Section 6.4)
assert round(DX[K], 2) == 0.28 and round(R[K], 3) == 0.875
top = (DX >= 0.24 - 1e-9) & (DX <= 0.36 + 1e-9)
assert R[top].min() >= 0.86 and R[~top].max() < 0.85                       # flat top 0.86 to 0.875 at 0.24 to 0.36 m
assert abs(R[0] - 0.6) < 0.03 and abs(R[-1] - 0.6) < 0.04                   # about 0.6 at both ends
