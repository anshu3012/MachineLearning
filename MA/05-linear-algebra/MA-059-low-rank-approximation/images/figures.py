"""Low-rank approximation figures (Plotly): image at several ranks, its first rank-1 layers, singular-value decay,
and noise reduction of a synthetic rank-3 picture. Image: scikit-learn's bundled sample photo china.jpg (offline)."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import load_sample_image

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=26)

img = load_sample_image("china.jpg").astype(float) @ [0.299, 0.587, 0.114] / 255   # grayscale, 0 = black, 1 = white
m, n = img.shape
U, s, Vt = np.linalg.svd(img, full_matrices=False)
rank_k = lambda k: (U[:, :k] * s[:k]) @ Vt[:k]


def gray(fig, z, row, col, zmin=0, zmax=1):
    fig.add_trace(go.Heatmap(z=z, colorscale="gray", zmin=zmin, zmax=zmax, showscale=False), row, col)


# 1. the image at ranks 1, 5, 20, 50, 100 and the original
ks = [1, 5, 20, 50, 100]
titles = [f"k = {k}: {k * (m + n + 1) / (m * n):.1%} stored, error {s[k] / s[0]:.1%}" for k in ks] + ["original: rank 427"]
fig = make_subplots(2, 3, subplot_titles=titles, horizontal_spacing=0.02, vertical_spacing=0.08)
for i, z in enumerate([rank_k(k) for k in ks] + [img]):
    r, c = i // 3 + 1, i % 3 + 1
    gray(fig, z, r, c)
    fig.update_xaxes(visible=False, row=r, col=c)
    fig.update_yaxes(visible=False, autorange="reversed", scaleanchor="x" if i == 0 else f"x{i + 1}", row=r, col=c)
fig.update_layout(template="simple_white", width=1500, height=740, font=FONT, margin=dict(l=10, r=10, t=60, b=10))
fig.update_annotations(font_size=30)
fig.write_image(HERE / "image_ranks.png", scale=2)
fig.write_image(HERE / "image_ranks.pdf")

# 2. the first four rank-1 layers sigma_i u_i v_i^T
fig = make_subplots(1, 4, subplot_titles=[f"layer {i + 1}: σ<sub>{i + 1}</sub> = {s[i]:.1f}"
                                          for i in range(4)], horizontal_spacing=0.02)
for i in range(4):
    layer = s[i] * np.outer(U[:, i], Vt[i])
    lim = np.abs(layer).max()
    fig.add_trace(go.Heatmap(z=layer, colorscale="RdBu", zmid=0, zmin=-lim, zmax=lim, showscale=False), 1, i + 1)
    fig.update_xaxes(visible=False, row=1, col=i + 1)
    fig.update_yaxes(visible=False, autorange="reversed", scaleanchor="x" if i == 0 else f"x{i + 1}", row=1, col=i + 1)
fig.update_layout(template="simple_white", width=1500, height=360, font=FONT, margin=dict(l=10, r=10, t=70, b=10))
fig.update_annotations(font_size=30)
fig.write_image(HERE / "rank1_layers.png", scale=2)
fig.write_image(HERE / "rank1_layers.pdf")

# 3. singular value decay and cumulative share of the squared singular values
share = np.cumsum(s ** 2) / np.sum(s ** 2)
fig = make_subplots(1, 2, subplot_titles=["singular values σ<sub>i</sub> (log scale)", "share of Σσ<sub>i</sub><sup>2</sup> kept by the first k"],
                    horizontal_spacing=0.12)
fig.add_trace(go.Scatter(x=np.arange(1, len(s) + 1), y=s, mode="lines", line=dict(color=BLUE, width=3), showlegend=False), 1, 1)
fig.add_trace(go.Scatter(x=np.arange(1, len(s) + 1), y=share, mode="lines", line=dict(color=ORANGE, width=3), showlegend=False), 1, 2)
for k in [5, 20, 50]:
    fig.add_trace(go.Scatter(x=[k], y=[share[k - 1]], mode="markers+text", marker=dict(size=10, color=ORANGE),
                             text=[f"k = {k}: {share[k - 1]:.1%}"], textposition="bottom right", showlegend=False), 1, 2)
fig.update_xaxes(title="i", row=1, col=1)
fig.update_yaxes(type="log", dtick=1, exponentformat="power", row=1, col=1)
fig.update_xaxes(title="k", type="log", tickvals=[1, 2, 5, 10, 20, 50, 100, 200, 427], row=1, col=2)
fig.update_yaxes(range=[0.9, 1.002], tickformat=".0%", row=1, col=2)
fig.update_layout(template="simple_white", width=1300, height=500, font=FONT, margin=dict(l=70, r=30, t=50, b=60))
fig.update_annotations(font_size=26)
fig.write_image(HERE / "singular_decay.png", scale=2)
fig.write_image(HERE / "singular_decay.pdf")

# 4. noise reduction: a rank-3 picture plus noise, cleaned by keeping 3 singular values
clean = np.zeros((120, 160))
clean[50:70, 10:150] += 0.5          # horizontal bar
clean[10:110, 70:90] += 0.5          # vertical bar
clean[20:45, 20:55] += 1.0           # square
noisy = clean + np.random.default_rng(0).normal(0, 0.3, clean.shape)
Un, sn, Vnt = np.linalg.svd(noisy, full_matrices=False)
err = lambda X: np.linalg.norm(X - clean) / np.linalg.norm(clean)
kk = np.arange(1, 51)
errs = [err((Un[:, :k] * sn[:k]) @ Vnt[:k]) for k in kk]
print("noisy error", round(err(noisy), 3), "rank-3 error", round(errs[2], 3), "first sigmas", sn[:6].round(2))
fig = make_subplots(2, 3, specs=[[{}, {}, {}], [{"colspan": 2}, None, {}]],
                    subplot_titles=["clean picture (rank 3)", f"plus noise: error {err(noisy):.0%}",
                                    f"rank 3 of the noisy one: error {errs[2]:.0%}",
                                    "singular values of the noisy picture", "error against k"],
                    vertical_spacing=0.14, horizontal_spacing=0.06)
for c, z in enumerate([clean, noisy, (Un[:, :3] * sn[:3]) @ Vnt[:3]], 1):
    gray(fig, z, 1, c, zmin=-0.2, zmax=1.4)
    fig.update_xaxes(visible=False, row=1, col=c)
    fig.update_yaxes(visible=False, autorange="reversed", scaleanchor="x" if c == 1 else f"x{c}", row=1, col=c)
fig.add_trace(go.Scatter(x=np.arange(1, 31), y=sn[:30], mode="markers", marker=dict(size=9, color=[RED] * 3 + [GREY] * 27),
                         showlegend=False), 2, 1)
fig.add_annotation(x=3, y=sn[2], text="3 signal values", showarrow=True, ax=90, ay=-25, xanchor="left", font=dict(color=RED), row=2, col=1)
fig.add_annotation(x=18, y=sn[17], text="noise floor", showarrow=True, ax=0, ay=-40, font=dict(color=GREY), row=2, col=1)
fig.add_trace(go.Scatter(x=kk, y=errs, mode="lines+markers", line=dict(color=BLUE, width=3), marker=dict(size=5), showlegend=False), 2, 3)
fig.update_xaxes(title="i", row=2, col=1)
fig.update_yaxes(title="σ<sub>i</sub>", row=2, col=1)
fig.update_xaxes(title="k", row=2, col=3)
fig.update_yaxes(title="error vs clean", tickformat=".0%", range=[0, 0.9], row=2, col=3)
fig.update_layout(template="simple_white", width=1400, height=820, font=FONT, margin=dict(l=70, r=20, t=50, b=60))
fig.update_annotations(font_size=26)
fig.write_image(HERE / "denoise.png", scale=2)
fig.write_image(HERE / "denoise.pdf")
