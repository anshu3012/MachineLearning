"""RRT growing through Chicago's streets, and the elastic band rounding a corner of a street route. Both are the
sampling project's own (projects/sampling-planning/planners.py and local_planner.py, imported, not copied); they run
in the streets as continuous free space, streets.FreeSpace. The RRT is drawn like the searches, with render.animate.

    python sampling_on_streets.py                      # the West Loop map: images/chicago-west-loop/rrt.gif
    python sampling_on_streets.py --map chicago        # the whole map: numbers only, RRT hardly grows there
    python sampling_on_streets.py --band               # the elastic band: images/chicago-west-loop/band_corner.gif
"""
import argparse
import math
import statistics
import sys
from pathlib import Path

import numpy as np

from streets import FreeSpace, load_map
import algorithms as A                     # noqa: E402  (found through the path streets.py adds)

HERE = Path(__file__).resolve().parent
sys.path.append(str(HERE.parent / "sampling-planning"))  # appended, so this folder's render.py and run.py come first
from local_planner import elastic_band     # noqa: E402
from planners import rrt                   # noqa: E402

STEP, SEED, CELL = 25.0, 2, 5.0             # metres per tree step, the seed drawn, FreeSpace cell (m)


class StreetSpace:
    """streets.FreeSpace behind the planners' interface: sample, distance, steer, free, segment_free, checks.
    A point is free on a street cell; a straight step is free when every cell it crosses is (one check each)."""

    def __init__(self, fs):
        self.fs, self.checks = fs, 0

    def sample(self, rng):
        x0, x1, y0, y1 = self.fs.bounds
        return (rng.uniform(x0, x1), rng.uniform(y0, y1))

    def distance(self, a, b):
        return math.dist(a, b)

    def steer(self, a, b, step):
        d = math.dist(a, b)
        return b if d <= step else (a[0] + step / d * (b[0] - a[0]), a[1] + step / d * (b[1] - a[1]))

    def free(self, p):
        self.checks += 1
        return self.fs.free(*p)

    def segment_free(self, a, b):
        self.checks += 1
        return self.fs.segment_free(a, b)


def as_result(r):
    """The RRT's events as a search log: every tree edge is a move that was looked at and added."""
    log = A.Log()
    for e in r["events"]:
        for child, parent in e["set"]:
            log.look(parent, child, True)
    return A.Result("RRT", r["path"] or [], r["length"] or 0.0, log, {"samples": r["samples"]})


def free_directions(fs, p, length, n=360):
    """How many of n evenly spread directions a straight step of this length can take from p."""
    return sum(fs.segment_free(p, (p[0] + length * math.cos(2 * math.pi * k / n),
                                   p[1] + length * math.sin(2 * math.pi * k / n))) for k in range(n))


def main(map_name="chicago-west-loop", draw=True, seeds=range(1, 11), max_samples=100_000):
    sm = load_map(map_name)
    fs = FreeSpace(sm, CELL)
    space = StreetSpace(fs)
    s, g = sm.xy(sm.start), sm.xy(sm.goal)
    best = A.a_star(sm, sm.start, sm.goal)
    print(f"{sm.label}: {fs.bounds[1]:,.0f} m x {fs.bounds[3]:,.0f} m, {100 * fs.grid.free.mean():.1f} percent of "
          f"the {CELL:g} m cells are street; start to goal {math.dist(s, g):,.0f} m in a straight line, "
          f"{best.length:,.0f} m by the shortest street route; a {STEP:g} m step from the start can point "
          f"{free_directions(fs, s, STEP)} ways of 360")
    runs = [rrt(space, s, g, STEP, seed, max_samples=max_samples) for seed in seeds]
    nodes = [1 + sum(len(e["set"]) for e in r["events"]) for r in runs]
    ok = [(r, n) for r, n in zip(runs, nodes) if r["path"]]
    print(f"RRT, {STEP:g} m steps, seeds {seeds.start}-{seeds.stop - 1}: {len(ok)} of {len(runs)} reached the goal "
          f"within {max_samples:,} samples" + (
              f"; median {statistics.median(r['samples'] for r, _ in ok):,.0f} samples, "
              f"{statistics.median(n for _, n in ok):,.0f} nodes, "
              f"route {statistics.median(r['length'] for r, _ in ok):,.0f} m" if ok
              else f"; median tree {statistics.median(nodes):,.0f} nodes"))
    for x in runs:  # every route runs from start to goal and every step of it stays on the streets
        assert not x["path"] or (x["path"][0] == s and x["path"][-1] == g and
                                 all(fs.segment_free(a, b) for a, b in zip(x["path"], x["path"][1:])))
    r = runs[list(seeds).index(SEED)]
    n = nodes[list(seeds).index(SEED)]
    print(f"seed {SEED}: {r['samples']:,} samples, {n:,} nodes, " +
          (f"route {r['length']:,.0f} m ({r['length'] / best.length:.2f} times the shortest street route)"
           if r["path"] else "no route"))
    if draw and r["path"]:
        import render
        out = HERE / "images" / sm.name
        out.mkdir(parents=True, exist_ok=True)
        render.animate(sm, fs, as_result(r), out / "rrt", what="tree edges",
                       numbers=f"{r['samples']:,} samples  ·  {n:,} nodes  ·  route {r['length'] / 1000:.2f} km")
    return r


BAND_SPACING, BAND_CAP, BAND_MARGIN, BAND_AROUND = 2.0, 3.0, 2.5, 60.0   # metres


def route_line(sm, route):
    """The street route as points: every street's own points, joined end to end."""
    pieces = [sm.edge_xy(a, b) for a, b in zip(route, route[1:])]
    return np.array([pieces[0][0]] + [p for e in pieces for p in e[1:]], float)


def corner_band(map_name="chicago-west-loop", draw=True):
    """The sampling project's elastic band on the first corner of the shortest street route that turns more than
    60 degrees: the route from BAND_AROUND m before the corner to BAND_AROUND m after it. A point is free when it and
    the four points BAND_MARGIN m (half a cell) away in x and y lie on street cells, so a straight piece between two
    free points never squeezes between two blocked cells."""
    sm = load_map(map_name)
    fs = FreeSpace(sm, CELL)
    best = A.a_star(sm, sm.start, sm.goal)
    P = route_line(sm, best.route)
    d = np.diff(P, axis=0)
    S = np.concatenate([[0], np.cumsum(np.hypot(*d.T))])
    heading = np.arctan2(d[:, 1], d[:, 0])
    turn = np.degrees(np.abs((np.diff(heading) + np.pi) % (2 * np.pi) - np.pi))
    k = int(np.argmax(turn > 60)) + 1                       # the corner: the route's point where it turns
    s0, s1 = S[k] - BAND_AROUND, S[k] + BAND_AROUND
    at = lambda s: (np.interp(s, S, P[:, 0]), np.interp(s, S, P[:, 1]))
    Q = np.array([at(s0)] + [tuple(p) for p in P[(S > s0) & (S < s1)]] + [at(s1)])
    street = np.vectorize(fs.free)
    ok = lambda x, y: (street(x, y) & street(x + BAND_MARGIN, y) & street(x - BAND_MARGIN, y)
                       & street(x, y + BAND_MARGIN) & street(x, y - BAND_MARGIN))
    hist, B = elastic_band(Q, ok, spacing=BAND_SPACING, cap=BAND_CAP, tol=0.01)
    length = lambda X: float(np.sum(np.hypot(*np.diff(X, axis=0).T)))
    assert all(fs.segment_free(a, b) for a, b in zip(B, B[1:])) and (B[[0, -1]] == Q[[0, -1]]).all()
    cut = max(np.hypot(*(B - P[k]).T).min(), 0)
    print(f"{sm.label}: the shortest street route ({best.length:,.0f} m) first turns {turn[k - 1]:.0f} degrees at "
          f"({P[k][0]:.0f}, {P[k][1]:.0f}), {S[k]:.0f} m from the start; the band on the {2 * BAND_AROUND:.0f} m round "
          f"it: {len(hist)} solves, {length(Q):.1f} m -> {length(B):.1f} m, passing {cut:.1f} m from the corner "
          f"point; points {BAND_SPACING:g} m apart, each moving at most {BAND_CAP:g} m sideways per solve")
    if draw:
        import render
        out = HERE / "images" / sm.name
        out.mkdir(parents=True, exist_ok=True)
        render.band_corner(sm, fs, Q, hist, B, out / "band_corner")
    return Q, hist, B


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--map", default="chicago-west-loop")
    ap.add_argument("--no-gif", action="store_true")
    ap.add_argument("--band", action="store_true", help="the elastic band on a corner of the street route")
    a = ap.parse_args()
    if a.band:
        corner_band(a.map, not a.no_gif)
    elif a.map == "chicago-west-loop":
        main(a.map, not a.no_gif)
    else:  # ponytail: the whole map gets 3 seeds of 40,000 samples, enough to show the tree hardly grows
        main(a.map, not a.no_gif, seeds=range(1, 4), max_samples=40_000)
