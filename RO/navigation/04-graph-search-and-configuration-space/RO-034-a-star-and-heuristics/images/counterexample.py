"""A* with a closed list on a five-waypoint roadmap in the room: S is the robot at (2.0, 1.0) m, G the doorway centre
(3.6, 4.0) m, A, B and C points of free floor; edges are straight and labelled with their lengths in m. Run 1: the
guess h is 0 everywhere except at A, where the robot remembers the exact distance left, 2.072 m (admissible: no guess
is above the true distance). B and then C come off the open list first, so C is closed with g = 3.192 m by way of B;
when A comes off, its shorter way into C (2.487 m) is thrown away because C is closed, and A* returns 4.358 m. The
shortest route, S-A-C-G, is 3.653 m. Run 2: h(A) lowered to 0.906 m (consistent); A comes off before C, C gets
g = 2.487 m and A* returns 3.653 m. Run -> counterexample.gif, counterexample_frames.png"""
from pathlib import Path

import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, PURPLE, RED, make_gif
from roommap import DOOR, POLES, POLE_R, TABLE
from searchkit import RM, RM_EDGES, rm_astar, rm_len

here = Path(__file__).parent
L = {frozenset(e): rm_len(*e) for e in RM_EDGES}
r3 = lambda x: round(x, 3)
H1 = dict(S=0.0, A=rm_len("A", "C") + rm_len("C", "G"), B=0.0, C=0.0, G=0.0)
H2 = dict(H1, A=rm_len("A", "C"))
R1, R2 = rm_astar(H1), rm_astar(H2)
# every number shown, and the rounded sums as shown
lens = {k: r3(v) for k, v in L.items()}
assert [lens[frozenset(e)] for e in RM_EDGES] == [1.581, 1.521, 0.906, 1.671, 1.166]
assert r3(H1["A"]) == 2.072 and r3(0.906 + 1.166) == 2.072 and r3(1.581 + 2.072) == 3.653
assert r3(1.521 + 1.671) == 3.192 and r3(3.192 + 1.166) == 4.358 and r3(1.581 + 0.906) == 2.487
assert r3(2.487 + 1.166) == 3.653 and r3(R1["cost"]) == 4.358 and r3(R2["cost"]) == 3.653
assert [s["cur"] for s in R1["steps"]] == list("SBCAG") and R1["steps"][3]["skipped"]
assert r3(R1["steps"][3]["skipped"][0][1]) == 2.487
assert [s["cur"] for s in R2["steps"]] == list("SBACG") and R1["path"] == list("SBCG") and R2["path"] == list("SACG")

HPOS = dict(S=(0.36, -0.02), A=(0.5, 0.0), B=(0.0, -0.22), C=(-0.46, 0.05), G=(0.44, -0.06))
LPOS = {frozenset("SA"): (0.18, 0.0), frozenset("SB"): (-0.2, 0.0), frozenset("AC"): (0.22, 0.0),
        frozenset("BC"): (-0.05, 0.16), frozenset("CG"): (-0.05, 0.17)}


def frame(run, k, title, note, final=False):
    R, H = (R1, H1) if run == 1 else (R2, H2)
    s = R["steps"][k - 1] if k else dict(cur=None, closed=[], open={"S": (0.0, H["S"], H["S"])}, skipped=[])
    fig = go.Figure()
    # the room around the roadmap, faint
    fig.add_trace(go.Scatter(x=[p[0] for p in TABLE + [TABLE[0]]], y=[p[1] for p in TABLE + [TABLE[0]]],
                             fill="toself", fillcolor="#E6E6E6", line=dict(color="#AAAAAA", width=2), mode="lines"))
    px, py = POLES["pink"]
    fig.add_shape(type="circle", x0=px - POLE_R, x1=px + POLE_R, y0=py - POLE_R, y1=py + POLE_R,
                  fillcolor="#AAAAAA", line=dict(color="#AAAAAA"))
    for a, b in ((0.7, DOOR[0]), (DOOR[1], 5.6)):
        fig.add_trace(go.Scatter(x=[a, b], y=[4.0, 4.0], mode="lines", line=dict(color="#555555", width=6)))
    fig.add_annotation(x=3.15, y=4.13, text="door", showarrow=False, font=dict(size=17, color=GREY))
    # edges
    route = R["path"] if final else []
    on_route = {frozenset(e) for e in zip(route, route[1:])}
    for a, b in RM_EDGES:
        e = frozenset((a, b))
        col, w = (BLUE, 7) if e in on_route else ("#9A9A9A", 3)
        fig.add_trace(go.Scatter(x=[RM[a][0], RM[b][0]], y=[RM[a][1], RM[b][1]], mode="lines",
                                 line=dict(color=col, width=w)))
        mx, my = (RM[a][0] + RM[b][0]) / 2 + LPOS[e][0], (RM[a][1] + RM[b][1]) / 2 + LPOS[e][1]
        fig.add_annotation(x=mx, y=my, text=f"{lens[e]:.3f}", showarrow=False, font=dict(size=18, color="#444444"),
                           bgcolor="white")
    if s["skipped"]:
        a, b = "A", "C"
        fig.add_trace(go.Scatter(x=[RM[a][0], RM[b][0]], y=[RM[a][1], RM[b][1]], mode="lines",
                                 line=dict(color=RED, width=6, dash="dash")))
    if final and run == 1:
        best = ["S", "A", "C", "G"]
        fig.add_trace(go.Scatter(x=[RM[v][0] for v in best], y=[RM[v][1] for v in best], mode="lines",
                                 line=dict(color=GREEN, width=4, dash="dash")))
    # vertices
    for v, (x, y) in RM.items():
        fill = "#F6B8B8" if v in s["closed"] else ("#C3E6B9" if v in s["open"] else "white")
        edge = ORANGE if v == s["cur"] else "black"
        fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers+text", text=[f"<b>{v}</b>"],
                                 marker=dict(size=40, color=fill, line=dict(color=edge, width=5 if v == s["cur"] else 2)),
                                 textfont=dict(size=20)))
        dx, dy = HPOS[v]
        col = PURPLE if v == "A" else "#1F3F66"
        fig.add_annotation(x=x + dx, y=y + dy, text=f"h = {H[v]:.3f}" if H[v] else "h = 0", showarrow=False,
                           font=dict(size=18, color=col), bgcolor="white")
    # the open list, as a table at the right
    lines = [f"<b>run {run}</b>: h(A) = {H['A']:.3f} m" + (" (remembered, exact)" if run == 1 else " (lowered)"),
             "", "<b>open list</b>  (g + h = f, in m)"]
    for v, (g, h, f) in sorted(s["open"].items(), key=lambda kv: kv[1][2]):
        lines.append(f"{v}:  {g:.3f} + {h:.3f} = {f:.3f}" if h else f"{v}:  {g:.3f} + 0 = {f:.3f}")
    if not s["open"]:
        lines.append("(empty)")
    lines += ["", "<b>closed</b>: " + (", ".join(s["closed"]) if s["closed"] else "none")]
    fig.add_annotation(x=5.85, y=3.8, text="<br>".join(lines), showarrow=False, xanchor="left", yanchor="top",
                       align="left", font=dict(size=19))
    fig.add_annotation(x=5.85, y=1.45, text=note, showarrow=False, xanchor="left", yanchor="top", align="left",
                       font=dict(size=19, color=RED if "thrown" in note or "wrong" in note else "black"))
    fig.update_xaxes(range=[0.65, 9.6], visible=False)
    fig.update_yaxes(range=[0.55, 4.3], visible=False, scaleanchor="x")
    fig.update_layout(template="simple_white", font=FONT, width=1200, height=600, showlegend=False,
                      title=dict(text=title, x=0.5, font_size=23), margin=dict(l=10, r=10, t=60, b=10))
    return fig


F = [
    (1, 0, "run 1, start: only S is on the open list", "h never overestimates:<br>admissible"),
    (1, 1, "run 1: take S off (f 0)", "B looks cheaper than A:<br>1.521 against 3.653"),
    (1, 2, "run 1: take B off (f 1.521)", "C is reached by way of B:<br>g = 1.521 + 1.671 = 3.192"),
    (1, 3, "run 1: take C off (f 3.192): C is now closed", "C is closed with g = 3.192,<br>by way of B"),
    (1, 4, "run 1: take A off (f 3.653)", "A's way into C: 1.581 + 0.906 = 2.487,<br>"
     "but C is closed: thrown away"),
    (1, 5, "run 1: take G off: A* returns 4.358 m", "wrong: S-A-C-G is 3.653 m<br>(green, dashed)"),
    (2, 0, "run 2: lower h(A) to 0.906 m", "now h falls by no more than<br>the edge's length: consistent"),
    (2, 1, "run 2: take S off (f 0)", "A: 1.581 + 0.906 = 2.487"),
    (2, 2, "run 2: take B off (f 1.521)", "C by way of B: 3.192"),
    (2, 3, "run 2: take A off (f 2.487) before C", "C improves: 1.581 + 0.906 = 2.487"),
    (2, 4, "run 2: take C off (f 2.487)", "G: 2.487 + 1.166 = 3.653"),
    (2, 5, "run 2: take G off: A* returns 3.653 m", "right: the shortest route,<br>S-A-C-G"),
]
figs = [frame(run, k, t, n, final=(k == 5)) for run, k, t, n in F]
holds = [5, 5, 5, 6, 9, 12, 6, 4, 4, 6, 4, 14]
make_gif(figs, here / "counterexample", fps=1, holds=holds, keys=[3, 4, 5, 11], cols=2, width=900)
