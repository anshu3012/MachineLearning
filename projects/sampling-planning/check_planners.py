"""Plain checks of the planners, on every world in worlds/ (run: python check_planners.py)."""
import math
import tempfile
from pathlib import Path

import networkx as nx
import numpy as np
import shapely
from PIL import Image

from collision import bisection_order
from planners import path_length

FINE = 0.001  # m: the paths are re-checked with test points 1 mm apart


def check(space, results):
    """Asserts on one run of each planner (the dict from run.run_all). Returns the planners that found no path."""
    for name, r in results.items():
        path = r["path"]
        if not path:
            continue
        assert path[0] == space.start and path[-1] == space.goal, f"{name}: path does not join start to goal"
        for a, b in zip(path, path[1:]):
            t = np.linspace(0, 1, max(2, math.ceil(math.dist(a, b) / FINE) + 1))
            xs, ys = a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])
            assert shapely.contains_xy(space.cfree, xs, ys).all(), f"{name}: segment {a}-{b} hits an obstacle"
        assert math.isclose(r["length"], path_length(space, path)), name
    costs = [e["cost"] for e in results["RRT*"]["events"] if e["cost"] is not None]
    assert all(c1 <= c0 for c0, c1 in zip(costs, costs[1:])), "RRT* cost rose"
    assert not costs or math.isclose(costs[-1], results["RRT*"]["length"])
    missing = [name for name, r in results.items() if not r["path"]]
    if "PRM" in missing:
        return missing
    roadmap = nx.Graph()
    for p, nbrs in results["PRM"]["graph"].items():
        roadmap.add_weighted_edges_from((p, x, w) for x, w in nbrs.items())
    best = nx.shortest_path_length(roadmap, space.start, space.goal, weight="weight")  # Dijkstra, from networkx
    assert math.isclose(results["PRM"]["length"], best), "PRM route is not the shortest in its roadmap"
    return missing


def check_grid_loader():
    """A 6 x 4 grid map with 0.5 m cells and a wall: the loader must put the wall, start and goal where the pixels
    are, in the grid project's coordinates (cell centres at multiples of 0.5 m)."""
    from world import grid_to_world
    px = np.full((4, 6, 3), 255, np.uint8)
    px[0:3, 3] = 0  # a wall in column 3, rows 0-2 (the top three rows)
    px[3, 0] = (0, 255, 0)  # start: bottom-left cell
    px[0, 5] = (255, 0, 0)  # goal: top-right cell
    with tempfile.TemporaryDirectory() as tmp:
        Image.fromarray(px).save(Path(tmp) / "tiny.png")
        (Path(tmp) / "tiny.json").write_text('{"label": "Tiny", "cell_m": 0.5}')
        w = grid_to_world(Path(tmp) / "tiny.png")
    assert w["bounds"] == [-0.25, -0.25, 2.75, 1.75] and w["name"] == "Tiny"
    assert w["start"] == [0.0, 0.0] and w["goal"] == [2.5, 1.5]
    wall = shapely.union_all([shapely.box(*o) for o in w["obstacles"]])
    assert wall.bounds == (1.25, 0.25, 1.75, 1.75) and math.isclose(wall.area, 0.75)


if __name__ == "__main__":
    from run import run_all  # here, not at the top: run.py imports check from this file
    from world import WORLDS, load_world
    assert bisection_order(4) == [4, 0, 2, 1, 3] and sorted(bisection_order(7)) == list(range(8))
    check_grid_loader()
    for f in sorted(WORLDS.glob("*.json")):
        space = load_world(f)
        res = run_all(space)
        assert not check(space, res), f"{space.name}: a planner found no path"
        print(f"{space.name}: ok  " + "  ".join(f"{n} {r['length']:.1f} m" for n, r in res.items()))
