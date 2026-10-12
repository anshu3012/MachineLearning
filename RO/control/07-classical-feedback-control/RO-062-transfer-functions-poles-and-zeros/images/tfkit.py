"""Shared model for this Note (no output when run on its own): the robot's heading loop with PD (and PID) control,
the worn gearbox's drag (RO-060), a time delay, the reversing robot's front point, and the speed loop under PI control.

Heading plant: I th'' = tau + d,   I = 0.1 kg m^2, d the gearbox's drag torque (N m).
Controller:    tau = Kp e + Ki (integral of e) - Kd th',  e = th_ref - th,  Kp = Kd = 0.4 (RO-061's design).
Speed plant:   m v' = u - b v - f, m = 8 kg, b = 2 N s/m, f the ramp's pull (N); PI: u = Kv e + Ki_v (int e), Kv = 20.
"""
import numpy as np
import scipy.signal as sig

M, B, I = 8.0, 2.0, 0.1
KP, KD = 0.4, 0.4                       # heading PD gains from RO-061 (N m/rad, N m s/rad)
D_DRAG = -0.02                        # the worn right gearbox's drag torque (N m), turning the robot right, as in RO-060
V_DRIVE = 0.5                           # driving speed (m/s)
KI_GOOD, KI_BAD = 0.2, 2.0              # integral gains (N m per rad s): a safe one and an unsafe one
KV = 20.0                               # speed loop P gain (N per m/s), RO-059 and RO-060


def char_poly(ki, kp=KP, kd=KD):
    """Closed-loop characteristic polynomial of the PID heading loop, I s^3 + Kd s^2 + Kp s + Ki."""
    return [I, kd, kp, ki]


def poles(ki, kp=KP, kd=KD):
    return np.roots(char_poly(ki, kp, kd))


def drag_response(t, ki, d=D_DRAG):
    """Heading (rad) after the gearbox drag d starts at t = 0, the command held at 0: transfer function
    s / (I s^3 + Kd s^2 + Kp s + Ki) times d / s. With Ki = 0 the s cancels, leaving d / (I s^2 + Kd s + Kp)."""
    if ki == 0:
        sysd = sig.lti([d], [I, KD, KP])
    else:
        sysd = sig.lti([d, 0], char_poly(ki))
    _, th = sig.step(sysd, T=t)
    return th


def drive_path(t, th):
    """Path of the robot driving at 0.5 m/s with heading th(t): x' = v cos th, y' = v sin th (trapezoid rule)."""
    dt = np.diff(t)
    vx, vy = V_DRIVE * np.cos(th), V_DRIVE * np.sin(th)
    x = np.r_[0, np.cumsum(0.5 * (vx[1:] + vx[:-1]) * dt)]
    y = np.r_[0, np.cumsum(0.5 * (vy[1:] + vy[:-1]) * dt)]
    return x, y


def turn_with_delay(t, delay, kp=KP, kd=KD, step=0.5):
    """Heading after a 0.5 rad turn command when the controller sees the heading and turn rate 'delay' seconds late.
    Euler steps of 1 ms (the controller itself runs at every step)."""
    dt = t[1] - t[0]
    nd = int(round(delay / dt))
    th, w = np.zeros(len(t)), np.zeros(len(t))
    for k in range(len(t) - 1):
        j = max(k - nd, 0)
        tau = kp * (step - th[j]) - kd * w[j]
        w[k + 1] = w[k] + dt * tau / I
        th[k + 1] = th[k] + dt * w[k + 1]
    return th


def reverse_front(t, v, a=0.1, step=0.5):
    """The robot turns 0.5 rad (RO-061's critically damped turn) while driving at v (negative: in reverse).
    Returns the axle centre (x, y), heading th and the sideways position of a point a metres ahead of the axle."""
    wn = 2.0
    th = step * (1 - np.exp(-wn * t) * (1 + wn * t))
    dt = np.diff(t)
    vx, vy = v * np.cos(th), v * np.sin(th)
    x = np.r_[0, np.cumsum(0.5 * (vx[1:] + vx[:-1]) * dt)]
    y = np.r_[0, np.cumsum(0.5 * (vy[1:] + vy[:-1]) * dt)]
    return x, y, th, y + a * np.sin(th)


def speed_pi(t, ki, kv=KV, v0=0.4, v_ref=0.5, push=0.785, t_push=10.0):
    """Speed under PI control (RO-060's speed loop: P gain 20 N per m/s), cruising at 0.4 m/s: at t = 0 the command
    steps to 0.5 m/s; from t_push the pull of the 1 % ramp of RO-059, 0.785 N, holds the robot back.
    From the command: (kv s + ki) / (m s^2 + (b + kv) s + ki); from the pull: -s / (same). A fixed push added to the
    command, such as RO-059's 1 N, changes no transfer function, so it is left out of these changes."""
    den = [M, B + kv, ki]
    _, y_ref = sig.step(sig.lti([kv, ki], den), T=t - t[0])
    _, y_unit = sig.step(sig.lti([-push, 0], den), T=t - t[0])
    y_push = np.interp(t - t_push, t - t[0], y_unit, left=0.0)
    return v0 + (v_ref - v0) * y_ref + y_push


if __name__ == "__main__":
    assert np.allclose(sorted(poles(0).real), [-2, -2, 0], atol=1e-6)
    p = poles(1.6)
    assert np.allclose(sorted(np.abs(p.imag)), [0, 2, 2], atol=1e-6) and abs(p.real.min() + 4) < 1e-9
    t = np.linspace(0, 40, 40001)
    assert abs(drag_response(t, 0)[-1] + 0.05) < 1e-6 and abs(drag_response(t, KI_GOOD)[-1]) < 1e-4
    th = turn_with_delay(np.linspace(0, 10, 10001), 0.0)
    assert abs(th.max() - 0.5) < 2e-3
