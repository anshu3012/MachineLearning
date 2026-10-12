"""Street maps behind the map interface of projects/grid-pathfinding/map_interface.py.

load_map(name) reads data/<name>.graphml.gz and data/<name>.json (made by get_map.py) into a StreetMap: a node is an
intersection, an edge is a street between two intersections, its cost is the street's length in metres, or with
weight="travel_time" the seconds it takes at the street's speed. Every street is treated as two-way. to_grid(streets) turns the same map into a grid (streets free, blocks blocked) for
the searches that need a grid. FreeSpace is the hook for sampling planners such as RRT and PRM."""
import gzip
import json
import math
import sys
from pathlib import Path

import networkx as nx
import numpy as np
import osmnx as ox
import shapely
from shapely.geometry import LineString

HERE = Path(__file__).resolve().parent
sys.path.append(str(HERE.parent / "grid-pathfinding"))   # the shared algorithms, map interface and grid
from grid import Grid                                    # noqa: E402
from map_interface import Map                            # noqa: E402

DATA = HERE / "data"


class StreetMap(Map):
    def __init__(self, G, name, info, weight="length"):
        """G: an undirected networkx graph whose nodes have x, y (metres) and whose edges have length (metres),
        travel_time (seconds) and line (the street's points from one end to the other). weight picks the cost."""
        self.G, self.name, self.info, self.weight = G, name, info, weight
        self.top_speed = max(d["length"] / d["travel_time"] for _, _, d in G.edges(data=True))   # metres per second
        self.label = info["label"]
        self.start, self.goal = info["start"]["node"], info["goal"]["node"]
        self.goals = tuple(g["node"] for g in info["goals"])

    def nodes(self):
        return list(self.G.nodes)

    def neighbours(self, node):
        return list(self.G.adj[node])

    def cost(self, a, b):
        return self.G.edges[a, b][self.weight]

    def heuristic(self, a, b):
        """Metres: the straight line. Seconds: the straight line driven at the map's top speed; no street is
        faster, so it never overestimates (but it is loose: most streets are much slower)."""
        d = math.dist(self.xy(a), self.xy(b))
        return d if self.weight == "length" else d / self.top_speed

    def xy(self, node):
        d = self.G.nodes[node]
        return (d["x"], d["y"])

    def edge_xy(self, a, b):
        if not self.G.has_edge(a, b):
            return [self.xy(a), self.xy(b)]
        pts = self.G.edges[a, b]["line"]
        return pts if math.dist(pts[0], self.xy(a)) <= math.dist(pts[-1], self.xy(a)) else pts[::-1]


def load_map(name="chicago", weight="length"):
    """data/<name>.graphml.gz -> StreetMap, in metres (UTM, shifted so the south-west corner is at 0, 0).
    Speeds: OSMnx's add_edge_speeds reads each street's OSM maxspeed tag and fills in the missing ones with the
    average of streets of the same road type; add_edge_travel_times divides length by speed."""
    info = json.loads((DATA / f"{name}.json").read_text())
    with gzip.open(DATA / f"{name}.graphml.gz", "rt", encoding="utf-8") as f:
        raw = ox.load_graphml(graphml_str=f.read())
    P = ox.project_graph(raw)
    for u, v, k, d in P.edges(keys=True, data=True):
        # the length measured along the drawn line, so the straight-line guess can never be longer than a street
        d["length"] = d["geometry"].length if "geometry" in d else math.dist(
            (P.nodes[u]["x"], P.nodes[u]["y"]), (P.nodes[v]["x"], P.nodes[v]["y"]))
    P = ox.add_edge_travel_times(ox.add_edge_speeds(P))
    x0 = min(d["x"] for _, d in P.nodes(data=True))
    y0 = min(d["y"] for _, d in P.nodes(data=True))
    G = nx.Graph()
    for n, d in P.nodes(data=True):
        G.add_node(n, x=d["x"] - x0, y=d["y"] - y0)
    for u, v, d in P.edges(data=True):
        if u == v:
            continue                       # a loop back to the same intersection never helps a route
        if "geometry" in d:
            pts = [(x - x0, y - y0) for x, y in d["geometry"].coords]
        else:
            pts = [(G.nodes[u]["x"], G.nodes[u]["y"]), (G.nodes[v]["x"], G.nodes[v]["y"])]
        if not G.has_edge(u, v):
            G.add_edge(u, v, length=d["length"], travel_time=d["travel_time"], line=pts)
        else:                              # two streets join the same intersections: keep the best of each
            e = G.edges[u, v]
            if d["length"] < e["length"]:
                e["length"], e["line"] = d["length"], pts
            e["travel_time"] = min(e["travel_time"], d["travel_time"])
    return StreetMap(G, name, info, weight)


def to_grid(sm, cell=15.0):
    """The street map as a grid of cell x cell metre squares: a cell is free if its centre is within 0.75 cell of a
    street, so every street becomes a band of free cells joined side to side. Start and goal are the cells under the
    map's start and goal."""
    xs, ys = zip(*(sm.xy(n) for n in sm.nodes()))
    cols, rows = int(max(xs) // cell) + 1, int(max(ys) // cell) + 1
    lines = shapely.union_all([LineString(d["line"]) for _, _, d in sm.G.edges(data=True)])
    band = shapely.buffer(lines, 0.75 * cell)
    cx, cy = np.meshgrid(np.arange(cols) * cell, (rows - 1 - np.arange(rows)) * cell)
    free = shapely.contains_xy(band, cx, cy)
    at = lambda n: (round(sm.xy(n)[0] / cell), rows - 1 - round(sm.xy(n)[1] / cell))
    return Grid(free, cell=cell, start=at(sm.start), goal=at(sm.goal), name=f"{sm.name}-grid", label=sm.label)


class FreeSpace:
    """Hook for the sampling planners of projects/sampling-planning (RRT, RRT*, PRM): the streets as continuous
    free space. A planner samples points (x, y) in metres inside bounds, keeps those where free(x, y), joins two
    points when segment_free(p, q), and logs ("look", p, q, True, 0) for every tree or roadmap edge it adds. Drawing
    it on the map is then render.animate(streets, FreeSpace(...), result, out), as for the graph searches."""

    def __init__(self, sm, cell=5.0):
        self.grid = to_grid(sm, cell)
        self.cell = cell
        rows, cols = self.grid.free.shape
        self.bounds = (0.0, (cols - 1) * cell, 0.0, (rows - 1) * cell)   # x min, x max, y min, y max

    def _cell(self, p):
        return (round(p[0] / self.cell), self.grid.free.shape[0] - 1 - round(p[1] / self.cell))

    def free(self, x, y):
        return self.grid.passable(*self._cell((x, y)))

    def segment_free(self, p, q):
        return self.grid.line_of_sight(self._cell(p), self._cell(q))

    def xy(self, p):
        return p

    def edge_xy(self, p, q):
        return [p, q]
