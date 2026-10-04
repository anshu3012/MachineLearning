"""Heart disease data: accuracy of five classifiers out of the box, on one test split and with 10-fold
cross-validation (Plotly)."""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

HERE = Path(__file__).parent
df = pd.read_csv(HERE.parent / "data" / "heart.csv")
X, y = df.iloc[:, :-1], df.iloc[:, -1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
models = {"random forest": RandomForestClassifier(random_state=42),
          "gradient boosting": GradientBoostingClassifier(random_state=42),
          "SVM": SVC(), "logistic regression": LogisticRegression(max_iter=5000),
          "SVM, scaled inputs": make_pipeline(StandardScaler(), SVC())}
split = [m.fit(X_train, y_train).score(X_test, y_test) for m in models.values()]
cv = [cross_val_score(m, X, y, cv=10).mean() for m in models.values()]
print([round(v, 3) for v in split], [round(v, 3) for v in cv])
names = list(models)
fig = go.Figure([go.Bar(x=names, y=split, name="one test split (61 rows)", marker_color="#4C78A8",
                        text=[f"{v:.3f}" for v in split], textposition="outside"),
                 go.Bar(x=names, y=cv, name="10-fold cross-validation", marker_color="#F58518",
                        text=[f"{v:.3f}" for v in cv], textposition="outside")])
fig.update_yaxes(title="accuracy", range=[0.5, 0.95])
fig.update_layout(template="simple_white", barmode="group", width=1200, height=560,
                  font=dict(family="Latin Modern Roman", size=20), margin=dict(l=80, r=20, t=30, b=60),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=1.08))
fig.write_image(HERE / "model_comparison.png", scale=2)
fig.write_image(HERE / "model_comparison.pdf")
