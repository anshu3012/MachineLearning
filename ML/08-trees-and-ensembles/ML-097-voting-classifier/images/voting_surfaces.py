"""Section 2 demo (Plotly): logistic regression, Gaussian naive Bayes and their hard vote on the concentric circles."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import figure, run          # same data, models and surface code as the app

res, X_train, y_train = run("concentric circles", ["logistic regression", "Gaussian naive Bayes"], "hard")
res = res[1:] + res[:1]
acc = [round(a, 2) for _, _, a in res]
print([(t, a) for (t, _, _), a in zip(res, acc)])
assert acc == [0.53, 0.60, 0.63]                                  # section 2 table
import numpy as np  # noqa: E402
from app import grid  # noqa: E402
gx, gy = grid(X_train)
P = np.c_[[a.ravel() for a in np.meshgrid(gx, gy)]].T
vote, m1, m2 = (m.predict(P) for _, m, _ in [res[2], res[0], res[1]])
assert (vote == (m1 & m2)).all()          # the text: class 1 only where both models say 1 (a tie goes to class 0)
fig = figure(res, X_train, y_train, cols=3)
fig.update_annotations(font_size=22)
fig.update_layout(width=1300, height=520, font=dict(family="Latin Modern Roman", size=18),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.05, font_size=20))
fig.write_image(HERE / "voting_surfaces.png", scale=2)
fig.write_image(HERE / "voting_surfaces.pdf")
