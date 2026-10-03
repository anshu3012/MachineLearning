"""AdaBoost from scratch on the 10-row toy data (same steps and seed as the Notebook), Plotly:
stages.png      - each stage's stump on its own dataset (marker size = copies of a row), and the final vote;
exp_curves.png  - the update factors e^alpha and e^-alpha against alpha."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.tree import DecisionTreeClassifier

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=19)
COLOURS = {0: "#F58518", 1: "#4C78A8"}
REGION = [[0, "#FDE5CC"], [1, "#DCE6F2"]]
X = np.c_[[1, 2, 3, 4, 5, 6, 6, 7, 9, 9], [5, 3, 6, 8, 1, 9, 5, 8, 9, 2]].astype(float)
Y = np.array([1, 1, 0, 1, 0, 1, 0, 1, 0, 0])
rng = np.random.default_rng(0)

rows = np.arange(10)                       # original row of every row in the current dataset
stages = []
for k in range(3):
    Xk, yk = X[rows], Y[rows]
    w = np.full(10, 0.1)
    stump = DecisionTreeClassifier(max_depth=1, random_state=0).fit(Xk, yk)
    wrong = stump.predict(Xk) != yk
    err = w[wrong].sum()
    alpha = 0.5 * np.log((1 - err) / err)
    stages.append(dict(rows=rows.copy(), stump=stump, err=err, alpha=alpha, wrong=wrong))
    w = np.where(wrong, w * np.exp(alpha), w * np.exp(-alpha))
    w = w / w.sum()
    upper = np.cumsum(w)
    rows = rows[[int(np.argmax(upper > rng.random())) for _ in range(10)]]
    print(k + 1, "rows", stages[-1]["rows"], "err", round(err, 3), "alpha", round(alpha, 4))

xs = np.linspace(0, 10, 300)
ys = np.linspace(0, 10, 300)
XX, YY = np.meshgrid(xs, ys)
grid = np.c_[XX.ravel(), YY.ravel()]
vote = sum(s["alpha"] * (2 * s["stump"].predict(grid) - 1) for s in stages)
final = sum(s["alpha"] * (2 * s["stump"].predict(X) - 1) for s in stages)
acc = np.mean((final > 0) == (Y == 1))
titles = [f"stage {k + 1}: error {s['err']:.1f}, alpha {s['alpha']:.2f}" for k, s in enumerate(stages)]
titles.append(f"weighted vote: {int(acc * 10)} of 10 correct")
fig = make_subplots(2, 2, subplot_titles=titles, horizontal_spacing=0.09, vertical_spacing=0.12)
for i in range(4):
    r, c = i // 2 + 1, i % 2 + 1
    if i < 3:
        s = stages[i]
        Z = s["stump"].predict(grid).reshape(XX.shape)
        counts = np.bincount(s["rows"], minlength=10)
        wrong_rows = set(s["rows"][s["wrong"]])
    else:
        Z = (vote > 0).astype(int).reshape(XX.shape)
        counts = np.ones(10, int)
        wrong_rows = set(np.where((final > 0) != (Y == 1))[0])
    fig.add_trace(go.Heatmap(x=xs, y=ys, z=Z, zmin=0, zmax=1, colorscale=REGION, showscale=False), r, c)
    for cls in (0, 1):
        m = (Y == cls) & (counts > 0)
        fig.add_trace(go.Scatter(x=X[m, 0], y=X[m, 1], mode="markers", name=f"class {cls}", showlegend=(i == 0),
                                 marker=dict(color=COLOURS[cls], size=10 + 7 * counts[m],
                                             line=dict(color="white", width=1))), r, c)
    bad = sorted(wrong_rows)
    fig.add_trace(go.Scatter(x=X[bad, 0], y=X[bad, 1], mode="markers", name="misclassified", showlegend=(i == 0),
                             marker=dict(color="rgba(0,0,0,0)", size=[16 + 7 * counts[b] for b in bad],
                                         line=dict(color="#E45756", width=3))), r, c)
    missing = np.where(counts == 0)[0]
    fig.add_trace(go.Scatter(x=X[missing, 0], y=X[missing, 1], mode="markers", name="not drawn", showlegend=(i == 1),
                             marker=dict(symbol="x-thin", size=12, line=dict(color="#6B6B6B", width=2))), r, c)
fig.update_xaxes(range=[0, 10], title_text="X1", dtick=2)
fig.update_yaxes(range=[0, 10], title_text="X2", dtick=2)
fig.update_annotations(font_size=21)
fig.update_layout(template="simple_white", width=1200, height=1080, font=FONT, margin=dict(l=60, r=20, t=50, b=60),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.07, font_size=20))
fig.write_image(HERE / "stages.png", scale=2)
fig.write_image(HERE / "stages.pdf")

# ---- update factors ----
a = np.linspace(0, 2, 200)
fig = go.Figure()
fig.add_trace(go.Scatter(x=a, y=np.exp(a), name="misclassified row: weight × e<sup>alpha</sup>", line=dict(color="#E45756", width=3)))
fig.add_trace(go.Scatter(x=a, y=np.exp(-a), name="correct row: weight × e<sup>−alpha</sup>", line=dict(color="#54A24B", width=3)))
for al in (stages[0]["alpha"], stages[1]["alpha"]):
    fig.add_trace(go.Scatter(x=[al, al], y=[np.exp(al), np.exp(-al)], mode="markers+text", showlegend=False,
                             text=[f"×{np.exp(al):.2f}", f"×{np.exp(-al):.2f}"], textposition="middle right",
                             marker=dict(color="black", size=10), textfont=dict(size=19)))
    fig.add_vline(x=al, line=dict(color="#6B6B6B", dash="dot", width=1))
fig.add_hline(y=1, line=dict(color="#6B6B6B", dash="dash", width=1))
fig.update_xaxes(title="alpha (the stump's say)")
fig.update_yaxes(title="factor applied to the weight", range=[0, 7.5])
fig.update_layout(template="simple_white", width=1000, height=560, font=FONT, margin=dict(l=70, r=20, t=20, b=70),
                  legend=dict(x=0.02, y=0.98, font_size=19))
fig.write_image(HERE / "exp_curves.png", scale=2)
fig.write_image(HERE / "exp_curves.pdf")
