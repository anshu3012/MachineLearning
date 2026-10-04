"""class_weight on imbalanced breast-cancer data (Plotly): all 357 benign + 20 random malignant (5% positive),
half for training, half for testing, 30 random draws (the notebook's experiment). Recall and precision on malignant."""
from pathlib import Path
import warnings
import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
warnings.simplefilter("ignore")

here = Path(__file__).parent
Xb, yb = load_breast_cancer(return_X_y=True)
yb = 1 - yb                                                   # 1 = malignant, the rare class here
res = {None: [], "balanced": []}
for s in range(30):
    rng = np.random.default_rng(s)
    pos = rng.choice(np.where(yb == 1)[0], 20, replace=False)
    idx = np.r_[np.where(yb == 0)[0], pos]
    a, b, c, d = train_test_split(Xb[idx], yb[idx], test_size=0.5, random_state=s, stratify=yb[idx])
    for cw in res:
        p = make_pipeline(StandardScaler(), LogisticRegression(class_weight=cw)).fit(a, c).predict(b)
        res[cw].append((recall_score(d, p), precision_score(d, p, zero_division=0)))
m = {cw: np.mean(v, axis=0) for cw, v in res.items()}
assert np.allclose(m[None], [0.770, 0.989], atol=5e-4) and np.allclose(m["balanced"], [0.850, 0.872], atol=5e-4), m

fig = go.Figure()
for cw, name, col in ((None, "class_weight = None", "#6B6B6B"), ("balanced", 'class_weight = "balanced"', "#F58518")):
    fig.add_trace(go.Bar(x=["recall<br>(malignant tumours found)", "precision<br>(alarms that are right)"], y=m[cw],
                         name=name, marker_color=col, text=[f"{v:.3f}" for v in m[cw]], textposition="outside"))
fig.update_layout(template="simple_white", barmode="group", width=900, height=520,
                  font=dict(family="Latin Modern Roman", size=22), yaxis=dict(range=[0, 1.12], title="average over 30 draws"),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=1.12), margin=dict(l=80, r=20, t=60, b=60))
fig.write_image(here / "class_weight.png", scale=2)
