"""What predict does on the 40 test students (random_state = 2): each prediction is the height of the best-fit line at
the student's CGPA; the grey segments are the gaps to the real packages. The first test student: CGPA 8.58, real 4.10,
predicted 3.89."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "placement.csv")
X, y = df.iloc[:, 0:1], df.iloc[:, -1]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=2)
lr = LinearRegression().fit(Xtr, ytr)
p = lr.predict(Xte)
assert len(Xte) == 40 and round(Xte.iloc[0, 0], 2) == 8.58 and round(p[0], 2) == 3.89 and round(lr.coef_[0], 3) == 0.558
x = Xte.iloc[:, 0].values
fig = go.Figure()
g = np.array([4, 10])
fig.add_scatter(x=g, y=lr.predict(pd.DataFrame({df.columns[0]: g})), mode="lines", line=dict(color="#F58518", width=4),
                name="best-fit line (trained on 160 students)")
xs, ys = [], []
for a, r, q in zip(x, yte.values, p):
    xs += [a, a, None]; ys += [r, q, None]
fig.add_scatter(x=xs, y=ys, mode="lines", line=dict(color="#9a9a9a", width=1.5), name="gap: real minus predicted")
fig.add_scatter(x=x, y=yte, mode="markers", marker=dict(size=9, color="#4C78A8"), name="40 test students (real package)")
fig.add_scatter(x=x, y=p, mode="markers", marker=dict(size=7, color="#F58518", symbol="diamond"), name="predicted package")
fig.add_annotation(x=x[0], y=p[0], text="CGPA 8.58: real 4.10, predicted 3.89", ax=-150, ay=-50, font=dict(size=17), arrowwidth=2)
fig.update_layout(template="simple_white", width=1100, height=560, font=dict(family="Latin Modern Roman", size=18),
                  title=dict(text="predict reads the line at each test student's CGPA", x=0.5),
                  xaxis=dict(title="CGPA"), yaxis=dict(title="package (LPA)"),
                  legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.85)"), margin=dict(l=80, r=30, t=70, b=70))
fig.write_image(here / "test_predictions.png", scale=2)
fig.write_image(here / "test_predictions.pdf")
