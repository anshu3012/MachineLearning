"""KNN on imbalanced classes, the Notebook's test (Plotly): make_classification with 98% class 0 and 2% class 1
(5,000 observations, 10 features, class_sep 0.5, random_state 0), stratified 30% test split, k = 5. The confusion
counts: almost every test observation is predicted as the common class; only 1 of the 30 rare ones is found."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score, confusion_matrix, recall_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from gifkit import FONT

here = Path(__file__).parent
Xi, yi = make_classification(n_samples=5000, n_features=10, weights=[0.98], flip_y=0, class_sep=0.5, random_state=0)
a, b, c, d = train_test_split(Xi, yi, test_size=0.3, stratify=yi, random_state=0)
p = KNeighborsClassifier(n_neighbors=5).fit(a, c).predict(b)
cm = confusion_matrix(d, p)
assert d.sum() == 30 and round(accuracy_score(d, p), 2) == 0.98 and round(recall_score(d, p), 2) == 0.03
lab = [[f"{cm[0, 0]:,}<br>common, predicted common", f"{cm[0, 1]}<br>common, predicted rare"],
       [f"{cm[1, 0]}<br>rare, predicted common", f"{cm[1, 1]}<br>rare, found"]]
fig = go.Figure(go.Heatmap(z=np.log10(cm[::-1] + 1), x=["predicted common (0)", "predicted rare (1)"], y=["actual rare (1)", "actual common (0)"],
                           text=lab[::-1], texttemplate="%{text}", textfont=dict(size=20), colorscale="Blues", showscale=False))
fig.update_layout(template="simple_white", width=900, height=480, font=FONT,
                  title=dict(text=f"accuracy {accuracy_score(d, p):.2f}, but recall of the rare class {recall_score(d, p):.2f}", x=0.5),
                  margin=dict(l=150, r=20, t=70, b=60))
fig.write_image(here / "imbalanced.png", scale=2)
