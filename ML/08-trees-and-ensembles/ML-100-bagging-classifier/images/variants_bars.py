"""Section 3 in one picture (Plotly): test accuracy of one tree and of every BaggingClassifier variant on the
10,000-observation make_classification data (same data, split and settings as the notebook)."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import make_classification
from sklearn.ensemble import BaggingClassifier
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

HERE = Path(__file__).parent
X, y = make_classification(n_samples=10000, n_features=10, n_informative=3, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
B = lambda **kw: BaggingClassifier(kw.pop("estimator", DecisionTreeClassifier()), n_estimators=500, random_state=42,
                                   n_jobs=-1, **kw)
models = {"one tree": DecisionTreeClassifier(random_state=42),
          "bagging<br>25% rows": B(max_samples=0.25),
          "bagging<br>50% rows": B(max_samples=0.5),
          "pasting": B(max_samples=0.25, bootstrap=False),
          "random<br>subspaces": B(max_samples=1.0, bootstrap=False, max_features=0.5, bootstrap_features=True),
          "random<br>patches": B(max_samples=0.25, max_features=0.5, bootstrap_features=True),
          "bagged<br>SVMs": B(estimator=SVC(), max_samples=0.25)}
acc = {k: m.fit(X_train, y_train).score(X_test, y_test) for k, m in models.items()}
print(acc)
assert np.allclose(list(acc.values()), [0.9265, 0.945, 0.950, 0.946, 0.9415, 0.938, 0.9125])   # section 3 numbers
col = ["#6B6B6B"] + ["#4C78A8"] * 5 + ["#E45756"]
fig = go.Figure(go.Bar(x=list(acc), y=list(acc.values()), marker_color=col, text=[f"{v:.3f}" for v in acc.values()],
                       textposition="outside"))
fig.add_hline(y=acc["one tree"], line=dict(color="#6B6B6B", dash="dash", width=2))
fig.update_layout(template="simple_white", width=1150, height=540, font=dict(family="Latin Modern Roman", size=22),
                  yaxis=dict(title="test accuracy", range=[0.9, 0.958]), margin=dict(l=100, r=20, t=30, b=100), bargap=0.3)
fig.write_image(HERE / "variants_bars.png", scale=2); fig.write_image(HERE / "variants_bars.pdf")
