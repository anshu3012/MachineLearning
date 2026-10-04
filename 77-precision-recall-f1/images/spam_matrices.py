"""Precision on the two spam filters of Section 2 (Plotly heatmaps): the confusion matrices of model A and model B,
each 1,000 emails, accuracy 0.80. The outlined column, everything predicted spam, is what precision reads: 100 of
200 for A (0.50), 100 of 110 for B (0.91)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import FONT, ORANGE

here = Path(__file__).parent
models = {"Model A": (100, 100, 100, 700), "Model B": (100, 10, 190, 700)}
prec = {k: tp / (tp + fp) for k, (tp, fp, fn, tn) in models.items()}
assert all((tp + tn) / 1000 == 0.8 for tp, fp, fn, tn in models.values()) and round(prec["Model A"], 2) == 0.5 and round(prec["Model B"], 2) == 0.91
fig = make_subplots(1, 2, horizontal_spacing=0.2, subplot_titles=[f"{k}: precision {v:.2f}" for k, v in prec.items()])
fig.update_annotations(font_size=22)
for col, (k, (tp, fp, fn, tn)) in enumerate(models.items(), 1):
    M = np.array([[tn, fp], [fn, tp]])                       # rows: actual 0, 1; columns: predicted 0, 1
    lab = [[f"TN {tn}", f"FP {fp}"], [f"FN {fn}", f"TP {tp}"]]
    fig.add_trace(go.Heatmap(z=M[::-1], x=["predicted not spam", "predicted spam"], y=["actual spam", "actual not spam"],
                             text=lab[::-1], texttemplate="%{text}", textfont=dict(size=24), colorscale="Blues", showscale=False,
                             zmin=0, zmax=900), 1, col)
    fig.add_shape(type="rect", x0=0.5, x1=1.5, y0=-0.5, y1=1.5, line=dict(color=ORANGE, width=6), fillcolor="rgba(0,0,0,0)", opacity=1,
                  xref=f"x{col if col > 1 else ''}", yref=f"y{col if col > 1 else ''}")
fig.update_layout(template="simple_white", width=1150, height=480, font=FONT, margin=dict(l=130, r=20, t=60, b=60))
fig.write_image(here / "spam_matrices.png", scale=2)
