"""The Chicago street graph: OpenStreetMap streets a car may drive within 2.5 km of (41.8819 N, 87.6300 W), 1628
intersections and 3857 arcs, each street drawn wider and darker the higher its speed limit, intersections as red dots. The fast roads (motorways and trunk roads,
above 50 km/h) are the expressways; most streets are 33 to 44 km/h. Run -> chicago_map.png"""
from pathlib import Path

import plotly.graph_objects as go
import roadkit as rk
from gifkit import FONT

here = Path(__file__).parent
C = rk.chicago()
At, pos = C["adj_time"], C["pos"]
X, Y = max(p[0] for p in pos.values()), max(p[1] for p in pos.values())
arcs = [(u, v) for u in At for v in At[u]]
one_way = sum(1 for u, v in arcs if u not in At[v])
assert (len(At), len(arcs), one_way) == (1628, 3857, 1409)
BANDS = [("up to 40 km/h", 0, 40.5, "#C4C4C4", 1.5), ("41 to 50 km/h", 40.5, 50.5, "#7D7D7D", 2.5),
         ("above 50 km/h", 50.5, 999, "#111111", 5)]
count = {}
fig = go.Figure()
for name, lo, hi, col, w in BANDS:
    xs, ys = [], []
    for e in arcs:
        if lo <= C["speed_kmh"][e] < hi:
            count[name] = count.get(name, 0) + 1
            xs += [p[0] for p in C["lines"][e]] + [None]
            ys += [p[1] for p in C["lines"][e]] + [None]
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=col, width=w), name=f"{name}"))
fig.add_trace(go.Scatter(x=[pos[n][0] for n in At], y=[pos[n][1] for n in At], mode="markers",
                         marker=dict(size=3.5, color="#E45756"), name="intersection"))
fig.update_xaxes(range=[-80, X + 80], visible=False)
fig.update_yaxes(range=[-560, Y + 60], visible=False, scaleanchor="x")
fig.add_shape(type="line", x0=X - 1000, x1=X, y0=-450, y1=-450, line=dict(color="black", width=3))
fig.add_annotation(x=X - 500, y=-370, text="1 km", showarrow=False, font=dict(size=18))
fig.update_layout(template="simple_white", font=FONT, width=820, height=1000, margin=dict(l=10, r=10, t=10, b=10),
                  legend=dict(x=0.0, y=0.0, xanchor="left", yanchor="bottom", orientation="h", entrywidth=135,
                              font_size=16))
print(count)
fig.write_image(here / "chicago_map.png", scale=2)
