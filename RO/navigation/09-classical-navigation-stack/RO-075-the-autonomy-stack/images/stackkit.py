"""The simulations of this Note (no output when run on its own), all in the room of RO-058 (bandkit.py, copied).

- Sense-plan-act: a loop that looks at the world once every T seconds. Between looks the robot drives the plan it made
  from the map (RO-058's drive in a clear room, bandkit's run without the person); at the first look after the person
  steps in (2.4 s) it brakes at the robot's limit, 0.5 m/s^2, along the same path.
- A Braitenberg vehicle: two light sensors at the front of the disk robot, 45 degrees either side of its heading,
  each wired to the wheel on its own side so that more light slows that wheel (Braitenberg's vehicle 3a); a lamp marks
  the door pose (3.6, 3.5). Wheel speeds v_wheel = 0.6 (1 - s) m/s for a reading s from 0 to 1.
- Subsumption (Brooks 1986): level 0 "avoid" (collide: halt if a range reading straight ahead is short; runaway: turn
  away from close readings) and level 1 "go to the light" (the Braitenberg wheels plus a turn away from close readings,
  which suppresses runaway's output). A ring of 36 range readings, one every 10 degrees, out to 1.0 m.
All steps are 0.01 s; the forward speed changes by at most 0.5 m/s^2 and each wheel turns at most 0.6 m/s."""
import math

import numpy as np

import bandkit as bk
from trajkit import A_MAX, L_AXLE, R_BODY, V_WHEEL

DT = 0.01
LAMP = np.array([3.6, 3.5])                       # the lamp marks the door pose
D0 = 1.0                                          # light reading falls to half at 1.0 m: I = 1 / (1 + (d / D0)^2)
K_WIRE = 2.0                                      # each wire multiplies its sensor's reading by 2
SENSOR_ANGLE = math.radians(45)                   # light sensors 45 degrees either side of the heading, at the rim
N_BEAMS, RANGE_MAX = 36, 1.0                      # range ring: 36 readings 10 degrees apart, out to 1.0 m from the rim
HALT_DIST, HALT_ARC = 0.42, math.radians(30)      # collide: halt if within 0.42 m of the rim, within 30 deg of ahead:
                                                  # 0.36 m to brake from 0.6 m/s at 0.5 m/s^2, plus 0.06 m in one 0.1 s look
FORCE_DIST = 0.5                                  # readings nearer than 0.5 m from the rim push the robot away
K_TURN = 2.0                                      # turn rate per unit of push (rad/s)


# ---------------------------------------------------------------- sense-plan-act at a slow rate
def spa(period, t_person=bk.T_PERSON):
    """Drive the clear-room plan; at the first look at or after t_person, brake at A_MAX along the same path.
    Returns times, positions, speeds, the look time and the gap left at the look."""
    F = bk.results()["free"]
    xs = np.array([o["x"][:2] for o in F])
    vs = np.array([o["v"] for o in F])
    ts = np.array([o["t"] for o in F])
    s = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(xs, axis=0).T))])
    t_look = math.ceil(round(t_person / period, 9)) * period
    v_look = float(np.interp(t_look, ts, vs))
    out_t, out_x, out_v = [], [], []
    t, s_now, v = 0.0, 0.0, 0.0
    while t <= ts[-1] + 1e-9:
        if t <= t_look + 1e-9:                     # still on the old plan, up to the look
            s_now = float(np.interp(t, ts, s))
            v = float(np.interp(t, ts, vs))
        else:                                      # braking: move with last step's speed, then slow down
            s_now += v * DT
            v = max(0.0, v_look - A_MAX * (t - t_look))
        p = np.array([np.interp(s_now, s, xs[:, 0]), np.interp(s_now, s, xs[:, 1])])
        out_t.append(t), out_x.append(p), out_v.append(v)
        if t > t_look and v == 0.0:
            break
        t = round(t + DT, 10)
    out_x = np.array(out_x)
    gaps = person_gap(out_x)
    k_look = int(round(t_look / DT))
    return dict(t=np.array(out_t), x=out_x, v=np.array(out_v), t_look=t_look, gap=gaps,
                gap_look=float(gaps[k_look]), v_look=v_look)


def person_gap(xy):
    xy = np.atleast_2d(xy)
    return np.hypot(xy[:, 0] - bk.PERSON[0], xy[:, 1] - bk.PERSON[1]) - bk.PERSON_R - R_BODY


# ---------------------------------------------------------------- range readings by ray marching on distance functions
def ranges(pose, person=None, n=N_BEAMS, rmax=RANGE_MAX, origin=R_BODY):
    """Distance from the robot's rim (origin = R_BODY; 0 for a sensor at the centre) to the nearest obstacle along n
    rays, bearings measured from the heading (positive = left), capped at rmax. Sphere tracing on the exact distance
    functions of bandkit (room, table, cabinet, poles, walls, and the person if given), all rays at once."""
    obs = bk.obstacles(person)
    x, y, th = pose
    b = np.arange(n) * 2 * math.pi / n
    b = np.where(b > math.pi, b - 2 * math.pi, b)
    dx, dy = np.cos(th + b), np.sin(th + b)
    t = np.full(n, float(origin))
    live = np.ones(n, bool)
    for _ in range(200):
        px, py = x + t * dx, y + t * dy
        d = np.min([o(px, py) for o in obs], axis=0)
        live &= (d >= 1e-3) & (t < origin + rmax)
        if not live.any():
            break
        t = np.where(live, t + d, t)
    return b, np.minimum(t, origin + rmax) - origin


# ---------------------------------------------------------------- the light sensors
def light(pose, lamp=LAMP):
    """Readings of the left and right light sensors, each from 0 to 1: the lamp's brightness at the sensor,
    1 / (1 + (d / D0)^2), times how squarely the sensor faces the lamp, (1 + cos a) / 2 for the angle a between
    the sensor's direction and the lamp: 1 straight ahead, 1/2 square to the side, 0 straight behind."""
    x, y, th = pose
    out = []
    for side in (+1, -1):                          # left, right
        a = th + side * SENSOR_ANGLE
        sx, sy = x + R_BODY * math.cos(a), y + R_BODY * math.sin(a)
        dx, dy = lamp[0] - sx, lamp[1] - sy
        d = math.hypot(dx, dy)
        facing = (1 + (dx * math.cos(a) + dy * math.sin(a)) / d) / 2 if d > 1e-9 else 1.0
        out.append(facing / (1 + (d / D0) ** 2))
    return out[0], out[1]


def braitenberg_wheels(sL, sR, wiring="3a"):
    """Wheel speeds from the two readings, each wire multiplying its reading by the gain K_WIRE and the wheel speed
    kept between 0 and V_WHEEL. 3a: same side, more light slows the wheel. 3b: crossed, more light slows the other
    wheel. 2a: same side, more light speeds the wheel up. 2b: crossed, more light speeds up the other wheel."""
    c = lambda u: float(np.clip(u, 0.0, 1.0)) * V_WHEEL
    k = K_WIRE
    if wiring == "3a":
        return c(1 - k * sL), c(1 - k * sR)
    if wiring == "3b":
        return c(1 - k * sR), c(1 - k * sL)
    if wiring == "2a":
        return c(k * sL), c(k * sR)
    return c(k * sR), c(k * sL)                     # 2b


def step(state, vL_cmd, vR_cmd, a_max=A_MAX):
    """Move the robot DT seconds: the forward speed follows the command within a_max, both wheels within V_WHEEL."""
    x, y, th, v = state
    v_cmd = (vR_cmd + vL_cmd) / 2
    w_cmd = (vR_cmd - vL_cmd) / L_AXLE
    v_new = float(np.clip(v + np.clip(v_cmd - v, -a_max * DT, a_max * DT), -V_WHEEL, V_WHEEL))
    lim = (V_WHEEL - abs(v_new)) / (L_AXLE / 2)
    w = float(np.clip(w_cmd, -lim, lim))
    th_m = th + w * DT / 2
    return np.array([x + DT * v_new * math.cos(th_m), y + DT * v_new * math.sin(th_m), th + w * DT, v_new]), w


def collided(state, person=None):
    return float(bk.gap(np.array([state[0]]), np.array([state[1]]), person)[0]) < 0


def run_braitenberg(start=(2.0, 1.0, math.radians(30)), wiring="3a", t_end=20.0, lamp=LAMP):
    """The vehicle alone, no person. Stops the run when it touches an obstacle or has nearly stopped."""
    s = np.array([*start, 0.0])
    rec = []
    t = 0.0
    while t <= t_end + 1e-9:
        sL, sR = light(s[:3], lamp)
        vL, vR = braitenberg_wheels(sL, sR, wiring)
        hit = collided(s)
        rec.append(dict(t=t, x=s.copy(), s=(sL, sR), wheels=(vL, vR), hit=hit))
        if hit:
            break
        s, _ = step(s, vL, vR)
        t = round(t + DT, 10)
    return rec


# ---------------------------------------------------------------- subsumption: two levels
def push(b, r):
    """Brooks's feelforce: each reading nearer than FORCE_DIST pushes away from its direction, harder when nearer.
    Returns the push in the robot's frame (ahead, left)."""
    k = r < FORCE_DIST
    w = (FORCE_DIST - r[k]) / FORCE_DIST
    return -float(np.sum(w * np.cos(b[k]))), -float(np.sum(w * np.sin(b[k])))


def run_subsumption(start=(2.0, 1.0, math.radians(30)), t_person=bk.T_PERSON, person=bk.PERSON, t_end=20.0,
                    levels=(0, 1), sense_dt=0.1):
    """Levels run in parallel on the same readings, taken every sense_dt seconds. Level 0: collide halts the robot
    when a reading within 30 degrees of ahead is under 0.42 m; runaway turns the robot towards the push and drives
    it away if pushed. Level 1: the Braitenberg wheels of vehicle 3a, plus a turn K_TURN times the sideways push;
    its command suppresses runaway's. Collide's halt is never suppressed. Records which module drives the wheels."""
    s = np.array([*start, 0.0])
    rec = []
    t = 0.0
    b, r = ranges(s[:3], None)
    cmd, who = (0.0, 0.0), "none"
    while t <= t_end + 1e-9:
        seen = person if (person is not None and t >= t_person - 1e-9) else None
        if abs(t / sense_dt - round(t / sense_dt)) < 1e-6:
            b, r = ranges(s[:3], seen)
            fx, fy = push(b, r)
            ahead = np.abs(b) <= HALT_ARC
            halt = bool(np.any(r[ahead] < HALT_DIST))
            # level 0, runaway: turn towards the push, drive along it if it points ahead
            mag = math.hypot(fx, fy)
            if mag > 1e-9:
                ang = math.atan2(fy, fx)
                w0 = K_TURN * ang
                v0 = 0.3 * max(0.0, math.cos(ang)) * min(1.0, mag)
                run = (v0 - w0 * L_AXLE / 2, v0 + w0 * L_AXLE / 2)
            else:
                run = (0.0, 0.0)
            who = "runaway"
            cmd = run
            if 1 in levels:
                sL, sR = light(s[:3])
                vL, vR = braitenberg_wheels(sL, sR, "3a")
                v1, w1 = (vL + vR) / 2, (vR - vL) / L_AXLE + K_TURN * fy
                cmd = (v1 - w1 * L_AXLE / 2, v1 + w1 * L_AXLE / 2)
                who = "go to the light"
            if halt and 0 in levels:
                v_keep = 0.0
                w_keep = (cmd[1] - cmd[0]) / L_AXLE
                cmd = (v_keep - w_keep * L_AXLE / 2, v_keep + w_keep * L_AXLE / 2)
                who = "collide: halt"
        hit = collided(s, seen)
        rec.append(dict(t=t, x=s.copy(), cmd=cmd, who=who, hit=hit, person=seen, b=b, r=r))
        if hit:
            break
        s, _ = step(s, *cmd)
        t = round(t + DT, 10)
    return rec


def run_open(wiring, start=(-1.5, -0.6, 0.0), lamp=(0.0, 0.0), t_end=10.0):
    """One vehicle on an open floor with a lamp and nothing else; its wheels follow the wiring at once (no
    acceleration limit), as in Braitenberg's thought experiments. Stops the run if its rim reaches the lamp."""
    lamp = np.array(lamp)
    s = np.array([*start, 0.0])
    rec = []
    t = 0.0
    while t <= t_end + 1e-9:
        sL, sR = light(s[:3], lamp)
        vL, vR = braitenberg_wheels(sL, sR, wiring)
        rec.append(dict(t=t, x=s.copy(), s=(sL, sR), wheels=(vL, vR)))
        if math.hypot(*(s[:2] - lamp)) < R_BODY:
            break
        s, _ = step(s, vL, vR, a_max=np.inf)
        t = round(t + DT, 10)
    return rec
