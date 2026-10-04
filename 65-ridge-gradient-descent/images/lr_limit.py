"""What the from-scratch code produces at two learning rates (Plotly), diabetes data (test size 0.2, random state 4),
alpha 0.001, 100 epochs. The largest coefficient size per epoch: with 0.005 it settles; with 0.006, just above the
limit 2/353 = 0.0057, every step overshoots and the coefficients grow to about 15,000."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from gifkit import BLUE, FONT, RED

here = Path(__file__).parent
X, y = load_diabetes(return_X_y=True)
Xtr, _, ytr, _ = train_test_split(X, y, test_size=0.2, random_state=4)
Xa = np.insert(Xtr, 0, 1, axis=1)
I = np.identity(Xa.shape[1]); I[0, 0] = 0
H = Xa.T @ Xa + 0.001 * I
assert round(np.linalg.eigvalsh(H).max()) == 353


def run(lr, epochs=100):
    w = np.insert(np.ones(Xa.shape[1] - 1), 0, 0.0)
    out = []
    for _ in range(epochs):
        w = w - lr * (Xa.T @ Xa @ w - Xa.T @ ytr + 0.001 * I @ w)
        out.append(np.abs(w[1:]).max())
    return np.array(out)


a, b = run(0.005), run(0.006)
assert a[-1] < 1000 and round(b[-1], -3) == 15000, b[-1]
e = np.arange(1, 101)
fig = go.Figure([go.Scatter(x=e, y=a, mode="lines", line=dict(color=BLUE, width=4), name="learning rate 0.005 (below 2/353)"),
                 go.Scatter(x=e, y=b, mode="lines", line=dict(color=RED, width=4), name="learning rate 0.006 (above 2/353)")])
fig.update_layout(template="simple_white", width=950, height=540, font=FONT,
                  xaxis=dict(title="epoch"), yaxis=dict(title="largest coefficient size (log scale)", type="log", exponentformat="power"),
                  legend=dict(x=0.01, y=0.99), margin=dict(l=90, r=30, t=20, b=70))
fig.write_image(here / "lr_limit.png", scale=2)
