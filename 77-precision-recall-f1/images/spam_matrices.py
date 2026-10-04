"""The two equal-accuracy model pairs of Sections 2 and 3 as confusion matrices (Plotly heatmaps).
spam_matrices.png: spam filters A and B, 1,000 emails, accuracy 0.80. The outlined column, everything predicted spam,
is what precision reads: 100 of 200 for A (0.50), 100 of 110 for B (0.91).
cancer_matrices.png: cancer detectors A and B, 1,000 X-rays, accuracy 0.90. The outlined row, everyone who really has
cancer, is what recall reads: 150 of 160 for A (0.94), 100 of 160 for B (0.63)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import FONT, ORANGE

here = Path(__file__).parent


def draw(models, word, metric, acc, expect, out):
    """models: name -> (TP, FP, FN, TN). metric 'precision' outlines the predicted-positive column, 'recall' the actual-positive row."""
    score = {k: int(100 * tp / (tp + (fp if metric == "precision" else fn)) + 0.5) / 100 for k, (tp, fp, fn, tn) in models.items()}   # half up: 0.625 -> 0.63
    assert all((tp + tn) / 1000 == acc for tp, fp, fn, tn in models.values()) and list(score.values()) == expect
    fig = make_subplots(1, 2, horizontal_spacing=0.2, subplot_titles=[f"{k}: {metric} {v:.2f}" for k, v in score.items()])
    fig.update_annotations(font_size=22)
    for col, (k, (tp, fp, fn, tn)) in enumerate(models.items(), 1):
        M = np.array([[tn, fp], [fn, tp]])                       # rows: actual 0, 1; columns: predicted 0, 1
        lab = [[f"TN {tn}", f"FP {fp}"], [f"FN {fn}", f"TP {tp}"]]
        fig.add_trace(go.Heatmap(z=M[::-1], x=[f"predicted not {word}", f"predicted {word}"], y=[f"actual {word}", f"actual not {word}"],
                                 text=lab[::-1], texttemplate="%{text}", textfont=dict(size=24), colorscale="Blues", showscale=False,
                                 zmin=0, zmax=900), 1, col)
        box = dict(x0=0.5, x1=1.5, y0=-0.5, y1=1.5) if metric == "precision" else dict(x0=-0.5, x1=1.5, y0=-0.5, y1=0.5)
        fig.add_shape(type="rect", **box, line=dict(color=ORANGE, width=6), fillcolor="rgba(0,0,0,0)", opacity=1,
                      xref=f"x{col if col > 1 else ''}", yref=f"y{col if col > 1 else ''}")
    fig.update_layout(template="simple_white", width=1150, height=480, font=FONT, margin=dict(l=150, r=20, t=60, b=60))
    fig.write_image(here / out, scale=2)


draw({"Model A": (100, 100, 100, 700), "Model B": (100, 10, 190, 700)}, "spam", "precision", 0.8, [0.5, 0.91], "spam_matrices.png")
draw({"Model A": (150, 90, 10, 750), "Model B": (100, 40, 60, 800)}, "cancer", "recall", 0.9, [0.94, 0.63], "cancer_matrices.png")
