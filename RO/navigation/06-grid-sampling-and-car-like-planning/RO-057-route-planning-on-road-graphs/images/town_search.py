"""Searches on the town graph from S to T, travel-time costs, one vertex taken off the open list per frame.
town_astar.gif: run 1, Dijkstra (h = 0): 10 vertices; run 2, A* with h = straight-line distance to T divided by the
top speed, 80 km/h: 7 vertices. town_alt.gif: A* with the landmark heuristic, landmark L: 6 vertices. All return
S-A-N-M-D-T, 197.1 s. Each frame lists the open list as g + h = f in seconds. Run -> town_astar.gif,
town_astar_frames.png, town_alt.gif, town_alt_frames.png"""
from pathlib import Path

import plotly.graph_objects as go
import roadkit as rk
import townplot as tp
from gifkit import BLUE, GREY, PURPLE, RED, make_gif

here = Path(__file__).parent
At = rk.town("time")
H = {"dij": lambda u: 0.0, "str": rk.straight(tp.P, "T", rk.town_vmax()),
     "alt": rk.alt_heuristic(rk.landmark_tables(At, ["L"]), "T")}
R = {k: rk.astar(At, "S", "T", h, trace=True) for k, h in H.items()}
r1 = lambda x: round(x, 1)
assert [len(R[k]["order"]) for k in ("dij", "str", "alt")] == [10, 7, 6]
assert all(R[k]["path"] == list("SANMDT") and r1(R[k]["cost"]) == 197.1 for k in R)
assert R["dij"]["order"] == list("SANBMECDLT") and R["str"]["order"] == list("SANMBDT")
assert R["alt"]["order"] == list("SANMDT")
assert r1(H["str"]("S")) == 112.5 and r1(H["str"]("B")) == 67.5 and r1(H["alt"]("S")) == 130.5
assert r1(H["alt"]("B")) == 147.0 and r1(H["alt"]("M")) == 1.8 and r1(H["str"]("M")) == 28.8
HPOS = {v: (0, 95) for v in tp.P}
HPOS.update(E=(0, -95), F=(0, -95), N=(0, 95), M=(0, 95), L=(0, 95), T=(0, -95), D=(0, -95), C=(0, -95),
            B=(0, -95), A=(0, -95), S=(0, -95))
TITLE = {"dij": "run 1: Dijkstra, h = 0", "str": "run 2: A*, h = straight line to T at 80 km/h",
         "alt": "A*, h from the landmark L"}


def fmt(x):
    return f"{x:.1f}"


def frame(key, k, title, note, final=False):
    R_, h = R[key], H[key]
    s = R_["snaps"][k - 1] if k else dict(cur=None, closed=[], open={"S": (0.0, h("S"), h("S"))})
    status = {v: "open" for v in s["open"]}
    status.update({v: "closed" for v in s["closed"]})
    fig = go.Figure()
    tp.roads(fig, label=None)
    if final:
        tp.route(fig, R_["path"], color=BLUE, width=7)
    tp.vertices(fig, status=status, cur=s["cur"])
    if key != "dij":
        for v in tp.P:
            dx, dy = HPOS[v]
            fig.add_annotation(x=tp.P[v][0] + dx, y=tp.P[v][1] + dy, text=f"h {fmt(h(v))}", showarrow=False,
                               font=dict(size=17, color=PURPLE), bgcolor="rgba(255,255,255,0.85)")
    if key == "alt":
        fig.add_annotation(x=3000, y=1150, text="landmark", showarrow=False, font=dict(size=17, color=PURPLE))
    lines = [f"<b>{TITLE[key]}</b>", "<b>open list</b> (g + h = f, in s):"]
    rows = sorted(s["open"].items(), key=lambda kv: (kv[1][2], kv[1][1]))
    if not rows:
        rows = []
    cells = [f"{v}: {fmt(g)} + {fmt(hh)} = {fmt(f)}" for v, (g, hh, f) in rows]
    lines += ["    ".join(cells[i:i + 3]) for i in range(0, len(cells), 3)] or ["(empty)"]
    lines.append(f"<b>taken off</b>: {', '.join(s['closed']) if s['closed'] else 'none'}  ({len(s['closed'])})")
    fig.add_annotation(x=-200, y=-60, text="<br>".join(lines), showarrow=False, xanchor="left", yanchor="top",
                       align="left", font=dict(size=20))
    fig.add_annotation(x=-200, y=-470, text=note, showarrow=False, xanchor="left", yanchor="top", align="left",
                       font=dict(size=20, color=RED if "never" in note or "pruned" in note else GREY))
    return tp.frame_layout(fig, title=title, width=1200, height=820, yr=(-620, 1200))


def run(key, label):
    n = len(R[key]["order"])
    F = [frame(key, 0, f"{label}: start, S on the open list", "")]
    for k in range(1, n + 1):
        v = R[key]["order"][k - 1]
        g, hv = R[key]["g"][v], H[key](v)
        F.append(frame(key, k, f"{label}: take {v} off (f {fmt(g + hv)})",
                       f"T comes off with g = {fmt(g)} s: the route" if v == "T" else "", final=(v == "T")))
    return F


f1, f2 = run("dij", "run 1"), run("str", "run 2")
f2[-1] = frame("str", 7, "run 2: take T off (f 197.1): 7 vertices, run 1 took 10",
               "B (old town) was taken off: its f, 96.0 + 67.5 = 163.5,<br>was below 197.1, because h = 67.5 s "
               "is far below<br>the true 156.0 s", final=True)
figs = f1 + f2
holds = [3] + [2] * 9 + [8] + [4] + [2] * 6 + [12]
assert len(holds) == len(figs)
make_gif(figs, here / "town_astar", fps=1, holds=holds, keys=[4, 10, 15, 18], cols=2, width=900)

f3 = run("alt", "landmark L")
f3[-1] = frame("alt", 6, "landmark L: take T off (f 197.1): 6 vertices",
               "B is never taken off: f = 96.0 + 147.0 = 243.0 is above 197.1,<br>because the landmark bound "
               "at B, 147.0 s, is near the true 156.0 s", final=True)
make_gif(f3, here / "town_alt", fps=1, holds=[3] + [2] * 5 + [12], keys=[1, 3, 4, 6], cols=2, width=900)
