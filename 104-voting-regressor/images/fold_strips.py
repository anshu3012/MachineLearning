"""Why the folds are shuffled (section 4.5): the 506 Boston rows in file order. Top strip: the towns, as
alternating grey bands (rows of one town sit together). Middle: the test rows of one of 10 folds cut in order,
one solid block of whole towns. Bottom: the test rows of one of 10 shuffled folds, spread over all towns.
(Plotly)"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.model_selection import KFold

HERE = Path(__file__).parent
bc = pd.read_csv(HERE.parent / "data" / "boston_corrected.txt", sep="\t", skiprows=8, encoding="latin1")
town = bc["TOWN#"].to_numpy()
n = len(town)
assert n == 506 and (np.diff(town) >= 0).all()                     # rows are grouped town by town
band = (np.cumsum(np.r_[0, np.diff(town) != 0]) % 2).astype(float)
FOLD = 4                                                            # the fifth of the 10 folds
ordered = list(KFold(10).split(np.zeros(n)))[FOLD][1]
shuffled = list(KFold(10, shuffle=True, random_state=0).split(np.zeros(n)))[FOLD][1]
unseen = lambda te: int((~np.isin(town[te], town[np.setdiff1d(np.arange(n), te)])).sum())
print("test rows from towns absent in training:", unseen(ordered), "of", len(ordered), "in order;",
      unseen(shuffled), "of", len(shuffled), "shuffled")
mask = lambda te: np.isin(np.arange(n), te).astype(float)
rows = [("towns (one band per town)", band, [[0, "#DDDDDD"], [1, "#8C8C8C"]]),
        (f"folds in order: the test rows of fold {FOLD + 1}", mask(ordered), [[0, "#F2F2F2"], [1, "#F58518"]]),
        (f"shuffled folds: the test rows of fold {FOLD + 1}", mask(shuffled), [[0, "#F2F2F2"], [1, "#4C78A8"]])]
fig = make_subplots(rows=3, cols=1, vertical_spacing=0.16, subplot_titles=[r[0] for r in rows])
for i, (_, z, scale) in enumerate(rows, 1):
    fig.add_trace(go.Heatmap(z=[z], x=np.arange(1, n + 1), colorscale=scale, showscale=False, zmin=0, zmax=1), i, 1)
    fig.update_yaxes(visible=False, row=i, col=1)
fig.update_xaxes(title="row of the data file", row=3, col=1)
fig.update_layout(template="simple_white", width=1200, height=560, margin=dict(l=20, r=20, t=50, b=70),
                  font=dict(family="Latin Modern Roman", size=22, color="black"))
fig.update_annotations(font_size=24)
fig.write_image(HERE / "fold_strips.png", scale=2)
fig.write_image(HERE / "fold_strips.pdf")
