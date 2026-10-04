"""Three more SVD-in-ML figures (Plotly), on the Note's own data:
pca_flats.png      : the 30 flats, centred, with the principal components from V^T; and the projected data U Sigma.
ratings_map.png    : viewers (sigma_i u_i) and films (v_i) on the two kept singular directions of the ratings matrix.
pinv_predictions.png: student packages, and the predictions of the normal equation and of the pseudo-inverse once a
                      copied column (percentage = 9.5 x CGPA) is added.  Run: python svd_ml_more.py"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY, PURPLE = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B", "#B279A2"
FONT = dict(family="Latin Modern Roman", size=24)

# 1. PCA of the flats through the SVD (data exactly as in the notebook and the PCA Notes)
rng = np.random.default_rng(7)
N = 30
rooms = rng.uniform(1, 5, N)
rng.normal(0, 0.35, N)
wash = 0.8 * rooms + rng.normal(0, 0.35, N) + 0.4
wash = wash * rooms.std() / wash.std()
wash += 3 - wash.mean()
Xc = np.c_[rooms, wash] - np.c_[rooms, wash].mean(axis=0)
U, s, Vt = np.linalg.svd(Xc, full_matrices=False)
assert np.allclose(s, [8.843, 1.243], atol=1e-3) and np.allclose(s ** 2 / N, [2.61, 0.05], atol=0.005)
Vt = Vt * np.sign(Vt[:, [1]])                              # sign of each pair is free: point both PCs upward
Z = Xc @ Vt.T
assert np.allclose(np.abs(Vt), 0.707, atol=0.001)
fig = make_subplots(1, 2, horizontal_spacing=0.1, subplot_titles=("centred flats and the rows of Vᵀ", "projected data UΣ"))
fig.add_trace(go.Scatter(x=Xc[:, 0], y=Xc[:, 1], mode="markers", marker=dict(size=10, color=BLUE)), 1, 1)
for k, (c, lab) in enumerate(((RED, f"PC1: variance {s[0]**2/N:.2f}"), (GREEN, f"PC2: variance {s[1]**2/N:.2f}"))):
    tip = Vt[k] * 2 * s[k] / np.sqrt(N) + Vt[k] * 0.3       # length: 2 standard deviations (+ a little to stay visible)
    fig.add_annotation(x=tip[0], y=tip[1], ax=0, ay=0, xref="x", yref="y", axref="x", ayref="y", showarrow=True,
                       arrowhead=2, arrowwidth=4, arrowcolor=c, text="")
    fig.add_annotation(x=tip[0], y=tip[1], xref="x", yref="y", text=lab, showarrow=False, font=dict(color=c, size=22),
                       xanchor="right", xshift=-8, yshift=22 if k == 0 else 8)
fig.add_trace(go.Scatter(x=Z[:, 0], y=Z[:, 1], mode="markers", marker=dict(size=10, color=BLUE)), 1, 2)
fig.update_xaxes(title="rooms (centred)", range=[-3.6, 3.6], row=1, col=1)
fig.update_yaxes(title="washrooms (centred)", range=[-3.6, 3.6], scaleanchor="x", row=1, col=1)
fig.update_xaxes(title="PC1 score", range=[-3.6, 3.6], row=1, col=2)
fig.update_yaxes(title="PC2 score", range=[-3.6, 3.6], scaleanchor="x2", row=1, col=2)
fig.update_layout(template="simple_white", width=1300, height=640, showlegend=False, font=FONT,
                  margin=dict(l=80, r=20, t=60, b=70))
fig.update_annotations(selector=dict(xref="paper"), font_size=24)
fig.write_image(HERE / "pca_flats.png", scale=2)

# 2. Ratings: kinds of viewer and kinds of film
R = np.array([[5, 4, 1, 1], [4, 5, 2, 1], [1, 1, 5, 4], [2, 1, 4, 5], [5, 5, 4, 4]], float)
users, films = ["Asha", "Ben", "Chitra", "Dev", "Esha"], ["Action 1", "Action 2", "Romance 1", "Romance 2"]
U, s, Vt = np.linalg.svd(R, full_matrices=False)
for i in range(2):                                         # flip pairs together so the Note's signs show
    sign = np.sign(Vt[i, 0]) * (-1 if i == 0 else 1)
    U[:, i] *= sign
    Vt[i] *= sign
assert np.allclose(Vt[0], [-0.54, -0.51, -0.49, -0.46], atol=0.006) and np.allclose(Vt[1], [0.44, 0.51, -0.50, -0.55], atol=0.006)
assert np.allclose(U[:, 1], [0.48, 0.42, -0.57, -0.51, 0.08], atol=0.006)
assert np.allclose(s[:2], [14.6, 6.6], atol=0.05)
pu = -U[:, 0] * s[0], U[:, 1] * s[1]                       # plot "liking" as positive
pv = -Vt[0], Vt[1]
fig = make_subplots(1, 2, horizontal_spacing=0.12, subplot_titles=("kinds of viewer: σᵢuᵢ", "kinds of film: vᵢ"))
cols_u = [RED, RED, BLUE, BLUE, PURPLE]
fig.add_trace(go.Scatter(x=pu[0], y=pu[1], mode="markers+text", text=users, marker=dict(size=16, color=cols_u),
                         textposition=["top left", "bottom left", "bottom left", "top left", "middle left"],
                         textfont=dict(size=24, color=cols_u)), 1, 1)
cols_v = [RED, RED, BLUE, BLUE]
fig.add_trace(go.Scatter(x=pv[0], y=pv[1], mode="markers+text", text=films, marker=dict(size=16, color=cols_v),
                         textposition=["middle right", "middle left", "middle right", "middle left"],
                         textfont=dict(size=24, color=cols_v)), 1, 2)
fig.update_xaxes(title="overall liking", range=[0, 11], row=1, col=1)
fig.update_yaxes(title="action (+) or romance (−)", range=[-5, 5], zeroline=True, row=1, col=1)
fig.update_xaxes(title="overall liking", range=[0.3, 0.7], row=1, col=2)
fig.update_yaxes(title="action (+) or romance (−)", range=[-0.75, 0.75], zeroline=True, row=1, col=2)
fig.update_layout(template="simple_white", width=1300, height=600, showlegend=False, font=FONT,
                  margin=dict(l=90, r=20, t=60, b=70))
fig.update_annotations(selector=dict(xref="paper"), font_size=24)
fig.write_image(HERE / "ratings_map.png", scale=2)

# 3. The normal equation against the pseudo-inverse with a copied column
cgpa = np.array([6.89, 5.12, 7.82, 7.42])
y = np.array([3.26, 1.98, 3.25, 3.67])
X3 = np.c_[np.ones(4), cgpa, 9.5 * cgpa]
b_inv = np.linalg.inv(X3.T @ X3) @ X3.T @ y               # machine-dependent garbage (the Note says so)
b_pinv = np.linalg.pinv(X3) @ y
p_inv, p_pinv = X3 @ b_inv, X3 @ b_pinv
assert np.allclose(b_pinv, [-0.81, 0.0062, 0.0589], atol=0.006)
p2 = np.c_[np.ones(4), cgpa] @ (np.linalg.pinv(np.c_[np.ones(4), cgpa]) @ y)
assert np.allclose(p_pinv, p2)                             # = the two-column model's predictions
print("normal-equation coefficients on this machine:", b_inv.round(2), "predictions:", p_inv.round(2))
names = [f"CGPA {c}" for c in cgpa]
fig = go.Figure()
fig.add_trace(go.Bar(x=names, y=y, name="real package", marker_color=GREY))
fig.add_trace(go.Bar(x=names, y=p_inv, name="normal equation (inv)", marker_color=RED))
fig.add_trace(go.Bar(x=names, y=p_pinv, name="pseudo-inverse (pinv)", marker_color=BLUE))
fig.update_layout(template="simple_white", width=1100, height=560, font=FONT, barmode="group",
                  yaxis=dict(title="package", range=[0, 6]), legend=dict(orientation="h", x=0, y=1.12),
                  margin=dict(l=80, r=20, t=70, b=60))
fig.write_image(HERE / "pinv_predictions.png", scale=2)
