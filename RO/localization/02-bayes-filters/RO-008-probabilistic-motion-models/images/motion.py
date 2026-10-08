"""Shared maths for this Note's figures: the odometry and velocity motion models with the noise settings of the Note
(no output when run on its own). Noise: standard deviation grows with the size of the motion (Freiburg slides 13, 31)."""
import numpy as np

START = (2.0, 1.0, np.radians(30))                 # pose of RO-001, Figure 1
ODO_END = (2.249, 1.409, 1.524)                     # odometry's end pose after 1 s at v = 0.5 m/s, omega = 1 rad/s
A_ODO = (0.1, 0.1, 0.1, 0.01)                       # alpha1..alpha4
A_VEL = (0.1, 0.02, 0.1, 0.1, 0.02, 0.02)           # alpha1..alpha6
V, W, DT = 0.5, 1.0, 1.0


def odo_deltas(p, q):
    """rot1, trans, rot2 that take pose p to pose q."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    rot1 = np.arctan2(dy, dx) - p[2]
    return rot1, np.hypot(dx, dy), q[2] - p[2] - rot1


def odo_sds(u, a=A_ODO):
    rot1, trans, rot2 = u
    return (a[0] * abs(rot1) + a[1] * trans, a[2] * trans + a[3] * (abs(rot1) + abs(rot2)),
            a[0] * abs(rot2) + a[1] * trans)


def sample_normal(b, rng, size):
    """Sum of 12 uniform numbers in [-b, b], halved: mean 0, standard deviation b."""
    return 0.5 * rng.uniform(-b, b, size=(12,) + np.shape(np.zeros(size))).sum(axis=0)


def sample_odometry(u, x, rng, n, a=A_ODO):
    """n samples of the pose after odometry u = (rot1, trans, rot2) from pose x (arrays of length n)."""
    s1, st, s2 = odo_sds(u, a)
    r1 = u[0] + sample_normal(s1, rng, n)
    tr = u[1] + sample_normal(st, rng, n)
    r2 = u[2] + sample_normal(s2, rng, n)
    return x[0] + tr * np.cos(x[2] + r1), x[1] + tr * np.sin(x[2] + r1), x[2] + r1 + r2


def arc_end(x, y, th, v, w, dt):
    """Exact end pose after driving v, w for dt (w not 0): the robot circles the point (x - R sin th, y + R cos th)."""
    R = v / w
    xc, yc = x - R * np.sin(th), y + R * np.cos(th)
    return xc + R * np.sin(th + w * dt), yc - R * np.cos(th + w * dt), th + w * dt


def sample_velocity(x, rng, n, a=A_VEL, gamma=True):
    sv, sw, sg = a[0] * V + a[1] * W, a[2] * V + a[3] * W, a[4] * V + a[5] * W
    vh = V + sample_normal(sv, rng, n)
    wh = W + sample_normal(sw, rng, n)
    gh = sample_normal(sg, rng, n) if gamma else 0.0
    xe, ye, te = arc_end(x[0], x[1], x[2], vh, wh, DT)
    return xe, ye, te + gh * DT
