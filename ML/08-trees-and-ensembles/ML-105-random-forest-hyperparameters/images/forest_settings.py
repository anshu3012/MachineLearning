"""Decision surfaces of random forests on the concentric-circles data for several forest-level settings (Plotly).
Each panel's surface is the forest trained on the app's split; its title gives the mean test accuracy over the
Notebook's 20 random splits with the same settings, so the titles match the numbers in the Note's text."""
import sys
from pathlib import Path

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import X, figure, fit, y          # same data, model and surface code as the app

splits = [train_test_split(X, y, random_state=s) for s in range(20)]          # as in the Notebook


def score(**kw):
    """Mean test accuracy over the 20 splits (the Notebook's score())."""
    return round(float(np.mean([RandomForestClassifier(random_state=s, n_jobs=-1, **kw).fit(a, c).score(b, d)
                                for s, (a, b, c, d) in enumerate(splits)])), 3)


settings = [("(a) 1 tree", dict(n_estimators=1)),
            ("(b) 5 trees", dict(n_estimators=5)),
            ("(c) 100 trees", dict(n_estimators=100)),
            ("(d) 100 trees, 25 observations each", dict(n_estimators=100, max_samples=25)),
            ("(e) 100 trees, 200 observations each", dict(n_estimators=100, max_samples=200)),
            ("(f) 100 trees, both features per split", dict(n_estimators=100, max_features=2))]
panels, accs = [], []
for title, kw in settings:
    rf, _ = fit(**kw)
    acc = score(**kw)
    accs.append(acc)
    panels.append((f"{title}: {acc:.3f}", rf))
assert accs == [0.846, 0.868, 0.887, 0.827, 0.892, 0.884], accs       # the numbers quoted in section 3.3
print([t for t, _ in panels])
fig = figure(panels, cols=3)
fig.update_xaxes(title_text="feature 1", title_standoff=4, row=2)
fig.update_yaxes(title_text="feature 2", title_standoff=4, col=1)
fig.update_annotations(font_size=20)
fig.update_layout(width=1350, height=960, font=dict(family="Latin Modern Roman", size=18),
                  legend=dict(y=-0.07, font_size=20), margin=dict(t=60, l=50, b=60))
fig.write_image(HERE / "forest_settings.png", scale=2)
fig.write_image(HERE / "forest_settings.pdf")
