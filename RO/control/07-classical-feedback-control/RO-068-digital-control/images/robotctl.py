"""The chapter's robot and its speed loop, shared by every figure script of this Note (no output when run).

Speed plant (all of chapter RO-07): m dv/dt = u - b v + d, with mass m = 8 kg, rolling drag b = 2 N s/m, drive force u
limited to +-4 N (largest acceleration 0.5 m/s^2 from rest), open-loop time constant m/b = 4 s, top speed 0.6 m/s,
cruise 0.5 m/s. Heading plant: I dw/dt = tau + tau_d, dtheta/dt = w, yaw inertia I = 0.1 kg m^2, torque limited to
+-0.2 N m; a gyro measures the yaw rate w. The controller runs at 100 Hz (dt = 0.01 s); the plant is stepped with
the same dt (forward Euler), fine because 0.01 s is 400 times shorter than the 4 s time constant.

Speed loop PI gains (fixed by RO-059 and RO-060): kp = 20 N per m/s, ki = 10 N per m. The closed loop
8 s^2 + (2 + kp) s + ki = 8 s^2 + 22 s + 10 has its poles at -0.575 and -2.175 rad/s.
"""
import numpy as np

M, B, U_MAX = 8.0, 2.0, 4.0          # kg, N s/m, N
V_TOP, V_CRUISE, A_PLAN = 0.6, 0.5, 0.5
I_YAW, TAU_MAX = 0.1, 0.2            # kg m^2, N m
DT = 0.01                            # s, 100 Hz
KP, KI = 20.0, 10.0                  # N/(m/s), N/m


def speed_loop(T, vref, *, kp=KP, ki=KI, aref=None, ff=False, b_model=B, b_true=B, dist=None, hold=None,
               mode="none", kaw=None, umax=U_MAX, v0=0.0, i0=None, sf=None):
    """Simulate the PI speed loop for T seconds at 100 Hz.
    vref(t), aref(t): reference speed and acceleration (functions of time). ff: add the feedforward m a_ref + b v_ref
    (with the model's drag b_model). dist(t): disturbance force in N. hold: (t0, t1), a hand holds the robot still.
    mode: 'none' (plain PI), 'clamp' (conditional integration), 'bc' (back-calculation with gain kaw).
    sf: (k, kf), state feedback u = -k v + kf r instead of PI (ki = 0 then means no integral state).
    i0: starting integral term in N (default: the force that holds v0). Returns a dict of arrays."""
    n = int(round(T / DT)) + 1
    t = np.arange(n) * DT
    v = v0
    I = b_true * v0 if i0 is None else i0
    out = {k: np.zeros(n) for k in ("v", "u", "c", "i", "e", "uff", "r")}
    for k in range(n):
        tk = t[k]
        r = vref(tk)
        e = r - v
        uff = (M * (aref(tk) if aref else 0.0) + b_model * r) if ff else 0.0
        if sf:
            c = -sf[0] * v + sf[1] * r + I
        else:
            c = uff + kp * e + I
        u = float(np.clip(c, -umax, umax))
        for key, val in zip(("v", "u", "c", "i", "e", "uff", "r"), (v, u, c, I, e, uff, r)):
            out[key][k] = val
        if mode == "none":
            I += ki * e * DT
        elif mode == "clamp":
            if not (c != u and e * c > 0):       # saturated and the error pushes further: stop integrating
                I += ki * e * DT
        elif mode == "bc":
            I += (ki * e + kaw * (u - c)) * DT
        d = dist(tk) if dist else 0.0
        if hold and hold[0] <= tk < hold[1]:
            v = 0.0
        else:
            v += DT * (u - b_true * v + d) / M
    out["t"] = t
    return out


if __name__ == "__main__":
    # closed-loop poles at -0.575 and -2.175 rad/s
    assert np.allclose(sorted(np.roots([M, B + KP, KI])), [-2.1754, -0.5746], atol=5e-4)
    # holding 0.5 m/s needs the drag force b v = 1 N, which the integral supplies in steady state
    s = speed_loop(30, lambda t: 0.5, v0=0.5)
    assert abs(s["v"][-1] - 0.5) < 1e-6 and abs(s["i"][-1] - 1.0) < 1e-6
