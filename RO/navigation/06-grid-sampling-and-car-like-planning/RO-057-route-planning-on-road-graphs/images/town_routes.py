"""The town's two candidate routes from S to T, each street labelled with its travel time (length divided by speed
limit). Shortest by length: S-A-B-C-D-T, 2500 m, 252.0 s, through the old town. Fastest: S-A-N-M-D-T, 3300 m,
197.1 s, by the bypass. Run -> town_routes.png"""
from pathlib import Path

import plotly.graph_objects as go
import roadkit as rk
import townplot as tp
from gifkit import BLUE, ORANGE

here = Path(__file__).parent
At, Al = rk.town("time"), rk.town("length")
fast, short = rk.astar(At, "S", "T"), rk.astar(Al, "S", "T")
assert fast["path"] == list("SANMDT") and short["path"] == list("SABCDT")
assert round(fast["cost"], 1) == 197.1 and round(rk.path_cost(Al, fast["path"])) == 3300
assert round(short["cost"]) == 2500 and round(rk.path_cost(At, short["path"]), 1) == 252.0
assert [round(x, 1) for x in (36, 28.8, 67.5, 28.8, 36)] == [round(At[a][b], 1) for a, b in zip("SANMD", "ANMDT")]
fig = go.Figure()
off = {frozenset("AN"): (-110, 0), frozenset("MD"): (110, 0), frozenset("BE"): (-90, 0), frozenset("FC"): (90, 0),
       frozenset("LT"): (120, -40), frozenset("ML"): (0, 45), frozenset("NM"): (0, 55), frozenset("EF"): (0, 45),
       frozenset("SA"): (0, 60), frozenset("AB"): (0, -85), frozenset("BC"): (0, -85), frozenset("CD"): (0, -85),
       frozenset("DT"): (0, 60)}
tp.roads(fig, label="time", offset=off)
fig.add_trace(go.Scatter(x=[tp.P[v][0] for v in short["path"]], y=[tp.P[v][1] - 30 for v in short["path"]],
                         mode="lines", line=dict(color=ORANGE, width=6, dash="dash")))   # drawn 30 m low: visible beside the blue
fig.add_trace(go.Scatter(x=[tp.P[v][0] for v in fast["path"]], y=[tp.P[v][1] + 15 for v in fast["path"]],
                         mode="lines", line=dict(color=BLUE, width=6)))
tp.vertices(fig)
fig.add_annotation(x=1250, y=1110, text="<b>fastest</b>: S-A-N-M-D-T, 3300 m, 197.1 s", showarrow=False,
                   font=dict(size=20, color=BLUE))
fig.add_annotation(x=2350, y=200, text="<b>shortest</b>: S-A-B-C-D-T,<br>2500 m, 252.0 s", showarrow=False,
                   font=dict(size=20, color=ORANGE), align="left")
tp.frame_layout(fig, width=1300, height=520, yr=(70, 1160))
fig.write_image(here / "town_routes.png", scale=2)
