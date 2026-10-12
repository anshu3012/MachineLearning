"""The grid planners of this Note on the room grid (no output when run on its own).

The grid is chapter RO-04's: the room in 0.5 m cells, 76 free, start cell S (4, 2), goal cell G (7, 7) under the door,
8-connected moves of 0.5 m and 0.707 m that never cut the corner of a blocked cell (searchkit.py).

- wavefront: breadth-first search from G, every free cell numbered with its fewest moves to G (Choset; LaValle 8.2.3);
- cost_to_go: Dijkstra's algorithm run from G to the end, every free cell's shortest distance to G in metres;
- downhill: from a cell, keep stepping to the neighbour with the smallest move + number (LaValle eq. 8.5);
- value_iteration: in-place sweeps of the update V(x) = min over moves (move + V(next)) (Sutton and Barto 4.4);
- dp_interp, interp, follow: value iteration with bilinear interpolation between cell centres, moves in K directions
  (LaValle 8.5.2), and the robot following it from any point;
- fmm, dijkstra8: arrival times on a fine grid by the fast marching method (Sethian 1996) and by 8-connected Dijkstra."""
import collections
import heapq
import math

import numpy as np
from searchkit import BLOCKED, C, GOAL, NX, NY, START, dist_from, free, free_cells, neighbours, path_cost

INF = math.inf
CELLS = free_cells()


def nb4(c):
    """Free 4-connected neighbours of c with the move's length."""
    i, j = c
    return [((i + dx, j + dy), C) for dx, dy in ((-1, 0), (0, -1), (0, 1), (1, 0)) if free((i + dx, j + dy))]


def wavefront(nbrs=nb4, src=GOAL):
    """Breadth-first search from src: each reached cell gets its fewest moves to src. Returns (number, rings), where
    rings[k] lists the cells numbered k in the order they were reached."""
    num, q, rings = {src: 0}, collections.deque([src]), [[src]]
    while q:
        c = q.popleft()
        for n, _ in nbrs(c):
            if n not in num:
                num[n] = num[c] + 1
                if num[n] == len(rings):
                    rings.append([])
                rings[num[n]].append(n)
                q.append(n)
    return num, rings


def cost_to_go():
    """Shortest distance in metres from every free cell to G: Dijkstra's algorithm from G, run until the queue is
    empty (moves cost the same both ways, so distance from G = distance to G)."""
    return dist_from(GOAL)


def downhill(c, V, nbrs=neighbours, goal=GOAL):
    """Follow the numbers V from cell c: always step to the neighbour with the smallest move + V(neighbour), ties to
    the smaller V, then to the smaller cell index."""
    p = [c]
    while c != goal:
        c = min(nbrs(c), key=lambda ns: (round(ns[1] + V[ns[0]], 9), V[ns[0]], ns[0]))[0]
        p.append(c)
    return p


SWEEP = sorted(CELLS, key=lambda c: (-c[1], c[0]))     # row by row from the door's wall down, left to right


def value_iteration(order=SWEEP, nbrs=neighbours):
    """In-place value iteration: start with V = 0 at G and infinity elsewhere; each sweep visits the cells in `order`
    and sets V(x) = min over moves of (move + V(next)), using values already changed earlier in the same sweep.
    Stops after the first sweep that changes nothing. Returns the snapshots: V after each sweep, with the cells that
    got their first value and the cells whose value was lowered (old, new)."""
    V = {c: INF for c in CELLS}
    V[GOAL] = 0.0
    out = [dict(V=dict(V), new=[], lowered={})]
    while True:
        new, lowered = [], {}
        for c in order:
            if c == GOAL:
                continue
            v = min((s + V[n] for n, s in nbrs(c)), default=INF)
            if v < V[c] - 1e-12:
                if V[c] == INF:
                    new.append(c)
                else:
                    lowered[c] = (V[c], v)
                V[c] = v
        out.append(dict(V=dict(V), new=new, lowered=lowered))
        if not new and not lowered:
            return out


def centre(c):
    return ((c[0] + 0.5) * C, (c[1] + 0.5) * C)


def interp(V, x, y):
    """Bilinear interpolation of the cell-centre values V at the point (x, y): the four centres around the point,
    each weighted by how close the point is to it along x times along y. Infinite if any of the four is blocked."""
    fx, fy = x / C - 0.5, y / C - 0.5
    i, j = math.floor(fx + 1e-12), math.floor(fy + 1e-12)
    ax, ay = fx - i, fy - j
    tot = 0.0
    for di, wx in ((0, 1 - ax), (1, ax)):
        for dj, wy in ((0, 1 - ay), (1, ay)):
            w = wx * wy
            if w < 1e-12:
                continue
            c = (i + di, j + dj)
            if not free(c):
                return INF
            tot += w * V[c]
    return tot


def directions(K):
    return [(math.cos(2 * math.pi * k / K), math.sin(2 * math.pi * k / K)) for k in range(K)]


GX, GY = centre(GOAL)


def best_move(V, x, y, K=16, D=C):
    """The local operator of DP with interpolation at the point (x, y): of the K moves of length D, the one with the
    smallest D + interpolated V at its end; a point within D of G's centre may go straight there. Returns (value,
    end point)."""
    d = math.hypot(GX - x, GY - y)
    best = (d, (GX, GY)) if d <= D + 1e-9 else (INF, None)
    for ux, uy in directions(K):
        e = (x + D * ux, y + D * uy)
        v = D + interp(V, *e)
        if v < best[0] - 1e-12:
            best = (v, e)
    return best


def dp_interp(K=16, D=C, tol=1e-6, order=SWEEP):
    """Value iteration with interpolation (LaValle 8.5.2): the values live at the free cell centres; each sweep sets a
    centre's value to best_move's value. Stops once no value changes by more than tol. Returns (V, sweeps)."""
    V = {c: INF for c in CELLS}
    V[GOAL] = 0.0
    sweeps = 0
    while True:
        sweeps += 1
        change = 0.0
        for c in order:
            if c == GOAL:
                continue
            v = best_move(V, *centre(c), K, D)[0]
            if v < V[c]:
                change = max(change, INF if V[c] == INF else V[c] - v)
                V[c] = v
        if change <= tol:
            return V, sweeps


def follow(V, x, y, K=16, D=C):
    """The feedback plan from DP with interpolation: from (x, y), take best_move until G's centre. Returns the
    points and the route's length."""
    pts = [(x, y)]
    while pts[-1] != (GX, GY):
        pts.append(best_move(V, *pts[-1], K, D)[1])
        assert len(pts) < 100
    return pts, sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))


def fine_grid(k):
    """The room's free cells cut into k x k smaller cells each (cell side 0.5 / k m); returns (free mask, side)."""
    return np.repeat(np.repeat(~BLOCKED, k, axis=0), k, axis=1), C / k


def fmm(freem, h, src, F=1.0):
    """Fast marching (Sethian 1996): Dijkstra's loop, but a cell's arrival time T comes from its smaller accepted
    neighbour across (a) and its smaller accepted neighbour up or down (b) through the grid Eikonal equation
    ((T - a)/h)^2 + ((T - b)/h)^2 = 1/F^2, or T = a + h/F when only one direction helps. Returns (T, accept order)."""
    ny, nx = freem.shape
    T = np.full((ny, nx), INF)
    acc = np.zeros((ny, nx), bool)
    T[src[1], src[0]] = 0.0
    pq, order = [(0.0, src)], []

    def known(i, j):
        return T[j, i] if 0 <= i < nx and 0 <= j < ny and acc[j, i] else INF

    while pq:
        t, (i, j) = heapq.heappop(pq)
        if acc[j, i]:
            continue
        acc[j, i] = True
        order.append((i, j, t))
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ii, jj = i + di, j + dj
            if 0 <= ii < nx and 0 <= jj < ny and freem[jj, ii] and not acc[jj, ii]:
                v = eikonal_update(min(known(ii - 1, jj), known(ii + 1, jj)),
                                   min(known(ii, jj - 1), known(ii, jj + 1)), h, F)
                if v < T[jj, ii]:
                    T[jj, ii] = v
                    heapq.heappush(pq, (v, (ii, jj)))
    return T, order


def eikonal_update(a, b, h, F=1.0):
    """Solve ((T - a)/h)^2 + ((T - b)/h)^2 = 1/F^2 for the larger root; with one finite neighbour, or neighbours
    too far apart for both to help, T = (smaller) + h/F."""
    a, b = min(a, b), max(a, b)
    if b - a >= h / F:
        return a + h / F
    return (a + b + math.sqrt(2 * (h / F) ** 2 - (a - b) ** 2)) / 2


def dijkstra8(freem, h, src):
    """8-connected Dijkstra on the same fine grid (moves h and h times sqrt 2, no corner cutting)."""
    ny, nx = freem.shape
    T = np.full((ny, nx), INF)
    T[src[1], src[0]] = 0.0
    pq, done, order = [(0.0, src)], np.zeros((ny, nx), bool), []
    while pq:
        t, (i, j) = heapq.heappop(pq)
        if done[j, i]:
            continue
        done[j, i] = True
        order.append((i, j, t))
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                ii, jj = i + di, j + dj
                if (di, dj) == (0, 0) or not (0 <= ii < nx and 0 <= jj < ny and freem[jj, ii]):
                    continue
                if di and dj and not (freem[j, i + di] and freem[j + dj, i]):
                    continue
                v = t + h * math.hypot(di, dj)
                if v < T[jj, ii]:
                    T[jj, ii] = v
                    heapq.heappush(pq, (v, (ii, jj)))
    return T, order
