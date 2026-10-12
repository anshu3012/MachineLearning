"""The room robot, its timed trajectory and the trackers of this Note, shared by the notebook and every figure script
(no output when run).

Robot: RO-001's differential drive (wheel radius 0.05 m, wheel separation 0.2 m, each wheel at most 0.6 m/s), driven by
its forward speed v and turn rate w (the unicycle model x' = v cos th, y' = v sin th, th' = w). A command that asks a
wheel for more than 0.6 m/s is scaled down, keeping its v : w ratio (the turning radius). The tracker runs at 20 Hz
(Nav2's default controller_frequency) and holds its command for 0.05 s; the robot is stepped every 0.01 s.

Timetable (the reference robot): from (0, 0) facing 0, at 0.3 m/s: 1 m straight along x, a 90 degree left arc of
radius 1 m (turn rate 0.3 rad/s), 1 m straight along y; it reaches (2, 2) at 11.90 s. The car's test course of this
chapter shrunk ten times. The robot starts at (-0.2, 0.1) facing 0: 0.2 m behind its timetable, 0.1 m to the left.

Trackers: replay the timetable's speeds (feedforward only); a path follower (Kanayama's law on the nearest path point,
speed fixed at 0.3 m/s); Kanayama's tracker (Kanayama et al. 1991, eq. 8); feedback linearisation of an offset point
P a distance d ahead of the axle (MR eq. 13.21 and 13.29, Paden V.B.2) with the reference's velocity added.
"""
import numpy as np

V_R, R_ARC, L_STRAIGHT = 0.3, 1.0, 1.0       # m/s, m, m
W_R = V_R / R_ARC                             # 0.3 rad/s on the arc
T1 = L_STRAIGHT / V_R                         # 3.333 s: end of the first straight
T2 = T1 + (np.pi / 2) * R_ARC / V_R           # 8.570 s: end of the arc
T_END = T2 + L_STRAIGHT / V_R                 # 11.903 s: end of the timetable
WHEEL_SEP, V_WHEEL = 0.2, 0.6                 # m, m/s
DT, CTRL_DT = 0.01, 0.05                      # s: robot step, 20 Hz tracker
START = (-0.2, 0.1, 0.0)                      # 0.2 m behind, 0.1 m to the left, facing along x
KX, KY, KTH = 1.0, 16.0, 8.0                  # 1/s, 1/m^2, 1/m: damping ratio KTH / (2 sqrt KY) = 1
D_P, K_P = 0.2, 1.0                           # m, 1/s: offset point and its gain


def ref(t):
    """Reference robot at time t: pose (x, y, th) and speeds (v, w)."""
    t = min(max(t, 0.0), T_END)
    if t <= T1:
        return V_R * t, 0.0, 0.0, V_R, 0.0
    if t <= T2:
        a = W_R * (t - T1)                    # angle turned on the arc
        return L_STRAIGHT + R_ARC * np.sin(a), R_ARC * (1 - np.cos(a)), a, V_R, W_R
    return L_STRAIGHT + R_ARC, R_ARC + V_R * (t - T2), np.pi / 2, V_R, 0.0


def path_xy(n=400):
    """Points of the reference path, for drawing."""
    ts = np.linspace(0, T_END, n)
    p = np.array([ref(t)[:2] for t in ts])
    return p[:, 0], p[:, 1]


def wrap(a):
    return (a + np.pi) % (2 * np.pi) - np.pi


def error_frame(pose, rpose):
    """Kanayama's error: the reference pose seen from the robot. x_e ahead, y_e to the left, th_e = th_r - th."""
    x, y, th = pose
    xr, yr, thr = rpose
    dx, dy = xr - x, yr - y
    c, s = np.cos(th), np.sin(th)
    return c * dx + s * dy, -s * dx + c * dy, wrap(thr - th)


def lyap(xe, ye, the, ky=KY):
    """Kanayama's Lyapunov function V = (x_e^2 + y_e^2) / 2 + (1 - cos th_e) / K_y, in m^2."""
    return 0.5 * (xe ** 2 + ye ** 2) + (1 - np.cos(the)) / ky


def clip_wheels(v, w):
    """Scale (v, w) down so that neither wheel passes 0.6 m/s; returns (v, w, clipped)."""
    peak = abs(v) + abs(w) * WHEEL_SEP / 2
    if peak <= V_WHEEL + 1e-12:
        return v, w, False
    return v * V_WHEEL / peak, w * V_WHEEL / peak, True


# ---- trackers: each takes (t, pose) and returns (v, w) ----
def replay(t, pose):
    return ref(t)[3], ref(t)[4]


def kanayama(t, pose, kx=KX, ky=KY, kth=KTH):
    xr, yr, thr, vr, wr = ref(t)
    xe, ye, the = error_frame(pose, (xr, yr, thr))
    return vr * np.cos(the) + kx * xe, wr + vr * (ky * ye + kth * np.sin(the))


def nearest_on_path(x, y):
    """Nearest point of the reference path to (x, y): its pose and the path's turn rate at speed V_R there."""
    cands = []
    s = np.clip(x, 0, L_STRAIGHT)                                   # first straight
    cands.append(((s, 0.0, 0.0, 0.0), (x - s) ** 2 + y ** 2))
    a = np.clip(np.arctan2(x - L_STRAIGHT, R_ARC - y), 0, np.pi / 2)  # arc about (1, 1)
    px, py = L_STRAIGHT + R_ARC * np.sin(a), R_ARC * (1 - np.cos(a))
    cands.append(((px, py, a, W_R), (x - px) ** 2 + (y - py) ** 2))
    s = np.clip(y - R_ARC, 0, L_STRAIGHT)                           # last straight
    cands.append(((L_STRAIGHT + R_ARC, R_ARC + s, np.pi / 2, 0.0), (x - 2.0) ** 2 + (y - R_ARC - s) ** 2))
    return min(cands, key=lambda c: c[1])[0]


def path_follower(t, pose, ky=KY, kth=KTH):
    """No clock: steer at the nearest path point (its curvature as feedforward), speed held at 0.3 m/s."""
    xr, yr, thr, wr = nearest_on_path(pose[0], pose[1])
    _, ye, the = error_frame(pose, (xr, yr, thr))
    return V_R, wr + V_R * (ky * ye + kth * np.sin(the))


def p_point(pose, d=D_P):
    x, y, th = pose
    return np.array([x + d * np.cos(th), y + d * np.sin(th)])


def p_ref(t, d=D_P):
    """The offset point of the reference robot and its velocity."""
    xr, yr, thr, vr, wr = ref(t)
    p = np.array([xr + d * np.cos(thr), yr + d * np.sin(thr)])
    pd = np.array([vr * np.cos(thr) - d * wr * np.sin(thr), vr * np.sin(thr) + d * wr * np.cos(thr)])
    return p, pd


def feedback_lin(t, pose, d=D_P, k=K_P):
    """Wanted velocity of P = reference P's velocity + k (reference P - P); then invert P's velocity map."""
    th = pose[2]
    pr, prd = p_ref(t, d)
    u = prd + k * (pr - p_point(pose, d))
    v = np.cos(th) * u[0] + np.sin(th) * u[1]
    w = (-np.sin(th) * u[0] + np.cos(th) * u[1]) / d
    return v, w


def simulate(tracker, start=START, T=T_END, limit=True):
    """Run the robot for T seconds. Returns arrays t, x, y, th, v, w (commands held over each 0.05 s), clipped flag."""
    n = int(round(T / DT))
    hold = int(round(CTRL_DT / DT))
    x, y, th = start
    out = {k: np.zeros(n + 1) for k in ("t", "x", "y", "th", "v", "w")}
    out["clipped"] = False
    v = w = 0.0
    for i in range(n + 1):
        t = i * DT
        if i % hold == 0:
            v, w = tracker(t, (x, y, th))
            if limit:
                v, w, c = clip_wheels(v, w)
                out["clipped"] |= c
        for k, val in zip(("t", "x", "y", "th", "v", "w"), (t, x, y, th, v, w)):
            out[k][i] = val
        x, y, th = x + v * np.cos(th) * DT, y + v * np.sin(th) * DT, th + w * DT
    return out


def errors(run):
    """Kanayama's error at every step, and the distance to the timetable's point."""
    e = np.array([error_frame((x, y, th), ref(t)[:3]) for t, x, y, th in zip(run["t"], run["x"], run["y"], run["th"])])
    return e[:, 0], e[:, 1], e[:, 2], np.hypot(e[:, 0], e[:, 1])
