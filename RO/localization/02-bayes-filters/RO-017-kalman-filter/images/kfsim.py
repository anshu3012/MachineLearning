"""The running example of the Kalman-filter Note, shared by every figure script.

A robot drives along a straight corridor. Every second it is commanded 0.5 m (u = 0.5 m); its wheels slip with
standard deviation 0.1 m per step (process noise variance Q = 0.01 m^2). A ceiling beacon system reports its position
with standard deviation 0.4 m (measurement noise variance R = 0.16 m^2). It starts near the dock: first guess 0 m
with variance 1 m^2. The true start is 0.3 m. The ten readings and true positions below were drawn once (seed 4) and
rounded to centimetres; every number in the Note comes from them.
"""
import numpy as np

U, Q, R = 0.5, 0.01, 0.16
X0, P0 = 0.0, 1.0
X_TRUE = np.array([0.3, 0.73, 1.22, 1.88, 2.45, 2.79, 3.28, 3.72, 4.24, 4.58, 5.1])
Z = np.array([0.82, 1.85, 2.01, 2.65, 2.19, 4.18, 2.95, 4.68, 4.45, 4.75])


def kf1d(z=Z, u=U, q=Q, r=R, x=X0, p=P0):
    """The one-dimensional Kalman filter. Returns one dict per step with the prediction, gain and update."""
    rows = []
    for zk in z:
        xb, pb = x + u, p + q                     # predict
        k = pb / (pb + r)                         # gain
        x, p = xb + k * (zk - xb), (1 - k) * pb   # update
        rows.append(dict(x_pred=xb, p_pred=pb, K=k, z=zk, x=x, p=p))
    return rows


# the two-variable version: state (position, speed), no odometry, position readings only
F = np.array([[1.0, 1.0], [0.0, 1.0]])
H = np.array([[1.0, 0.0]])
Q2 = np.diag([0.01, 0.001])


def kf2d(z=Z, Hm=H, x=None, P=None):
    """The matrix Kalman filter with the constant-speed model. Returns one dict per step."""
    x = np.zeros(2) if x is None else x
    P = np.eye(2) if P is None else P
    rows = []
    for zk in z:
        xb, Pb = F @ x, F @ P @ F.T + Q2
        S = (Hm @ Pb @ Hm.T)[0, 0] + R
        K = (Pb @ Hm.T / S).ravel()
        y = zk - (Hm @ xb)[0]
        x, P = xb + K * y, (np.eye(2) - np.outer(K, Hm)) @ Pb
        rows.append(dict(x_pred=xb, P_pred=Pb, S=S, K=K, y=y, x=x, P=P))
    return rows


def normal(x, m, v):
    return np.exp(-0.5 * (x - m) ** 2 / v) / np.sqrt(2 * np.pi * v)


if __name__ == "__main__":
    r = kf1d()
    assert abs(r[0]["K"] - 0.8632) < 1e-4 and abs(r[0]["x"] - 0.776) < 1e-3
    assert abs(r[-1]["K"] - 0.2239) < 1e-4
    r2 = kf2d()
    assert np.allclose(r2[0]["K"], [0.9263, 0.4608], atol=1e-4)
    print("ok")
