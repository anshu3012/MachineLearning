"""Contraction hierarchy on the town graph, travel-time costs.
town_contract.gif: the vertices contracted one at a time in the order E, F, B, C, S, T, L, A, D, N, M (old town
first, bypass last). Contracting a vertex removes it from the graph; for each way u -> v -> w through it, a
search looks for another way from u to w that avoids v and is no slower. None found: a shortcut u -> w (green) with
the two edges' time; one found: no shortcut (purple, dashed). Three shortcuts are added: B -> F 108 s, A -> C and
C -> A 120 s.
town_chquery.gif: queries on the result. Top: the town; bottom: the same vertices raised to their rank (contraction
order, 0 at the bottom). A search from the start (red) and a search back from the goal (blue) each follow only
edges that climb. S to T meets at M: 197.1 s. S to C meets at A: 36 + 120 = 156 s, and the shortcut A -> C unpacks
to A, B, C. Run -> town_contract.gif, town_contract_frames.png, town_chquery.gif, town_chquery_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import roadkit as rk
import townplot as tp
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, PURPLE, RED, make_gif
from plotly.subplots import make_subplots

here = Path(__file__).parent
P = tp.P
At = rk.town("time")
CH = rk.contract(At, rk.CH_ORDER)
rank = CH["rank"]
r1 = lambda x: round(x, 1)
ev = {v: (added, wit) for v, added, wit in CH["events"]}
assert [(a, b, r1(c)) for a, b, c in ev["E"][0]] == [("B", "F", 108.0)]
assert [(a, b, r1(c), r1(d)) for a, b, c, d in ev["E"][1]] == [("F", "B", 108.0, 108.0)]
assert [(a, b, r1(c), r1(d)) for a, b, c, d in ev["F"][1]] == [("B", "C", 156.0, 60.0)]
assert sorted((a, b, r1(c)) for a, b, c in ev["B"][0]) == [("A", "C", 120.0), ("C", "A", 120.0)]
assert sorted((a, b, r1(c), r1(d)) for a, b, c, d in ev["C"][1]) == [("A", "D", 180.0, 125.1), ("D", "A", 180.0, 125.1)]
assert sorted((a, b, r1(c), r1(d)) for a, b, c, d in ev["T"][1]) == [("D", "L", 82.8, 73.8), ("L", "D", 82.8, 73.8)]
assert all(not ev[v][0] for v in "CSTLADNM") and len(CH["mid"]) == 3
Q1, Q2 = rk.ch_query(CH, "S", "T"), rk.ch_query(CH, "S", "C")
assert r1(Q1["cost"]) == 197.1 and Q1["top"] == "M" and Q1["path"] == list("SANMDT")
assert Q1["steps"] == [(0, "S"), (1, "T"), (0, "A"), (1, "D"), (0, "N"), (1, "L"), (0, "M"), (1, "M")]
assert r1(Q2["cost"]) == 156.0 and Q2["top"] == "A" and Q2["hops"] == list("SAC") and Q2["path"] == list("SABC")
assert r1(rk.astar(At, "S", "C")["cost"]) == 156.0


def bezier(a, b, bend):
    """Points on a gentle curve from a to b, pushed `bend` metres to the left of the direction a -> b."""
    (x0, y0), (x1, y1) = a, b
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    dx, dy = x1 - x0, y1 - y0
    n = np.hypot(dx, dy)
    cx, cy = mx - dy / n * bend, my + dx / n * bend
    t = np.linspace(0, 1, 30)
    return (1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t ** 2 * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t ** 2 * y1


SHORT = {("B", "F"): -170, ("A", "C"): 230}           # how each shortcut is drawn (bend in m)


def shortcut(fig, u, w, label, kw=None, color=GREEN):
    kw = kw or {}
    bend = SHORT.get((u, w), SHORT.get((w, u)))
    xs, ys = bezier(P[u], P[w], bend)
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=color, width=5), hoverinfo="skip"), **kw)
    k = len(xs) // 2
    if label:
        lx, ly = (xs[k], ys[k] + 40) if bend > 0 else (800, 420)       # B→F: left of the street B-E
        fig.add_annotation(x=lx, y=ly, text=label, showarrow=False,
                           font=dict(size=18, color=color), bgcolor="rgba(255,255,255,0.9)", **kw)
    if (u, w) == ("B", "F"):                           # one way only: an arrowhead near F
        fig.add_annotation(x=xs[-4], y=ys[-4], ax=xs[-8], ay=ys[-8], xref="x", yref="y", axref="x", ayref="y",
                           showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=3, arrowcolor=color, text="")


def witness(fig, path, label, at):
    fig.add_trace(go.Scatter(x=[P[v][0] for v in path], y=[P[v][1] + 25 for v in path], mode="lines",
                             line=dict(color=PURPLE, width=6, dash="dash"), hoverinfo="skip"))
    fig.add_annotation(x=at[0], y=at[1], text=label, showarrow=False, font=dict(size=18, color=PURPLE),
                       bgcolor="rgba(255,255,255,0.9)")


def cframe(done, cur, title, lines, shortcuts, wit=None, via=None):
    """done: vertices already contracted; cur: the one being contracted; shortcuts: [(u, w, label)]."""
    fig = go.Figure()
    gone = set(done) | ({cur} if cur else set())
    dim = {frozenset((a, b)) for a, b, _, _ in rk.TOWN_ROADS if a in done or b in done}
    tp.roads(fig, label=None, dim=dim)
    if via:
        u, v, w = via
        fig.add_trace(go.Scatter(x=[P[u][0], P[v][0], P[w][0]], y=[P[u][1] - 25, P[v][1] - 25, P[w][1] - 25],
                                 mode="lines", line=dict(color=ORANGE, width=6), hoverinfo="skip"))
    for u, w, lab in shortcuts:
        shortcut(fig, u, w, lab)
    if wit:
        witness(fig, *wit)
    status = {v: "pale" for v in done}
    tp.vertices(fig, status=status, cur=cur)
    for v in done:
        fig.add_annotation(x=P[v][0] - 95, y=P[v][1] - 62, text=f"rank {rank[v]}", showarrow=False,
                           font=dict(size=16, color=GREY))
    fig.add_annotation(x=-200, y=-60, text="<br>".join(lines), showarrow=False, xanchor="left", yanchor="top",
                       align="left", font=dict(size=20))
    return tp.frame_layout(fig, title=title, width=1200, height=760, yr=(-480, 1200))


ALL = [("B", "F", "B→F 108 s"), ("A", "C", "A–C 120 s, both ways")]
order = rk.CH_ORDER
F, H, K = [], [], []


def add(fig, hold, key=False):
    if key:
        K.append(len(F))
    F.append(fig)
    H.append(hold)


add(cframe([], None, "contract the vertices one at a time, least important first",
           ["<b>order</b>: E, F, B, C (old town), S, T, L (ends), A, D (junctions), N, M (bypass)",
            "contracting v: remove v; for each way u → v → w, keep its time with a shortcut u → w",
            "unless another way from u to w, avoiding v, is no slower"], []), 4)
add(cframe([], "E", "contract E (rank 0): B → E → F",
           ["B → E → F takes 48 + 60 = 108 s", "search from B without E: F cannot be reached (F → C is one-way)",
            "<b>shortcut B → F, 108 s</b>"], [ALL[0]], via=("B", "E", "F")), 5)
add(cframe([], "E", "contract E (rank 0): F → E → B",
           ["F → E → B takes 60 + 48 = 108 s", "other way F → C → B: 48 + 60 = 108 s, no slower",
            "<b>no shortcut F → B</b>"], [ALL[0]], wit=(list("FCB"), "other way F→C→B, 108 s", (1250, 760)),
           via=("F", "E", "B")), 5, key=True)
add(cframe(["E"], "F", "contract F (rank 1): B → F → C",
           ["B → F → C takes 108 (shortcut) + 48 = 156 s", "other way B → C: 60 s, faster", "<b>no shortcut</b>"],
           [ALL[0]], wit=(list("BC"), "other way B→C, 60 s", (1250, 760)), via=("B", "F", "C")), 5)
add(cframe(["E", "F"], "B", "contract B (rank 2): A → B → C",
           ["A → B → C takes 60 + 60 = 120 s", "search from A without B: the fastest other way,",
            "A → N → M → D → C, takes 185.1 s: slower", "<b>shortcut A → C and C → A, 120 s</b>"],
           [ALL[1]], via=("A", "B", "C")), 6, key=True)
add(cframe(["E", "F", "B"], "C", "contract C (rank 3): A → C → D",
           ["A → C → D takes 120 (shortcut) + 60 = 180 s",
            "other way A → N → M → D: 28.8 + 67.5 + 28.8 = 125.1 s, faster", "<b>no shortcut</b> (nor D → A)"],
           [ALL[1]], wit=(list("ANMD"), "other way A→N→M→D, 125.1 s", (1250, 1130)), via=("A", "C", "D")), 6,
    key=True)
add(cframe(["E", "F", "B", "C"], "S", "contract S (rank 4)",
           ["S has one neighbour left, A: no way u → S → w to keep"], []), 3)
add(cframe(["E", "F", "B", "C", "S"], "T", "contract T (rank 5): D → T → L",
           ["D → T → L takes 36 + 46.8 = 82.8 s", "other way D → M → L: 28.8 + 45 = 73.8 s, faster",
            "<b>no shortcut</b> (nor L → D)"], [], wit=(list("DML"), "other way D→M→L, 73.8 s", (2500, 1130)),
           via=("D", "T", "L")), 5)
for i, v in enumerate("LADN"):
    done = list(order[:6 + i])
    add(cframe(done, v, f"contract {v} (rank {rank[v]})", [f"{v} has one neighbour left: no shortcut"], []), 2)
add(cframe(list(order), None, "done: every vertex has a rank, 3 shortcuts added",
           ["<b>shortcuts</b>: B → F 108 s; A → C and C → A 120 s",
            "the graph to search = the 13 streets + the 3 shortcuts; each vertex keeps its rank",
            "the ranks rise from the old town (0) to the bypass (9, 10)"], ALL), 14, key=True)
make_gif(F, here / "town_contract", fps=1, holds=H, keys=K, cols=2, width=900)

# ------------------------------------------------------------------ queries, map above, ranks below
Y0 = -2400                       # the side view: y = Y0 + 160 * rank
side = {v: (P[v][0], Y0 + 160 * rank[v]) for v in P}
arcs = {(u, w) for u in CH["out"] for w in CH["out"][u]}


def qframe(q, k, title, lines, final=False, unpack=False):
    steps = q["steps"][:k]
    fwd = [v for s_, v in steps if s_ == 0]
    bwd = [v for s_, v in steps if s_ == 1]
    fig = go.Figure()
    tp.roads(fig, label=None)
    # side view: every arc of the searched graph, original grey, shortcut green
    for u, w in arcs:
        if (w, u) in arcs and u > w:
            continue
        col, wd = (GREEN, 4) if (u, w) in CH["mid"] or (w, u) in CH["mid"] else ("#BDBDBD", 2.5)
        fig.add_trace(go.Scatter(x=[side[u][0], side[w][0]], y=[side[u][1], side[w][1]], mode="lines",
                                 line=dict(color=col, width=wd), hoverinfo="skip"))
    if final:
        hop = q["hops"]
        fig.add_trace(go.Scatter(x=[side[v][0] for v in hop], y=[side[v][1] for v in hop], mode="lines",
                                 line=dict(color=BLUE, width=7), hoverinfo="skip"))
        path = q["path"] if unpack else q["hops"]
        fig.add_trace(go.Scatter(x=[P[v][0] for v in path], y=[P[v][1] for v in path], mode="lines",
                                 line=dict(color=BLUE, width=7), hoverinfo="skip"))
    for v in P:
        both = v in fwd and v in bwd
        fill = "#D9B8E8" if both else "#F6B8B8" if v in fwd else "#BCD3EE" if v in bwd else "white"
        mark = q["top"] if final else (steps[-1][1] if steps else None)
        edge = ORANGE if v == mark else "black"
        for (x, y) in (P[v], side[v]):
            fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers+text", text=[f"<b>{v}</b>"], textfont=dict(size=19),
                                     marker=dict(size=38, color=fill, line=dict(color=edge, width=5 if edge == ORANGE
                                                                                   else 2)), hoverinfo="skip"))
        fig.add_annotation(x=side[v][0] + 120, y=side[v][1] - 50, text=str(rank[v]), showarrow=False,
                           font=dict(size=16, color=GREY))
    fig.add_annotation(x=-230, y=Y0 + 800, text="rank", textangle=-90, showarrow=False, font=dict(size=18, color=GREY))
    fig.add_annotation(x=1250, y=-40, text="the same vertices, raised to their rank (side view)", showarrow=False,
                       font=dict(size=18, color=GREY))
    fig.add_annotation(x=-200, y=Y0 - 140, text="<br>".join(lines), showarrow=False, xanchor="left", yanchor="top",
                       align="left", font=dict(size=20))
    return tp.frame_layout(fig, title=title, width=1200, height=1150, yr=(Y0 - 560, 1150))


def lab(q, k):
    s_, v = q["steps"][k - 1]
    d = q["df"][v] if s_ == 0 else q["db"][v]
    return f"{'up from the start' if s_ == 0 else 'up from the goal'}: take {v} off ({r1(d)} s)"


G, HQ, KQ = [], [], []
G.append(qframe(Q1, 0, "query S to T: two searches that only climb",
                ["red: the search from S follows edges to higher ranks",
                 "blue: the search back from T follows edges that come down from higher ranks"]))
HQ.append(4)
for k in range(1, 9):
    s_, v = Q1["steps"][k - 1]
    txt = [lab(Q1, k)]
    if k == 8:
        txt = [lab(Q1, k), "M is taken off by both searches: 132.3 + 64.8 = 197.1 s"]
    G.append(qframe(Q1, k, f"query S to T, step {k}", txt))
    HQ.append(2)
G.append(qframe(Q1, 8, "S to T: they meet at M, 197.1 s, the fastest route",
                ["neither search has anything left to take off",
                 "route S-A-N-M-D-T: 8 take-offs (M by both), against 10 for Dijkstra"], final=True))
HQ.append(8)
KQ += [4, len(G) - 1]
G.append(qframe(Q2, 0, "query S to C (old town)", ["the same two climbing searches, now to C"]))
HQ.append(3)
for k in range(1, len(Q2["steps"]) + 1):
    G.append(qframe(Q2, k, f"query S to C, step {k}", [lab(Q2, k)] + (
        ["A is reached by both: 36 + 120 (shortcut A → C) = 156 s"] if Q2["steps"][k - 1] == (1, "A") else [])))
    HQ.append(2)
both = {v: Q2["df"][v] + Q2["db"][v] for v in set(Q2["fwd"]) & set(Q2["bwd"])}
assert {v: r1(x) for v, x in both.items()} == {"A": 156.0, "N": 213.6, "M": 221.1}
G.append(qframe(Q2, len(Q2["steps"]), "S to C: 156 s by the shortcut A → C",
                ["taken off by both: A 36 + 120 = 156 s, N 64.8 + 148.8 = 213.6 s, M 132.3 + 88.8 = 221.1 s",
                 "the smallest sum, at A, is the route: it climbs S → A, then comes down the shortcut A → C",
                 "the shortcut stands for A → B → C, so the route on the map is S-A-B-C"], final=True, unpack=True))
HQ.append(12)
KQ += [len(G) - 4, len(G) - 1]
make_gif(G, here / "town_chquery", fps=1, holds=HQ, keys=KQ, cols=2, width=900)
