"""Decision surfaces on the moons data: one tree, then bagging, pasting, random subspaces, random patches (100 trees
each), and bagged KNN (Plotly)."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import figure, fit          # same data, models and surface code as the app

settings = [
    ("bagging<br>50 rows, with replacement", "decision tree", dict(max_samples=50)),
    ("pasting<br>50 rows, without replacement", "decision tree", dict(max_samples=50, bootstrap=False)),
    ("random subspaces<br>all rows, 1 of 2 columns", "decision tree",
     dict(max_samples=375, bootstrap=False, max_features=1, bootstrap_features=True)),
    ("random patches<br>50 rows, 1 of 2 columns", "decision tree", dict(max_samples=50, max_features=1, bootstrap_features=True)),
    ("bagged KNN<br>50 rows, with replacement", "KNN", dict(max_samples=50)),
]
(single, acc), _ = fit("decision tree")
panels = [(f"one fully grown tree<br>test accuracy {acc:.3f}", single)]
for title, base, kw in settings:
    _, (bag, a) = fit(base, n_estimators=100, **kw)
    panels.append((f"{title}: {a:.3f}", bag))
print([t.replace("<br>", " ") for t, _ in panels])
fig = figure(panels, cols=3)
fig.update_annotations(font_size=20)
fig.update_layout(width=1350, height=980, font=dict(family="Latin Modern Roman", size=18),
                  legend=dict(y=-0.03, font_size=20), margin=dict(t=90))
fig.write_image(HERE / "bagging_types_surfaces.png", scale=2)
fig.write_image(HERE / "bagging_types_surfaces.pdf")
