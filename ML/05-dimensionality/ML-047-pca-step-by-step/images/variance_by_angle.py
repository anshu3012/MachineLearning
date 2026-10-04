"""PCA's objective as a curve: the variance of the projections sigma^2(u) of the 30 made-up flats (rooms, washrooms;
the data of the previous Note, flats.py) for every unit vector u = (cos a, sin a). It equals u^T C u, peaks at
2.61 near 45 degrees (PC1, the top eigenvector) and is smallest, 0.05, at right angles to it."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from flats import rooms, washrooms

here = Path(__file__).parent
P = np.c_[rooms, washrooms]
C = np.cov(P.T, ddof=0)
a = np.radians(np.arange(0, 180.5, 0.5))
U = np.c_[np.cos(a), np.sin(a)]
var = ((P - P.mean(0)) @ U.T).var(axis=0)
assert np.allclose(var, np.einsum("ij,jk,ik->i", U, C, U))
w, V = np.linalg.eigh(C)
best = np.degrees(a[var.argmax()])
assert round(var[0], 2) == 1.33 and round(var.max(), 2) == 2.61 and round(var.min(), 2) == 0.05 and np.isclose(var.max(), w[-1])
fig = go.Figure(go.Scatter(x=np.degrees(a), y=var, mode="lines", line=dict(color="#4C78A8", width=4)))
for deg, txt in ((0, "rooms axis: 1.33"), (90, "washrooms axis"), (best, f"PC1 ({best:.1f}°): 2.61, the largest eigenvalue"),
                 (np.degrees(a[var.argmin()]), "PC2: 0.05")):
    i = int(round(deg * 2))
    fig.add_scatter(x=[deg], y=[var[i]], mode="markers", marker=dict(size=13, color="#F58518"))
    fig.add_annotation(x=deg, y=var[i], text=txt, ax=0 if var[i] < 2 else 120, ay=-40 if var[i] < 2 else 20, font=dict(size=17))
fig.update_layout(template="simple_white", width=1100, height=520, font=dict(family="Latin Modern Roman", size=18),
                  showlegend=False, title=dict(text="σ²(u) = uᵀCu for every direction u", x=0.5),
                  xaxis=dict(title="angle of u (degrees)", dtick=15), yaxis=dict(title="variance of the projections", range=[0, 3.1]),
                  margin=dict(l=80, r=30, t=70, b=70))
fig.write_image(here / "variance_by_angle.png", scale=2)
fig.write_image(here / "variance_by_angle.pdf")
