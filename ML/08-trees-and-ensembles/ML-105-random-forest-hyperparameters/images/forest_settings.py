"""Decision surfaces of random forests on the concentric-circles data for several forest-level settings (Plotly)."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import figure, fit          # same data, model and surface code as the app

settings = [("(a) 1 tree", dict(n_estimators=1)),
            ("(b) 5 trees", dict(n_estimators=5)),
            ("(c) 50 trees", dict(n_estimators=50)),
            ("(d) 50 trees, 25 rows each", dict(n_estimators=50, max_samples=25)),
            ("(e) 50 trees, 200 rows each", dict(n_estimators=50, max_samples=200)),
            ("(f) 50 trees, both columns per split", dict(n_estimators=50, max_features=2))]
panels = []
for title, kw in settings:
    rf, acc = fit(**kw)
    panels.append((f"{title}: {acc:.3f}", rf))
print([t for t, _ in panels])
fig = figure(panels, cols=3)
fig.update_annotations(font_size=20)
fig.update_layout(width=1350, height=960, font=dict(family="Latin Modern Roman", size=18),
                  legend=dict(y=-0.03, font_size=20), margin=dict(t=60))
fig.write_image(HERE / "forest_settings.png", scale=2)
fig.write_image(HERE / "forest_settings.pdf")
