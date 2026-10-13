"""Animation: the global costmap of the main run at 3.0 s, built layer by layer (our Python version of Nav2's
costmaps, written from nav2_costmap_2d and the bring-up parameters; not Nav2 running). 1. static layer: the map's
occupied cells; 2. obstacle layer: cells where laser beams ended within 2.5 m, the person (seen from 2.4 s) among
them; 3. inflation layer: 253 within the robot's radius 0.25 m, then 252 exp(-3 (d - 0.25)) out to 0.70 m (65);
4. the master costmap with NavFn's plans, 3.26 m at 0 s and 2.986 m at 3.0 s; 5. the local costmap at 3.0 s, a
3 m x 3 m window of laser cells round the robot in the odom frame.
Run -> costmap_layers.gif, costmap_layers_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

import navdraw as nd
import nav2sim as N
from gifkit import BLUE, GREY, RED, make_gif

here = Path(__file__).parent
R = N.results()
m = R["main"]
snap = {round(x["t"], 2): x for x in m["log"] if x["gcm"] is not None}
s3 = snap[3.0]
gcost, glethal = s3["gcm"]
occ = m["occ"]
marks = glethal & ~occ
P0, P1 = m["plans"][0][1], m["plans"][1][1]
assert round(N.D.path_length(P0), 3) == 3.26 and round(N.D.path_length(P1), 3) == 2.986 and m["plans"][1][0] == 3.0
assert (gcost == N.LETHAL).any() and (gcost == N.INSCRIBED).any()


def base(title, sub):
    fig = go.Figure()
    fig.add_annotation(x=0.5, y=1.0, xref="paper", yref="paper", text=sub, showarrow=False,
                       font=dict(size=17, color=GREY), yanchor="bottom")
    nd.layout(fig, 900, 900, title, margin=dict(l=20, r=20, t=110, b=20))
    return fig


figs, holds = [], []
f = base("1. static layer: the map", "black: the map's occupied cells (0.05 m)")
nd.lethal_cells(f, occ, N.OX, N.OY)
nd.view(f)
f.update_yaxes(scaleanchor="x")
figs.append(f)
holds.append(8)

f = base("2. obstacle layer: what the laser sees", "red: cells where a beam ended within 2.5 m (scan at 3.0 s); the person seen from 2.4 s")
nd.lethal_cells(f, occ, N.OX, N.OY)
nd.lethal_cells(f, marks, N.OX, N.OY, color=RED)
nd.robot(f, s3["map"], BLUE)
nd.view(f)
f.update_yaxes(scaleanchor="x")
figs.append(f)
holds.append(8)

f = base("3. inflation layer: cost round every obstacle cell", "purple 253 within 0.25 m (the robot's radius); orange 216 at 0.30 m to pale 65 at 0.70 m")
nd.cost_cells(f, gcost, N.OX, N.OY)
nd.robot(f, s3["map"], BLUE)
nd.view(f)
f.update_yaxes(scaleanchor="x")
figs.append(f)
holds.append(10)

f = base("4. the master costmap and NavFn's plans", "dashed: the plan at 0 s, 3.26 m, through the person; blue: the plan at 3.0 s, 2.986 m")
nd.cost_cells(f, gcost, N.OX, N.OY)
nd.plan(f, P0, GREY, 3, "dash")
nd.plan(f, P1, BLUE, 4)
nd.robot(f, s3["map"], BLUE)
nd.goal(f)
nd.view(f)
f.update_yaxes(scaleanchor="x")
figs.append(f)
holds.append(12)

lc, lox, loy, ll = s3["lcm"]
f = base("5. the local costmap at 3.0 s (odom frame)", "3 m x 3 m round the robot, laser cells and inflation only: no static layer")
nd.cost_cells(f, lc, lox, loy)
o = s3["odom"]
f.add_trace(go.Scatter(x=[lox, lox + 3, lox + 3, lox, lox], y=[loy, loy, loy + 3, loy + 3, loy], mode="lines",
                       line=dict(color=GREY, width=2, dash="dot"), hoverinfo="skip"))
nd.robot(f, o, BLUE)
nd.view(f)
f.update_yaxes(scaleanchor="x")
figs.append(f)
holds.append(16)
make_gif(figs, here / "costmap_layers", fps=2, holds=holds, keys=[0, 1, 2, 3, 4], cols=3, width=800)
