"""SVD in ML figures (Plotly): documents in the 2D latent space of LSA, and a ratings matrix with its rank-1 and
rank-2 approximations."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.feature_extraction.text import CountVectorizer

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY, PURPLE = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B", "#B279A2"
FONT = dict(family="Latin Modern Roman", size=24)

# 1. LSA: seven short documents, two topics
docs = ["batsman hits a century", "bowler takes a wicket", "batsman and bowler: century, wicket, match",
        "chef cooks a curry", "rice and dal", "chef serves curry with rice and dal", "chef watches the match"]
X = CountVectorizer(stop_words="english").fit_transform(docs).toarray().astype(float)
U, s, Vt = np.linalg.svd(X, full_matrices=False)
Z = U[:, :2] * s[:2]
Z *= np.sign(Z[:, 0].sum())                    # sign of a singular pair is arbitrary; make topic 1 positive
Z[:, 1] *= np.sign(Z[0, 1])                    # cricket documents on the positive side of topic 2
colours = [GREEN] * 3 + [ORANGE] * 3 + [PURPLE]
fig = go.Figure()
for i, (d, z) in enumerate(zip(docs, Z)):
    fig.add_trace(go.Scatter(x=[0, z[0]], y=[0, z[1]], mode="lines", line=dict(color=colours[i], width=2), showlegend=False))
pos = ["middle left", "middle left", "middle right", "middle left", "middle left", "middle right", "middle right"]
fig.add_trace(go.Scatter(x=Z[:, 0], y=Z[:, 1], mode="markers+text", marker=dict(size=14, color=colours),
                         text=["d1 = d2", ""] + [f"d{i + 3}" for i in range(5)], textposition=pos, textfont=dict(size=34), showlegend=False))
fig.update_xaxes(title="topic 1 (σ<sub>1</sub>u<sub>1</sub>)", range=[-0.2, 2.0], zeroline=True)
fig.update_yaxes(title="topic 2 (σ<sub>2</sub>u<sub>2</sub>)", range=[-1.7, 2.0], zeroline=True, scaleanchor="x")
fig.update_layout(template="simple_white", width=900, height=820, font=dict(family="Latin Modern Roman", size=34), margin=dict(l=80, r=30, t=20, b=70))
fig.write_image(HERE / "lsa_docs.png", scale=2)
fig.write_image(HERE / "lsa_docs.pdf")
print("latent coordinates\n", Z.round(3))

# 2. ratings: 5 viewers x 4 films, rank-1 and rank-2 approximations
R = np.array([[5, 4, 1, 1], [4, 5, 2, 1], [1, 1, 5, 4], [2, 1, 4, 5], [5, 5, 4, 4]], float)
users, films = ["Asha", "Ben", "Chitra", "Dev", "Esha"], ["Action 1", "Action 2", "Romance 1", "Romance 2"]
U, s, Vt = np.linalg.svd(R, full_matrices=False)
R1 = s[0] * np.outer(U[:, 0], Vt[0])
R2 = R1 + s[1] * np.outer(U[:, 1], Vt[1])
fig = make_subplots(1, 3, subplot_titles=["ratings R", f"rank 1 (σ₁ = {s[0]:.1f})", f"rank 2 (adds σ₂ = {s[1]:.1f})"],
                    horizontal_spacing=0.04)
for c, M in enumerate([R, R1, R2], 1):
    fig.add_trace(go.Heatmap(z=M, x=films, y=users, zmin=1, zmax=5, colorscale="Blues", showscale=False,
                             text=np.round(M, 1), texttemplate="%{text}", textfont=dict(size=34)), 1, c)
    fig.update_yaxes(autorange="reversed", showticklabels=(c == 1), row=1, col=c)
    fig.update_xaxes(tickangle=-30, row=1, col=c)
fig.update_layout(template="simple_white", width=1500, height=620, font=dict(family="Latin Modern Roman", size=30), margin=dict(l=110, r=20, t=60, b=150))
fig.update_annotations(font_size=32)
fig.write_image(HERE / "ratings.png", scale=2)
fig.write_image(HERE / "ratings.pdf")
print("s", s.round(2), "\nU", U.round(2), "\nVt", Vt.round(2), "\nR1", R1.round(2), "\nR2", R2.round(2))
