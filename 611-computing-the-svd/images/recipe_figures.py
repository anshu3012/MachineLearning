"""Four still figures for the hand recipe, all on the Note's own matrices.
recipe_step3.png  : A = [[3, 0], [4, 5]]: v_i on the circle -> A v_i on the ellipse -> u_i = A v_i / sigma_i on the circle.
sign_trap.png     : same ellipse, but the mismatched product [[0, 3], [5, 4]] sends i-hat and j-hat to swapped places.
rank_one.png      : C = [[2, 1], [4, 2]] squashes the unit circle onto a segment of the line through [1, 2]; v2 goes to 0.
rounding_loss.png : M = [[1, 1], [1, 1 + eps]]: small singular value from svd(M) versus sqrt(eig(M^T M)).
Run: python recipe_figures.py"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
BLUE, ORANGE, RED, GREEN, GREY = "#4C78A8", "#F58518", "#E45756", "#54A24B", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=22)
t = np.linspace(0, 2 * np.pi, 300)
circle = np.array([np.cos(t), np.sin(t)])


def arrow(fig, v, color, col, label=None, shift=(0, 0)):
    fig.add_annotation(x=v[0], y=v[1], ax=0, ay=0, xref=f"x{col}", yref=f"y{col}", axref=f"x{col}", ayref=f"y{col}",
                       showarrow=True, arrowhead=2, arrowwidth=4, arrowcolor=color, text="")
    if label:
        fig.add_annotation(x=v[0], y=v[1], xref=f"x{col}", yref=f"y{col}", text=label, showarrow=False,
                           font=dict(color=color, size=24), xshift=shift[0], yshift=shift[1])


def axes(fig, col, lim):
    fig.update_xaxes(range=[-lim, lim], zeroline=True, row=1, col=col)
    fig.update_yaxes(range=[-lim, lim], zeroline=True, scaleanchor=f"x{col}", row=1, col=col)


# Step 3 of the recipe
A = np.array([[3.0, 0.0], [4.0, 5.0]])
v1, v2 = np.array([1, 1]) / np.sqrt(2), np.array([-1, 1]) / np.sqrt(2)
s1, s2 = np.sqrt(45), np.sqrt(5)
u1, u2 = A @ v1 / s1, A @ v2 / s2
assert np.allclose(u1, np.array([1, 3]) / np.sqrt(10)) and np.allclose(u2, np.array([-3, 1]) / np.sqrt(10))
assert abs(u1 @ u2) < 1e-12
U, V = np.column_stack([u1, u2]), np.column_stack([v1, v2])
assert np.allclose(U @ np.diag([s1, s2]) @ V.T, A)
fig = make_subplots(1, 3, horizontal_spacing=0.06,
                    subplot_titles=("step 2: v₁, v₂ (eigenvectors of AᵀA)", "apply A: lengths 6.71, 2.24", "step 3: divide by σᵢ"))
for col, (p, q, la, lb, lim) in enumerate([(v1, v2, "v₁", "v₂", 1.4), (A @ v1, A @ v2, "Av₁", "Av₂", 7.2),
                                            (u1, u2, "u₁", "u₂", 1.4)], start=1):
    curve = A @ circle if col == 2 else circle
    fig.add_trace(go.Scatter(x=curve[0], y=curve[1], mode="lines", line=dict(color=GREY, width=2)), 1, col)
    arrow(fig, p, BLUE, col, la, (18, 12))
    arrow(fig, q, ORANGE, col, lb, (-18, 14))
    axes(fig, col, lim)
fig.update_layout(template="simple_white", width=1400, height=520, showlegend=False, font=FONT,
                  margin=dict(l=40, r=20, t=70, b=30))
fig.update_annotations(selector=dict(xref="paper"), font_size=24)
fig.write_image(HERE / "recipe_step3.png", scale=2)

# The sign trap
W = np.column_stack([u1, -u2]) @ np.diag([s1, s2]) @ V.T
assert np.allclose(W, [[0, 3], [5, 4]])
assert np.allclose(np.linalg.svd(W)[1], [s1, s2])               # same singular values, so the same ellipse
fig = make_subplots(1, 2, horizontal_spacing=0.08,
                    subplot_titles=("matched pairs: U Σ Vᵀ = A", "u₂ flipped alone: [[0, 3], [5, 4]] ≠ A"))
for col, M in ((1, A), (2, W)):
    e = M @ circle
    fig.add_trace(go.Scatter(x=e[0], y=e[1], mode="lines", line=dict(color=GREY, width=2)), 1, col)
    for k, (name, c) in enumerate((("î", BLUE), ("ĵ", GREEN))):
        w = M[:, k]                                             # label left of a vertical arrow, right of a slanted one
        arrow(fig, w, c, col, f"{name} → [{w[0]:.0f}, {w[1]:.0f}]", (-70, 14) if abs(w[0]) < 1e-9 else (60, 18))
    axes(fig, col, 7.2)
fig.update_layout(template="simple_white", width=1100, height=560, showlegend=False, font=FONT,
                  margin=dict(l=40, r=20, t=70, b=30))
fig.update_annotations(selector=dict(xref="paper"), font_size=24)
fig.write_image(HERE / "sign_trap.png", scale=2)

# Rank 1
C = np.array([[2.0, 1.0], [4.0, 2.0]])
cv1, cv2 = np.array([2, 1]) / np.sqrt(5), np.array([-1, 2]) / np.sqrt(5)
assert np.allclose(C @ cv2, 0) and np.allclose(np.linalg.svd(C)[1], [5, 0])
img = C @ circle
assert np.isclose(np.linalg.norm(img, axis=0).max(), 5, atol=1e-3)  # the segment reaches 5 from the origin
fig = make_subplots(1, 2, horizontal_spacing=0.08, subplot_titles=("input: unit circle", "output: a segment (rank 1)"))
fig.add_trace(go.Scatter(x=circle[0], y=circle[1], mode="lines", line=dict(color=GREY, width=2)), 1, 1)
arrow(fig, cv1, BLUE, 1, "v₁", (16, 14))
arrow(fig, cv2, RED, 1, "v₂", (-16, 14))
fig.add_trace(go.Scatter(x=img[0], y=img[1], mode="lines", line=dict(color=GREY, width=6)), 1, 2)
arrow(fig, C @ cv1, BLUE, 2, "Cv₁ = 5 u₁", (70, 0))
fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers+text", text=["Cv₂ = 0"], textposition="middle left",
                         marker=dict(size=14, color=RED), textfont=dict(color=RED, size=24)), 1, 2)
axes(fig, 1, 1.4)
axes(fig, 2, 5.5)
fig.update_layout(template="simple_white", width=1100, height=560, showlegend=False, font=FONT,
                  margin=dict(l=40, r=20, t=70, b=30))
fig.update_annotations(selector=dict(xref="paper"), font_size=24)
fig.write_image(HERE / "rank_one.png", scale=2)

# Rounding loss
eps = 10.0 ** -np.arange(1, 13)
true_small, svd_small, eig_small = [], [], []
for e in eps:
    M = np.array([[1, 1], [1, 1 + e]])
    sv = np.linalg.svd(M)[1]
    ev = np.sqrt(np.clip(np.linalg.eigvalsh(M.T @ M), 0, None))
    svd_small.append(sv[1])
    eig_small.append(ev[0])
    true_small.append(abs(np.linalg.det(M)) / sv[0])            # sigma1 sigma2 = |det M| = eps, exact enough
svd_small, eig_small, true_small = map(np.array, (svd_small, eig_small, true_small))
i9 = list(eps).index(1e-9)
assert np.isclose(svd_small[i9], 5e-10, rtol=1e-3) and eig_small[i9] == 0.0   # the Note's Python box
assert np.all(np.abs(svd_small / true_small - 1) < 1e-3)        # svd stays right all the way down
floor = 1e-17
fig = go.Figure()
fig.add_trace(go.Scatter(x=eps, y=true_small, mode="lines", name="true σ₂", line=dict(color=GREY, width=3, dash="dot")))
fig.add_trace(go.Scatter(x=eps, y=svd_small, mode="lines+markers", name="np.linalg.svd(M)", line=dict(color=BLUE, width=4),
                         marker=dict(size=10)))
fig.add_trace(go.Scatter(x=eps, y=np.maximum(eig_small, floor), mode="lines+markers", name="sqrt of eig(MᵀM)",
                         line=dict(color=RED, width=4), marker=dict(size=10)))
fig.update_layout(template="simple_white", width=1000, height=560, font=FONT,
                  xaxis=dict(title="ε in M = [[1, 1], [1, 1 + ε]]", type="log", autorange="reversed", exponentformat="power"),
                  yaxis=dict(title="small singular value σ₂", type="log", exponentformat="power", range=[-17.3, 0]),
                  legend=dict(x=0.02, y=0.02, yanchor="bottom"), margin=dict(l=80, r=30, t=30, b=70))
fig.add_annotation(x=np.log10(1e-11), y=np.log10(floor), text="lost: computed as 0", showarrow=False, yshift=24,
                   font=dict(color=RED, size=22))
fig.write_image(HERE / "rounding_loss.png", scale=2)
print("eig route at eps:", dict(zip(eps, eig_small.round(12))))
