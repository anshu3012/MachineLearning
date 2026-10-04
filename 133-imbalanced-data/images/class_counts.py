"""Section 2.1: observations per class in the training and test sets of the Note's dataset (299 and 21, 73 and 7).
Plotly."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from imb import data, BLUE, RED, FONT

here = Path(__file__).parent
Xtr, Xte, ytr, yte = data()
tr, te = np.bincount(ytr), np.bincount(yte)
assert tr.tolist() == [21, 299] and te.tolist() == [7, 73]
fig = go.Figure()
for cls, col, name in ((1, BLUE, "class 1 (majority)"), (0, RED, "class 0 (minority)")):
    vals = [tr[cls], te[cls]]
    fig.add_bar(x=["training set (320)", "test set (80)"], y=vals, name=name, marker_color=col, text=vals, textposition="outside")
fig.update_layout(template="simple_white", width=900, height=420, font=FONT, barmode="group",
                  yaxis=dict(title="observations", range=[0, 340]), legend=dict(x=0.6, y=0.98), margin=dict(l=70, r=20, t=20, b=50))
fig.write_image(here / "class_counts.png", scale=2)
fig.write_image(here / "class_counts.pdf")
