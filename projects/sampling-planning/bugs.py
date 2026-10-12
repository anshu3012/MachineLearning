"""Bug 1 and Bug 2 (Lumelsky and Stepanov 1987; LaValle sec. 12.3.3), on any world.

The robot knows no map: only where the goal is (a goal sensor) and the edge of what it touches. We follow its centre,
so every obstacle is grown by the robot's radius: the robot's centre stays in the Space's cfree and may slide along
its edge. Both bugs head straight for the goal and, on a hit, turn left, so the obstacle stays on their right.
  Bug 1: go once round the whole edge, back to the hit point, then return to the edge point nearest the goal, the
         shorter way, and leave from there.
  Bug 2: follow the edge until back on the start-goal line, nearer the goal than the hit point, and leave there.
Each returns a dict: path (points), length, legs [(kind, points)], marks [(label, point)], reached (True/False)."""
import math

from shapely.geometry import LineString, Point
from shapely.geometry.polygon import orient
from shapely.ops import substring

EPS = 1e-7


def free_piece(space):
    """The piece of the robot's free space that holds the start, its rings oriented so that walking along a ring in
    its stored order keeps the free space on the left and the obstacle on the right."""
    pieces = getattr(space.cfree, "geoms", [space.cfree])
    poly = next(p for p in pieces if p.covers(Point(space.start)))
    return orient(poly, 1.0)


def to_goal(poly, p, goal):
    """Drive straight from p toward the goal. Returns (end point, reached goal?, moved?). Stops at the first point
    where the straight line would leave the free space; does not move if the very first bit is blocked."""
    seg = LineString([p, goal])
    hits = seg.intersection(poly.boundary)
    pts = [g for g in getattr(hits, "geoms", [hits]) if not g.is_empty]
    ts = sorted({round(seg.project(Point(c)), 12) for g in pts for c in g.coords} | {seg.length})
    t0 = 0.0
    for t in ts:
        if t <= EPS:
            continue
        mid = seg.interpolate((t0 + t) / 2)
        if not poly.covers(mid):  # this piece is blocked: stop at its start
            return seg.interpolate(t0).coords[0], False, t0 > 0
        t0 = t
    return tuple(goal), True, True


def ring_of(poly, p):
    return min([poly.exterior, *poly.interiors], key=lambda r: r.distance(Point(p)))


def along(ring, s0, d):
    """The points of the ring from arc length s0 going d forward (d > 0) or -d backward (d < 0)."""
    L = ring.length
    if d < 0:
        return along(ring, (s0 + d) % L, -d)[::-1]
    a, b = s0, s0 + d
    if b <= L:
        return list(substring(ring, a, b).coords)
    return list(substring(ring, a, L).coords) + list(substring(ring, 0, b - L).coords)[1:]


def drive(space, leave):
    """The loop both bugs share. leave(poly, ring, hit) -> ([(kind, edge points)], leave point, label) or None if
    there is no way on."""
    poly, goal = free_piece(space), space.goal
    p, legs, marks = tuple(space.start), [], []
    for k in range(1, 51):  # each leave point is nearer the goal than the last hit, so this ends; 50 is a safety cap
        q, reached, _ = to_goal(poly, p, goal)
        legs.append(("to goal", [p, q]))
        if reached:
            break
        marks.append((f"H{k}", q))
        out = leave(poly, ring_of(poly, q), q)
        if out is None:
            break
        legs += out[0]
        p = out[1]
        marks.append((f"{out[2]}{k}", p))
    if len(marks) <= 2:  # one hit: just H and C (or L)
        marks = [(label[0], q) for label, q in marks]
    path = [legs[0][1][0]] + [c for _, pts in legs for c in pts[1:]]
    return dict(path=path, length=LineString(path).length, legs=legs, marks=marks, reached=path[-1] == tuple(goal))


def bug1(space):
    goal = space.goal

    def leave(poly, ring, hit):
        L, s_hit = ring.length, ring.project(Point(hit))
        s_c = ring.project(Point(goal))  # the edge point nearest the goal
        ahead = (s_c - s_hit) % L
        back = ahead if ahead <= L - ahead else ahead - L  # return the shorter way
        loop = along(ring, s_hit, L)
        ret = along(ring, s_hit, back)
        c = ret[-1]
        if not to_goal(poly, c, goal)[2]:
            return None  # no way toward the goal from the nearest point: the goal cannot be reached
        return [("round the edge", loop), ("back to the nearest point", ret)], c, "C"

    return dict(bug1=True, **drive(space, leave))


def bug2(space):
    start, goal = space.start, space.goal
    mline = LineString([start, goal])

    def leave(poly, ring, hit):
        L, s_hit = ring.length, ring.project(Point(hit))
        d_hit = math.dist(hit, goal)
        xs = ring.intersection(mline)
        best = None
        for g in getattr(xs, "geoms", [xs]):
            for c in g.coords:
                if math.dist(c, goal) >= d_hit - 1e-6 or not to_goal(poly, c, goal)[2]:
                    continue  # not nearer the goal than the hit point, or the way to the goal is blocked there
                ahead = (ring.project(Point(c)) - s_hit) % L
                if best is None or ahead < best[0]:
                    best = (ahead, c)
        if best is None:
            return None
        pts = along(ring, s_hit, best[0])
        return [("follow the edge", pts)], pts[-1], "L"

    return dict(bug1=False, **drive(space, leave))
