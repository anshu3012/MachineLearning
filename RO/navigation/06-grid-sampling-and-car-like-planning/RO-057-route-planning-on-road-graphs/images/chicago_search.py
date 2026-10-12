"""The same trip on the Chicago street graph (1628 intersections, travel-time costs) searched four ways, 40
intersections taken off the open list per frame in every panel; a panel that has finished holds its last frame.
Top left: Dijkstra (h = 0), 1526 intersections. Top right: A* with the straight line to the goal divided by the top
speed, 88.5 km/h, 1229. Bottom left: A* with 16 landmarks (purple diamonds), 108. Bottom right: the contraction
hierarchy's two upward searches, from the start (red) and from the goal (blue), 67 + 92 = 159. All four return the
same 492.8 s route (blue line). Run -> chicago_search.gif, chicago_search_frames.png"""
from pathlib import Path

import plotly.graph_objects as go
import roadkit as rk
from gifkit import BLUE, FONT, GREEN, PURPLE, RED, make_gif
from plotly.subplots import make_subplots

here = Path(__file__).parent
CHI = rk.chicago()
At, Al, pos = CHI["adj_time"], CHI["adj_len"], CHI["pos"]
vmax = max(Al[u][v] / At[u][v] for u in At for v in At[u])
X, Y = max(p[0] for p in pos.values()), max(p[1] for p in pos.values())
s, t = rk.nearest(pos, (0.12 * X, 0.1 * Y)), rk.nearest(pos, (0.88 * X, 0.9 * Y))
marks = rk.farthest_landmarks(At, 16, sorted(At)[0])
runs = {"dij": rk.astar(At, s, t), "str": rk.astar(At, s, t, rk.straight(pos, t, vmax)),
        "alt": rk.astar(At, s, t, rk.alt_heuristic(rk.landmark_tables(At, marks), t))}
q = rk.contract(At)
chq = rk.ch_query(q, s, t)
assert len(At) == 1628 and round(vmax * 3.6, 1) == 88.5
assert [len(runs[k]["order"]) for k in ("dij", "str", "alt")] == [1526, 1229, 108]
assert (len(chq["fwd"]), len(chq["bwd"])) == (67, 92)
assert all(round(r["cost"], 1) == 492.8 for r in runs.values()) and round(chq["cost"], 1) == 492.8
route = runs["dij"]["path"]
assert chq["path"] == route

xs, ys = [], []
for (u, v), pts in CHI["lines"].items():
    xs += [p[0] for p in pts] + [None]
    ys += [p[1] for p in pts] + [None]
STEP = 40
PANELS = [("dij", "Dijkstra, h = 0", (1, 1)), ("str", "A*, straight line ÷ 88.5 km/h", (1, 2)),
          ("alt", "A*, 16 landmarks", (2, 1)), ("ch", "contraction hierarchy", (2, 2))]
TOTAL = {"dij": 1526, "str": 1229, "alt": 108, "ch": 159}
nframes = -(-1526 // STEP)


def settled(key, k):
    n = min(k * STEP, TOTAL[key])
    if key != "ch":
        return runs[key]["order"][:n], [], n
    steps = chq["steps"][:n]
    return [v for sd, v in steps if sd == 0], [v for sd, v in steps if sd == 1], n


def frame(k):
    fig = make_subplots(rows=2, cols=2, horizontal_spacing=0.03, vertical_spacing=0.07,
                        subplot_titles=[p[1] for p in PANELS])
    for key, name, (r, c) in PANELS:
        fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color="#CFCFCF", width=1),
                                 hoverinfo="skip"), row=r, col=c)
        a, b, n = settled(key, k)
        done = n == TOTAL[key]
        for vs, col in ((a, RED), (b, BLUE)):
            if vs:
                fig.add_trace(go.Scatter(x=[pos[v][0] for v in vs], y=[pos[v][1] for v in vs], mode="markers",
                                         marker=dict(size=5, color=col), hoverinfo="skip"), row=r, col=c)
        if key == "alt":
            fig.add_trace(go.Scatter(x=[pos[v][0] for v in marks], y=[pos[v][1] for v in marks],
                                     mode="markers", marker=dict(size=14, color=PURPLE, symbol="diamond",
                                                                 line=dict(color="white", width=1)),
                                     hoverinfo="skip"), row=r, col=c)
        if done:
            fig.add_trace(go.Scatter(x=[pos[v][0] for v in route], y=[pos[v][1] for v in route], mode="lines",
                                     line=dict(color=BLUE if key != "ch" else "#1F3F66", width=4),
                                     hoverinfo="skip"), row=r, col=c)
        for v, lab in ((s, "start"), (t, "goal")):
            fig.add_trace(go.Scatter(x=[pos[v][0]], y=[pos[v][1]], mode="markers",
                                     marker=dict(size=13, color=GREEN, line=dict(color="black", width=1.5)),
                                     hoverinfo="skip"), row=r, col=c)
        txt = (f"{n} taken off" if key != "ch" else f"{len(a)} up from start + {len(b)} up from goal")
        txt += ": done, 492.8 s" if done else ""
        fig.add_annotation(x=0.02 * X, y=1.02 * Y, text=txt, showarrow=False, xanchor="left", yanchor="top",
                           font=dict(size=19, color="black"), bgcolor="rgba(255,255,255,0.85)", row=r, col=c)
        fig.update_xaxes(range=[-80, X + 80], visible=False, row=r, col=c)
        fig.update_yaxes(range=[-80, Y + 220], visible=False, row=r, col=c,
                         scaleanchor=f"x{'' if (r, c) == (1, 1) else (r - 1) * 2 + c}")
    fig.update_annotations(font_size=21, selector=dict(text=PANELS[0][1]))
    for p in PANELS[1:]:
        fig.update_annotations(font_size=21, selector=dict(text=p[1]))
    fig.update_layout(template="simple_white", font=FONT, width=1100, height=1160, showlegend=False,
                      margin=dict(l=10, r=10, t=40, b=10))
    return fig


figs = [frame(k) for k in range(0, nframes + 1)]
holds = [3] + [1] * (nframes - 1) + [14]
make_gif(figs, here / "chicago_search", fps=4, holds=holds, keys=[1, 3, 15, nframes], cols=2, width=760)
