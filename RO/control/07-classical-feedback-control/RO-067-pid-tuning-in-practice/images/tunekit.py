"""The running example of the PID-tuning Note, shared by every figure script (no output when run on its own).

Speed loop: the chapter's robot, m dv/dt = u - b v + d (m = 8 kg, b = 2 N s/m, |u| <= 4 N), at 100 Hz. The controller
does not see the true speed: it averages the wheel speeds over the last 20 samples (0.2 s), so the measured speed
describes the robot of about 0.1 s ago. Heading loop: I dw/dt = tau (I = 0.1 kg m^2, |tau| <= 0.2 N m) under a PID
with RO-060's gains kp = 0.2 N m/rad, ki = 0.05 N m/(rad s), kd = 0.283 N m s/rad.
"""
import numpy as np
from scipy import signal

from robotctl import B, DT, I_YAW, KI, KP, M, TAU_MAX, U_MAX

NW = 20                                  # samples in the speed average (0.2 s)
G = 9.81
RAMP = M * G * np.sin(np.radians(1.0))   # 1.37 N pulling back on a 1 degree ramp
KC, TC = 200.0, 0.40                     # critical gain (N per m/s) and period (s) read off the experiment
ZN_PI = (0.45 * KC, 0.45 * KC / (TC / 1.2))                      # 90, 270
K_FOTD, TAU_FOTD, T_FOTD = 0.5, 0.094, 4.00                      # bump-test model
FBS_PI = ((0.15 * TAU_FOTD + 0.35 * T_FOTD) / (K_FOTD * TAU_FOTD),
          (0.46 * TAU_FOTD + 0.02 * T_FOTD) / (K_FOTD * TAU_FOTD ** 2))   # 30.1, 27.9
GAINS = {"RO-060's gains": (KP, KI), "bump-test rule": FBS_PI, "Ziegler–Nichols": ZN_PI}
HKP, HKI, HKD = 0.2, 0.05, 0.283         # heading PID of RO-060
TD = HKD / HKP                           # derivative time 0.5 s
R_WHEEL, L_WHEELS, TICKS = 0.05, 0.2, 1024
DS = 2 * np.pi * R_WHEEL / TICKS         # 0.307 mm of wheel travel per encoder tick
F_VIB, A_VIB = 10.0, 0.3                 # frame bending: 10 Hz, 0.3 rad/s on the gyro


def speed_run(T, kp, ki, *, r=lambda t: 0.5, d=lambda t: 0.0, v0=0.5, bias=None, extra=0, nw=NW):
    """PI (or P with a fixed bias force) on the averaged speed. extra: samples of added delay. Returns t, v, y, u."""
    n = int(round(T / DT)) + 1
    t = np.arange(n) * DT
    v, buf = v0, [v0] * (nw + extra)
    integ = B * v0
    V, Y, U = np.zeros(n), np.zeros(n), np.zeros(n)
    for k in range(n):
        y = np.mean(buf[len(buf) - nw - extra:len(buf) - extra])
        e = r(t[k]) - y
        c = (bias + kp * e) if bias is not None else kp * e + integ
        u = float(np.clip(c, -U_MAX, U_MAX))
        V[k], Y[k], U[k] = v, y, u
        integ += ki * e * DT
        v += DT * (u - B * v + d(t[k])) / M
        buf.append(v)
    return t, V, Y, U


def bump_test(T=30.0, force=1.0):
    """Open loop from rest: the drive force steps to 1 N at t = 0. Returns t, true speed, averaged speed."""
    n = int(round(T / DT)) + 1
    t = np.arange(n) * DT
    v, buf, V, Y = 0.0, [0.0] * NW, np.zeros(n), np.zeros(n)
    for k in range(n):
        V[k], Y[k] = v, np.mean(buf[-NW:])
        v += DT * (force - B * v) / M
        buf.append(v)
    return t, V, Y


def fotd_fit(t, y, force=1.0):
    """Read the bump test as Feedback Systems Fig. 11.7a: steepest tangent, its intercepts, T63 and K."""
    K = y[-1] / force
    sl = np.gradient(y, t)
    j = int(np.argmax(sl))
    tau = t[j] - y[j] / sl[j]
    a = sl[j] * t[j] - y[j]
    t63 = t[int(np.argmax(y >= 0.632 * y[-1]))]
    return dict(K=K, slope=sl[j], tj=t[j], tau=tau, a=a, T63=t63, T=t63 - tau)


def speed_loop_tf(kp, ki, w, extra=0):
    """Loop transfer L(e^{i w h}) of the 100 Hz speed loop (plant, 20-sample average, PI)."""
    z = np.exp(1j * w * DT)
    P = (DT / M) / (z - (1 - DT * B / M))
    avg = sum(z ** (-i) for i in range(NW)) / NW * z ** (-extra)
    return (kp + ki * DT / (z - 1)) * P * avg


def margins(L, w):
    """Phase margin (deg), gain crossover (rad/s), delay margin (s), stability margin min|1 + L|."""
    ig = int(np.argmin(abs(abs(L) - 1)))
    pm = np.angle(-L[ig])                    # 180 degrees plus the phase of L, in (-180, 180]
    return dict(pm=np.degrees(pm), wgc=w[ig], dm=pm / w[ig], sm=np.min(abs(1 + L)))


def lowpass(fc):
    """First-order low-pass at 100 Hz (backward difference, Feedback Systems eq. 11.18 form): (b, a)."""
    tf = 1 / (2 * np.pi * fc)
    return np.array([DT / (tf + DT)]), np.array([1.0, -tf / (tf + DT)])


def notch(f0=F_VIB, bw=5.0):
    """Second-order notch at f0 Hz, width bw Hz, at 100 Hz: (b, a)."""
    return signal.iirnotch(f0, f0 / bw, fs=1 / DT)


def heading_run(T, *, step=0.1, t_step=0.5, beta=1.0, gamma=1.0, N=None, quant=False, gyro=False, vib=False,
                filt=None, drive=0.5, phase=0.37):
    """Heading PID at 100 Hz. Derivative: on the error (gamma = 1) or on the measured heading (gamma = 0), by
    differencing the measured heading, filtered with Tf = Td/N when N is given; or from the gyro (gyro=True), with
    the frame's 10 Hz bending added (vib=True) and a filter (b, a) on the gyro. quant: the heading comes from
    1024-tick wheel encoders while driving forward at `drive` m/s. Returns a dict of arrays."""
    n = int(round(T / DT)) + 1
    t = np.arange(n) * DT
    th = w = integ = D = 0.0
    yprev = rprev = None
    s = 0.0
    zi = None if filt is None else signal.lfilter_zi(*filt) * 0.0
    keys = ("th", "y", "r", "c", "u", "P", "I", "D", "g")
    out = {k: np.zeros(n) for k in keys}
    y0 = None
    for k in range(n):
        r = step if t[k] >= t_step else 0.0
        if quant:
            nr = np.floor((s + L_WHEELS * th / 2) / DS)
            nl = np.floor((s - L_WHEELS * th / 2) / DS + phase)
            y = (nr - nl) * DS / L_WHEELS
            y0 = y if y0 is None else y0
            y -= y0
        else:
            y = th
        if yprev is None:
            yprev, rprev = y, r
        e = r - y
        P = HKP * (beta * r - y)
        g = 0.0
        if gyro:
            g = w + (A_VIB * np.sin(2 * np.pi * F_VIB * t[k]) if vib else 0.0)
            if filt is not None:
                gf, zi = signal.lfilter(*filt, [g], zi=zi)
                g = gf[0]
            D = -HKD * g
        else:
            dd = gamma * (r - rprev) - (y - yprev)
            if N:
                tf = TD / N
                D = tf / (tf + DT) * D + HKD / (tf + DT) * dd
            else:
                D = HKD * dd / DT
        c = P + integ + D
        u = float(np.clip(c, -TAU_MAX, TAU_MAX))
        for key, val in zip(keys, (th, y, r, c, u, P, integ, D, g)):
            out[key][k] = val
        integ += HKI * e * DT
        yprev, rprev = y, r
        w += DT * u / I_YAW
        th += DT * w
        s += drive * DT
    out["t"] = t
    return out


def heading_loop_tf(w, *, N=None, gyro_filt=None):
    """Loop transfer at the plant input of the 100 Hz heading PID (derivative on measurement)."""
    z = np.exp(1j * w * DT)
    W = (DT / I_YAW) / (z - 1)                 # torque -> turn rate (w[k+1] = w[k] + h u/I)
    TH = DT * z * W / (z - 1)                  # torque -> heading (th[k+1] = th[k] + h w[k+1])
    pi = HKP + HKI * DT / (z - 1)
    if gyro_filt is not None:
        b, a = gyro_filt
        F = np.polyval(b[::-1], 1 / z) / np.polyval(a[::-1], 1 / z)
        return pi * TH + HKD * F * W
    if N:
        tf = TD / N
        dpath = HKD / (tf + DT) * (1 - 1 / z) / (1 - tf / (tf + DT) / z)
    else:
        dpath = HKD * (1 - 1 / z) / DT
    return (pi + dpath) * TH


def overshoot(o, step=0.1):
    return (o["th"].max() - step) / step * 100


def settle(o, step=0.1, band=0.02, t_step=0.5):
    out = np.where(abs(o["th"] - step) > band * step)[0]
    return o["t"][out[-1]] - t_step if len(out) else 0.0


if __name__ == "__main__":
    assert np.allclose(np.roots([I_YAW, HKD, HKP, HKI]), [-2, -2, -2], atol=1e-3)
    assert np.allclose(ZN_PI, (90, 270)) and np.allclose(FBS_PI, (30.09, 27.89), atol=0.01)
