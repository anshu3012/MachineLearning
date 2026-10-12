"""Route planning on road graphs for this Note (no output when run on its own).

A road graph is a dict adj[u] = {v: cost}: one entry per one-way arc u -> v; a two-way street is two arcs.
- astar(): A* with any heuristic h (h = 0 gives Dijkstra), with a trace of every expansion for the animations.
- dists(): one full Dijkstra from a vertex (all costs out of it), or into it on the reversed graph.
- landmark tables and the ALT heuristic (A*, landmarks, triangle inequality).
- contraction hierarchies: contract vertices in an order, add shortcuts found by witness searches, then answer a
  query with two upward searches.
- the small town graph of the Note, and the Chicago street graph from data/chicago.graphml.gz.
"""
import gzip
import heapq
import math
from pathlib import Path

INF = math.inf
DATA = Path(__file__).resolve().parent.parent / "data"


# ---------------------------------------------------------------- graphs
def reverse(adj):
    r = {u: {} for u in adj}
    for u, nb in adj.items():
        for v, c in nb.items():
            r[v][u] = c
    return r


def path_cost(adj, path):
    return sum(adj[a][b] for a, b in zip(path, path[1:]))


# ---------------------------------------------------------------- search
def astar(adj, s, t, h=None, trace=False):
    """A* from s to t (Dijkstra when h is None). Returns dict(cost, path, order, g, snaps).
    order: vertices in the order they come off the open list; snaps[i]: the open list and closed set after
    expansion i (only with trace)."""
    h = h or (lambda u: 0.0)
    g, parent, closed, order, snaps = {s: 0.0}, {s: None}, set(), [], []
    heap = [(h(s), h(s), 0, s)]
    tick = 1
    while heap:
        f, hh, _, u = heapq.heappop(heap)
        if u in closed or g[u] + h(u) < f - 1e-9:
            continue
        closed.add(u)
        order.append(u)
        if u != t:
            for v, c in adj[u].items():
                if v in closed:
                    continue
                ng = g[u] + c
                if ng < g.get(v, INF) - 1e-12:
                    g[v], parent[v] = ng, u
                    heapq.heappush(heap, (ng + h(v), h(v), tick, v))
                    tick += 1
        if trace:
            snaps.append(dict(cur=u, closed=list(order),
                              open={v: (g[v], h(v), g[v] + h(v)) for v in g if v not in closed},
                              parent=dict(parent)))
        if u == t:
            break
    path = []
    if t in closed:
        v = t
        while v is not None:
            path.append(v)
            v = parent[v]
        path.reverse()
    return dict(cost=g.get(t, INF), path=path, order=order, g=g, snaps=snaps)


def dists(adj, s):
    """Every vertex's cost from s (a full Dijkstra)."""
    d, heap = {s: 0.0}, [(0.0, s)]
    done = set()
    while heap:
        du, u = heapq.heappop(heap)
        if u in done:
            continue
        done.add(u)
        for v, c in adj[u].items():
            if du + c < d.get(v, INF):
                d[v] = du + c
                heapq.heappush(heap, (d[v], v))
    return d


# ---------------------------------------------------------------- landmarks (ALT)
def landmark_tables(adj, marks):
    """For each landmark L: (cost from L to every vertex, cost from every vertex to L): one Dijkstra each way."""
    radj = reverse(adj)
    return {L: (dists(adj, L), dists(radj, L)) for L in marks}


def alt_heuristic(tables, t):
    """h(u) = largest lower bound over the landmarks of the cost from u to t, by the triangle inequality:
    cost(u, t) >= cost(u, L) - cost(t, L) and cost(u, t) >= cost(L, t) - cost(L, u)."""
    def h(u):
        best = 0.0
        for frm, to in tables.values():
            best = max(best, to.get(u, INF) - to.get(t, INF) if to.get(u, INF) < INF else 0.0,
                       frm.get(t, INF) - frm.get(u, INF) if frm.get(t, INF) < INF else 0.0)
        return best
    return h


def farthest_landmarks(adj, k, first):
    """Pick k landmarks spread over the graph: start from the vertex farthest from `first`, then repeatedly the
    vertex whose cost to the nearest chosen landmark is largest (Goldberg and Harrelson's 'farthest' rule)."""
    radj = reverse(adj)

    def both(s):                      # cost there and back, so one-way streets count both ways
        back = dists(radj, s)
        return {v: d + back.get(v, INF) for v, d in dists(adj, s).items()}
    d0 = both(first)
    marks = [max(d0, key=d0.get)]
    near = both(marks[0])
    while len(marks) < k:
        nxt = max(near, key=near.get)
        marks.append(nxt)
        dn = both(nxt)
        near = {v: min(near[v], dn.get(v, INF)) for v in near}
    return marks


# ---------------------------------------------------------------- contraction hierarchies
def _witness(out, rank, src, skip, low, limit):
    """Costs from src using only vertices ranked above `low`, never `skip`, stopping beyond `limit`."""
    d, heap, done = {src: 0.0}, [(0.0, src)], set()
    while heap:
        du, u = heapq.heappop(heap)
        if u in done or du > limit:
            continue
        done.add(u)
        for v, c in out[u].items():
            if v == skip or rank.get(v, INF) <= low:
                continue
            if du + c < d.get(v, INF):
                d[v] = du + c
                heapq.heappush(heap, (d[v], v))
    return d


def _shortcuts(out, inn, rank, v):
    """Shortcuts that contracting v needs: for each arc u -> v and v -> w between vertices still in the graph,
    a shortcut u -> w unless a witness path u ~> w that avoids v is at least as cheap."""
    low = rank[v]
    ins = [(u, c) for u, c in inn[v].items() if rank.get(u, INF) > low]
    outs = [(w, c) for w, c in out[v].items() if rank.get(w, INF) > low]
    need, witnessed = [], []
    for u, cu in ins:
        targets = [(w, cw) for w, cw in outs if w != u]
        if not targets:
            continue
        d = _witness(out, rank, u, v, low, cu + max(cw for _, cw in targets))
        for w, cw in targets:
            via = cu + cw
            if d.get(w, INF) > via + 1e-9:
                need.append((u, w, via))
            else:
                witnessed.append((u, w, via, d[w]))
    return need, witnessed, len(ins) + len(outs)


def contract(adj, order=None):
    """Contract every vertex, in `order` if given, else by edge difference (shortcuts added minus arcs removed,
    plus the number of neighbours already contracted, re-checked lazily). Returns dict(rank, out, inn, mid,
    events): out/inn hold the original arcs plus the shortcuts; mid[(u, w)] = v for a shortcut made by
    contracting v; events[i] = (v, shortcuts added, witnessed pairs)."""
    out = {u: dict(nb) for u, nb in adj.items()}
    inn = reverse(adj)
    mid, events = {}, []
    if order is not None:
        rank = {v: i for i, v in enumerate(order)}
        seq = list(order)
    else:
        rank = {v: INF for v in adj}
        deleted = {v: 0 for v in adj}
        tmp = len(adj) + 1

        def prio(v):
            rank[v] = tmp                              # pretend v goes next, everything else is above
            need, _, deg = _shortcuts(out, inn, rank, v)
            rank[v] = INF
            return len(need) - deg + deleted[v]
        heap = [(prio(v), i, v) for i, v in enumerate(adj)]
        heapq.heapify(heap)
        seq = []
    i = 0
    while True:
        if order is not None:
            if i == len(seq):
                break
            v = seq[i]
        else:
            if not heap:
                break
            p, k, v = heapq.heappop(heap)
            q = prio(v)
            if heap and q > heap[0][0]:
                heapq.heappush(heap, (q, k, v))
                continue
            rank[v] = i
            seq.append(v)
        need, witnessed, _ = _shortcuts(out, inn, rank, v)
        added = []
        for u, w, via in need:
            if via < out[u].get(w, INF) - 1e-12:
                out[u][w] = via
                inn[w][u] = via
                mid[(u, w)] = v
                added.append((u, w, via))
        events.append((v, added, witnessed))
        if order is None:
            for x in set(out[v]) | set(inn[v]):
                if rank.get(x, INF) == INF:
                    deleted[x] += 1
        i += 1
    if order is None:
        rank = {v: k for k, v in enumerate(seq)}
    return dict(rank=rank, out=out, inn=inn, mid=mid, events=events, order=seq)


def unpack(mid, u, w):
    """The original vertices of the arc u -> w: a shortcut is replaced by its two halves, recursively."""
    if (u, w) not in mid:
        return [u, w]
    v = mid[(u, w)]
    return unpack(mid, u, v)[:-1] + unpack(mid, v, w)


def ch_query(ch, s, t):
    """Two searches that only climb: from s along arcs to higher-ranked vertices, from t backwards along arcs that
    come from higher-ranked vertices, one step of each in turn. A vertex settled by both gives a route; a search
    stops once its smallest open cost is at least the best route so far (Geisberger et al. 2008).
    Returns dict(cost, top, path, hops, fwd, bwd, steps): fwd/bwd are each search's settled vertices in order,
    steps the (side, vertex) sequence."""
    rank = ch["rank"]
    nbrs = (ch["out"], ch["inn"])
    d = ({s: 0.0}, {t: 0.0})
    par = ({s: None}, {t: None})
    heaps = ([(0.0, s)], [(0.0, t)])
    done = (set(), set())
    orders = ([], [])
    steps = []
    best, top, side = INF, None, 0
    while heaps[0] or heaps[1]:
        if heaps[side] and heaps[side][0][0] >= best:
            heaps[side].clear()
        if not heaps[side]:
            side ^= 1
            continue
        du, u = heapq.heappop(heaps[side])
        if u in done[side]:
            continue
        done[side].add(u)
        orders[side].append(u)
        steps.append((side, u))
        if u in done[side ^ 1] and du + d[side ^ 1][u] < best:
            best, top = du + d[side ^ 1][u], u
        for v, c in nbrs[side][u].items():
            if rank[v] > rank[u] and du + c < d[side].get(v, INF):
                d[side][v], par[side][v] = du + c, u
                heapq.heappush(heaps[side], (du + c, v))
        side ^= 1
    up, v = [], top
    while v is not None:
        up.append(v)
        v = par[0][v]
    up.reverse()
    down, v = [], par[1][top]
    while v is not None:
        down.append(v)
        v = par[1][v]
    hops = up + down
    path = [s]
    for a, b in zip(hops, hops[1:]):
        path += unpack(ch["mid"], a, b)[1:]
    return dict(cost=best, top=top, path=path, hops=hops, fwd=orders[0], bwd=orders[1], steps=steps,
                df=d[0], db=d[1])


# ---------------------------------------------------------------- the town of the Note
KMH = {"bypass": 80, "main": 50, "old": 30}
TOWN_POS = {"S": (0, 600), "A": (500, 600), "B": (1000, 600), "C": (1500, 600), "D": (2000, 600),
            "T": (2500, 600), "E": (1000, 200), "F": (1500, 200), "N": (500, 1000), "M": (2000, 1000),
            "L": (3000, 1000)}
# (a, b, road type, length in m, one_way): each length is at least the straight line between its ends
TOWN_ROADS = [("S", "A", "main", 500), ("A", "B", "old", 500), ("B", "C", "old", 500), ("C", "D", "old", 500),
              ("D", "T", "main", 500), ("A", "N", "main", 400), ("N", "M", "bypass", 1500),
              ("M", "D", "main", 400), ("M", "L", "bypass", 1000), ("L", "T", "main", 650),
              ("B", "E", "old", 400), ("E", "F", "old", 500), ("F", "C", "old", 400)]
ONE_WAY = {("F", "C")}            # one-way streets: this arc exists, its reverse does not
CH_ORDER = list("EFBCSTLADNM")    # old town first, then the ends, the junctions, the bypass last


def town(weight="time"):
    """adj for the town: weight 'time' (s) or 'length' (m). ONE_WAY arcs exist in one direction only."""
    adj = {v: {} for v in TOWN_POS}
    for a, b, kind, length in TOWN_ROADS:
        c = length / (KMH[kind] / 3.6) if weight == "time" else float(length)
        for u, v in ((a, b), (b, a)):
            if ((v, u) in ONE_WAY):
                continue
            adj[u][v] = c
    return adj


def town_vmax():
    return max(KMH.values()) / 3.6


def straight(pos, t, speed=1.0):
    """Straight-line distance to t, divided by speed (speed 1: metres; the top speed: seconds)."""
    tx, ty = pos[t]
    return lambda u: math.dist(pos[u], (tx, ty)) / speed


# ---------------------------------------------------------------- Chicago
def chicago():
    """The Chicago street graph: OpenStreetMap drivable streets within 2.5 km of (41.8819 N, 87.6300 W), saved
    with OSMnx. Returns dict(adj_time, adj_len, pos, speed_kmh, kind, lines): the largest strongly connected
    part (every intersection can reach every other), one arc per direction a car may drive, its length measured
    along the street in metres (projected), its time in s at the street's speed limit (OSM maxspeed where
    tagged, otherwise OSMnx's average for the road type)."""
    import networkx as nx
    import osmnx as ox
    with gzip.open(DATA / "chicago.graphml.gz", "rt", encoding="utf-8") as f:
        raw = ox.load_graphml(graphml_str=f.read())
    P = ox.add_edge_travel_times(ox.add_edge_speeds(ox.project_graph(raw)))
    x0 = min(d["x"] for _, d in P.nodes(data=True))
    y0 = min(d["y"] for _, d in P.nodes(data=True))
    pos = {n: (d["x"] - x0, d["y"] - y0) for n, d in P.nodes(data=True)}
    G = nx.DiGraph()
    best = {}
    tagged = sum(1 for *_, d in P.edges(keys=True, data=True) if "maxspeed" in d)
    for u, v, k, d in P.edges(keys=True, data=True):
        if u == v:
            continue
        if "geometry" in d:
            pts = [(x - x0, y - y0) for x, y in d["geometry"].coords]
            length = d["geometry"].length
        else:
            pts = [pos[u], pos[v]]
            length = math.dist(pos[u], pos[v])
        kind = d["highway"] if isinstance(d["highway"], str) else d["highway"][0]
        tt = length / (d["speed_kph"] / 3.6)
        if (u, v) not in best or tt < best[(u, v)][0]:
            best[(u, v)] = (tt, length, d["speed_kph"], kind, pts)
    for (u, v), (tt, length, sp, kind, pts) in best.items():
        G.add_edge(u, v)
    keep = max(nx.strongly_connected_components(G), key=len)
    adj_t = {u: {} for u in keep}
    adj_l = {u: {} for u in keep}
    speed, kind, lines = {}, {}, {}
    for (u, v), (tt, length, sp, kd, pts) in best.items():
        if u in keep and v in keep:
            adj_t[u][v], adj_l[u][v] = tt, length
            speed[(u, v)], kind[(u, v)], lines[(u, v)] = sp, kd, pts
    return dict(adj_time=adj_t, adj_len=adj_l, pos={n: pos[n] for n in keep}, speed_kmh=speed, kind=kind,
                lines=lines, raw_nodes=P.number_of_nodes(), raw_edges=P.number_of_edges(), tagged=tagged)


def nearest(pos, xy):
    return min(pos, key=lambda n: math.dist(pos[n], xy))
