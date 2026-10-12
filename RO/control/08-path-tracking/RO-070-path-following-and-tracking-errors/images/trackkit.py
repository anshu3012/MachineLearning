"""The car, the test course and the path coordinates of this Note (no output when run on its own).

The car is RO-055's: wheelbase 2.5 m, largest steering angle 26.6 deg (tan = 0.5), so its tightest circle has radius
5 m at the rear axle; body 4.0 m x 1.8 m with the rear axle 0.75 m from the rear bumper. Its pose (x, y, th) is the
middle of the rear axle and its heading. It moves by the kinematic bicycle model: x' = v cos th, y' = v sin th,
th' = v tan(delta) / L. Commands come at 20 Hz (held 0.05 s); the car is moved in Euler steps of 0.01 s.

The test course: 10 m straight along x from (0, 0); a 90 deg left arc of radius 10 m (curvature 0.1 per m) round
(10, 10) to (20, 10); 10 m straight up to (20, 20). Length 10 + 5 pi + 10 = 35.708 m. The car starts with its rear axle
at (0, 1.0), 1.0 m left of the line, heading 0 deg.

Path coordinates (Snider 2009, 3.1.1; Paden et al. 2016, V): the nearest course point to a point of the car, its
distance s along the course, the signed lateral error e (+ to the left of the course's direction) and the heading
error th_e = th - th_path(s), wrapped.

The demonstration driver is RO-069's line rule applied to the course's tangent at the nearest point:
w = -K_D e - K_H th_e, turned into a steering angle by the bicycle model, tan(delta) = L w / v, and clipped at the
car's 26.6 deg. With v = 2 m/s, K_D = 0.5 and K_H = 2 the error equation has spring v K_D = 1 and damper 2
(critically damped, 1 rad/s)."""
import numpy as np

WHEELBASE = 2.5
DELTA_MAX = np.arctan(0.5)                 # 26.57 deg: tightest circle 2.5 / 0.5 = 5 m
CAR_L, CAR_W, REAR_OH = 4.0, 1.8, 0.75
DT_CTRL, DT_SIM = 0.05, 0.01
V_BASE = 2.0
K_D, K_H = 0.5, 2.0
R_ARC = 10.0
C_ARC = (10.0, 10.0)
L1, L_ARC, L2 = 10.0, R_ARC * np.pi / 2, 10.0
S_END = L1 + L_ARC + L2
START = (0.0, 1.0, 0.0)


def wrap(a):
    return (a + np.pi) % (2 * np.pi) - np.pi


def course_point(s):
    """(x, y, heading, curvature) of the course at distance s along it (s clipped to the course)."""
    s = float(np.clip(s, 0.0, S_END))
    if s <= L1:
        return s, 0.0, 0.0, 0.0
    if s <= L1 + L_ARC:
        phi = -np.pi / 2 + (s - L1) / R_ARC
        return C_ARC[0] + R_ARC * np.cos(phi), C_ARC[1] + R_ARC * np.sin(phi), phi + np.pi / 2, 1.0 / R_ARC
    return 20.0, 10.0 + (s - L1 - L_ARC), np.pi / 2, 0.0


def course_xy(n=400):
    s = np.linspace(0, S_END, n)
    p = np.array([course_point(v) for v in s])
    return p[:, 0], p[:, 1]


def nearest_s(x, y):
    """Distance along the course of the course point nearest to (x, y): the closest of the three pieces."""
    cands = [float(np.clip(x, 0.0, L1))]                                       # first straight, y = 0
    phi = np.clip(np.arctan2(y - C_ARC[1], x - C_ARC[0]), -np.pi / 2, 0.0)     # the arc
    cands.append(L1 + R_ARC * (phi + np.pi / 2))
    cands.append(L1 + L_ARC + float(np.clip(y - 10.0, 0.0, L2)))              # second straight, x = 20
    d = [np.hypot(x - course_point(s)[0], y - course_point(s)[1]) for s in cands]
    return cands[int(np.argmin(d))]


def frenet(x, y, th):
    """Path coordinates of a point (x, y) with heading th: s, lateral error e (+ left), heading error th_e."""
    s = nearest_s(x, y)
    px, py, pth, k = course_point(s)
    dx, dy = x - px, y - py
    e = -np.sin(pth) * dx + np.cos(pth) * dy
    return s, e, wrap(th - pth), k


def front_axle(q):
    return q[0] + WHEELBASE * np.cos(q[2]), q[1] + WHEELBASE * np.sin(q[2])


def steer_from_turn_rate(w, v):
    """The bicycle model backwards: the steering angle that turns the car at w (rad/s) at speed v, clipped."""
    return float(np.clip(np.arctan(WHEELBASE * w / v), -DELTA_MAX, DELTA_MAX))


def line_rule(q, v=V_BASE, k_d=K_D, k_h=K_H):
    """RO-069's line rule on the tangent at the nearest course point (rear axle): returns (v, delta)."""
    _, e, the, _ = frenet(*q)
    return v, steer_from_turn_rate(-k_d * e - k_h * the, v)


def first_line_rule(q, v=V_BASE, k_d=K_D, k_h=K_H):
    """RO-069's line rule on one fixed line, the first straight y = 0 heading 0 (the opening problem)."""
    e, the = q[1], wrap(q[2])
    return v, steer_from_turn_rate(-k_d * e - k_h * the, v)


HOLD, K_S, V_FAST = 1.5, 1.0, 5.0         # the delayed start, the tracker's speed gain (per s), its top speed


def timetable_s(t):
    """The timed reference of Section 3: the distance along the course where the timetable says the car should be,
    2 m/s from t = 0 (past the end of the course the timetable runs on, so a late car keeps its along-track error)."""
    return V_BASE * t


def tracker(q, t):
    """Trajectory tracking for the comparison of Section 3: speed 2 m/s plus K_S times the along-track error (the
    timetable's distance minus the car's), between 0.1 and 5 m/s; steering as the line rule."""
    s = nearest_s(q[0], q[1])
    v = float(np.clip(V_BASE + K_S * (timetable_s(t) - s), 0.1, V_FAST))
    return line_rule(q, v=v)


def run(law, q0=START, t_max=40.0, stop=None, hold=0.0):
    """Simulate a law (q, t) -> (v, delta) from q0; hold: seconds standing still at the start.
    Ends when the nearest course point reaches the end of the course (or stop(q) is True)."""
    stop = stop or (lambda q: nearest_s(q[0], q[1]) >= S_END - 1e-6)
    q = np.array(q0, dtype=float)
    out = {k: [] for k in ("t", "x", "y", "th", "v", "delta")}
    n_sub = int(round(DT_CTRL / DT_SIM))
    t, k = 0.0, 0
    v = d = 0.0
    while t < t_max + 1e-9:
        if k % n_sub == 0:
            if stop(q):
                break
            v, d = (0.0, 0.0) if t < hold - 1e-9 else law(q, t)
        for key, val in zip(out, (t, q[0], q[1], q[2], v, d)):
            out[key].append(val)
        q = q + DT_SIM * np.array([v * np.cos(q[2]), v * np.sin(q[2]), v * np.tan(d) / WHEELBASE])
        t = round(t + DT_SIM, 10)
        k += 1
    for key, val in zip(out, (t, q[0], q[1], q[2], v, d)):
        out[key].append(val)
    r = {k: np.array(v) for k, v in out.items()}
    F = np.array([frenet(x, y, th) for x, y, th in zip(r["x"], r["y"], r["th"])])
    r["s"], r["e"], r["the"], r["kappa"] = F[:, 0], F[:, 1], F[:, 2], F[:, 3]
    return r


def body(q):
    """Corners of the car's body at pose q (closed polygon)."""
    x, y, th = q
    c, s = np.cos(th), np.sin(th)
    pts = [(-REAR_OH, CAR_W / 2), (CAR_L - REAR_OH, CAR_W / 2), (CAR_L - REAR_OH, -CAR_W / 2), (-REAR_OH, -CAR_W / 2),
           (-REAR_OH, CAR_W / 2)]
    return np.array([(x + a * c - b * s, y + a * s + b * c) for a, b in pts])


def metrics(r, s_arc=(L1 + 3.0, L1 + L_ARC)):
    """Peak |lateral error|, steady error on the arc (mean over its last part) and the distance along the course
    after which |e| stays within 0.1 m for good."""
    peak = float(np.max(np.abs(r["e"])))
    on = (r["s"] >= s_arc[0]) & (r["s"] <= s_arc[1])
    k_last = np.where(np.abs(r["e"]) > 0.1)[0]
    return peak, r["e"][on], (r["s"][k_last[0]] if len(k_last) else 0.0)
