"""Note ML-077 figures (Plotly): predicted probabilities by class with three thresholds; ROC curve with thresholds; two models' ROC and AUC."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

here = Path(__file__).parent
font = dict(family="Latin Modern Roman", size=16)
df = pd.read_csv(here.parent / "data" / "diabetes.csv")
X, y = df.drop(columns="Outcome"), df["Outcome"]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
lr = make_pipeline(StandardScaler(), LogisticRegression()).fit(Xtr, ytr)
p = lr.predict_proba(Xte)[:, 1]
np.savetxt(here / "lr_probs.csv", np.c_[yte.values, p], delimiter=",", header="y,p", comments="", fmt="%.6f")

# 1. probabilities by class
fig = go.Figure()
fig.add_trace(go.Histogram(x=p[yte.values == 0], xbins=dict(start=0, end=1, size=0.05), name="no diabetes (0)",
                           marker_color="#4C78A8", opacity=0.7))
fig.add_trace(go.Histogram(x=p[yte.values == 1], xbins=dict(start=0, end=1, size=0.05), name="diabetes (1)",
                           marker_color="#E45756", opacity=0.7))
for t, c in ((0.3, "#54A24B"), (0.5, "black"), (0.7, "#F58518")):
    fig.add_trace(go.Scatter(x=[t, t], y=[0, 30], mode="lines", line=dict(color=c, width=3, dash="dash"), name=f"threshold {t}"))
fig.update_layout(template="simple_white", width=1000, height=440, font=font, barmode="overlay", margin=dict(l=60, r=20, t=30, b=60),
                  legend=dict(x=0.76, y=0.98, bgcolor="rgba(255,255,255,0.9)"), xaxis=dict(title="predicted probability of diabetes", range=[0, 1]),
                  yaxis=dict(title="number of test patients", range=[0, 30]))
fig.write_image(here / "probabilities.png", scale=2); fig.write_image(here / "probabilities.pdf")

# 2. ROC with thresholds, and two models
fpr, tpr, thr = roc_curve(yte, p)
dt = DecisionTreeClassifier(max_depth=3, random_state=0).fit(Xtr, ytr)
pd_ = dt.predict_proba(Xte)[:, 1]
fpr2, tpr2, _ = roc_curve(yte, pd_)
auc1, auc2 = roc_auc_score(yte, p), roc_auc_score(yte, pd_)
best = np.hypot(fpr, 1 - tpr).argmin()
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1,
                    subplot_titles=("Logistic regression: one point per threshold", "Comparing models by the area under the curve"))
for col in (1, 2):
    fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", line=dict(color="#BBBBBB", width=2, dash="dash"),
                             name="random guessing (AUC 0.5)", showlegend=(col == 2)), 1, col)
fig.add_trace(go.Scatter(x=fpr, y=tpr, mode="lines", line=dict(color="#4C78A8", width=4), showlegend=False), 1, 1)
for t in (0.1, 0.3, 0.5, 0.7, 0.9):
    pred = p >= t
    tp_ = (pred & (yte.values == 1)).sum(); fp_ = (pred & (yte.values == 0)).sum()
    x0, y0 = fp_ / (yte.values == 0).sum(), tp_ / (yte.values == 1).sum()
    fig.add_trace(go.Scatter(x=[x0], y=[y0], mode="markers+text", marker=dict(size=11, color="#F58518"), text=[f"t = {t}"],
                             textposition="bottom right", textfont=dict(color="#F58518", size=14), showlegend=False), 1, 1)
fig.add_trace(go.Scatter(x=[fpr[best]], y=[tpr[best]], mode="markers", marker=dict(size=16, color="#E45756", symbol="star"),
                         showlegend=False), 1, 1)
fig.add_annotation(x=fpr[best] + 0.06, y=tpr[best] - 0.12, text=f"closest to (0, 1): t = {thr[best]:.3f}", showarrow=False, bgcolor="white",
                   xanchor="left", font=dict(color="#E45756", size=14), row=1, col=1)
fig.add_trace(go.Scatter(x=[0], y=[1], mode="markers", marker=dict(size=10, color="black", symbol="x"), showlegend=False), 1, 1)
fig.add_trace(go.Scatter(x=fpr, y=tpr, mode="lines", line=dict(color="#4C78A8", width=4), fill="tozeroy",
                         fillcolor="rgba(76,120,168,0.15)", name=f"logistic regression: AUC {auc1:.3f}"), 1, 2)
fig.add_trace(go.Scatter(x=fpr2, y=tpr2, mode="lines", line=dict(color="#54A24B", width=4), name=f"decision tree (depth 3): AUC {auc2:.3f}"), 1, 2)
fig.update_xaxes(title="false positive rate (cost)", range=[-0.02, 1.02])
fig.update_yaxes(title="true positive rate (benefit)", range=[-0.02, 1.05], row=1, col=1)
fig.update_yaxes(range=[-0.02, 1.05], row=1, col=2)
fig.update_layout(template="simple_white", width=1150, height=540, font=font, margin=dict(l=70, r=20, t=50, b=110),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2))
fig.write_image(here / "roc.png", scale=2); fig.write_image(here / "roc.pdf")
print("auc", auc1, auc2, "best", thr[best], fpr[best], tpr[best])
