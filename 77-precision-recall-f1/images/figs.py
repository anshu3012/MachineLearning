"""Note 77 figures (Plotly): arithmetic mean vs F1 (harmonic mean); a 3-class confusion matrix with per-class precision and recall."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.metrics import classification_report, precision_score, recall_score

here = Path(__file__).parent
font = dict(family="Latin Modern Roman", size=16)

p = np.linspace(0, 1, 201)
fig = go.Figure()
for r, c in ((1.0, "#4C78A8"), (0.8, "#54A24B")):
    am = (p + r) / 2
    f1 = np.where(p + r > 0, 2 * p * r / (p + r), 0)
    fig.add_trace(go.Scatter(x=p, y=am, mode="lines", line=dict(color=c, width=3, dash="dash"), name=f"arithmetic mean, recall {r}"))
    fig.add_trace(go.Scatter(x=p, y=f1, mode="lines", line=dict(color=c, width=4), name=f"F1, recall {r}"))
for pp, r, txt in ((0.6, 1.0, "precision 0.6, recall 1:<br>mean 0.80, F1 0.75"), (0.0, 1.0, "precision 0, recall 1:<br>mean 0.50, F1 0")):
    f1 = 2 * pp * r / (pp + r)
    fig.add_trace(go.Scatter(x=[pp], y=[f1], mode="markers+text", marker=dict(size=11, color="#E45756"), text=[txt],
                             textposition="top right" if pp == 0 else "top left", textfont=dict(color="#E45756", size=14), showlegend=False))
fig.update_layout(template="simple_white", width=1000, height=480, font=font, margin=dict(l=60, r=20, t=30, b=60),
                  legend=dict(x=0.6, y=0.32, bgcolor="rgba(255,255,255,0.9)", font=dict(size=14)),
                  xaxis=dict(title="precision"), yaxis=dict(title="combined score", range=[-0.02, 1.02]))
fig.write_image(here / "f1_vs_mean.png", scale=2); fig.write_image(here / "f1_vs_mean.pdf")

labels = ["dog", "cat", "rabbit"]
cm = np.array([[25, 10, 5], [1, 30, 3], [3, 11, 20]])
y_true = np.repeat(np.repeat(np.arange(3), 3), cm.ravel())
y_pred = np.tile(np.arange(3), 9)[:0]  # placeholder, rebuilt below
y_true, y_pred = [], []
for i in range(3):
    for j in range(3):
        y_true += [i] * cm[i, j]; y_pred += [j] * cm[i, j]
prec, rec = precision_score(y_true, y_pred, average=None), recall_score(y_true, y_pred, average=None)
print(classification_report(y_true, y_pred, target_names=labels, digits=3))
z = np.zeros((4, 4)); text = [[""] * 4 for _ in range(4)]
for i in range(3):
    for j in range(3):
        z[i, j] = 2 if i == j else 1; text[i][j] = f"<b>{cm[i, j]}</b>"
    text[i][3] = f"total {cm[i].sum()}<br>recall {cm[i, i]}/{cm[i].sum()} = {rec[i]:.3f}"
    text[3][i] = f"total {cm[:, i].sum()}<br>precision {cm[i, i]}/{cm[:, i].sum()} = {prec[i]:.3f}"
text[3][3] = f"{cm.sum()} animals"
fig = go.Figure(go.Heatmap(z=z, x=[f"pred {l}" for l in labels] + ["row total"], y=[f"actual {l}" for l in labels] + ["column total"],
                           colorscale=[[0, "#F4F4F4"], [0.5, "#F8D3D3"], [1, "#D6ECD2"]], showscale=False, zmin=0, zmax=2,
                           text=text, texttemplate="%{text}", textfont=dict(size=14), xgap=2, ygap=2))
fig.update_yaxes(autorange="reversed")
fig.update_layout(template="simple_white", width=1000, height=520, font=font, margin=dict(l=130, r=20, t=20, b=60))
fig.write_image(here / "multiclass.png", scale=2); fig.write_image(here / "multiclass.pdf")
