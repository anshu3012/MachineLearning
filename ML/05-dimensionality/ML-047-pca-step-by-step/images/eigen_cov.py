"""The flats from the previous Note (rooms, washrooms): the eigenvectors of their covariance matrix point along
PC1 and PC2, and each arrow's length shows the variance along it (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go

here = Path(__file__).parent
BLUE, ORANGE, GREEN, GREY = "#4C78A8", "#F58518", "#54A24B", "#6B6B6B"
rng = np.random.default_rng(7)                      # same made-up data as Note ML-046
N = 30
rooms = rng.uniform(1, 5, N)
rng.normal(0, 0.35, N)                              # (shops column of Note ML-046, keeps the random stream identical)
washrooms = 0.8 * rooms + rng.normal(0, 0.35, N) + 0.4
washrooms = washrooms * rooms.std() / washrooms.std()
washrooms += 3 - washrooms.mean()
P = np.c_[rooms, washrooms]
C = np.cov(P.T, bias=True)                          # divide by n, as in Note ML-046
vals, vecs = np.linalg.eigh(C)                      # eigh: for symmetric matrices, ascending order
order = np.argsort(vals)[::-1]
vals, vecs = vals[order], vecs[:, order]
print("covariance\n", C.round(2), "\neigenvalues", vals.round(2), "\neigenvectors (columns)\n", vecs.round(3))
c = P.mean(axis=0)
fig = go.Figure(go.Scatter(x=P[:, 0], y=P[:, 1], mode="markers", marker=dict(size=10, color=BLUE, opacity=0.6)))
for k, (colour, name) in enumerate(((ORANGE, "PC1"), (GREEN, "PC2"))):
    v = vecs[:, k] * np.sign(vecs[0, k] if k == 0 else vecs[1, k])
    tip = c + 2 * np.sqrt(vals[k]) * v              # length: 2 standard deviations along this direction
    fig.add_annotation(x=tip[0], y=tip[1], ax=c[0], ay=c[1], xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowwidth=4, arrowcolor=colour, text="")
    fig.add_annotation(x=tip[0], y=tip[1], text=f"<b>{name}</b>: eigenvalue {vals[k]:.2f}", showarrow=False,
                       xanchor="left" if k == 0 else "right", yshift=14, font=dict(color=colour, size=17))
fig.update_layout(template="simple_white", width=760, height=640, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=70, r=30, t=70, b=60),
                  title=dict(text=f"Covariance matrix [[{C[0,0]:.2f}, {C[0,1]:.2f}], [{C[1,0]:.2f}, {C[1,1]:.2f}]]", x=0.5),
                  xaxis=dict(title="Rooms", range=[0, 6.5]), yaxis=dict(title="Washrooms", range=[0, 6], scaleanchor="x"))
fig.write_image(here / "eigen_cov.png", scale=2)
fig.write_image(here / "eigen_cov.pdf")
