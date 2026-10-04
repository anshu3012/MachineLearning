"""Decision surfaces on the concentric-circles data: three base models, then hard and soft voting (Plotly)."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import figure, run          # same data, models and surface code as the app

names = ["logistic regression", "Gaussian naive Bayes", "random forest"]
hard, X_train, y_train = run("concentric circles", names, "hard")
soft, _, _ = run("concentric circles", names, "soft")
results = hard[1:] + [hard[0], soft[0]]
print([(t, round(a, 3)) for t, _, a in results])
fig = figure(results, X_train, y_train)
fig.update_annotations(font_size=21)
fig.update_layout(width=1300, height=900, font=dict(family="Latin Modern Roman", size=18),
                  legend=dict(x=0.84, y=0.25, xanchor="center", orientation="v", font_size=20))
fig.add_annotation(x=0.84, y=0.4, xref="paper", yref="paper", showarrow=False, font=dict(size=19),
                   text="titles: model and<br>test accuracy")
fig.write_image(HERE / "hard_soft_surfaces.png", scale=2)
fig.write_image(HERE / "hard_soft_surfaces.pdf")
