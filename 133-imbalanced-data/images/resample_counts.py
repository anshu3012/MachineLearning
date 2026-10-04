"""Sections 5 to 7: the training set's class counts before and after each resampler (299/21 -> 21/21, 299/299, 299/299
with 278 synthetic points). Plotly."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from imb import data, undersample, oversample, smote, BLUE, RED, ORANGE, FONT

here = Path(__file__).parent
Xtr, Xte, ytr, yte = data()
yu, yo = undersample(Xtr, ytr)[1], oversample(Xtr, ytr)[1]
Xs, ys, new = smote(Xtr, ytr)
rows = [("original", np.bincount(ytr), 0), ("random undersampling", np.bincount(yu), 0),
        ("random oversampling", np.bincount(yo), 0), ("SMOTE", np.bincount(ys), len(new))]
assert [r[1].tolist() for r in rows] == [[21, 299], [21, 21], [299, 299], [299, 299]] and len(new) == 278
labels = [r[0] for r in rows]
fig = go.Figure()
fig.add_bar(x=labels, y=[r[1][1] for r in rows], name="class 1 (majority)", marker_color=BLUE, text=[r[1][1] for r in rows],
            textposition="outside", offsetgroup=0)
fig.add_bar(x=labels, y=[r[1][0] - r[2] for r in rows], name="class 0, real", marker_color=RED, offsetgroup=1,
            text=[str(r[1][0]) if not r[2] else "" for r in rows], textposition="outside")
fig.add_bar(x=labels, y=[r[2] for r in rows], name="class 0, synthetic (SMOTE)", marker_color=ORANGE, offsetgroup=1,
            base=[r[1][0] - r[2] for r in rows], text=[f"21 real + {r[2]} new" if r[2] else "" for r in rows], textposition="outside")
fig.update_layout(template="simple_white", width=1000, height=440, font=FONT, barmode="group",
                  yaxis=dict(title="training observations", range=[0, 340]), legend=dict(orientation="h", x=0.5, xanchor="center", y=1.12),
                  margin=dict(l=70, r=20, t=60, b=50))
fig.write_image(here / "resample_counts.png", scale=2)
fig.write_image(here / "resample_counts.pdf")
