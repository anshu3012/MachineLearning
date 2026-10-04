"""Note 78 stills (Plotly), from the logistic regression probabilities in lr_probs.csv (154 Pima test patients).
rates.png (Section 3): at five thresholds, the 54 diabetic patients split into caught/missed (caught share = TPR)
  and the 100 healthy patients into flagged/cleared (flagged share = FPR).
pairs.png (Section 5): every (diabetic, healthy) pair, 54 x 100; green where the diabetic patient gets the higher
  probability. The green share is the AUC.
Run: python rates_pairs.py"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.metrics import roc_auc_score

HERE = Path(__file__).parent
RED, BLUE, GREEN, GREY = "#E45756", "#4C78A8", "#54A24B", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=20)
d = np.loadtxt(HERE / "lr_probs.csv", delimiter=",", skiprows=1)
Y, P = d[:, 0].astype(int), d[:, 1]
pos, neg = P[Y == 1], P[Y == 0]
assert len(pos) == 54 and len(neg) == 100
T = [0.1, 0.3, 0.5, 0.7, 0.9]
TP = np.array([(pos >= t).sum() for t in T]); FP = np.array([(neg >= t).sum() for t in T])
assert TP.tolist() == [53, 44, 28, 20, 5] and FP.tolist() == [66, 30, 18, 8, 0]   # the Note's table

fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1,
                    subplot_titles=("54 patients with diabetes", "100 patients without diabetes"))
xs = [f"{t}" for t in T]
fig.add_trace(go.Bar(x=xs, y=TP / 54, marker_color=RED, name="caught (TP)"), 1, 1)
fig.add_trace(go.Bar(x=xs, y=1 - TP / 54, marker_color="#F6C4C4", name="missed (FN)"), 1, 1)
fig.add_trace(go.Bar(x=xs, y=FP / 100, marker_color=BLUE, name="wrongly flagged (FP)"), 1, 2)
fig.add_trace(go.Bar(x=xs, y=1 - FP / 100, marker_color="#D3E0EE", name="correctly cleared (TN)"), 1, 2)
fig.update_layout(template="simple_white", width=1150, height=560, font=FONT, barmode="stack",
                  margin=dict(l=70, r=20, t=50, b=170), legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.3))
fig.update_yaxes(range=[0, 1], title="share of the group", row=1, col=1)
fig.update_yaxes(range=[0, 1], row=1, col=2)
fig.update_xaxes(tickvals=xs, ticktext=[f"{x}<br><b>TPR {v:.2f}</b>" for x, v in zip(xs, TP / 54)], tickangle=0, tickfont=dict(size=18), title="threshold", row=1, col=1)
fig.update_xaxes(tickvals=xs, ticktext=[f"{x}<br><b>FPR {v:.2f}</b>" for x, v in zip(xs, FP / 100)], tickangle=0, tickfont=dict(size=18), title="threshold", row=1, col=2)
fig.update_annotations(font_size=22)
fig.write_image(HERE / "rates.png", scale=2)

ps, ns = np.sort(pos)[::-1], np.sort(neg)
win = (ps[:, None] > ns[None, :]) + 0.5 * (ps[:, None] == ns[None, :])
auc = win.mean()
assert abs(auc - roc_auc_score(Y, P)) < 1e-12 and round(auc, 3) == 0.823
fig = go.Figure(go.Heatmap(z=win, x=np.arange(1, 101), y=np.arange(1, 55), showscale=False, zmin=0, zmax=1,
                           colorscale=[[0, "#F6C4C4"], [0.5, "#EEEEEE"], [1, "#BFE0B8"]], xgap=0.5, ygap=0.5))
fig.update_layout(template="simple_white", width=1100, height=640, font=FONT, margin=dict(l=80, r=20, t=70, b=70),
                  title=dict(text=f"green: the diabetic patient gets the higher probability, {int(win.sum()):,} of 5,400 pairs = AUC {auc:.3f}",
                             x=0.5, font=dict(size=22)),
                  xaxis=dict(title="healthy patients, lowest probability → highest"),
                  yaxis=dict(title="diabetic patients, highest → lowest", autorange="reversed"))
fig.write_image(HERE / "pairs.png", scale=2)
print("pairs won", win.sum())
