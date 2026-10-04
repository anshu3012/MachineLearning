"""What the np.linalg lines of section 4.8 compute, drawn: the length of v = (3, 4) is 5, and the eigenvectors of
A = [[2, 1], [1, 3]] are the two directions that A only stretches (by its eigenvalues 1.38 and 3.62)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
v = np.array([3, 4]); A = np.array([[2, 1], [1, 3]])
w, V = np.linalg.eigh(A)            # A is symmetric, so eigh gives real eigenvalues
order = np.argsort(w); w, V = w[order], V[:, order]
assert np.linalg.norm(v) == 5 and np.allclose(A @ V, V * w) and list(np.round(w, 2)) == [1.38, 3.62]
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1, subplot_titles=[
    "np.linalg.norm(v) = 5: the length of v", "np.linalg.eig(A): directions A only stretches"])
fig.add_annotation(x=3, y=4, ax=0, ay=0, xref="x", yref="y", axref="x", ayref="y", arrowhead=3, arrowwidth=4,
                   arrowcolor="#4C78A8", showarrow=True)
fig.add_scatter(x=[0, 3, 3], y=[0, 0, 4], mode="lines", line=dict(color="#9a9a9a", dash="dot"), row=1, col=1)
fig.add_scatter(x=[1.2, 3.25, 1.5], y=[2.5, 2, -0.35], mode="text", text=["length 5", "4", "3"], textfont=dict(size=20),
                row=1, col=1)
for k, c in ((0, "#54A24B"), (1, "#F58518")):
    e = V[:, k] * np.sign(V[1, k])
    for vec, dash, lab in ((e, None, f"eigenvector {k + 1}"), (A @ e, None, f"A × eigenvector = {w[k]:.2f} ×")):
        fig.add_annotation(x=vec[0], y=vec[1], ax=0, ay=0, xref="x2", yref="y2", axref="x2", ayref="y2", arrowhead=3,
                           arrowwidth=4 if lab.startswith("eig") else 2, arrowcolor=c, opacity=1 if lab.startswith("eig") else 0.55,
                           showarrow=True)
    fig.add_scatter(x=[(A @ e)[0]], y=[(A @ e)[1]], mode="text", text=[f"λ = {w[k]:.2f}"], textposition="top right",
                    textfont=dict(size=19, color=c), row=1, col=2)
fig.update_xaxes(range=[-0.5, 5.5], zeroline=True, row=1, col=1)
fig.update_yaxes(range=[-0.6, 5], zeroline=True, scaleanchor="x", row=1, col=1)
fig.update_xaxes(range=[-1.5, 3], zeroline=True, row=1, col=2)
fig.update_yaxes(range=[-0.5, 3.6], zeroline=True, scaleanchor="x2", row=1, col=2)
for a in fig.layout.annotations[:2]:
    a.font.size = 19
fig.update_layout(template="simple_white", width=1300, height=560, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=40, r=20, t=60, b=40))
fig.write_image(here / "numpy_outputs.png", scale=2)
fig.write_image(here / "numpy_outputs.pdf")
