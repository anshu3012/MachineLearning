"""VotingClassifier on the heart disease data (Plotly): each base model, the hard and soft vote, and the best
soft-vote weights (3, 3, 2). Repeated stratified 10-fold cross-validation, 5 shuffles, as in the notebook."""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RepeatedStratifiedKFold, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

HERE = Path(__file__).parent
heart = pd.read_csv(HERE.parent / "data" / "heart.csv", encoding="utf-8-sig")
X, y = heart.drop(columns="target"), heart["target"]
cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=5, random_state=0)
est = [("lr", make_pipeline(StandardScaler(), LogisticRegression())), ("rf", RandomForestClassifier(random_state=42)),
       ("knn", make_pipeline(StandardScaler(), KNeighborsClassifier()))]
models = {"logistic<br>regression": est[0][1], "random<br>forest": est[1][1], "KNN": est[2][1],
          "hard<br>vote": VotingClassifier(est, voting="hard"), "soft<br>vote": VotingClassifier(est, voting="soft"),
          "soft vote,<br>weights 3, 3, 2": VotingClassifier(est, voting="soft", weights=[3, 3, 2])}
acc = {k: round(cross_val_score(m, X, y, cv=cv, n_jobs=-1).mean(), 3) for k, m in models.items()}
print(acc)
assert list(acc.values()) == [0.825, 0.817, 0.821, 0.834, 0.841, 0.844]     # section 4 numbers
col = ["#4C78A8"] * 3 + ["#F58518", "#54A24B", "#54A24B"]
fig = go.Figure(go.Bar(x=list(acc), y=list(acc.values()), marker_color=col, text=[f"{v:.3f}" for v in acc.values()],
                       textposition="outside"))
fig.add_hline(y=0.825, line=dict(color="black", dash="dash", width=2))
fig.add_annotation(x=1.5, y=0.8255, text="best single model", showarrow=False, yanchor="bottom")
fig.update_layout(template="simple_white", width=1100, height=540, font=dict(family="Latin Modern Roman", size=22),
                  yaxis=dict(title="cross-validated accuracy", range=[0.80, 0.852]), margin=dict(l=100, r=20, t=30, b=110),
                  bargap=0.3)
fig.write_image(HERE / "heart_votes.png", scale=2); fig.write_image(HERE / "heart_votes.pdf")
