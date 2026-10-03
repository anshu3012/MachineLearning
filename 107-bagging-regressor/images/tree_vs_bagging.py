"""One fully grown regression tree against a bagging regressor of 50 trees (25 rows each) on noisy data (Plotly)."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import figure, fit          # same data and models as the app

(single, r1), (bag, r2) = fit("decision tree", n_estimators=50, max_samples=25, bootstrap=True)
print(round(r1, 3), round(r2, 3))
fig = figure([(f"(a) one fully grown tree: test R² {r1:.2f}", single, "#E45756"),
              (f"(b) bagging, 50 trees of 25 rows: test R² {r2:.2f}", bag, "#4C78A8")])
fig.update_annotations(font_size=21)
fig.update_layout(width=1300, height=560, font=dict(family="Latin Modern Roman", size=19),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2), margin=dict(b=110))
fig.write_image(HERE / "tree_vs_bagging.png", scale=2)
fig.write_image(HERE / "tree_vs_bagging.pdf")
