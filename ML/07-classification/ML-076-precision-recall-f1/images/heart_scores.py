"""What the scikit-learn calls return on the heart-disease test set (Plotly): precision, recall and F1 of standardised
logistic regression and of a decision tree (random_state 1), split test size 0.2, random state 2, as in the Notebook."""
import warnings
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from gifkit import BLUE, FONT, ORANGE

warnings.simplefilter("ignore")
here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "heart.csv")
X_train, X_test, y_train, y_test = train_test_split(df.iloc[:, :-1], df.iloc[:, -1], test_size=0.2, random_state=2)
res = {}
for name, m in (("logistic regression", make_pipeline(StandardScaler(), LogisticRegression())),
                ("decision tree", DecisionTreeClassifier(random_state=1))):
    p = m.fit(X_train, y_train).predict(X_test)
    res[name] = [precision_score(y_test, p), recall_score(y_test, p), f1_score(y_test, p)]
assert [round(v, 3) for v in res["logistic regression"]] == [0.800, 0.966, 0.875]
assert [round(v, 3) for v in res["decision tree"]] == [0.788, 0.897, 0.839]
mets = ["precision", "recall", "F1"]
fig = go.Figure([go.Bar(x=mets, y=v, name=k, marker_color=c, text=[f"{x:.3f}" for x in v], textposition="outside", textfont=dict(size=20))
                 for (k, v), c in zip(res.items(), (BLUE, ORANGE))])
fig.update_layout(template="simple_white", width=900, height=500, font=FONT, barmode="group",
                  yaxis=dict(title="score on 61 test patients", range=[0, 1.2]), legend=dict(x=0.01, y=1.08, orientation="h"),
                  margin=dict(l=80, r=30, t=50, b=60))
fig.write_image(here / "heart_scores.png", scale=2)
