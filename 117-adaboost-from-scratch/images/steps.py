"""AdaBoost from scratch, the numbers of each step drawn (Plotly; same data, steps and seed as the Notebook):
stage_errors.png   - error = total weight of the mistakes, for each stage, and the alpha it gives (section 3);
weight_update.png  - stage 1 weights: start, after the exponential update, after normalising (section 4);
zero_error.png     - alpha against the error near 0, with and without eps (section 7);
vote.png           - the weighted vote for the two queries, built up stump by stump (section 9);
upsample_vs_weights.png - our upsampled stumps against scikit-learn's weighted stumps (section 10)."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=20)
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
COLOURS = {0: ORANGE, 1: BLUE}
REGION = [[0, "#FDE5CC"], [1, "#DCE6F2"]]
X = np.c_[[1, 2, 3, 4, 5, 6, 6, 7, 9, 9], [5, 3, 6, 8, 1, 9, 5, 8, 9, 2]].astype(float)
Y = np.array([1, 1, 0, 1, 0, 1, 0, 1, 0, 0])
rng = np.random.default_rng(0)

stages, rows = [], np.arange(10)
for k in range(3):
    stump = DecisionTreeClassifier(max_depth=1, random_state=0).fit(X[rows], Y[rows])
    wrong = stump.predict(X[rows]) != Y[rows]
    w = np.full(10, 0.1)
    err = w[wrong].sum()
    alpha = 0.5 * np.log((1 - err) / err)
    updated = np.where(wrong, w * np.exp(alpha), w * np.exp(-alpha))
    norm = updated / updated.sum()
    stages.append(dict(rows=rows, stump=stump, wrong=wrong, err=err, alpha=alpha, updated=updated, norm=norm))
    upper = np.cumsum(norm)
    rows = rows[[int(np.argmax(upper > rng.random())) for _ in range(10)]]
s1 = stages[0]
assert np.allclose([s["err"] for s in stages], [0.3, 0.1, 0.2])
assert np.allclose([s["alpha"] for s in stages], [0.4236, 1.0986, 0.6931], atol=1e-4)
assert list(np.where(s1["wrong"])[0]) == [2, 6, 8]
assert np.isclose(s1["updated"].sum(), 0.9165, atol=1e-4)
assert np.allclose(sorted(set(np.round(s1["updated"], 4))), [0.0655, 0.1528])
assert np.allclose(sorted(set(np.round(s1["norm"], 4))), [0.0714, 0.1667])


def save(fig, name):
    fig.write_image(HERE / f"{name}.png", scale=2)
    fig.write_image(HERE / f"{name}.pdf")


# ---- section 3: the error is the total weight of the mistakes ----
fig = go.Figure()
for k, s in enumerate(stages):
    orig = s["rows"]
    for i in range(10):
        fig.add_trace(go.Bar(y=[f"stage {k + 1}"], x=[0.1], orientation="h", showlegend=False,
                             marker=dict(color=RED if s["wrong"][i] else "#D9D9D9", line=dict(color="white", width=2)),
                             text=[str(orig[i])], textposition="inside", insidetextanchor="middle",
                             textfont=dict(size=18, color="white" if s["wrong"][i] else "black")))
    fig.add_annotation(x=1.02, y=f"stage {k + 1}", xanchor="left", showarrow=False, font=dict(size=20),
                       text=f"error {s['err']:.1f} → alpha {s['alpha']:.2f}")
fig.add_trace(go.Bar(y=[None], x=[None], marker_color=RED, name="misclassified (weight 0.1 each)"))
fig.add_trace(go.Bar(y=[None], x=[None], marker_color="#D9D9D9", name="correct"))
fig.update_layout(barmode="stack", template="simple_white", width=1200, height=430, font=FONT,
                  xaxis=dict(title="weight (the ten rows of the stage's dataset, labelled by original row)",
                             range=[0, 1.42], tickvals=[0, 0.2, 0.4, 0.6, 0.8, 1.0]),
                  yaxis=dict(autorange="reversed"), margin=dict(l=100, r=20, t=60, b=70),
                  legend=dict(orientation="h", x=0, y=1.02, yanchor="bottom"))
save(fig, "stage_errors")

# ---- section 4: stage 1 weights, update then normalise ----
fig = go.Figure()
labels = [str(i) for i in range(10)]
for name, vals, col in (("start: 0.1 each", np.full(10, 0.1), "#BDBDBD"),
                        ("× e<sup>±alpha</sup>: 0.1528 or 0.0655 (sum 0.9165)", s1["updated"], GREY),
                        ("÷ 0.9165: 0.1667 or 0.0714 (sum 1)", s1["norm"], BLUE)):
    fig.add_trace(go.Bar(x=labels, y=vals, name=name, marker_color=col))
for i in np.where(s1["wrong"])[0]:
    fig.add_annotation(x=str(i), y=0.185, text="mistake", showarrow=False, font=dict(color=RED, size=19))
fig.update_layout(template="simple_white", width=1100, height=520, font=FONT, barmode="group",
                  xaxis=dict(title="row"), yaxis=dict(title="weight", range=[0, 0.2]),
                  margin=dict(l=80, r=20, t=110, b=70), legend=dict(x=0, y=1.02, yanchor="bottom", font_size=19))
save(fig, "weight_update")

# ---- section 7: alpha near error 0, with and without eps ----
eps = 1e-10
e = np.logspace(-14, np.log10(0.5), 400)
fig = go.Figure()
fig.add_trace(go.Scatter(x=e, y=0.5 * np.log((1 - e) / e), name="without eps: grows without limit",
                         line=dict(color=RED, width=3, dash="dash")))
fig.add_trace(go.Scatter(x=e, y=0.5 * np.log((1 - e + eps) / (e + eps)), name="with eps = 10<sup>−10</sup>",
                         line=dict(color=BLUE, width=3)))
cap = 0.5 * np.log((1 + eps) / eps)
assert np.isclose(cap, 11.51, atol=0.01)
fig.add_trace(go.Scatter(x=[1e-14], y=[cap], mode="markers+text", text=[f"error near 0: alpha {cap:.1f}, finite"],
                         textposition="top right", showlegend=False, marker=dict(size=11, color="black"),
                         textfont=dict(size=19)))
fig.add_trace(go.Scatter(x=[s["err"] for s in stages], y=[s["alpha"] for s in stages], mode="markers",
                         showlegend=False, marker=dict(size=11, color="black")))
fig.add_annotation(x=np.log10(0.1), y=1.1, ax=-120, ay=-90, showarrow=True, arrowhead=2, font=dict(size=19),
                   text="our stages: 0.42, 1.10, 0.69")
fig.update_layout(template="simple_white", width=1000, height=560, font=FONT,
                  xaxis=dict(type="log", title="error (log scale)", exponentformat="power", dtick=2),
                  yaxis=dict(title="alpha (the stump's say)", range=[0, 17]),
                  margin=dict(l=70, r=30, t=20, b=70), legend=dict(x=0.45, y=0.98, font_size=19))
save(fig, "zero_error")

# ---- section 9: the weighted vote, built up ----
queries = {"query (1, 5), true class 1": [1, 5], "query (9, 9), true class 0": [9, 9]}
fig = make_subplots(1, 2, subplot_titles=list(queries), horizontal_spacing=0.12)
for c, (title, q) in enumerate(queries.items(), start=1):
    votes = [2 * s["stump"].predict([q])[0] - 1 for s in stages]
    parts = [s["alpha"] * v for s, v in zip(stages, votes)]
    total = sum(parts)
    assert np.isclose(total, {1: 0.8291, 2: 0.0181}[c], atol=1e-4)
    fig.add_trace(go.Waterfall(x=["stump 1", "stump 2", "stump 3", "total"], measure=["relative"] * 3 + ["total"],
                               y=parts + [total], showlegend=False,
                               text=[f"{p:+.2f}" for p in parts] + [f"{total:+.2f}"], textposition="outside",
                               increasing=dict(marker_color=BLUE), decreasing=dict(marker_color=ORANGE),
                               totals=dict(marker_color=BLUE if total > 0 else ORANGE),
                               connector=dict(line=dict(color=GREY, dash="dot"))), 1, c)
    verdict = "class 1: correct" if c == 1 else "class 1: wrong, just"
    fig.add_annotation(x="total", y=1.65, text=verdict, showarrow=False, font=dict(size=19), row=1, col=c)
fig.add_hline(y=0, line=dict(color="black", width=1))
fig.update_yaxes(title_text="alpha × vote (running total)", range=[-1.0, 1.8], row=1, col=1)
fig.update_yaxes(range=[-1.0, 1.8], row=1, col=2)
fig.update_annotations(font_size=21)
fig.update_layout(template="simple_white", width=1200, height=560, font=FONT, margin=dict(l=80, r=20, t=50, b=50))
save(fig, "vote")

# ---- section 10: upsampled stumps against weighted stumps (SAMME) ----
abc = AdaBoostClassifier(DecisionTreeClassifier(max_depth=1), n_estimators=3, random_state=0).fit(X, Y)
assert np.allclose(abc.estimator_weights_, [0.8473, 1.2993, 1.8458], atol=1e-4)
xs = np.linspace(0, 10, 300)
XX, YY = np.meshgrid(xs, xs)
grid = np.c_[XX.ravel(), YY.ravel()]
ours = lambda P: sum(s["alpha"] * (2 * s["stump"].predict(P) - 1) for s in stages) > 0
models = {"ours: upsampling, alpha with 1/2": ours, "scikit-learn: sample_weight, SAMME": lambda P: abc.predict(P) == 1}
fig = make_subplots(1, 2, horizontal_spacing=0.08,
                    subplot_titles=[f"{n}<br>{int(np.sum(m(X) == (Y == 1)))} of 10 correct" for n, m in models.items()])
assert [int(np.sum(m(X) == (Y == 1))) for m in models.values()] == [9, 10]
for c, m in enumerate(models.values(), start=1):
    fig.add_trace(go.Heatmap(x=xs, y=xs, z=m(grid).astype(int).reshape(XX.shape), zmin=0, zmax=1,
                             colorscale=REGION, showscale=False), 1, c)
    for cls in (0, 1):
        k = Y == cls
        fig.add_trace(go.Scatter(x=X[k, 0], y=X[k, 1], mode="markers", name=f"class {cls}", showlegend=c == 1,
                                 marker=dict(color=COLOURS[cls], size=16, line=dict(color="white", width=1))), 1, c)
    bad = np.where(m(X) != (Y == 1))[0]
    fig.add_trace(go.Scatter(x=X[bad, 0], y=X[bad, 1], mode="markers", name="misclassified", showlegend=c == 1,
                             marker=dict(color="rgba(0,0,0,0)", size=28, line=dict(color=RED, width=3))), 1, c)
fig.update_xaxes(range=[0, 10], title_text="X1", dtick=2)
fig.update_yaxes(range=[0, 10], title_text="X2", dtick=2)
fig.update_annotations(font_size=21)
fig.update_layout(template="simple_white", width=1200, height=640, font=FONT, margin=dict(l=60, r=20, t=90, b=60),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.14))
save(fig, "upsample_vs_weights")
print("ok")
