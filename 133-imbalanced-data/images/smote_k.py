"""SMOTE's dependence on k (section 7.3, disadvantage 3), on the Note's training data (299 majority, 21 minority).
The 278 new minority points for k = 1, 5 and 20 neighbours. k = 1: the new points sit on a few short segments.
k = 20: every minority point is a neighbour of every other, and new points spread across the majority. Plotly."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from imblearn.over_sampling import SMOTE
from plotly.subplots import make_subplots
from imb import BLUE, FONT, ORANGE, RED, data

here = Path(__file__).parent
Xtr, _, ytr, _ = data()
KS = [1, 5, 20]
fig = make_subplots(1, 3, shared_yaxes=True, horizontal_spacing=0.03,
                    subplot_titles=[f"k = {k}" + ("  (the default)" if k == 5 else "") for k in KS])
for c, k in enumerate(KS, 1):
    Xs, ys = SMOTE(k_neighbors=k, random_state=42).fit_resample(Xtr, ytr)
    new = Xs[len(Xtr):]
    assert len(new) == 278
    for pts, col, name, size, op in ((Xtr[ytr == 1], BLUE, "majority (class 1)", 5, 0.35), (new, ORANGE, "new SMOTE points", 6, 0.8),
                                     (Xtr[ytr == 0], RED, "minority (class 0)", 9, 1.0)):
        fig.add_trace(go.Scatter(x=pts[:, 0], y=pts[:, 1], mode="markers", name=name, showlegend=c == 1,
                                 marker=dict(size=size, color=col, opacity=op, line=dict(color="black", width=1 if col == RED else 0))), 1, c)
    fig.update_xaxes(title="feature 1", row=1, col=c)
fig.update_yaxes(title="feature 2", row=1, col=1)
fig.update_annotations(font_size=21)
fig.update_layout(template="simple_white", width=1200, height=470, font=FONT, margin=dict(l=60, r=20, t=50, b=110),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.22, font_size=18))
fig.write_image(here / "smote_k.png", scale=2)
fig.write_image(here / "smote_k.pdf")
