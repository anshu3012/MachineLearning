"""Collision checking for a disk robot, and the space the planners work in.

The free region is the floor the robot may touch: the bounds minus the obstacles (or, for a street map, the roads).
Shrinking it by the robot radius gives the free configuration space: the robot fits wherever its centre is inside it.
`free` tests one point. `segment_free` tests a straight segment by edge resolution: points at most `eps` apart, tried
coarse to fine. Every point test adds one to `checks`, so a planner's cost can be counted."""
import math

import shapely
from shapely.geometry import box


def bisection_order(n):
    """Indexes 0..n of the points on a segment cut into n equal pieces, in the order we test them: both ends, then the
    middle, then the two quarter points, then the eighths, ... (LaValle 2006, sec. 5.3.4)."""
    order, queue = [n, 0], [(0, n)]
    for lo, hi in queue:  # the queue grows while we walk it, so this goes level by level
        if hi - lo > 1:
            mid = (lo + hi) // 2
            order.append(mid)
            queue += [(lo, mid), (mid, hi)]
    return order


class Space:
    """A world the planners can run in. Built from a world dict (see world.py) that holds a shapely `free_region`.

    Planner interface: sample(rng), distance(a, b), steer(a, b, step), free(p), segment_free(a, b), checks.
    Drawing data: name, bounds, start, goal, radius, blocked (polygons), notes."""

    def __init__(self, world):
        self.name = world["name"]
        self.bounds = tuple(world["bounds"])
        self.radius = world["robot_radius"]
        self.start, self.goal = tuple(world["start"]), tuple(world["goal"])
        x0, y0, x1, y1 = self.bounds
        self.step = world.get("step") or round(math.hypot(x1 - x0, y1 - y0) / 25, 2)
        self.eps = world.get("eps") or self.radius / 5  # edge resolution: 5 test points per robot radius
        self.notes = world.get("notes", [])
        self.free_region = world["free_region"]
        self.cfree = self.free_region.buffer(-self.radius, quad_segs=64)  # where the robot's centre may go
        # Two test points eps apart can both be clear while the segment between them dips into a corner by up to
        # eps^2 / (8 r). So each point is tested with the robot grown by twice that: then the whole segment is clear.
        self.pad = self.eps ** 2 / (4 * self.radius)
        self.tested = self.free_region.buffer(-(self.radius + self.pad), quad_segs=64)
        shapely.prepare(self.cfree)
        shapely.prepare(self.tested)
        self.free_area = self.cfree.area
        blocked = box(*self.bounds).difference(self.free_region)
        self.blocked = list(getattr(blocked, "geoms", [blocked]))
        self.checks = 0
        assert self.free(self.start) and self.free(self.goal), f"{self.name}: start or goal is blocked"
        self.checks = 0

    def sample(self, rng):
        x0, y0, x1, y1 = self.bounds
        return (rng.uniform(x0, x1), rng.uniform(y0, y1))

    def distance(self, a, b):
        return math.dist(a, b)

    def steer(self, a, b, step):
        d = math.dist(a, b)
        if d <= step:
            return b
        t = step / d
        return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))

    def free(self, p):
        self.checks += 1
        return bool(shapely.contains_xy(self.tested, p[0], p[1]))

    def segment_free(self, a, b):
        n = max(1, math.ceil(math.dist(a, b) / self.eps))  # n pieces, each at most eps long
        for i in bisection_order(n):
            t = i / n
            if not self.free((a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))):
                return False
        return True
