"""Eckart-Young on the Note's matrix A with rows [3, 0] and [4, 5] (Plotly). Left: the unit circle sent through the
error matrices; the error of the truncated SVD, A - A1, squeezes it to a line segment of half-length sigma2 = 2.24,
while the other rank-1 guess B (rows [0, 0], [4, 5]) leaves an error that stretches up to 3. Right: 20,000 random
rank-1 matrices B = c u v^T (seeded): none gets a spectral error below 2.236."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, RED

here = Path(__file__).parent
A = np.array([[3.0, 0.0], [4.0, 5.0]])
U, s, Vt = np.linalg.svd(A)
A1 = s[0] * np.outer(U[:, 0], Vt[0])
B = np.array([[0.0, 0.0], [4.0, 5.0]])
E1, EB = A - A1, A - B
n2 = lambda M: np.linalg.norm(M, 2)
assert np.allclose(A1, [[1.5, 1.5], [4.5, 4.5]]) and round(n2(E1), 2) == 2.24 and n2(EB) == 3
rng = np.random.default_rng(0)
errs = []
for _ in range(20_000):
    u, v = rng.normal(size=2), rng.normal(size=2)
    c = rng.uniform(0, 12)
    errs.append(n2(A - c * np.outer(u / np.linalg.norm(u), v / np.linalg.norm(v))))
errs = np.array(errs)
assert errs.min() >= s[1] - 1e-9
t = np.linspace(0, 2 * np.pi, 400)
C = np.vstack([np.cos(t), np.sin(t)])
fig = make_subplots(1, 2, column_widths=[0.5, 0.5], horizontal_spacing=0.12,
                    subplot_titles=["the unit circle through each error matrix", "error of 20,000 random rank-1 guesses"])
fig.update_annotations(font_size=21)
fig.add_trace(go.Scatter(x=C[0], y=C[1], mode="lines", line=dict(color=GREY, width=2, dash="dot"), name="unit circle"), 1, 1)
for M, c, name in ((EB, RED, f"A − B: longest stretch {n2(EB):.2f}"), (E1, GREEN, f"A − Â₁: longest stretch {n2(E1):.2f}")):
    P = M @ C
    fig.add_trace(go.Scatter(x=P[0], y=P[1], mode="lines", line=dict(color=c, width=5), name=name), 1, 1)
fig.update_xaxes(range=[-3.4, 3.4], zeroline=True, row=1, col=1)
fig.update_yaxes(range=[-3.4, 3.4], zeroline=True, scaleanchor="x", row=1, col=1)
fig.add_trace(go.Histogram(x=errs, nbinsx=80, marker_color=BLUE, name="random rank-1 B", showlegend=False), 1, 2)
fig.add_vline(x=s[1], line=dict(color=GREEN, width=3), opacity=1, row=1, col=2)
fig.add_annotation(x=s[1], y=1, yref="y2 domain", xref="x2", text=f"σ₂ = {s[1]:.3f}: the truncated SVD", xanchor="left",
                   xshift=6, showarrow=False, font=dict(size=18, color=GREEN))
fig.update_xaxes(title="spectral error ‖A − B‖₂", range=[0, 12], row=1, col=2)
fig.update_yaxes(title="number of guesses", row=1, col=2)
fig.update_layout(template="simple_white", width=1250, height=580, font=FONT,
                  legend=dict(orientation="h", x=0.22, xanchor="center", y=-0.12), margin=dict(l=60, r=30, t=60, b=110))
fig.write_image(here / "eckart_young.png", scale=2)
