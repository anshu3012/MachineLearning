"""Section 4 Extra, ccp_alpha: forests of 100 pruned trees on the concentric-circles data. Each panel is the decision
surface on the app's split; titles give leaves per tree and the mean test accuracy over the Notebook's 20 splits.
Stronger pruning gives smaller trees, and from 0.01 on the forest loses the rings. (Plotly)"""
import sys
from pathlib import Path

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import X, X_train, figure, y, y_train  # noqa: E402  same data and surface code as the app

splits = [train_test_split(X, y, random_state=s) for s in range(20)]          # as in the Notebook
panels, leaves, accs = [], [], []
for a in [0.0, 0.002, 0.01, 0.05]:
    rf = RandomForestClassifier(n_estimators=100, ccp_alpha=a, random_state=42, n_jobs=-1).fit(X_train, y_train)
    lv = np.mean([t.get_n_leaves() for t in rf.estimators_])
    acc = np.mean([RandomForestClassifier(n_estimators=100, ccp_alpha=a, random_state=s, n_jobs=-1).fit(p, r).score(q, u)
                   for s, (p, q, r, u) in enumerate(splits)])
    leaves.append(round(lv, 1)); accs.append(round(acc, 3))
    panels.append((f"ccp_alpha = {a:g}: {lv:.1f} leaves, accuracy {acc:.3f}", rf))
assert leaves == [41.9, 39.2, 12.1, 3.9] and accs == [0.887, 0.886, 0.878, 0.776], (leaves, accs)
fig = figure(panels, cols=2)
fig.update_xaxes(title_text="feature 1", title_standoff=4, row=2)
fig.update_yaxes(title_text="feature 2", title_standoff=4, col=1)
fig.update_annotations(font_size=22)
fig.update_layout(width=1200, height=1000, font=dict(family="Latin Modern Roman", size=20), legend=dict(font_size=20, y=-0.08), margin=dict(l=50, b=70))
fig.write_image(HERE / "pruning.png", scale=2)
fig.write_image(HERE / "pruning.pdf")
