"""Figure 5: the search loop with a frontier and a visited list, run as breadth-first search on the waypoint graph.
Each frame is one expansion: take the vertex at the front of the line (red outline), mark it visited (blue), and
add to the back of the line each neighbour that is neither visited nor already waiting (orange). The parent edges
(blue) form a tree that holds each waypoint once. The goal test is made when a vertex is taken off the frontier: G comes
off at the 7th expansion, and the route S-D-G is read back along the parent edges.
Run: python loop_trace.py -> loop_trace.gif, loop_trace_frames.png"""
from pathlib import Path

import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, RED, make_gif
from griddraw import LBLUE, LORANGE, furniture_fill, room_lines, wp_nodes, wp_traces
from roomsearch import WP, bfs, wp_nbrs

here = Path(__file__).parent
R = bfs(start="S", goal="G", nbrs=wp_nbrs)
ORDER = [s["cur"] for s in R["snaps"]]
assert ORDER == ["S", "A", "D", "P", "B", "C", "G"] and R["path"] == ["S", "D", "G"]


def frame(k, title, lines):
    """k = number of expansions done (0: only S on the queue)."""
    snap = R["snaps"][k - 1] if k else dict(cur=None, visited=[], frontier=["S"], parent={"S": None})
    fig = go.Figure()
    for t in furniture_fill() + room_lines(color="#bbb") + wp_traces():
        fig.add_trace(t)
    for v, p in snap["parent"].items():                                 # the tree the search has built
        if p:
            (x0, y0), (x1, y1) = WP[p], WP[v]
            fig.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1], mode="lines", line=dict(color=BLUE, width=6),
                                     hoverinfo="skip"))
    if k == len(ORDER):
        for a, b in zip(R["path"], R["path"][1:]):
            (x0, y0), (x1, y1) = WP[a], WP[b]
            fig.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1], mode="lines", line=dict(color=GREEN, width=9),
                                     hoverinfo="skip"))
    fill = {v: LBLUE for v in snap["visited"]} | {v: LORANGE for v in snap["frontier"]}
    edge = {snap["cur"]: RED} if snap["cur"] else {}
    for t in wp_nodes(fill=fill, edge=edge):
        fig.add_trace(t)
    for i, v in enumerate(snap["frontier"]):                            # queue position next to each waiting vertex
        x, y = WP[v]
        fig.add_annotation(x=x + 0.2, y=y + 0.2, text=f"{i + 1}", showarrow=False, font=dict(size=17, color=ORANGE))
    fig.update_xaxes(range=[-0.1, 7.1], visible=False)
    fig.update_yaxes(range=[-0.1, 4.25], visible=False, scaleanchor="x")
    q = ", ".join(snap["frontier"]) or "(empty)"
    vis = ", ".join(snap["visited"]) or "(none)"
    rows = [(f"frontier, in line (first comes off next): {q}", ORANGE), (f"visited: {vis}", BLUE)] + lines
    fig.update_layout(template="simple_white", width=1000, height=820, font=FONT, showlegend=False,
                      margin=dict(l=20, r=20, t=70, b=220), title=dict(text=title, x=0.5, font=dict(size=22)))
    for i, (s, col) in enumerate(rows):
        fig.add_annotation(x=0.0, y=-0.03 - 0.065 * i, xref="paper", yref="paper", xanchor="left", yanchor="top",
                           showarrow=False, text=s, font=dict(size=20, color=col))
    return fig


figs, holds = [frame(0, "start: the frontier holds S", [("nothing visited yet", GREY)])], [10]
for k, cur in enumerate(ORDER, start=1):
    snap = R["snaps"][k - 1]
    before = (["S"] if k == 1 else R["snaps"][k - 2]["frontier"])
    seen_before = set(R["snaps"][k - 2]["parent"]) if k > 1 else {"S"}
    added = [n for n, _ in wp_nbrs(cur) if n not in seen_before] if cur != "G" else []
    waiting = [n for n, _ in wp_nbrs(cur) if n in before[1:]] if cur != "G" else []
    done = [n for n, _ in wp_nbrs(cur) if n in snap["visited"][:-1]] if cur != "G" else []
    if cur == "G":
        title = f"expansion {k}: G comes off the frontier: goal reached"
        lines = [("route, read back along the blue parent edges: G ← D ← S, so S–D–G", GREEN),
                 ("7 expansions; the tree of every path had 40", "black")]
    else:
        title = f"expansion {k}: take {cur} off the front"
        lines = [(f"added to the back: {', '.join(added) or 'none'}", ORANGE)]
        skip = [f"{n} (visited)" for n in done] + [f"{n} (already waiting)" for n in waiting]
        lines.append((f"skipped: {', '.join(skip) or 'none'}", GREY))
    figs.append(frame(k, title, lines))
    holds.append(30 if cur == "G" else 9)
make_gif(figs, here / "loop_trace.gif", fps=3, holds=holds, keys=[0, 1, 3, 7], cols=2, width=760)
print(ORDER)
