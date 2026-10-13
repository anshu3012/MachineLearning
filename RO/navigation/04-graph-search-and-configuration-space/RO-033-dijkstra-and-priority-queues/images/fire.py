"""Figure 3: Dijkstra's algorithm on the waypoint graph as a fire. A fire is lit at S at time 0 and spreads along every
edge at 1 m per second; a waypoint catches fire when the first flame reaches it, so its time in seconds is its
shortest distance from S in metres. Top: burnt parts of the edges in red, burnt waypoints filled red with their
time. Bottom: the priority queue, the arrival time of the first flame now on its way to each waypoint not yet on
fire, smallest first; its first entry is always the next waypoint to catch fire. Settling order: S 0, A 1.000,
P 2.236, D 2.500, B 3.000, G 3.505, C 4.562; when D catches fire, G's entry drops from 5.022 to 3.505.
Run: python fire.py -> fire.gif, fire_frames.png"""
import math
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import FONT, GREEN, GREY, ORANGE, RED, make_gif
from griddraw import furniture_fill, room_lines, wp_labels
from roomsearch import WP, WP_EDGES, dijkstra, wp_dist, wp_nbrs

here = Path(__file__).parent
R = dijkstra(wp_nbrs, "S", "G", stop_at_goal=False)
T = {s["cur"]: s["cost"] for s in R["snaps"]}                        # ignition time = settled cost
ORDER = [s["cur"] for s in R["snaps"]]
assert ORDER == ["S", "A", "P", "D", "B", "G", "C"] and R["path"] == ["S", "D", "G"]
assert [round(T[v], 3) for v in ORDER] == [0.0, 1.0, 2.236, 2.5, 3.0, 3.505, 4.562]
snapD = R["snaps"][3]
assert [(n, round(a, 3), round(b, 3)) for n, a, b in snapD["improved"]] == [("G", 5.022, 3.505)]


def queue_at(t):
    """Live queue at time t: for each waypoint not yet on fire with a burning neighbour, the earliest arrival."""
    q = {}
    for u, tu in T.items():
        if tu > t + 1e-9:
            continue
        for v, w in wp_nbrs(u):
            if T[v] > t + 1e-9:
                q[v] = min(q.get(v, math.inf), tu + w)
    return sorted((c, v) for v, c in q.items())


def frame(t, title, lines, path=()):
    fig = go.Figure()
    for tr in furniture_fill() + room_lines(color="#bbb"):
        fig.add_trace(tr)
    for a, b in WP_EDGES:
        (x0, y0), (x1, y1) = WP[a], WP[b]
        fig.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1], mode="lines", line=dict(color="#999", width=2),
                                 hoverinfo="skip"))
        L = wp_dist(a, b)
        fa = float(np.clip((t - T[a]) / L, 0, 1))
        fb = float(np.clip((t - T[b]) / L, 0, 1))
        if fa + fb >= 1:
            fa, fb = 1.0, 0.0
        for (p, q, f) in (((x0, y0), (x1, y1), fa), ((x1, y1), (x0, y0), fb)):
            if f > 0:
                fig.add_trace(go.Scatter(x=[p[0], p[0] + f * (q[0] - p[0])], y=[p[1], p[1] + f * (q[1] - p[1])],
                                         mode="lines", line=dict(color=RED, width=7), hoverinfo="skip"))
    for a, b in zip(path, path[1:]):
        (x0, y0), (x1, y1) = WP[a], WP[b]
        fig.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1], mode="lines", line=dict(color=GREEN, width=11),
                                 hoverinfo="skip"))
    wp_labels(fig, size=14)
    for v, (x, y) in WP.items():
        on = T[v] <= t + 1e-9
        fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers+text", text=[f"<b>{v}</b>"],
                                 marker=dict(size=34, color=RED if on else "white", line=dict(color="#444", width=2)),
                                 textfont=dict(size=18, color="white" if on else "black"), hoverinfo="skip"))
        if on:
            dx, dy = {"S": (0, -0.33), "A": (0, -0.33), "B": (0, -0.33), "D": (-0.55, 0.25), "G": (0, 0.33),
                      "P": (0, 0.33), "C": (0, 0.33)}[v]
            fig.add_annotation(x=x + dx, y=y + dy, text=f"<b>{T[v]:.3f}</b>", showarrow=False, bgcolor="white",
                               font=dict(size=17, color=RED))
    q = queue_at(t)
    qs = " | ".join(f"{v} {c:.3f}" for c, v in q) or "(empty)"
    rows = [(f"priority queue, smallest first: {qs}", ORANGE),
            ("red: on fire (settled), with its time = shortest distance from S in m", RED)] + lines
    fig.update_xaxes(range=[-0.1, 7.1], visible=False)
    fig.update_yaxes(range=[-0.1, 4.55], visible=False, scaleanchor="x")
    fig.update_layout(template="simple_white", width=1000, height=860, font=FONT, showlegend=False,
                      margin=dict(l=20, r=20, t=70, b=240), title=dict(text=title, x=0.5, font=dict(size=22)))
    for i, (s, col) in enumerate(rows):
        fig.add_annotation(x=0.0, y=-0.03 - 0.06 * i, xref="paper", yref="paper", xanchor="left", yanchor="top",
                           showarrow=False, text=s, font=dict(size=19, color=col))
    return fig


def event_lines(k):
    """What settling waypoint k changes, as text lines."""
    s = R["snaps"][k]
    u, c = s["cur"], s["cost"]
    out = []
    for v, w in wp_nbrs(u):
        if v in R["snaps"][k]["settled"][:-1]:
            continue
        new = c + w
        old = R["snaps"][k - 1]["g"].get(v) if k else None
        if old is None:
            out.append(f"{v}: new entry {c:.3f} + {w:.3f} = {new:.3f}")
        elif new < old - 1e-12:
            out.append(f"{v}: {c:.3f} + {w:.3f} = {new:.3f} is less than {old:.3f}: entry lowered")
        else:
            out.append(f"{v}: {c:.3f} + {w:.3f} = {new:.3f}, not less than {old:.3f}: kept")
    return out or ["no neighbour left that is not on fire"]


figs, holds, keys = [], [], []
times = sorted(set(np.round(np.arange(0, 4.7, 0.125), 3)) | {round(v, 6) for v in T.values()})
for t in times:
    events = [k for k, v in enumerate(ORDER) if abs(T[v] - t) < 1e-6]
    if events:
        k = events[0]
        v = ORDER[k]
        title = f"t = {t:.3f} s: {v} catches fire, settled at {t:.3f} m"
        lines = [(s, "black") for s in event_lines(k)]
        figs.append(frame(t, title, lines))
        holds.append(14)
        if v in ("S", "D", "G"):
            keys.append(len(figs) - 1)
    else:
        figs.append(frame(t, f"t = {t:.3f} s: the flames spread at 1 m per second", []))
        holds.append(1)
figs.append(frame(4.75, "every waypoint on fire: each time is its shortest distance from S",
                  [("green: the route to G, read back along the edges the first flames came by: S–D–G = 3.505 m",
                    GREEN), ("G's first entry, 5.022 by the pink pole P, was lowered to 3.505 when D caught fire", GREY)],
                  path=("S", "D", "G")))
holds.append(30)
keys.append(len(figs) - 1)
make_gif(figs, here / "fire.gif", fps=6, holds=holds, keys=keys, cols=2, width=760)
print(len(figs), "frames;", {v: round(T[v], 3) for v in ORDER})
