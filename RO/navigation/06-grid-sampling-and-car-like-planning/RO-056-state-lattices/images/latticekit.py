"""The state lattice of this Note (no output when run on its own).

Lattice states: positions on whole metres and 8 headings, multiples of 45 deg (index h = 0..7). The control set, worked
out once before planning: from a heading along an axis, a 1 m straight move, two 45 deg turns and two 90 deg turns; from
a diagonal heading, a 1.414 m straight move and two 45 deg turns; each forward, and each also in reverse (the same
shape mirrored). Every turn uses arcs of the 5 m circle, joined to straight pieces chosen so that the move ends exactly
on a lattice state. For each start heading the cells of a 0.1 m map covered by the car's body during each move (its
swath) are also worked out once; checking a move during the search is then a look-up. The search is A* (RO-034) with
the cost and the guess of RO-055: length, reverse x2, +2 m per switch; max(Reeds-Shepp length, grid distance)."""
import heapq
import math

import numpy as np
from carkit import (CAR_L, CAR_W, GOAL, LOT_H, LOT_W, MARGIN, OBS, REAR_OH, REV_MULT, RHO, START, SWITCH, collides,
                    h_grid, rs_length)
from carpaths import step

NH = 8
DIRS = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]   # lattice direction of each heading


def turn_piece(h0, dh, rho=RHO):
    """A forward move from heading index h0 turning by dh * 45 deg (dh = +-1, +-2): straight a, arc, straight b,
    with a, b >= 0 as short as possible such that the end is a whole-metre point. Returns (a, b, (X, Y))."""
    th0, th1 = h0 * math.pi / 4, (h0 + dh) * math.pi / 4
    turn = th1 - th0
    kind = "L" if turn > 0 else "R"
    ax, ay, _ = step((0.0, 0.0, th0), kind, abs(turn) * rho, rho)         # the arc alone
    u0, u1 = np.array([math.cos(th0), math.sin(th0)]), np.array([math.cos(th1), math.sin(th1)])
    m = np.column_stack([u0, u1])
    best = None
    for X in range(-12, 13):
        for Y in range(-12, 13):
            a, b = np.linalg.solve(m, np.array([X - ax, Y - ay]))
            if a > -1e-9 and b > -1e-9:
                total = a + b
                if best is None or total < best[0] - 1e-12:
                    best = (total, max(a, 0.0), max(b, 0.0), (X, Y))
    return best[1], best[2], best[3]


def forward_set(h):
    """The forward moves from heading index h: list of (name, segments, (dX, dY), dh)."""
    out = []
    dx, dy = DIRS[h]
    out.append(("straight", [("S", math.hypot(dx, dy))], (dx, dy), 0))
    turns = (1, -1, 2, -2) if h % 2 == 0 else (1, -1)
    for dh in turns:
        a, b, end = turn_piece(h, dh)
        kind = "L" if dh > 0 else "R"
        segs = [s for s in (("S", a), (kind, abs(dh) * math.pi / 4 * RHO), ("S", b)) if s[1] > 1e-9]
        out.append((f"{'left' if dh > 0 else 'right'} {45 * abs(dh)}", segs, end, dh))
    return out


def mirror(h, segs, end, dh):
    """The same move driven in reverse: mirrored across the car's sideways axis. Ends on a lattice state too."""
    th = h * math.pi / 4
    c, s = math.cos(th), math.sin(th)
    fx, fy = c * end[0] + s * end[1], -s * end[0] + c * end[1]          # in the car's own frame
    fx = -fx
    X, Y = c * fx - s * fy, s * fx + c * fy
    return [(k, -v) for k, v in segs], (int(round(X)), int(round(Y))), -dh


def control_set(h):
    """Every move of the control set from heading index h: dicts with name, direction, segments, end, dh, length."""
    out = []
    for name, segs, end, dh in forward_set(h):
        L = sum(v for _, v in segs)
        out.append(dict(name=name, d=1, segs=segs, end=end, dh=dh, length=L))
        rs, rend, rdh = mirror(h, segs, end, dh)
        out.append(dict(name=name, d=-1, segs=rs, end=rend, dh=rdh, length=L))
    for p in out:                                                      # every move must land exactly on a state
        x, y, th = 0.0, 0.0, h * math.pi / 4
        for k, v in p["segs"]:
            x, y, th = step((x, y, th), k, v, RHO)
        assert abs(x - p["end"][0]) < 1e-9 and abs(y - p["end"][1]) < 1e-9
        assert abs(math.remainder(th - (h + p["dh"]) * math.pi / 4, 2 * math.pi)) < 1e-9
    return out


CONTROL = {h: control_set(h) for h in range(NH)}


def move_poses(x, y, h, move, ds=0.05):
    """Poses every ds metres along a move from the lattice state (x, y, h)."""
    p = (float(x), float(y), h * math.pi / 4)
    out = [p]
    for k, v in move["segs"]:
        n = max(1, int(math.ceil(abs(v) / ds)))
        for i in range(1, n + 1):
            out.append(step(p, k, v * i / n, RHO))
        p = out[-1]
    return np.array(out)


# ---------------------------------------------------------------- swaths on a 0.1 m map
RES = 0.1
MX, MY = int(round(LOT_W / RES)), int(round(LOT_H / RES))
_cx = (np.arange(MX) + 0.5) * RES
_cy = (np.arange(MY) + 0.5) * RES
OCC = np.zeros((MY, MX), dtype=bool)                                   # OCC[j, i]: cell centre inside an obstacle
for x0, x1, y0, y1 in OBS:
    OCC[np.ix_((_cy >= y0) & (_cy <= y1), (_cx >= x0) & (_cx <= x1))] = True


def body_cells(pose):
    """Offsets (i, j), in 0.1 m cells from the lattice point at the origin, of every map cell whose centre the body,
    grown by the 0.1 m margin of RO-055, covers at this pose (the pose is relative to the lattice point)."""
    x, y, th = pose
    c, s = math.cos(th), math.sin(th)
    r = math.hypot(CAR_L, CAR_W)
    i0, i1 = int(math.floor((x - r) / RES)), int(math.ceil((x + r) / RES))
    j0, j1 = int(math.floor((y - r) / RES)), int(math.ceil((y + r) / RES))
    ii, jj = np.meshgrid(np.arange(i0, i1 + 1), np.arange(j0, j1 + 1))
    px, py = (ii + 0.5) * RES - x, (jj + 0.5) * RES - y               # cell centre relative to the rear axle
    along, side = px * c + py * s, -px * s + py * c
    m = (along >= -REAR_OH - MARGIN) & (along <= CAR_L - REAR_OH + MARGIN) & (np.abs(side) <= CAR_W / 2 + MARGIN)
    return set(zip(ii[m].tolist(), jj[m].tolist()))


def swath(h, move):
    cells = set()
    for p in move_poses(0, 0, h, move, ds=0.05):
        cells |= body_cells(p)
    return np.array(sorted(cells))


SWATH = {(h, k): swath(h, mv) for h in range(NH) for k, mv in enumerate(CONTROL[h])}


def swath_free(x, y, h, k):
    """Look up the move's swath at the lattice point (x, y): free when no covered cell is occupied or off the map.
    Lattice points are whole metres, so the swath shifts by exactly 10 cells per metre."""
    sw = SWATH[(h, k)]
    # the cell (i, j) with centre ((i + 0.5) 0.1, (j + 0.5) 0.1) relative to the lattice point sits at map cell
    # (i + 10 x, j + 10 y); centres are on the half cell, matching the map's centres
    ii, jj = sw[:, 0] + int(round(x / RES)), sw[:, 1] + int(round(y / RES))
    if ii.min() < 0 or jj.min() < 0 or ii.max() >= MX or jj.max() >= MY:
        return False
    return not bool(OCC[jj, ii].any())


# ---------------------------------------------------------------- search
def heuristic(x, y, h):
    p = (float(x), float(y), h * math.pi / 4)
    return max(rs_length(p), h_grid(p))


def move_cost(move, prev_d):
    c = move["length"] * (REV_MULT if move["d"] < 0 else 1.0)
    if prev_d is not None and prev_d != move["d"]:
        c += SWITCH
    return c


def lattice_astar(start=(2, 3, 0), goal=(12, 23, 6), trace=False, hfun=heuristic):
    """A* over lattice states (x, y, heading index, last direction). Returns the moves of the cheapest path in the
    lattice, its cost and length, the expansions and, with trace, the order of expansions."""
    s0 = (start[0], start[1], start[2], 0)
    g, parent = {s0: 0.0}, {s0: None}
    heap = [(hfun(*start), 0, s0)]
    closed, count, log = set(), 1, []
    found = None
    while heap:
        _, _, s = heapq.heappop(heap)
        if s in closed:
            continue
        closed.add(s)
        x, y, h, d = s
        kids = []
        if trace:
            log.append(dict(state=s, kids=kids))
        if (x, y, h) == tuple(goal):
            found = s
            break
        for k, mv in enumerate(CONTROL[h]):
            if not swath_free(x, y, h, k):
                kids.append((k, "blocked"))
                continue
            n = (x + mv["end"][0], y + mv["end"][1], (h + mv["dh"]) % NH, mv["d"])
            ng = g[s] + move_cost(mv, d if d != 0 else None)
            if n not in closed and ng < g.get(n, math.inf) - 1e-12:
                g[n], parent[n] = ng, (s, k)
                heapq.heappush(heap, (ng + hfun(n[0], n[1], n[2]), count, n))
                count += 1
                kids.append((k, "added"))
            else:
                kids.append((k, "dropped"))
    out = dict(expanded=len(closed), found=found is not None, log=log, generated=count)
    if found is None:
        return out
    moves, s = [], found
    while parent[s] is not None:
        ps, k = parent[s]
        moves.append((ps, k))
        s = ps
    moves.reverse()
    out.update(moves=moves, cost=g[found], length=sum(CONTROL[ps[2]][k]["length"] for ps, k in moves))
    poses = [np.array([[start[0], start[1], start[2] * math.pi / 4]])]
    for ps, k in moves:
        poses.append(move_poses(ps[0], ps[1], ps[2], CONTROL[ps[2]][k])[1:])
    out["poses"] = np.vstack(poses)
    out["dirs"] = [CONTROL[ps[2]][k]["d"] for ps, k in moves]
    out["cusps"] = int(sum(a != b for a, b in zip(out["dirs"], out["dirs"][1:])))
    out["exact_free"] = not bool(np.any(collides(out["poses"])))
    return out
