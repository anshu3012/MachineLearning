"""Admission figures (Plotly) from results.json, which the Notebook writes after training.
Run: python figs.py -> curves.png, pred_vs_actual.png (each also .pdf)."""
import json
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
r = json.loads((here / "results.json").read_text())
font = dict(family="Latin Modern Roman", size=18)
TRAIN, VAL = "#4C78A8", "#F58518"

# training curves: first network (10 epochs) and second network (100 epochs)
fig = make_subplots(1, 2, horizontal_spacing=0.1,
                    subplot_titles=["First network: 7-7-1, 10 epochs", "Second network: 7-7-7-1, 100 epochs"])
for col, key in [(1, "history1"), (2, "history")]:
    h = r[key]
    ep = list(range(1, len(h["loss"]) + 1))
    fig.add_scatter(x=ep, y=h["loss"], name="training", line=dict(color=TRAIN, width=3), showlegend=col == 1, row=1, col=col)
    fig.add_scatter(x=ep, y=h["val_loss"], name="validation", line=dict(color=VAL, width=3), showlegend=col == 1,
                    row=1, col=col)
fig.update_xaxes(title="epoch")
fig.update_yaxes(title="loss (mean squared error)", row=1, col=1)
fig.update_yaxes(range=[0, 0.45])
fig.update_layout(template="simple_white", width=1100, height=430, font=font, margin=dict(l=80, r=20, t=50, b=60),
                  legend=dict(x=0.3, y=0.95))
fig.update_annotations(font=dict(size=20))
fig.write_image(here / "curves.png", scale=2)
fig.write_image(here / "curves.pdf")

# predicted vs actual chance of admit on the 100 test students
fig = make_subplots(1, 2, horizontal_spacing=0.1,
                    subplot_titles=[f"First network: R² = {r['r2_1']:.2f}", f"Second network: R² = {r['r2_2']:.2f}"])
for col, key in [(1, "y_pred1"), (2, "y_pred2")]:
    fig.add_scatter(x=[0.15, 1.05], y=[0.15, 1.05], mode="lines", line=dict(color="#6B6B6B", dash="dash", width=2),
                    name="perfect prediction", showlegend=col == 1, row=1, col=col)
    fig.add_scatter(x=r["y_test"], y=r[key], mode="markers", name="test student", showlegend=col == 1,
                    marker=dict(color=TRAIN, size=9, line=dict(color="white", width=0.5)), row=1, col=col)
fig.update_xaxes(title="actual chance of admit", range=[0.15, 1.05])
fig.update_yaxes(range=[0.15, 1.05], scaleanchor="x")
fig.update_yaxes(title="predicted", row=1, col=1)
fig.update_yaxes(scaleanchor="x2", row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=560, font=font, margin=dict(l=80, r=20, t=50, b=60),
                  legend=dict(x=0.02, y=0.98))
fig.update_annotations(font=dict(size=20))
fig.write_image(here / "pred_vs_actual.png", scale=2)
fig.write_image(here / "pred_vs_actual.pdf")
print("done")
