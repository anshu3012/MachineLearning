"""Plotly charts for the decision tree intuition Note: entropy curve, Gini against entropy, continuous spread, threshold search."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=20, color="black")


def entropy(counts):
    p = np.asarray(counts, float) / np.sum(counts)
    p = p[p > 0]
    return float(-(p * np.log2(p)).sum())


def save(fig, name, w=1000, h=560):
    fig.update_layout(template="simple_white", font=FONT, width=w, height=h)
    fig.write_image(HERE / f"{name}.png", scale=2)
    fig.write_image(HERE / f"{name}.pdf")


p = np.linspace(0.0005, 0.9995, 400)
H = -(p * np.log2(p) + (1 - p) * np.log2(1 - p))
G = 1 - p**2 - (1 - p) ** 2

# 1. Entropy against P(yes), with the worked examples marked
fig = go.Figure(go.Scatter(x=p, y=H, mode="lines", line=dict(color=BLUE, width=4), showlegend=False))
for px, label, pos in [(0.0, "0 of 5 yes: H = 0", "top right"), (0.2, "1 of 5 yes: H = 0.722", "top left"),
                       (0.4, "2 of 5 yes: H = 0.971", "top left"), (0.5, "5 of 10 yes: H = 1", "top center")]:
    hy = entropy([px, 1 - px]) if px > 0 else 0.0
    fig.add_trace(go.Scatter(x=[px], y=[hy], mode="markers+text", text=[label], textposition=pos,
                             marker=dict(color="black", size=12), textfont=dict(size=18), showlegend=False))
fig.update_xaxes(title="P(yes): share of yes rows", range=[-0.03, 1.03], dtick=0.1)
fig.update_yaxes(title="entropy H (bits)", range=[0, 1.15])
fig.update_layout(margin=dict(l=80, r=30, t=20, b=70))
save(fig, "entropy_curve")
print("entropy at 0.2, 0.4, 0.5:", [round(entropy([q, 1 - q]), 3) for q in (0.2, 0.4, 0.5)])

# 2. Gini against entropy
fig = go.Figure()
fig.add_trace(go.Scatter(x=p, y=H, mode="lines", name="entropy (maximum 1)", line=dict(color=BLUE, width=4)))
fig.add_trace(go.Scatter(x=p, y=G, mode="lines", name="Gini impurity (maximum 0.5)", line=dict(color=ORANGE, width=4)))
fig.add_trace(go.Scatter(x=[0.4, 0.4], y=[entropy([2, 3]), 0.48], mode="markers+text", showlegend=False,
                         text=["0.971", "0.48"], textposition="bottom right", marker=dict(color="black", size=11),
                         textfont=dict(size=18)))
fig.update_xaxes(title="P(yes): share of yes rows", range=[-0.03, 1.03], dtick=0.1)
fig.update_yaxes(title="impurity", range=[0, 1.15])
fig.update_layout(legend=dict(x=0.5, xanchor="center", y=1.12, orientation="h"), margin=dict(l=80, r=30, t=50, b=70))
save(fig, "gini_vs_entropy")

# 3. Two numerical columns: a peaked one and a spread one
x = np.linspace(-4.5, 4.5, 500)
fig = go.Figure()
for s, name, col in [(0.5, "dataset 1: most values in -1 to 1", BLUE), (1.5, "dataset 2: values spread over -3 to 3", ORANGE)]:
    fig.add_trace(go.Scatter(x=x, y=np.exp(-x**2 / (2 * s * s)) / (s * np.sqrt(2 * np.pi)), mode="lines", name=name,
                             line=dict(color=col, width=4), fill="tozeroy"))
fig.update_xaxes(title="price (standardized)", dtick=1)
fig.update_yaxes(title="density")
fig.update_layout(legend=dict(x=0.99, xanchor="right", y=0.98), margin=dict(l=80, r=30, t=20, b=70))
save(fig, "spread_entropy", h=520)

# 4. Information gain for every candidate threshold of a numerical column
rating = np.array([1.6, 2.1, 2.9, 3.2, 3.3, 3.5, 4.1, 4.6])
down = np.array([0, 0, 0, 0, 1, 0, 1, 1])               # 1 = downloaded
parent = entropy(np.bincount(down))
gains = []
for v in rating[:-1]:
    left, right = down[rating <= v], down[rating > v]
    w = len(left) / 8 * entropy(np.bincount(left, minlength=2)) + len(right) / 8 * entropy(np.bincount(right, minlength=2))
    gains.append(parent - w)
gains = np.array(gains)
print("parent entropy", round(parent, 3), "gains", gains.round(3))
best = int(gains.argmax())
fig = go.Figure(go.Bar(x=[f"≤ {v}" for v in rating[:-1]], y=gains, text=[f"{g:.3f}" for g in gains], textposition="outside",
                       marker_color=[GREEN if i == best else GREY for i in range(len(gains))], textfont=dict(size=18)))
fig.update_xaxes(title="split: rating ≤ v against rating > v")
fig.update_yaxes(title="information gain", range=[0, 0.65])
fig.update_layout(margin=dict(l=80, r=30, t=20, b=70))
save(fig, "rating_gains", h=500)
