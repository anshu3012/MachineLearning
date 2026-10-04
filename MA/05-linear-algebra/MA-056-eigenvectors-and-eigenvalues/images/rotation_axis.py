"""The axis of rotation is an eigenvector with eigenvalue 1 (Plotly 3D frames -> GIF). A rotation by 0 to 120
degrees about the axis through (1, 1, 1): the three basis vectors (red) sweep round and trace circles, while the
axis vector (green) does not move at all, R u = 1 u. At 120 degrees the rotation sends x to y, y to z and z to x.
Our own design."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from gifkit import FONT, GREEN, RED, GREY, make_gif

here = Path(__file__).parent
u = np.ones(3) / np.sqrt(3)


def R(deg):
    """Rodrigues' formula: rotation by deg degrees about the unit axis u."""
    t = np.radians(deg)
    K = np.array([[0, -u[2], u[1]], [u[2], 0, -u[0]], [-u[1], u[0], 0]])
    return np.eye(3) + np.sin(t) * K + (1 - np.cos(t)) * K @ K


assert np.allclose(R(120) @ np.eye(3)[0], [0, 1, 0]) and all(np.allclose(R(d) @ u, u) for d in range(0, 361, 15))
vals = np.linalg.eigvals(R(120))
assert np.isclose(vals, 1).sum() == 1                       # exactly one real eigenvalue, 1: the axis
E = np.eye(3)
names = ["x", "y", "z"]


def arrow(p, c, w, name):
    return [go.Scatter3d(x=[0, p[0]], y=[0, p[1]], z=[0, p[2]], mode="lines", line=dict(color=c, width=w), name=name,
                         showlegend=False),
            go.Cone(x=[p[0]], y=[p[1]], z=[p[2]], u=[p[0]], v=[p[1]], w=[p[2]], sizemode="absolute", sizeref=0.18,
                    anchor="tip", colorscale=[[0, c], [1, c]], showscale=False)]


def frame(deg):
    M = R(deg)
    data = []
    for i in range(3):
        trail = np.array([R(d) @ E[i] for d in np.linspace(0, deg, 40)])
        data.append(go.Scatter3d(x=trail[:, 0], y=trail[:, 1], z=trail[:, 2], mode="lines",
                                 line=dict(color=RED, width=4, dash="dot"), showlegend=False))
        data += arrow(M @ E[i], RED, 9, names[i])
        p = 1.18 * M @ E[i]
        data.append(go.Scatter3d(x=[p[0]], y=[p[1]], z=[p[2]], mode="text", text=[names[i]],
                                 textfont=dict(size=26, color=RED), showlegend=False))
    data += arrow(1.6 * u, GREEN, 14, "axis")
    data.append(go.Scatter3d(x=[-1.2 * u[0], 0], y=[-1.2 * u[1], 0], z=[-1.2 * u[2], 0], mode="lines",
                             line=dict(color=GREEN, width=4, dash="dash"), showlegend=False))
    fig = go.Figure(data)
    ax = dict(range=[-1.1, 1.6], showbackground=False, title="", showticklabels=False, gridcolor="#E5E5E5")
    fig.update_layout(width=900, height=760, font=FONT, showlegend=False,
                      scene=dict(xaxis=ax, yaxis=ax, zaxis=ax, aspectmode="cube",
                                 camera=dict(eye=dict(x=1.5, y=-1.35, z=0.75))),
                      title=dict(text=f"rotation by {deg}° about the green axis<br>"
                                      f"<span style='color:{GREEN}'>the axis: R u = 1 · u, it never moves</span><br>"
                                      f"<span style='color:{RED}'>x, y, z: turned off their lines</span>",
                                 x=0.5, y=0.95), margin=dict(l=0, r=0, t=140, b=0))
    return fig


if __name__ == "__main__":
    degs = list(range(0, 121, 8)) + [120]
    holds = [4] + [1] * (len(degs) - 2) + [8]
    make_gif([frame(d) for d in degs], here / "rotation_axis", fps=8, holds=holds, keys=[0, 8, len(degs) - 1], cols=3, width=640)
