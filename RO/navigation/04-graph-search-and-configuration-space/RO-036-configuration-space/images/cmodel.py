"""The numbers of this Note (no output when run on its own): the floor robot and its configuration, the circle it
drives (RO-001: 0.5 m/s, 1 rad/s), the 2R arm on the robot, degree-of-freedom counts, and the planned path from
the start to the door with its clearance from the obstacles."""
import numpy as np
from roommap import CAB, POLE_R, POLES, TABLE
from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union

TWO_PI = 2 * np.pi
Q0 = (2.0, 1.0, np.radians(30))                 # the robot's configuration (x m, y m, theta rad)
R_BODY = 0.25                                    # the body seen from above: a disk of radius 0.25 m
L1, L2 = 0.3, 0.2                                # the arm's two links (m)
V, W = 0.5, 1.0                                  # RO-001's circle: linear and angular velocity


def body_point(q, local):
    """World position of a point given in the robot's own frame (forward, left): rotate by theta, then shift."""
    x, y, th = q
    a, b = local
    return x + a * np.cos(th) - b * np.sin(th), y + a * np.sin(th) + b * np.cos(th)


def circle_drive(t):
    """Configuration after t seconds on RO-001's circle (exact arc), heading not wrapped."""
    x0, y0, th0 = Q0
    th = th0 + W * t
    r = V / W
    return x0 + r * (np.sin(th) - np.sin(th0)), y0 - r * (np.cos(th) - np.cos(th0)), th


def wrap(th):
    """Heading in [0, 2 pi)."""
    return np.mod(th, TWO_PI)


def arm(t1, t2):
    """Elbow and hand of the 2R arm, shoulder at the origin."""
    e = (L1 * np.cos(t1), L1 * np.sin(t1))
    h = (e[0] + L2 * np.cos(t1 + t2), e[1] + L2 * np.sin(t1 + t2))
    return e, h


def grubler(m, N, J, f):
    """Degrees of freedom m (N - 1 - J) + sum of joint freedoms (MR eq. 2.4)."""
    return m * (N - 1 - J) + sum(f)


# the motion from the start to the doorway centre (as in RO-037): turn on the spot, then drive straight
WAY = [(2.0, 1.0), (3.6, 4.0)]
TH_GOAL = np.arctan2(4.0 - 1.0, 3.6 - 2.0)                    # the robot ends facing along its drive
OBST = unary_union([Polygon(TABLE)] + [box(x0, y0, x1, y1) for x0, x1, y0, y1 in CAB]
                   + [Point(p).buffer(POLE_R, quad_segs=128) for p in POLES.values()])
WALLS = unary_union([LineString([(3.0, 4), (0, 4), (0, 0), (7, 0), (7, 4), (4.2, 4)])])


def plan_configs(n_turn=8, n_drive=16):
    """Configurations along the plan: (x, y, theta) with theta unwrapped, and a stage label for each."""
    out = []
    x, y, th = Q0
    legs = [np.arctan2(b[1] - a[1], b[0] - a[0]) for a, b in zip(WAY, WAY[1:])]
    targets = []
    for k, h in enumerate(legs):
        targets.append(("turn", h))
        targets.append(("drive", WAY[k + 1]))
    if not np.isclose(TH_GOAL, legs[-1]):
        targets.append(("turn", TH_GOAL))
    out.append((x, y, th, "start"))
    for kind, goal in targets:
        if kind == "turn":
            for s in np.linspace(0, 1, n_turn + 1)[1:]:
                out.append((x, y, th + s * (goal - th), "turn"))
            th = goal
        else:
            for s in np.linspace(0, 1, n_drive + 1)[1:]:
                out.append((x + s * (goal[0] - x), y + s * (goal[1] - y), th, "drive"))
            x, y = goal
    return out, legs


def clearance():
    """Smallest distance from the path of the robot's centre to an obstacle or a wall (m)."""
    path = LineString(WAY)
    return min(path.distance(OBST), path.distance(WALLS))


if __name__ == "__main__":
    print("front point", np.round(body_point(Q0, (R_BODY, 0)), 3), "left point", np.round(body_point(Q0, (0, R_BODY)), 3))
    tw = TWO_PI - Q0[2]
    print("wrap at t =", round(tw, 3), "s; back at start after", round(TWO_PI, 3), "s; end",
          np.round(circle_drive(TWO_PI), 6))
    print("arm hand at (30, 60) deg", np.round(arm(np.radians(30), np.radians(60))[1], 3))
    print("grubler 2R", grubler(3, 3, 2, [1, 1]), "3R", grubler(3, 4, 3, [1] * 3), "four-bar", grubler(3, 4, 4, [1] * 4),
          "floor", grubler(3, 2, 0, []))
    cfg, legs = plan_configs()
    print("leg headings deg", np.round(np.degrees(legs), 2), "clearance", round(clearance(), 3))
    print("leg lengths", [round(float(np.hypot(b[0] - a[0], b[1] - a[1])), 3) for a, b in zip(WAY, WAY[1:])])
    print("heading 359 -> 1 deg: theta", round(np.radians(359), 3), round(np.radians(1), 3), "implicit",
          np.round([np.cos(np.radians(359)), np.sin(np.radians(359))], 4), "->",
          np.round([np.cos(np.radians(1)), np.sin(np.radians(1))], 4))
