"""The normal log-likelihood of the five mouse weights as a 3-D surface over (mean, standard deviation), then tilted to
the top view: the contour map of normal_surface.png. The two one-parameter searches are drawn on the surface (orange:
sigma fixed at 2; green: mu fixed at 32); the red point is the peak (32, 2), l = -10.56.
Run: python normal_surface_3d.py -> normal_surface_3d.gif, normal_surface_3d_frames.png"""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy import stats
from tilt import tilt_gif

here = Path(__file__).parent
X = np.array([29, 31, 32, 33, 35.0])
ll = lambda m, s: stats.norm(np.asarray(m)[..., None], np.asarray(s)[..., None]).logpdf(X).sum(axis=-1)
M, S = np.meshgrid(np.linspace(28, 36, 90), np.linspace(0.8, 5, 90))
Z = np.maximum(ll(M, S), -22)
assert abs(ll(32, 2) + 10.56) < 0.01
mu, sg = np.linspace(28, 36, 100), np.linspace(0.8, 5, 100)


def marks(a):
    return [go.Scatter3d(x=mu, y=0 * mu + 2, z=np.maximum(ll(mu, 0 * mu + 2), -22) + 0.15, mode="lines", line=dict(color="#F58518", width=7)),
            go.Scatter3d(x=0 * sg + 32, y=sg, z=np.maximum(ll(0 * sg + 32, sg), -22) + 0.15, mode="lines", line=dict(color="#54A24B", width=7)),
            go.Scatter3d(x=[32], y=[2], z=[-10.56 + 0.4], mode="markers", marker=dict(size=7, color="#E45756"))]


tilt_gif(here / "normal_surface_3d", M, S, Z, "Blues", (-22, -11, 1.5), (-22, -10), labels=("mean μ", "std. dev. σ", "log-likelihood"),
         extra=marks, aspect=0.7, titles=("Log-likelihood ℓ(μ, σ) of the five mice: a single hill", "Turn to the top view …",
                                          "From above: the contour map of Figure 7, the peak (red)"))
