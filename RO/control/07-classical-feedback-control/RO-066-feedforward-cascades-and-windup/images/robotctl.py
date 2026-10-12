"""The chapter's robot and the controllers of this Note, shared by every figure script (no output when run).

Speed plant (all of chapter RO-07): m dv/dt = u - b v + d, with mass m = 8 kg, rolling drag b = 2 N s/m, drive force u
limited to +-4 N (largest acceleration 0.5 m/s^2 from rest), open-loop time constant m/b = 4 s, top speed 0.6 m/s,
cruise 0.5 m/s. Heading plant: I dw/dt = tau + tau_d, dtheta/dt = w, yaw inertia I = 0.1 kg m^2, torque limited to
+-0.2 N m; a gyro measures the yaw rate w. The controller runs at 100 Hz (dt = 0.01 s); the plant is stepped with
the same dt (forward Euler), fine because 0.01 s is 400 times shorter than the 4 s time constant.

Speed loop PI gains, the chapter's (RO-060): kp = 20 N per m/s, ki = 10 N per m. The closed loop
8 s^2 + (2 + kp) s + ki = 8 s^2 + 22 s + 10 has its poles at -0.575 and -2.175 rad/s.
Heading PID, the chapter's (RO-060): kp = 0.2 N m per rad, kd = 0.283 N m s per rad (on the gyro), ki = 0.05.
"""
import numpy as np

M, B, U_MAX = 8.0, 2.0, 4.0          # kg, N s/m, N
V_TOP, V_CRUISE, A_PLAN = 0.6, 0.5, 0.5
I_YAW, TAU_MAX = 0.1, 0.2            # kg m^2, N m
DT = 0.01                            # s, 100 Hz
KP, KI = 20.0, 10.0                  # N/(m/s), N/m, RO-060's speed PI
H_KP, H_KD, H_KI = 0.2, 0.283, 0.05  # RO-060's heading PID
G = 9.81
A_SMOOTH = 0.25                      # m/s^2, the speed-up of the planner's profile and the smoother's limit
RAMP_1DEG = M * G * np.sin(np.radians(1.0))    # 1.37 N pulling back on a 1 degree ramp
KTH, KW, KIW, W_CAP = 1.0, 2.0, 10.0, 1.0      # heading cascade: outer P, inner PI on the gyro, yaw-rate cap
RES = (1.0, 6.0, 17.5)               # resonator: w0 = 1 rad/s, gains on its two states


def profile(t, a=A_SMOOTH, v=V_CRUISE):
    """The planner's speed-up: from rest at a m/s^2 up to v, then cruise."""
    return min(a * t, v) if t >= 0 else 0.0


def profile_acc(t, a=A_SMOOTH, v=V_CRUISE):
    return a if 0 <= t < v / a else 0.0


def speed_loop(T, vref, *, kp=KP, ki=KI, aref=None, ff=False, b_model=B, b_true=B, dist=None, hold=None,
               mode="none", kaw=None, umax=U_MAX, u_act=None, v0=0.0, i0=None, sf=None, res=None):
    """Simulate the speed loop for T seconds at 100 Hz.
    vref(t), aref(t): reference speed and acceleration (functions of time). ff: add the feedforward m a_ref + b v_ref
    (with the model's drag b_model). dist(t): disturbance force in N. hold: (t0, t1), the robot is held still.
    mode: 'none' (plain PI), 'clamp' (conditional integration), 'bc' (back-calculation with gain kaw, 1/s).
    sf: (k, kf), state feedback u = -k v + kf r (+ the integral state when ki > 0) instead of PI.
    res: (w0, kr1, kr2), add a resonator q'' = -w0^2 q + e whose output kr1 q + kr2 q' joins the command.
    umax: the limit the controller assumes; u_act: the drive's real limit if lower (a weak battery).
    i0: starting integral term in N (default: the force that holds v0). Returns a dict of arrays."""
    n = int(round(T / DT)) + 1
    t = np.arange(n) * DT
    v = v0
    I = b_true * v0 if i0 is None else i0
    q1 = q2 = 0.0
    keys = ("v", "u", "c", "i", "e", "uff", "r", "ures")
    out = {k: np.zeros(n) for k in keys}
    for k in range(n):
        tk = t[k]
        r = vref(tk)
        e = r - v
        uff = (M * (aref(tk) if aref else 0.0) + b_model * r) if ff else 0.0
        ures = res[1] * q1 + res[2] * q2 if res else 0.0
        c = (-sf[0] * v + sf[1] * r + I) if sf else (uff + kp * e + I + ures)
        u = float(np.clip(c, -umax, umax))
        ua = float(np.clip(u, -u_act, u_act)) if u_act else u
        for key, val in zip(keys, (v, ua, c, I, e, uff, r, ures)):
            out[key][k] = val
        if mode == "none":
            I += ki * e * DT
        elif mode == "clamp":
            if not (c != u and e * c > 0):       # saturated and the error pushes further: stop integrating
                I += ki * e * DT
        elif mode == "bc":
            I += (ki * e + kaw * (u - c)) * DT
        if res:                                  # exact 100 Hz oscillator at w0, driven by the error
            cw, sw = np.cos(res[0] * DT), np.sin(res[0] * DT)
            q1, q2 = cw * q1 + sw / res[0] * q2, -res[0] * sw * q1 + cw * q2 + DT * e
        d = dist(tk) if dist else 0.0
        if hold and hold[0] <= tk < hold[1]:
            v = 0.0
        else:
            v += DT * (ua - b_true * v + d) / M
    out["t"] = t
    return out


def heading_loop(T, th_ref, *, kth=KTH, kw=KW, kiw=KIW, wcap=W_CAP, tau_d=None, th0=0.0):
    """The heading cascade at 100 Hz: outer P on the heading gives a yaw-rate command, capped at wcap; inner PI on
    the gyro's yaw rate gives the torque, limited to +-0.2 N m, with clamping. tau_d(t): disturbance torque."""
    n = int(round(T / DT)) + 1
    th, w, I = th0, 0.0, 0.0
    keys = ("th", "w", "wc", "tau", "c", "i")
    out = {k: np.zeros(n) for k in keys}
    for k in range(n):
        t = k * DT
        wc = float(np.clip(kth * (th_ref(t) - th), -wcap, wcap))
        e = wc - w
        c = kw * e + I
        tau = float(np.clip(c, -TAU_MAX, TAU_MAX))
        for key, val in zip(keys, (th, w, wc, tau, c, I)):
            out[key][k] = val
        if not (c != tau and e * c > 0):
            I += kiw * e * DT
        d = tau_d(t) if tau_d else 0.0
        w += DT * (tau + d) / I_YAW
        th += DT * w
    out["t"] = np.arange(n) * DT
    return out


def heading_pid(T, th_ref, *, kp=H_KP, ki=H_KI, kd=H_KD, tau_d=None, clamp=False):
    """A single heading loop at 100 Hz: torque = kp e + ki (running total of e) - kd w, with the gyro's yaw rate w as
    the derivative (no kick), limited to +-0.2 N m; optional clamping. Same plant as heading_loop."""
    n = int(round(T / DT)) + 1
    th, w, I = 0.0, 0.0, 0.0
    keys = ("th", "w", "tau")
    out = {k: np.zeros(n) for k in keys}
    for k in range(n):
        t = k * DT
        e = th_ref(t) - th
        c = kp * e + I - kd * w
        tau = float(np.clip(c, -TAU_MAX, TAU_MAX))
        for key, val in zip(keys, (th, w, tau)):
            out[key][k] = val
        if not (clamp and c != tau and e * c > 0):
            I += ki * e * DT
        d = tau_d(t) if tau_d else 0.0
        w += DT * (tau + d) / I_YAW
        th += DT * w
    out["t"] = np.arange(n) * DT
    return out


def smoother(cmds, f=20.0, acc=A_SMOOTH, dec=A_SMOOTH, vmax=V_TOP, deadband=0.02):
    """Nav2's velocity smoother, open loop, one axis: each cycle clamp the command to +-vmax, move the last output
    towards it by at most acc/f (speeding up) or dec/f (slowing down), and publish 0 if the result is below the
    deadband (the internal value keeps the unrounded result). Returns (published, internal)."""
    last, pub, inner = 0.0, [], []
    for c in cmds:
        c = float(np.clip(c, -vmax, vmax))
        up = abs(c) >= abs(last) and c * last >= 0
        step = (acc if up else dec) / f
        last = last + float(np.clip(c - last, -step, step))
        inner.append(last)
        pub.append(0.0 if abs(last) < deadband else last)
    return np.array(pub), np.array(inner)


F_DOCK = 2.0                         # N, the contact force the dock's charging contacts want


def dock_run(T, ctrl, *, t_back=32.0, x_dock=0.1, creep=0.05):
    """Docking at 100 Hz. The robot creeps at 0.05 m/s (feedforward plus PI) towards a rigid dock 0.1 m ahead; it
    touches at t = 2 s. At t_back the plan says back away at 0.05 m/s. The dock pushes back but never pulls: while the
    robot stands against it, the dock's force equals the drive force.
    ctrl: 'none' or 'clamp' (motion control throughout, without or with clamping), or 'force' (from contact until
    t_back the drive force is set to F_DOCK; then motion control again with a fresh integral)."""
    n = int(round(T / DT)) + 1
    v, I, x, touched = creep, 0.0, 0.0, False
    keys = ("x", "v", "u", "f", "i")
    out = {k: np.zeros(n) for k in keys}
    for k in range(n):
        t = k * DT
        r = creep if t < t_back else -creep
        e = r - v
        if ctrl == "force" and touched and t < t_back:
            c = F_DOCK
        else:
            if ctrl == "force" and t >= t_back and touched:
                touched, I = False, 0.0              # back to motion control
            c = B * r + KP * e + I
        u = float(np.clip(c, -U_MAX, U_MAX))
        motion = not (ctrl == "force" and t < t_back and touched)
        if motion and (ctrl == "none" or not (c != u and e * c > 0)):
            I += KI * e * DT
        vn = v + DT * (u - B * v) / M
        xn = x + DT * vn
        f = 0.0
        if xn >= x_dock and u > 0:                   # against the dock: still, and the dock pushes back with u
            xn, vn, f = x_dock, 0.0, u
            touched = touched or ctrl == "force"
        for key, val in zip(keys, (x, v, u, f, I)):
            out[key][k] = val
        v, x = vn, xn
    out["t"] = np.arange(n) * DT
    return out


if __name__ == "__main__":
    # both closed-loop poles at -1 rad/s; the inner heading loop's at -10 rad/s
    assert np.allclose(sorted(np.roots([M, B + KP, KI])), [-2.1754, -0.5746], atol=1e-4)
    assert np.allclose(np.roots([I_YAW, KW, KIW]), [-10, -10])
    # holding 0.5 m/s needs the drag force b v = 1 N, which the integral supplies in steady state
    s = speed_loop(30, lambda t: 0.5, v0=0.5)
    assert abs(s["v"][-1] - 0.5) < 1e-6 and abs(s["i"][-1] - 1.0) < 1e-6
    # the smoother climbs 0.0125 m/s per 20 Hz cycle; outputs under the 0.02 m/s deadband are published as 0
    p, inner = smoother([0.5] * 3 + [0.015] * 200)
    assert np.allclose(inner[:3], [0.0125, 0.025, 0.0375]) and np.allclose(p[:3], [0.0, 0.025, 0.0375])
    assert abs(inner[-1] - 0.015) < 1e-12 and p[-1] == 0.0
