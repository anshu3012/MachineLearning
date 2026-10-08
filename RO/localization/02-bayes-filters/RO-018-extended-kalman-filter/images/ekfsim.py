"""The running example of the extended-Kalman-filter Note, shared by every figure script.

The corridor robot of the Kalman-filter Note: commanded 0.5 m per step, slip standard deviation 0.1 m (Q = 0.01 m^2),
first guess 0 m with variance 1 m^2, true start 0.3 m. Its position sensor is now a radio beacon fixed on the wall
2 m to the side of the corridor, at corridor position 6 m. The robot measures its straight-line distance to the
beacon, h(x) = sqrt((6 - x)^2 + 2^2), with standard deviation 0.1 m (R = 0.01 m^2). The 16 true positions and readings
below were drawn once (seed 4) and rounded to centimetres.
"""
import numpy as np

B, D = 6.0, 2.0                 # beacon position along the corridor, and its distance to the side (m)
U, Q, R = 0.5, 0.01, 0.01
X0, P0 = 0.0, 1.0
X_TRUE = np.array([0.73, 1.4, 1.74, 2.17, 2.51, 3.04, 3.57, 3.92, 4.23, 4.7, 5.13, 5.67, 6.32, 6.82, 7.39, 7.86])
Z = np.array([5.61, 5.08, 4.71, 4.33, 4.04, 3.73, 3.2, 3.11, 2.78, 2.3, 2.11, 2.02, 1.84, 2.07, 2.23, 2.75])


def h(x):
    """Measurement model: distance from the robot at x to the beacon (m)."""
    return np.sqrt((B - x) ** 2 + D ** 2)


def dh(x):
    """Its slope (derivative): how much the distance changes per metre driven."""
    return -(B - x) / h(x)


def ekf(z=Z, q=Q, r=R, x=X0, p=P0, u=U):
    """The one-dimensional extended Kalman filter. One dict per step."""
    rows = []
    for zk in z:
        xb, pb = x + u, p + q                    # predict (the motion is linear here)
        H = dh(xb)                               # slope of h at the prediction
        S = H * pb * H + r                       # innovation variance
        K = pb * H / S                           # gain
        y = zk - h(xb)                           # innovation
        x, p = xb + K * y, (1 - K * H) * pb
        rows.append(dict(x_pred=xb, p_pred=pb, H=H, h_pred=h(xb), S=S, K=K, y=y, x=x, p=p))
    return rows


def simulate(n, T=16, x0_sd=1.0):
    """A fresh run: true start drawn around the first guess, slips and sensor noise drawn with seed n."""
    rg = np.random.default_rng(1000 + n)
    xt, xs, zs = rg.normal(X0, x0_sd), [], []
    for _ in range(T):
        xt += U + rg.normal(0, np.sqrt(Q))
        xs.append(xt)
        zs.append(h(xt) + rg.normal(0, np.sqrt(R)))
    return np.array(xs), np.array(zs)


def consistency(q, r, N=500):
    """Average NEES and NIS per step over N simulated runs, for a filter that assumes noises q and r."""
    nees, nis = [], []
    for n in range(N):
        xs, zs = simulate(n)
        rows = ekf(zs, q=q, r=r)
        nees.append([(t - row["x"]) ** 2 / row["p"] for t, row in zip(xs, rows)])
        nis.append([row["y"] ** 2 / row["S"] for row in rows])
    return np.mean(nees, 0), np.mean(nis, 0)


if __name__ == "__main__":
    r = ekf()
    assert abs(r[0]["K"] + 1.0523) < 1e-3 and abs(r[0]["x"] - 0.755) < 1e-3
    print("ok")
