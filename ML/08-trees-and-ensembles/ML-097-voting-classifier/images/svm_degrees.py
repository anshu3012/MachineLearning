"""One algorithm, five settings (Plotly): polynomial-kernel SVMs of degree 1 to 5 on make_classification
(1,000 observations, 20 features), each alone and all five in a soft vote. 10-fold cross-validation, as in the notebook."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from sklearn.calibration import CalibratedClassifierCV
from sklearn.datasets import make_classification
from sklearn.ensemble import VotingClassifier
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC

HERE = Path(__file__).parent
X, y = make_classification(n_samples=1000, n_features=20, n_informative=15, n_redundant=5, random_state=2)
svms = [(f"svm{d}", CalibratedClassifierCV(SVC(kernel="poly", degree=d), ensemble=False)) for d in range(1, 6)]
acc = [round(cross_val_score(m, X, y, cv=10, n_jobs=-1).mean(), 3) for _, m in svms]
vote = round(cross_val_score(VotingClassifier(svms, voting="soft"), X, y, cv=10, n_jobs=-1).mean(), 3)
print(acc, vote)
assert acc == [0.851, 0.855, 0.894, 0.854, 0.871] and vote == 0.928                  # section 5 table
x = [f"degree {d}" for d in range(1, 6)] + ["soft vote<br>of all five"]
col = ["#4C78A8"] * 5 + ["#54A24B"]
col[2] = "#F58518"
fig = go.Figure(go.Bar(x=x, y=acc + [vote], marker_color=col, text=[f"{v:.3f}" for v in acc + [vote]],
                       textposition="outside"))
fig.add_annotation(x=2, y=0.894, ax=0, ay=-70, text="the one we would<br>normally keep", font=dict(color="#F58518"),
                   arrowcolor="#F58518", yshift=30)
fig.update_layout(template="simple_white", width=1100, height=540, font=dict(family="Latin Modern Roman", size=22),
                  yaxis=dict(title="cross-validated accuracy", range=[0.80, 0.96]), margin=dict(l=100, r=20, t=30, b=100),
                  bargap=0.3)
fig.write_image(HERE / "svm_degrees.png", scale=2); fig.write_image(HERE / "svm_degrees.pdf")
