"""Animation: the map cells one move sweeps, worked out once. The car drives the 90 deg left turn from (12, 3) facing
0 deg, the move the lattice path takes round the end of the middle row; each frame adds the 0.1 m map cells its body
(grown by 0.1 m) has passed over so far (blue). Grey: map cells inside parked cars; green: the body. Last frame: all
3260 swept cells; none is grey, so the move is free, and checking it during the search is a look-up of this list.
Run -> swath_anim.gif, swath_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from carkit import body_corners
from gifkit import BLUE, GREEN, make_gif
from latticekit import CONTROL, OCC, RES, SWATH, body_cells, move_poses, swath_free
from lotdraw import FONT

here = Path(__file__).parent
K = next(i for i, m in enumerate(CONTROL[0]) if m["name"] == "left 90" and m["d"] > 0)
SW = SWATH[(0, K)]
X0, Y0 = 12, 3
SHIFT = (int(round(X0 / RES)), int(round(Y0 / RES)))
assert swath_free(X0, Y0, 0, K) and len(SW) == 3260
REL = move_poses(0, 0, 0, CONTROL[0][K], ds=0.05)                  # the same poses the swath was built from
ABS = REL + np.array([X0, Y0, 0.0])
cum, sofar = [], set()
for p in REL:
    sofar |= body_cells(tuple(p))
    cum.append(np.array(sorted(sofar)))
assert len(cum[-1]) == len(SW) and set(map(tuple, cum[-1].tolist())) == set(map(tuple, SW.tolist()))
jj, ii = np.nonzero(OCC)
keep = (ii * RES > 9) & (ii * RES < 21) & (jj * RES > 0) & (jj * RES < 13)
assert not any(OCC[j + SHIFT[1], i + SHIFT[0]] for i, j in SW.tolist())   # no swept cell is occupied


def frame(n, final=False):
    cells = cum[n] + np.array(SHIFT)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=(ii[keep] + 0.5) * RES, y=(jj[keep] + 0.5) * RES, mode="markers",
                             marker=dict(color="#9A9A9A", size=3, symbol="square"), hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=(cells[:, 0] + 0.5) * RES, y=(cells[:, 1] + 0.5) * RES, mode="markers",
                             marker=dict(color="rgba(76,120,168,0.55)", size=3, symbol="square"), hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=ABS[: n + 1, 0], y=ABS[: n + 1, 1], mode="lines", line=dict(color="black", width=3),
                             hoverinfo="skip"))
    cs = body_corners(tuple(ABS[n]))
    xs, ys = zip(*(cs + [cs[0]]))
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=GREEN, width=3), hoverinfo="skip"))
    if final:
        title, sub = f"the cells one move sweeps: {len(SW)} cells of 0.1 m", "no blue cell is grey: the move is free"
    else:
        title = f"the cells one move sweeps: {len(cells)} so far"
        sub = "90 deg left turn from (12, 3): blue swept cells, grey parked cars, green body"
    fig.update_layout(template="simple_white", width=820, height=820, showlegend=False, font=FONT,
                      title=dict(text=title, x=0.5, xanchor="center", font_size=22),
                      margin=dict(l=30, r=30, t=110, b=30))
    fig.add_annotation(x=0.5, y=1.03, xref="paper", yref="paper", showarrow=False, font=dict(size=18), text=sub)
    fig.update_xaxes(range=[9.5, 20.5], showgrid=False, zeroline=False, tickvals=[10, 12, 14, 16, 18, 20],
                     tickfont=dict(size=15))
    fig.update_yaxes(range=[0, 12.5], showgrid=False, zeroline=False, scaleanchor="x", tickvals=[0, 4, 8, 12],
                     tickfont=dict(size=15))
    return fig


IDX = [int(round(v)) for v in np.linspace(0, len(REL) - 1, 13)]
figs = [frame(n) for n in IDX] + [frame(IDX[-1], final=True)]
holds = [6] + [2] * (len(IDX) - 1) + [24]
make_gif(figs, here / "swath_anim", fps=4, holds=holds, keys=[0, 4, 8, len(figs) - 1], cols=2, width=700)
