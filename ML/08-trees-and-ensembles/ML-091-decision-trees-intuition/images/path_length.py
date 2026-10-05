"""How many questions a prediction needs (Plotly): fully grown scikit-learn trees (DecisionTreeClassifier,
random_state 0) on make_classification data (10 features, flip_y 0.01, random_state 0) with n from 1,000 to 300,000
training observations. The average number of questions on the path of 2,000 test observations grows in a straight line
against log2 n (about 1.8 more questions each time n doubles), from 8.2 to 23.2 while n grows 300-fold."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier
from gifkit import BLUE, FONT, GREY

here = Path(__file__).parent
ns = [1_000, 3_000, 10_000, 30_000, 100_000, 300_000]
X, y = make_classification(n_samples=max(ns) + 2000, n_features=10, flip_y=0.01, random_state=0)
Xte = X[-2000:]
avg, leaves = [], []
for n in ns:
    t = DecisionTreeClassifier(random_state=0).fit(X[:n], y[:n])
    avg.append(float(t.decision_path(Xte).sum(1).mean() - 1))         # nodes on the path minus the leaf
    leaves.append(t.get_n_leaves())                                     # pure leaves hold several observations
lg = np.log2(ns)
slope = np.polyfit(lg, avg, 1)[0]
assert np.all(np.diff(avg) > 0) and round(avg[0], 1) == 8.2 and round(avg[-1], 1) == 23.2 and 1.5 < slope < 2.2
assert leaves[0] == 103                                                  # 103 leaves for 1,000 observations: log2 103 = 6.7
fig = go.Figure([go.Scatter(x=ns, y=avg, mode="lines+markers+text", text=[f"{a:.1f}" for a in avg], textposition="top left",
                            textfont=dict(size=17), line=dict(color=BLUE, width=4), marker=dict(size=10), name="fully grown tree: average questions"),
                 go.Scatter(x=ns, y=lg, mode="lines+markers", line=dict(color=GREY, width=3, dash="dash"), name="log₂ n: perfectly balanced tree")])
fig.update_layout(template="simple_white", width=950, height=540, font=FONT,
                  xaxis=dict(title="training observations n (log scale)", type="log"), yaxis=dict(title="questions per prediction", rangemode="tozero"),
                  legend=dict(x=0.01, y=0.99), margin=dict(l=80, r=30, t=20, b=70))
fig.write_image(here / "path_length.png", scale=2)
