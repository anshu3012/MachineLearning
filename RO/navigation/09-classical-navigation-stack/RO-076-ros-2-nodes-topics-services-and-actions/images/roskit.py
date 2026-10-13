"""The room robot's stack as ROS 2 nodes, for this Note's numbers and animations (no output when run on its own).

The drive is RO-058's (bandkit.py and trajkit.py, copied): the robot starts at rest at (2.0, 1.0) facing 30 degrees,
a person steps in at 2.4 s, the local planner re-plans every 0.1 s and the robot stops at the door pose at 8.0 s.
Here we read off what the messages between the nodes would carry:
- /scan: a laser scan like the Hokuyo URG-04LX-UG01 of RO-075 (240 degrees in 0.352 degree steps, 682 readings,
  0.02 to 5.6 m), from the robot's centre, every 0.1 s;
- /cmd_vel: the speed and turn rate the controller sends every 0.05 s (the drive of bandkit.run_loop, replayed);
- the navigate-to-pose action's feedback: the distance left along the global plan, as Nav2 measures it, and the
  time so far.
Also: the room's map as an occupancy grid of 0.05 m cells."""
import math

import numpy as np

import bandkit as bk
from trajkit import A_MAX, GOAL, L_AXLE, R_BODY, ROUTE_PTS, V_WHEEL

R = bk.results()
L = R["loop"]
N_SCAN, STEP_DEG, RMIN, RMAX = 682, 0.352, 0.02, 5.6
ANGLE_MIN = -math.radians(STEP_DEG) * (N_SCAN - 1) / 2


def ranges(pose, person=None, n=N_SCAN, rmax=RMAX):
    """Laser readings from the robot's centre: n beams from ANGLE_MIN in STEP_DEG steps (bearings from the heading,
    positive = left), by sphere tracing on bandkit's exact distance functions."""
    obs = bk.obstacles(person)
    x, y, th = pose
    b = ANGLE_MIN + np.arange(n) * math.radians(STEP_DEG)
    dx, dy = np.cos(th + b), np.sin(th + b)
    t = np.zeros(n)
    live = np.ones(n, bool)
    for _ in range(300):
        px, py = x + t * dx, y + t * dy
        d = np.min([o(px, py) for o in obs], axis=0)
        live &= (d >= 1e-3) & (t < rmax)
        if not live.any():
            break
        t = np.where(live, t + d, t)
    return b, np.minimum(t, rmax)


def scan(t):
    """The LaserScan message the driver publishes at time t (a multiple of 0.1 s)."""
    k = int(round(t / bk.CYCLE))
    o = L[k]
    person = bk.PERSON if t >= bk.T_PERSON - 1e-9 else None
    b, r = ranges(tuple(o["x"][:3]), person)
    return dict(stamp=t, angle_min=ANGLE_MIN, angle_max=ANGLE_MIN + (N_SCAN - 1) * math.radians(STEP_DEG),
                angle_increment=math.radians(STEP_DEG), scan_time=0.1, range_min=RMIN, range_max=RMAX,
                ranges=r, bearings=b)


def cmd(t):
    """The /cmd_vel message (linear.x, angular.z) at time t, a multiple of 0.05 s: the speed and turn rate the robot
    drove in that 0.005 s step of bandkit's drive."""
    k = int(math.floor(t / bk.CYCLE + 1e-9))
    j = int(round((t - k * bk.CYCLE) / (bk.CYCLE / 20)))
    o = L[k]
    P, DT, v = o["P"], o["DT"], o["v"]
    vv, ww, _, _, _ = bk.band_terms(P, DT, v, o["final"])
    Tb = np.concatenate([[0], np.cumsum(DT)])
    hh = bk.CYCLE / 20
    w = 0.0
    for i in range(j + 1):
        tm = (i + 0.5) * hh
        n = min(np.searchsorted(Tb, tm, side="right") - 1, len(DT) - 1)
        v_c, w_c = (float(vv[n]), float(ww[n])) if tm < Tb[-1] else (0.0, 0.0)
        v = float(np.clip(v + np.clip(v_c - v, -A_MAX * hh, A_MAX * hh), 0, V_WHEEL))
        w = float(np.clip(w_c, -(V_WHEEL - v) / (L_AXLE / 2), (V_WHEEL - v) / (L_AXLE / 2)))
    return v, w


# ---------------------------------------------------------------- the action's feedback
PATH = np.concatenate([np.linspace(ROUTE_PTS[i], ROUTE_PTS[i + 1], 200, endpoint=False)
                       for i in range(len(ROUTE_PTS) - 1)] + [ROUTE_PTS[-1:]])   # the global plan, dense


def distance_remaining(xy):
    """Nav2's feedback: the length of the global plan from the plan point nearest the robot to its end."""
    i = int(np.argmin(np.hypot(PATH[:, 0] - xy[0], PATH[:, 1] - xy[1])))
    return float(np.sum(np.hypot(*np.diff(PATH[i:], axis=0).T)))


def feedback(t):
    k = min(int(round(t / bk.CYCLE)), len(L) - 1)
    o = L[k]
    d = distance_remaining(o["x"][:2])
    v = o["v"]
    eta = d / v if (v > 0.01 and d > 0.1) else 0.0
    return dict(t=o["t"], pose=o["x"][:3], distance_remaining=d, speed=v, estimated_time_remaining=eta)


PLAN_LENGTH = float(np.sum(np.hypot(*np.diff(PATH, axis=0).T)))
T_ARRIVE = L[-1]["t"]


# ---------------------------------------------------------------- the map
MAP_RES, MAP_W, MAP_H = 0.05, 7.0, 4.0
MAP_CELLS = (int(round(MAP_W / MAP_RES)), int(round(MAP_H / MAP_RES)))     # (140, 80)
