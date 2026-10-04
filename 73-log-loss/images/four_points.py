"""Note 73: the four points of the two-model table, placed so that sigma(w . x) gives exactly the table's probabilities.
Model 1 is the line x1 = 0 (P(green) = sigma(x1)); model 2 is the line x2 = 0 (P(green) = sigma(x2)).
toy_models.png: both models on the points (Section 2).  one_formula.png: the two cost curves and model 1's points (Section 6).
gd_four.gif + gd_four_frames.png: batch gradient descent on the log loss, starting from model 1 (Section 7).
Run: python four_points.py  (Plotly; animation via Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
BLUE, GREEN, ORANGE, RED, GREY = "#4C78A8", "#54A24B", "#F58518", "#E45756", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=20)
sig = lambda z: 1 / (1 + np.exp(-z))
logit = lambda p: np.log(p / (1 - p))

y = np.array([1, 0, 1, 0])                                       # green, red, green, red
X = np.array([[logit(.7), logit(.7)], [logit(.6), logit(.4)], [logit(.4), logit(.7)], [logit(.2), logit(.4)]])
Xb = np.c_[np.ones(4), X]
W1, W2 = np.array([0, 1.0, 0]), np.array([0, 0, 1.0])            # (intercept, w1, w2)
p_true = lambda w: np.where(y == 1, sig(Xb @ w), 1 - sig(Xb @ w))
loss = lambda w: -np.mean(np.log(p_true(w)))
assert np.allclose(p_true(W1), [.7, .4, .4, .8]) and np.allclose(p_true(W2), [.7, .6, .7, .6])
assert round(p_true(W1).prod(), 3) == 0.090 and round(p_true(W2).prod(), 3) == 0.176
assert round(loss(W1), 3) == 0.603 and round(-np.log(p_true(W2)).sum(), 2) == 1.74
LIM = 2.2
g = np.linspace(-LIM, LIM, 120)
GX, GY = np.meshgrid(g, g)


def field(w):                                                     # P(green) over the plane, as a pale background
    return go.Heatmap(x=g, y=g, z=sig(w[0] + w[1] * GX + w[2] * GY), colorscale=[[0, "#F6D5D5"], [1, "#D5EBD1"]],
                      zmin=0, zmax=1, showscale=False)


def line(w, **kw):                                                # the line where P(green) = 0.5
    if abs(w[2]) > abs(w[1]):
        return go.Scatter(x=[-LIM, LIM], y=[-(w[0] + w[1] * -LIM) / w[2], -(w[0] + w[1] * LIM) / w[2]], mode="lines", **kw)
    return go.Scatter(x=[-(w[0] + w[2] * -LIM) / w[1], -(w[0] + w[2] * LIM) / w[1]], y=[-LIM, LIM], mode="lines", **kw)


def points(w):
    pt = p_true(w)
    return go.Scatter(x=X[:, 0], y=X[:, 1], mode="markers+text", text=[f"{i + 1}: {v:.1f}" for i, v in enumerate(pt)],
                      textposition="top center", textfont=dict(size=20),
                      marker=dict(size=22, color=[GREEN if c else RED for c in y], line=dict(color="black", width=1.5),
                                  symbol=["circle" if v > 0.5 else "x" for v in pt]), showlegend=False)


# --- Section 2: the two models on the four points
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08,
                    subplot_titles=("Model 1: likelihood 0.090", "Model 2: likelihood 0.176"))
for c, w in ((1, W1), (2, W2)):
    fig.add_trace(field(w), 1, c)
    fig.add_trace(line(w, line=dict(color="black", width=4), showlegend=False), 1, c)
    fig.add_trace(points(w), 1, c)
fig.update_xaxes(range=[-LIM, LIM], showticklabels=False, title="feature 1")
fig.update_yaxes(range=[-LIM, LIM], showticklabels=False, scaleanchor="x")
fig.update_yaxes(title="feature 2", col=1)
fig.update_yaxes(scaleanchor="x2", col=2)
fig.update_layout(template="simple_white", width=1100, height=600, font=FONT, margin=dict(l=60, r=20, t=60, b=60))
fig.update_annotations(font_size=24)
fig.write_image(HERE / "toy_models.png", scale=2)

# --- Section 6: one formula, two curves
yh = np.linspace(0.01, 0.99, 300)
c1 = sig(Xb @ W1)                                                 # model 1's P(green) = y hat: 0.7, 0.6, 0.4, 0.2
cost = np.where(y == 1, -np.log(c1), -np.log(1 - c1))
assert np.allclose(c1, [.7, .6, .4, .2]) and round(cost.sum(), 2) == 2.41 and round(cost[1], 2) == round(cost[2], 2) == 0.92
fig = go.Figure()
fig.add_trace(go.Scatter(x=yh, y=-np.log(yh), mode="lines", line=dict(color=GREEN, width=4), name="green point (y = 1): cost −log ŷ"))
fig.add_trace(go.Scatter(x=yh, y=-np.log(1 - yh), mode="lines", line=dict(color=RED, width=4), name="red point (y = 0): cost −log(1 − ŷ)"))
for i in range(4):
    fig.add_trace(go.Scatter(x=[c1[i]], y=[cost[i]], mode="markers+text", text=[f"point {i + 1}: {cost[i]:.2f}"],
                             textposition="middle right" if i in (0, 1) else "middle left", showlegend=False, textfont=dict(size=19),
                             marker=dict(size=16, color=GREEN if y[i] else RED, line=dict(color="black", width=1.5))))
fig.update_layout(template="simple_white", width=1000, height=560, font=FONT, margin=dict(l=70, r=20, t=40, b=60),
                  xaxis=dict(title="ŷ = model's P(green)", range=[0, 1]), yaxis=dict(title="cost of the point", range=[0, 3]),
                  legend=dict(x=0.5, xanchor="center", y=1.02, yanchor="bottom", orientation="h"))
fig.write_image(HERE / "one_formula.png", scale=2)

# --- Section 7: gradient descent from model 1
LR, STEPS = 1.0, 40
path, w = [W1.copy()], W1.copy()
for _ in range(STEPS):
    w = w + LR * Xb.T @ (y - sig(Xb @ w)) / 4
    path.append(w.copy())
L = np.array([loss(v) for v in path])
assert np.all(np.diff(L) < 0) and L[3] < loss(W2) and round(L[-1], 3) == 0.072


def frame(k):
    f = make_subplots(rows=1, cols=2, horizontal_spacing=0.1, column_widths=[0.5, 0.5],
                      subplot_titles=(f"step {k}: the line moves", f"log loss {L[k]:.3f}"))
    f.add_trace(field(path[k]), 1, 1)
    f.add_trace(line(W1, line=dict(color=GREY, width=2, dash="dot"), showlegend=False), 1, 1)
    f.add_trace(line(path[k], line=dict(color="black", width=4), showlegend=False), 1, 1)
    f.add_trace(points(path[k]), 1, 1)
    f.add_trace(go.Scatter(x=[0, STEPS], y=[loss(W2)] * 2, mode="lines", line=dict(color=GREY, dash="dash", width=2),
                           showlegend=False), 1, 2)
    f.update_annotations(font_size=24)
    f.add_annotation(x=STEPS, y=loss(W2), text="model 2: 0.434", showarrow=False, yshift=16, xanchor="right",
                     font=dict(color=GREY, size=18), row=1, col=2)
    f.add_trace(go.Scatter(x=np.arange(k + 1), y=L[:k + 1], mode="lines+markers", line=dict(color=BLUE, width=4),
                           marker=dict(size=6), showlegend=False), 1, 2)
    f.update_xaxes(range=[-LIM, LIM], showticklabels=False, row=1, col=1)
    f.update_yaxes(range=[-LIM, LIM], showticklabels=False, scaleanchor="x", row=1, col=1)
    f.update_xaxes(title="step", range=[0, STEPS], row=1, col=2)
    f.update_yaxes(title="log loss", range=[0, 0.65], row=1, col=2)
    f.update_layout(template="simple_white", width=1100, height=560, font=FONT, margin=dict(l=40, r=20, t=60, b=60))
    return f


if __name__ == "__main__":
    tmp = HERE / ".gd_frames"
    tmp.mkdir(exist_ok=True)
    ks = list(range(0, 10)) + list(range(10, STEPS + 1, 3))
    if ks[-1] != STEPS:
        ks.append(STEPS)
    for i, k in enumerate(ks):
        frame(k).write_image(tmp / f"{i:03d}.png")
    n = len(ks)
    for i in range(n, n + 8):                                     # hold the last frame
        shutil.copy(tmp / f"{n - 1:03d}.png", tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "4", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "gd_four.gif")], check=True)
    keys = [Image.open(tmp / f"{ks.index(k):03d}.png").convert("RGB") for k in (0, 3, STEPS)]
    w_, h_ = keys[0].size                                         # one column: two-panel frames stay readable in the PDF
    sheet = Image.new("RGB", (w_, 3 * h_ + 32), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, (0, i * (h_ + 16)))
    sheet.save(HERE / "gd_four_frames.png")
    shutil.rmtree(tmp)
