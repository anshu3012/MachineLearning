"""Note ML-071 figures (Plotly): sigmoid vs step; the probability map around a line; push/pull strength; step vs sigmoid perceptron vs logistic regression."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression

here = Path(__file__).parent
font = dict(family="Latin Modern Roman", size=16)
G, B_, R, O = "#54A24B", "#4C78A8", "#E45756", "#F58518"
sig = lambda z: 1 / (1 + np.exp(-z))


def save(fig, name):
    fig.write_image(here / f"{name}.png", scale=2); fig.write_image(here / f"{name}.pdf")


# 1. step vs sigmoid
z = np.linspace(-8, 8, 400)
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1, subplot_titles=("Step: only 0 or 1", "Sigmoid: any value between 0 and 1"))
fig.add_trace(go.Scatter(x=z[z <= 0], y=0 * z[z <= 0], mode="lines", line=dict(color=R, width=4), showlegend=False), 1, 1)
fig.add_trace(go.Scatter(x=z[z > 0], y=0 * z[z > 0] + 1, mode="lines", line=dict(color=R, width=4), showlegend=False), 1, 1)
fig.add_trace(go.Scatter(x=z, y=sig(z), mode="lines", line=dict(color=B_, width=4), showlegend=False), 1, 2)
pts = np.array([-4, -2, 0, 2, 4])
fig.add_trace(go.Scatter(x=pts, y=sig(pts), mode="markers+text", marker=dict(size=10, color=B_),
                         text=[f"σ({p}) = {sig(p):.2f}".replace("-", "−") for p in pts],
                         textposition=["bottom right", "top left", "top left", "bottom right", "bottom right"],
                         textfont=dict(size=14, color=B_), showlegend=False), 1, 2)
for c in (1, 2):
    fig.add_trace(go.Scatter(x=[-8, 8], y=[0.5, 0.5], mode="lines", line=dict(color="#BBBBBB", width=1, dash="dot"), showlegend=False), 1, c)
fig.update_xaxes(title="z = w · x", range=[-8, 8])
fig.update_yaxes(range=[-0.08, 1.08], title="output", row=1, col=1)
fig.update_layout(template="simple_white", width=1100, height=430, font=font, margin=dict(l=70, r=20, t=50, b=60))
save(fig, "step_vs_sigmoid")

# 2. probability map around a line (surface beside contour map): see prob_map.py

# 3. strength of the push or pull: y - sigmoid(z)
z = np.linspace(-5, 5, 400)
fig = go.Figure()
fig.add_trace(go.Scatter(x=z, y=1 - sig(z), mode="lines", line=dict(color=G, width=4), name="positive point (y = 1): y − σ(z)"))
fig.add_trace(go.Scatter(x=z, y=0 - sig(z), mode="lines", line=dict(color=B_, width=4), name="negative point (y = 0): y − σ(z)"))
fig.add_trace(go.Scatter(x=[-5, 5], y=[0, 0], mode="lines", line=dict(color="#BBBBBB", width=1), showlegend=False))
fig.add_trace(go.Scatter(x=[0, 0], y=[-1, 1], mode="lines", line=dict(color="#BBBBBB", width=1, dash="dot"), showlegend=False))
for x0, txt, xa in ((-3.2, "positive point on the negative side:<br>misclassified, strong pull", "center"),
                    (3.2, "positive point on the positive side:<br>correct, weak push", "center")):
    fig.add_annotation(x=x0, y=1 - sig(x0) + 0.17, text=txt, showarrow=False, font=dict(color=G, size=14))
fig.add_annotation(x=0, y=-0.92, text="z = 0: on the line", showarrow=False, font=dict(color="#777777", size=14))
fig.update_layout(template="simple_white", width=1000, height=500, font=font, margin=dict(l=70, r=20, t=30, b=60),
                  legend=dict(x=0.6, y=0.35, bgcolor="rgba(255,255,255,0.9)"),
                  xaxis=dict(title="z = w · x   (negative side ← line → positive side)"),
                  yaxis=dict(title="y − ŷ  (size and sign of the update)", range=[-1.05, 1.15]))
save(fig, "push_pull")

# 4. step perceptron vs sigmoid perceptron vs logistic regression
X, y = make_classification(n_samples=100, n_features=2, n_informative=1, n_redundant=0, n_classes=2,
                           n_clusters_per_class=1, random_state=41, hypercube=False, class_sep=30)
Xb = np.insert(X, 0, 1, axis=1)


def train(f, seed=0, lr=0.1, loops=1000):
    rng = np.random.default_rng(seed); w = np.ones(3)
    for _ in range(loops):
        j = rng.integers(0, len(y)); w = w + lr * (y[j] - f(Xb[j] @ w)) * Xb[j]
    return w


def gaps(w):
    d = (Xb @ w) / np.linalg.norm(w[1:]); return d[y == 1].min(), -d[y == 0].max()


lines = [("perceptron with step", train(lambda z: 1.0 if z > 0 else 0.0), R),
         ("perceptron with sigmoid", train(sig), O)]
lr = LogisticRegression().fit(X, y)
lines.append(("logistic regression (scikit-learn)", np.r_[lr.intercept_, lr.coef_[0]], "black"))
fig = go.Figure()
for k, c in ((1, G), (0, B_)):
    fig.add_trace(go.Scatter(x=X[y == k, 0], y=X[y == k, 1], mode="markers", marker=dict(color=c, size=8), showlegend=False))
ys = np.linspace(-3.2, 2.4, 20)
for name, w, c in lines:
    g = gaps(w)
    print(name, w.round(3), "gaps", round(g[0], 2), round(g[1], 2))
    fig.add_trace(go.Scatter(x=-(w[0] + w[2] * ys) / w[1], y=ys, mode="lines", line=dict(color=c, width=4),
                             name=f"{name}: gaps {g[1]:.2f} (blue) and {g[0]:.2f} (green)"))
fig.update_layout(template="simple_white", width=1000, height=600, font=font, margin=dict(l=60, r=20, t=30, b=150),
                  legend=dict(x=0.5, y=-0.2, xanchor="center", yanchor="top", font=dict(size=14)),
                  xaxis=dict(title="x₁", range=[-6.2, 3.2]), yaxis=dict(title="x₂", range=[-3.2, 2.4]))
save(fig, "three_lines")
