"""The sampled speed loop of this Note, shared by every figure script (no output when run on its own).

The chapter's robot (robotctl.py): m dv/dt = u - b v, m = 8 kg, b = 2 N s/m, force limited to +-4 N. Its PI speed
controller, kp = 14 N per m/s and ki = 8 N per m, runs as code on a computer: every sample period T it reads the speed
(A/D), computes the force, holds that force until the next sample (D/A with a zero-order hold), then updates its
integral. The plant between samples is stepped finely (0.5 ms), so it stands for the real, continuous robot.
The test: the robot cruises at 0.4 m/s and the command steps to 0.5 m/s at t = 0.
"""
import numpy as np

from robotctl import B, KI, KP, M, U_MAX

DTP = 0.0005                 # s, the fine step that stands for continuous time
R0, R1 = 0.4, 0.5            # m/s, the speed before and after the command step
RATES = (100, 10, 2)         # Hz, the three sample rates compared
W_RIP, A_RIP = 10.0, 0.01    # rad/s and m/s: the once-per-turn ripple of an out-of-round wheel in the speed reading


def sampled_loop(fs, method="fwd", T=8.0, ripple=0.0, tau_f=None, r0=R0, r1=R1, digits=None):
    """Run the PI speed loop sampled at fs Hz for T seconds. method: how the integral is updated,
    'fwd' (forward Euler, output first, then I += ki T e), 'bwd' (backward Euler, I += ki T e first) or
    'tus' (Tustin, I += ki T (e + e_last) / 2 first). ripple: amplitude of the wheel ripple in the reading (m/s).
    tau_f: time constant of an analog low-pass filter on the reading before sampling (s), or None.
    digits: if given, the A/D rounds each reading to this many decimals (0.0001 m/s for 4).
    Returns a dict: fine time t, true speed v, applied force u, and per-sample arrays tk, yk (reading), ek, uk, ik."""
    n_hold = int(round(1.0 / (fs * DTP)))
    Ts = n_hold * DTP
    n = int(round(T / DTP))
    v, I, u, vf, e_last = r0, B * r0, B * r0, r0, 0.0
    t = np.arange(n + 1) * DTP
    vs, us = np.empty(n + 1), np.empty(n + 1)
    rows = []
    for i in range(n + 1):
        y = v + ripple * np.sin(W_RIP * t[i])                 # what the sensor reads
        if tau_f:
            vf += DTP * (y - vf) / tau_f                       # analog filter before the A/D
            y = vf
        if i % n_hold == 0:                                    # a clock tick: A/D, compute, D/A
            if digits is not None:
                y = round(y, digits)
            e = r1 - y
            if method == "fwd":
                c = KP * e + I
                I_next = I + KI * Ts * e
            elif method == "bwd":
                I_next = I + KI * Ts * e
                c = KP * e + I_next
            else:
                I_next = I + KI * Ts * (e + e_last) / 2
                c = KP * e + I_next
            u = float(np.clip(c, -U_MAX, U_MAX))
            rows.append((t[i], y, e, u, I))
            I, e_last = I_next, e
        vs[i], us[i] = v, u
        v += DTP * (u - B * v) / M
    k = np.array(rows)
    return dict(t=t, v=vs, u=us, tk=k[:, 0], yk=k[:, 1], ek=k[:, 2], uk=k[:, 3], ik=k[:, 4], Ts=Ts)


def continuous_loop(T=8.0, **kw):
    """The PI controller updated every 0.5 ms: as close to the continuous formula as we need."""
    return sampled_loop(1.0 / DTP, T=T, **kw)


def overshoot(run, r0=R0, r1=R1):
    """Overshoot of the speed, in percent of the step."""
    return (run["v"].max() - r1) / (r1 - r0) * 100


def plant_zoh(Ts):
    """The robot's speed, sampled every Ts with the force held: v[k+1] = a v[k] + g u[k] (exact)."""
    a = np.exp(-B * Ts / M)
    return a, (1 - a) / B


def loop_poles(Ts):
    """Poles of the sampled loop (forward-Euler PI): states v[k] and I[k]."""
    a, g = plant_zoh(Ts)
    A = np.array([[a - g * KP, g], [-KI * Ts, 1.0]])
    return np.linalg.eigvals(A)


if __name__ == "__main__":
    ov = {fs: overshoot(sampled_loop(fs)) for fs in RATES}
    assert abs(overshoot(continuous_loop()) - 4.9) < 0.05
    assert [round(ov[f], 1) for f in RATES] == [5.0, 5.7, 17.5]
    assert abs(loop_poles(1.1175)).max() > 1 > abs(loop_poles(1.117)).max()   # a pole leaves through -1 at T = 1.1175 s
    assert abs(min(loop_poles(2.0).real) + 2.029) < 5e-4                     # 0.5 Hz: a pole at -2.029
