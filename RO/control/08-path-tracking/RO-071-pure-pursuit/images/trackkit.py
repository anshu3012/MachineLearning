"""The test course, the car and the path trackers of chapter RO-08 (Path tracking), shared by the figure scripts and
notebooks of RO-071 (pure pursuit) and RO-072 (Stanley and rear-wheel feedback); RO-074 reuses it (no output when
imported; run it on its own for its self-check).

The car (the car of RO-055): a kinematic bicycle with wheelbase L = 2.5 m and steering angle at most 26.57 degrees
(tan = 0.5), so its tightest circle has radius 5 m at the rear axle. The front wheel steers, the rear wheel follows;
no tyre slip. The car's pose (x, y, th) is its rear axle and heading.
The course: 10 m straight along x from (0, 0); a 90-degree left arc of radius 10 m (curvature 0.1 per m); 10 m
straight. For finding look-ahead points the two straights are extended past the course's ends.
The start: rear axle at (0, 1.0), 1.0 m left of the line, heading 0.
The rates: every tracker runs at 20 Hz (Nav2's default controller_frequency) and its steering command is held
between ticks; the car is stepped every 0.01 s along exact arcs.
The lateral error: signed distance from the tracker's reference point to the nearest course point, positive to the
left. Reference point: rear axle for pure pursuit and rear-wheel feedback, front axle for Stanley.
Optional (default off, so the plan's car is the default): tau, a first-order lag of the steering motor, the model
Stanford's car used for its steering (Hoffmann et al. 2007, eq. 4, tau = 0.4 s).
"""
from functools import partial

import numpy as np

L = 2.5                              # m, wheelbase
DELTA_MAX = np.arctan(0.5)           # rad, largest steering angle, 26.57 deg
RATE, DT = 20.0, 0.01                # Hz tracker rate, s simulation step
HOLD = int(round(1 / (RATE * DT)))   # simulation steps per tracker tick (5)
V_BASE, V_FAST = 2.0, 5.0            # m/s
START = (0.0, 1.0, 0.0)              # rear axle x, y (m), heading (rad)
R_ARC = 10.0                         # m
S1 = 10.0                            # course distance where the arc starts
S2 = S1 + np.pi / 2 * R_ARC          # where the arc ends, 25.708 m
S_END = S2 + 10.0                    # end of the course, 35.708 m
S_MID = (S1 + S2) / 2                # middle of the arc, 17.854 m
LD_BASE = 4.0                        # m, pure pursuit's base look-ahead
K_ST, KS_ST = 1.0, 1.0               # Stanley gain (per s) and softening speed (m/s)
KTH_RW, KE_RW = 1.0, 0.5             # rear-wheel feedback: heading gain (per m), lateral gain (per m^2)


def wrap(a):
    return (a + np.pi) % (2 * np.pi) - np.pi


def course(s):
    """Point, heading and curvature of the course at distance s along it (arrays allowed)."""
    s = np.asarray(s, float)
    phi = -np.pi / 2 + (np.clip(s, S1, S2) - S1) / R_ARC
    x = np.where(s < S1, s, np.where(s <= S2, S1 + R_ARC * np.cos(phi), S1 + R_ARC))
    y = np.where(s < S1, 0.0, np.where(s <= S2, R_ARC + R_ARC * np.sin(phi), R_ARC + (s - S2)))
    h = np.where(s < S1, 0.0, np.where(s <= S2, (s - S1) / R_ARC, np.pi / 2))
    k = np.where((s >= S1) & (s <= S2), 1 / R_ARC, 0.0)
    return x, y, h, k


def nearest(px, py):
    """Distance along the course of the course point nearest to (px, py)."""
    cand = [min(px, S1)]
    phi = np.clip(np.arctan2(py - R_ARC, px - S1), -np.pi / 2, 0.0)
    cand.append(S1 + R_ARC * (phi + np.pi / 2))
    cand.append(S2 + max(py - R_ARC, 0.0))
    xs, ys, _, _ = course(cand)
    return cand[int(np.argmin(np.hypot(xs - px, ys - py)))]


def errors(px, py, th):
    """Nearest course distance s, lateral error e (m, + = left) and heading error th - path heading (rad)."""
    s = nearest(px, py)
    cx, cy, h, k = course(s)
    e = -(px - cx) * np.sin(h) + (py - cy) * np.cos(h)
    return s, float(e), float(wrap(th - h)), float(k)


def lookahead_point(px, py, ld):
    """The first course point at or after the nearest point that lies ld from (px, py) (Coulter 1992, §3.3).
    If the car is already more than ld from the course, the nearest point itself."""
    s0 = nearest(px, py)
    ss = s0 + np.arange(0, 2 * ld + 5, 0.002)
    xs, ys, _, _ = course(ss)
    d = np.hypot(xs - px, ys - py)
    if d[0] >= ld:
        return s0, xs[0], ys[0]
    i = int(np.argmax(d >= ld))
    f = (ld - d[i - 1]) / (d[i] - d[i - 1])
    return ss[i - 1] + f * (ss[i] - ss[i - 1]), xs[i - 1] + f * (xs[i] - xs[i - 1]), ys[i - 1] + f * (ys[i] - ys[i - 1])


def to_car(px, py, th, gx, gy):
    """A world point (gx, gy) in the car's frame: x forward, y left, origin at the rear axle (px, py)."""
    dx, dy = gx - px, gy - py
    return np.cos(th) * dx + np.sin(th) * dy, -np.sin(th) * dx + np.cos(th) * dy


# ---------------------------------------------------------------- the trackers: each returns a dict with 'delta'

def pure_pursuit(x, y, th, v, ld=LD_BASE, ld_time=None, ld_min=2.0, ld_max=10.0):
    """Pure pursuit (Coulter 1992): the arc from the rear axle, tangent to the heading, through the course point ld
    ahead; curvature 2 y / ld^2 with y the point's sideways offset in the car's frame; steering atan(L kappa).
    ld_time: if given, the look-ahead grows with speed, ld = |v| ld_time clamped to [ld_min, ld_max] (Nav2 RPP)."""
    if ld_time is not None:
        ld = float(np.clip(abs(v) * ld_time, ld_min, ld_max))
    sg, gx, gy = lookahead_point(x, y, ld)
    cx, cy = to_car(x, y, th, gx, gy)
    kappa = 2 * cy / (cx ** 2 + cy ** 2)
    return dict(delta=float(np.arctan(L * kappa)), kappa=kappa, ld=ld, sg=sg, gx=gx, gy=gy, cx=cx, cy=cy,
                alpha=float(np.arctan2(cy, cx)))


def regulated_pp(x, y, th, v, v_max=V_FAST, r_min=25.0, v_min=0.25, ld_time=2.0, ld_min=2.0, ld_max=10.0):
    """Regulated pure pursuit (Nav2, curvature heuristic only): speed-scaled look-ahead from the present speed, and
    the speed command cut to v_max * R / r_min when the commanded arc's radius R is below r_min, but not below v_min
    (regulation_functions.hpp curvatureConstraint; regulated_linear_scaling_min_speed, Nav2's default 0.25 m/s)."""
    out = pure_pursuit(x, y, th, v, ld_time=ld_time, ld_min=ld_min, ld_max=ld_max)
    radius = 1 / max(abs(out["kappa"]), 1e-9)
    out["v"] = max(v_max * radius / r_min, v_min) if radius < r_min else v_max
    return out


def stanley(x, y, th, v, k=K_ST, ks=KS_ST):
    """Stanley (Hoffmann et al. 2007; Thrun et al. 2006): from the front axle, delta = -th_e - atan(k e / (ks + |v|)),
    where e is the front axle's lateral error (+ = left) and th_e the heading minus the course heading there."""
    fx, fy = x + L * np.cos(th), y + L * np.sin(th)
    s, e, the, _ = errors(fx, fy, th)
    head, cross = -the, -float(np.arctan(k * e / (ks + abs(v))))
    return dict(delta=head + cross, head=head, cross=cross, s=s, e=e, the=the, fx=fx, fy=fy)


def rear_wheel(x, y, th, v, kth=KTH_RW, ke=KE_RW):
    """Rear-wheel feedback (Paden et al. 2016, eq. V.12): turn rate
    omega = v kappa cos(th_e) / (1 - kappa e) - kth |v| th_e - ke v (sin(th_e) / th_e) e, steering atan(L omega / v).
    kth in 1/m, ke in 1/m^2; e and th_e at the rear axle."""
    s, e, the, kap = errors(x, y, th)
    ff = v * kap * np.cos(the) / (1 - kap * e)
    fb_h = -kth * abs(v) * the
    fb_e = -ke * v * np.sinc(the / np.pi) * e
    omega = ff + fb_h + fb_e
    return dict(delta=float(np.arctan(L * omega / v)), omega=omega, ff=ff, fb_h=fb_h, fb_e=fb_e, s=s, e=e, the=the,
                kappa=kap)


# ---------------------------------------------------------------- the simulator

def simulate(law, v=V_BASE, start=START, s_stop=S_END, t_max=60.0, tau=0.0, a_max=None):
    """Drive the car with law(x, y, th, v) -> dict(delta, [v]) called at 20 Hz; the steering command is clamped to
    +-26.57 deg and held until the next tick. tau > 0: the wheels follow the command with a first-order lag of tau s.
    a_max: if given, the speed follows a law's speed command at most a_max m/s^2. Stops when the rear axle's nearest
    course point passes s_stop. Returns a dict of arrays (one row per 0.01 s) and 'ticks', the law's outputs."""
    x, y, th = start
    delta, v_now, v_cmd, delta_cmd = 0.0, v, v, 0.0
    rows, ticks = [], []
    for i in range(int(round(t_max / DT)) + 1):
        if i % HOLD == 0:
            out = law(x, y, th, v_now)
            delta_cmd = float(np.clip(out["delta"], -DELTA_MAX, DELTA_MAX))
            v_cmd = out.get("v", v_now)
            out.update(t=i * DT, x=x, y=y, th=th, v_now=v_now, delta_cmd=delta_cmd)
            ticks.append(out)
            if tau == 0:
                delta = delta_cmd
        s, e, the, _ = errors(x, y, th)
        rows.append((i * DT, x, y, th, delta, v_now, s, e, the))
        if s >= s_stop:
            break
        if tau > 0:
            delta += (delta_cmd - delta) * (1 - np.exp(-DT / tau))
        v_now = v_cmd if a_max is None else v_now + float(np.clip(v_cmd - v_now, -a_max * DT, a_max * DT))
        kap = np.tan(delta) / L
        ds = v_now * DT
        if abs(kap) < 1e-9:
            x, y = x + ds * np.cos(th), y + ds * np.sin(th)
        else:
            x += (np.sin(th + kap * ds) - np.sin(th)) / kap
            y += (np.cos(th) - np.cos(th + kap * ds)) / kap
            th += kap * ds
    a = np.array(rows)
    run = dict(zip(["t", "x", "y", "th", "delta", "v", "s", "e", "the"], a.T))
    fx, fy = run["x"] + L * np.cos(run["th"]), run["y"] + L * np.sin(run["th"])
    sf = np.array([errors(px, py, h) for px, py, h in zip(fx, fy, run["th"])])
    run.update(fx=fx, fy=fy, sf=sf[:, 0], ef=sf[:, 1], ticks=ticks)
    return run


def metrics(run, ref="rear"):
    """The numbers the Notes quote, at the reference point (rear or front axle):
    reach: course distance where |e| first falls below 0.1 m; over: largest error to the right on the first straight
    (m, positive); arc_peak: largest |e| on the arc (signed); arc_mid: e at the middle of the arc;
    exit_peak: largest |e| on the last straight (signed)."""
    s, e = (run["s"], run["e"]) if ref == "rear" else (run["sf"], run["ef"])
    below = np.abs(e) < 0.1
    reach = float(s[np.argmax(below)]) if below.any() else np.nan
    first = s < S1
    over = float(max(0.0, -e[first].min())) if first.any() else 0.0
    arc = (s >= S1) & (s <= S2)
    i_pk = np.argmax(np.abs(np.where(arc, e, 0)))
    i_mid = np.argmin(np.abs(s - S_MID))
    last = s > S2
    i_ex = np.argmax(np.abs(np.where(last, e, 0)))
    return dict(reach=reach, over=over, arc_peak=float(e[i_pk]), arc_mid=float(e[i_mid]),
                exit_peak=float(e[i_ex]) if last.any() else np.nan, steer_max=float(np.degrees(np.abs(run["delta"]).max())))


def law(name, **kw):
    """A tracker by name with its keyword settings fixed: 'pp', 'rpp', 'stanley', 'rear'."""
    f = dict(pp=pure_pursuit, rpp=regulated_pp, stanley=stanley, rear=rear_wheel)[name]
    return partial(f, **kw)


if __name__ == "__main__":
    x, y, h, k = course([0, S1, S_MID, S2, S_END])
    assert np.allclose(x, [0, 10, 10 + 10 * np.cos(-np.pi / 4), 20, 20]) and np.allclose(y[-1], 20)
    assert abs(np.degrees(DELTA_MAX) - 26.565) < 1e-3 and abs(L / np.tan(DELTA_MAX) - 5) < 1e-12
    s, e, the, _ = errors(*START)
    assert s == 0 and abs(e - 1.0) < 1e-12
    out = pure_pursuit(*START, V_BASE)
    assert abs(out["gx"] - np.sqrt(15)) < 1e-3 and abs(out["kappa"] + 0.125) < 1e-4
    print("ok")
