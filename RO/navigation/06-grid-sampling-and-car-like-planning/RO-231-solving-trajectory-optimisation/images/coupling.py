"""Which unknowns each motion-rule equation touches, for the three transcriptions of the 8 s least-effort drive, at
their solutions. One row per equation (a component of a defect), one column per unknown, both in time order; a blue
cell is a non-zero entry of the Jacobian (the equation changes when that unknown changes), found by central
differences. Single shooting: the 4 numbers of the miss at the end against the 60 controls, 75 percent blue.
Multiple shooting: 4 joins and the end (20 equations) against each piece's start state and its 12 controls (76
unknowns), 15 percent. Collocation: the start, 30 collocation constraints and the end (128 equations) against the 6
numbers of each of the 31 knot points (186 unknowns), 2.5 percent; the 4 equations between two neighbouring knot
points touch only those knot points' 12 numbers. Run -> coupling.png"""
from pathlib import Path

import numpy as np
import trajkit as tk

T, N, M = 8.0, 30, 5          # the drive's time, its intervals, the pieces of multiple shooting
K = N // M                    # intervals per piece


def _jac(fun, z, eps=1e-6):
    f0 = fun(z)
    J = np.zeros((len(f0), len(z)))
    for i in range(len(z)):
        d = np.zeros(len(z))
        d[i] = eps
        J[:, i] = (fun(z + d) - fun(z - d)) / (2 * eps)
    return J


def _multi_res(z):
    """Unknowns per piece: its start state (pieces 2 to 5) then its 6 x 2 controls. Residuals: each piece's end
    minus the next start, then the last end minus the door pose."""
    starts, U, i = [tk.START], [], 0
    for j in range(M):
        if j:
            starts.append(z[i:i + 4])
            i += 4
        U.append(z[i:i + 2 * K].reshape(K, 2))
        i += 2 * K
    ends = [tk.simulate(starts[j], U[j], T / M)[-1] for j in range(M)]
    return np.concatenate([ends[j] - (starts[j + 1] if j < M - 1 else tk.GOAL) for j in range(M)])


def _colloc_res(z):
    """Unknowns per knot point: x, y, theta, v, a, omega. Residuals: the start, the 30 trapezoid defects, the end."""
    Z = z.reshape(N + 1, 6)
    X, U = Z[:, :4], Z[:, 4:]
    F = tk.f(X, U)
    d = X[1:] - X[:-1] - T / N / 2 * (F[1:] + F[:-1])
    return np.concatenate([X[0] - tk.START, d.ravel(), X[-1] - tk.GOAL])


def patterns():
    """{name: boolean matrix, True where the equation (row) depends on the unknown (column)}."""
    S = tk.solutions()
    U1 = S["single"]["U"].ravel()
    Um, Sm = S["multi"]["U"], S["multi"]["S"]
    zm = np.concatenate([np.concatenate(([Sm[j]] if j else []) + [Um[K * j:K * (j + 1)].ravel()]) for j in range(M)])
    zc = np.hstack([S["colloc"]["X"], S["colloc"]["U"]]).ravel()
    return dict(single=np.abs(_jac(lambda z: tk.simulate(tk.START, z.reshape(N, 2), T)[-1] - tk.GOAL, U1)) > 1e-10,
                multi=np.abs(_jac(_multi_res, zm)) > 1e-10,
                colloc=np.abs(_jac(_colloc_res, zc)) > 1e-10)


if __name__ == "__main__":
    import plotly.graph_objects as go
    from gifkit import BLUE, FONT

    P = patterns()
    pct = {k: 100 * v.mean() for k, v in P.items()}
    assert [v.shape for v in P.values()] == [(4, 60), (20, 76), (128, 186)]
    assert [round(p, 1) for p in pct.values()] == [75.0, 15.0, 2.5], pct
    assert max(P["colloc"][4 + 4 * k:8 + 4 * k].any(axis=0).sum() for k in range(N)) == 12
    assert max(P["multi"][4 * j:4 * j + 4].any(axis=0).sum() for j in range(M)) == 20
    titles = {"single": "single shooting: 4 equations, 60 unknowns",
              "multi": "multiple shooting: 20 equations, 76 unknowns",
              "colloc": "collocation: 128 equations, 186 unknowns"}
    W, TITLE, GAP = 1060, 50, 30                # plot width, title band and gap between panels, in pixels
    px = {k: A.shape[0] * W / A.shape[1] for k, A in P.items()}  # square cells: each panel's height in pixels
    H = sum(px.values()) + len(P) * TITLE + (len(P) - 1) * GAP
    fig = go.Figure()
    top = 1.0
    for i, (k, A) in enumerate(P.items(), start=1):
        lo = top - (px[k] + TITLE) / H
        ax = "" if i == 1 else str(i)
        fig.add_trace(go.Heatmap(z=A[::-1].astype(int), colorscale=[[0, "white"], [1, BLUE]], showscale=False,
                                 xaxis=f"x{ax}", yaxis=f"y{ax}", xgap=1, ygap=1))
        fig.update_layout({f"xaxis{ax}": dict(domain=[0, 1], visible=False, anchor=f"y{ax}"),
                           f"yaxis{ax}": dict(domain=[max(lo, 0), top - TITLE / H], visible=False, anchor=f"x{ax}")})
        r, c = A.shape
        fig.add_shape(type="rect", x0=-0.5, x1=c - 0.5, y0=-0.5, y1=r - 0.5, xref=f"x{ax}", yref=f"y{ax}",
                      line=dict(color="#555555", width=1.5), fillcolor="rgba(0,0,0,0)", layer="above")
        fig.add_annotation(x=0, y=top, xref="paper", yref="paper", xanchor="left", yanchor="top",
                           text=f"{titles[k]}: <b>{pct[k]:.1f} percent</b> blue", showarrow=False, font=dict(size=22))
        top = lo - GAP / H
    fig.update_layout(template="simple_white", font=FONT, width=W + 40, height=round(H) + 40, showlegend=False,
                      margin=dict(l=20, r=20, t=20, b=20))
    fig.write_image(Path(__file__).parent / "coupling.png", scale=2)
    print({k: round(p, 1) for k, p in pct.items()})
