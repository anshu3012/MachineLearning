"""The room robot of this Note and its three controllers (no output when run on its own).

The robot is RO-001's differential drive: wheel separation 0.2 m, each wheel at most 0.6 m/s over the floor. It is
commanded with a forward speed v (m/s) and a turn rate w (rad/s), the unicycle model x' = v cos th, y' = v sin th,
th' = w. A command whose wheel speeds v +- w L/2 would pass 0.6 m/s is scaled down, v and w by the same factor, so the
robot drives the same arc more slowly. The controller runs at 20 Hz (each command is held 0.05 s) and the robot is
moved in Euler steps of 0.01 s.

Start (RO-001, RO-058): (2.0, 1.0) facing 30 deg. The charging dock: the robot must stop at (3.6, 3.5) facing 90 deg,
its front against the dock on the wall y = 3.75 (the robot is a disk of radius 0.25 m, as in RO-058).

Controllers
- point (Corke RVC3 drivepoint, NPTEL L37): v = K_RHO_P rho, w = K_ALPHA_P alpha;
- line (Corke RVC3 driveline): v = V_LINE, w = -K_D e - K_H psi, e = signed distance to the line (+ left of its
  direction), psi = heading minus the line's direction;
- pose (Corke RVC3 driveconfig, PythonRobotics move_to_pose, Siegwart via COS 495 L6): v = K_RHO rho,
  w = K_ALPHA alpha + K_BETA beta, beta = goal heading - line-of-sight direction; the goal behind (|alpha| > 90 deg at
  the start) makes the robot reverse, with alpha measured from its back (direction fixed at the start, as in Corke);
- graceful (Nav2 nav2_graceful_controller smooth_control_law.cpp, Park and Kuipers 2011): curvature from the
  egocentric polar coordinates, speed v_max / (1 + beta |kappa|^lambda), slowed near the target."""
import numpy as np

L_AXLE = 0.2                 # wheel separation, m
V_WHEEL = 0.6                # largest wheel speed over the floor, m/s
DT_CTRL, DT_SIM = 0.05, 0.01
START = (2.0, 1.0, np.radians(30.0))
GOAL = (3.6, 3.5, np.radians(90.0))
WALL_Y = 3.75                # the dock's face; the robot's front touches it at y = 3.5 + 0.25
R_ROBOT = 0.25
STOP_RHO = 0.01              # the controller stops within 1 cm of the goal point

K_RHO_P, K_ALPHA_P = 1.0, 5.0           # point: 1 per s, 5 per s
V_LINE, K_D, K_H = 0.5, 2.0, 2.0         # line: 0.5 m/s, 2 rad/s per m, 2 per s
K_RHO, K_ALPHA, K_BETA = 1.0, 5.0, -4.0  # pose: 1, 5, -4 per s (spring 4, damper 4: critically damped at 2 rad/s)


def wrap(a):
    """Angle wrapped into (-pi, pi]."""
    return (a + np.pi) % (2 * np.pi) - np.pi


def limit(v, w):
    """Scale (v, w) down so that neither wheel passes V_WHEEL; the ratio w / v (the arc) is kept."""
    top = max(abs(v + w * L_AXLE / 2), abs(v - w * L_AXLE / 2))
    k = min(1.0, V_WHEEL / top) if top > 0 else 1.0
    return v * k, w * k


def polar(q, goal=GOAL, direction=1):
    """rho (m), alpha (rad), beta (rad) of the goal seen from pose q; direction -1 measures alpha from the back."""
    dx, dy = goal[0] - q[0], goal[1] - q[1]
    rho = np.hypot(dx, dy)
    los = np.arctan2(dy, dx) if direction > 0 else np.arctan2(-dy, -dx)
    alpha = wrap(los - q[2])
    beta = wrap(goal[2] - los)
    return rho, alpha, beta


def point_law(q, goal=GOAL, k_rho=K_RHO_P, k_alpha=K_ALPHA_P):
    rho, alpha, _ = polar(q, goal)
    return k_rho * rho, k_alpha * alpha


def line_dist(q, p0=(GOAL[0], 0.0), th_line=GOAL[2]):
    """Signed distance e from the line through p0 with direction th_line (+ to its left), and heading error psi."""
    dx, dy = q[0] - p0[0], q[1] - p0[1]
    e = -np.sin(th_line) * dx + np.cos(th_line) * dy
    return e, wrap(q[2] - th_line)


def line_law(q, v=V_LINE, k_d=K_D, k_h=K_H):
    e, psi = line_dist(q)
    return v, -k_d * e - k_h * psi


def pose_law(q, goal=GOAL, k=(K_RHO, K_ALPHA, K_BETA), direction=1):
    rho, alpha, beta = polar(q, goal, direction)
    return direction * k[0] * rho, k[1] * alpha + k[2] * beta


def graceful_law(q, goal=GOAL, k_phi=2.0, k_delta=1.0, beta=0.4, lam=2.0, v_max=0.5, w_max=1.0,
                 slowdown=1.5, dec_max=2.5, v_min=0.1):
    """Nav2 SmoothControlLaw::calculateRegularVelocity (forward), with the controller's default parameters."""
    dx, dy = goal[0] - q[0], goal[1] - q[1]
    los = np.arctan2(-dy, dx)                    # as in ego_polar_coords.hpp: minus the line of sight
    r = np.hypot(dx, dy)
    phi = wrap(goal[2] + los)                    # goal heading minus the line of sight
    delta = wrap(q[2] + los)                     # robot heading minus the line of sight
    prop = k_delta * (delta - np.arctan(-k_phi * phi))
    fb = (1.0 + k_phi / (1.0 + (k_phi * phi) ** 2)) * np.sin(delta)
    kappa = -1.0 / r * (prop + fb)
    v = v_max / (1.0 + beta * abs(kappa) ** lam)
    v = min(v_max * r / slowdown, v)
    v = min(np.sqrt(2 * r * dec_max), v)
    v = float(np.clip(v, v_min, v_max))
    w = float(np.clip(kappa * v, -w_max, w_max))
    v = w / kappa if kappa != 0 else v
    return v, w


def run(law, q0=START, t_max=20.0, stop=None, use_limit=True):
    """Simulate a law from q0; returns dict of arrays t, x, y, th, v, w (commands as applied).
    stop(q) -> True ends the run; by default the run ends within STOP_RHO of the goal."""
    stop = stop or (lambda q: np.hypot(GOAL[0] - q[0], GOAL[1] - q[1]) < STOP_RHO)
    q = np.array(q0, dtype=float)
    out = {k: [] for k in ("t", "x", "y", "th", "v", "w")}
    n_sub = int(round(DT_CTRL / DT_SIM))
    t = 0.0
    v = w = 0.0
    k = 0
    while t < t_max + 1e-9:
        if k % n_sub == 0:
            if stop(q):
                break
            v, w = law(q)
            if use_limit:
                v, w = limit(v, w)
        for key, val in zip(out, (t, q[0], q[1], q[2], v, w)):
            out[key].append(val)
        q = q + DT_SIM * np.array([v * np.cos(q[2]), v * np.sin(q[2]), w])
        t = round(t + DT_SIM, 10)
        k += 1
    for key, val in zip(out, (t, q[0], q[1], q[2], 0.0, 0.0)):
        out[key].append(val)
    return {k: np.array(v) for k, v in out.items()}
