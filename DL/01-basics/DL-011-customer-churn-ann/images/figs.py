"""Training curves and confusion matrices (Plotly) from results.json, which the Notebook writes after training.
Run: python figs.py -> curves.png/.pdf, confusion.png/.pdf."""
import json
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
r = json.loads((here / "results.json").read_text())
font = dict(family="Latin Modern Roman", size=18)
TRAIN, VAL = "#4C78A8", "#F58518"

# training curves of the second network: loss (left) and accuracy (right)
h = r["history"]
ep = list(range(1, len(h["loss"]) + 1))
fig = make_subplots(1, 2, horizontal_spacing=0.1, subplot_titles=["Loss (binary cross-entropy)", "Accuracy"])
for col, key in [(1, "loss"), (2, "accuracy")]:
    fig.add_scatter(x=ep, y=h[key], name="training", line=dict(color=TRAIN, width=3), showlegend=col == 1, row=1, col=col)
    fig.add_scatter(x=ep, y=h["val_" + key], name="validation", line=dict(color=VAL, width=3), showlegend=col == 1,
                    row=1, col=col)
fig.update_xaxes(title="epoch")
fig.update_layout(template="simple_white", width=1100, height=430, font=font, margin=dict(l=60, r=20, t=50, b=60),
                  legend=dict(x=0.25, y=0.95))
fig.update_annotations(font=dict(size=20))
fig.write_image(here / "curves.png", scale=2)
fig.write_image(here / "curves.pdf")

# confusion matrices on the 2,000 test customers: first network vs second network
labels_x = ["predicted 0<br>(stays)", "predicted 1<br>(leaves)"]
labels_y = ["actual 0<br>(stays)", "actual 1<br>(leaves)"]
fig = make_subplots(1, 2, horizontal_spacing=0.16,
                    subplot_titles=[f"First network: accuracy {r['acc1']:.1%}", f"Second network: accuracy {r['acc2']:.1%}"])
names = [["TN", "FP"], ["FN", "TP"]]
for k, cm in enumerate([r["cm1"], r["cm"]]):
    fig.add_trace(go.Heatmap(z=[[1, 0], [0, 1]], x=labels_x, y=labels_y, showscale=False, zmin=0, zmax=1,
                             colorscale=[[0, "#F8D3D3"], [1, "#D6ECD2"]],
                             text=[[f"{names[i][j]}<br><b>{cm[i][j]}</b>" for j in range(2)] for i in range(2)],
                             texttemplate="%{text}", textfont=dict(size=24)), 1, k + 1)
fig.update_yaxes(autorange="reversed")
fig.update_layout(template="simple_white", width=1100, height=450, font=font, margin=dict(l=110, r=20, t=50, b=60))
fig.update_annotations(font=dict(size=20))
fig.write_image(here / "confusion.png", scale=2)
fig.write_image(here / "confusion.pdf")
print("done")
