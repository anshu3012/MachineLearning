"""Section 3: the two loops as a table filling in. Rows: the 5 epochs (outer loop); columns: the 4 students (inner loop).
Each frame adds one student's loss; the last column is the epoch's average. Regression network, weights 0.1, biases 0,
learning rate 0.001. Plotly frames -> loss_grid.gif + _frames.png"""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from common import FONT, save_gif

here = Path(__file__).parent
X = np.array([[8, 8], [7, 9], [6, 10], [5, 12]], float)
Y = np.array([4, 5, 6, 7], float)
W1, b1, W2, b2, lr = np.full((2, 2), 0.1), np.zeros(2), np.full(2, 0.1), 0.0, 0.001
L = np.zeros((5, 4))
for ep in range(5):
    for i, (x, y) in enumerate(zip(X, Y)):
        O1 = W1.T @ x + b1
        yh = W2 @ O1 + b2
        L[ep, i] = (y - yh) ** 2
        g = -2 * (y - yh)
        W1, b1, W2, b2 = W1 - lr * np.outer(x, g * W2), b1 - lr * g * W2, W2 - lr * g * O1, b2 - lr * g
avg = L.mean(1)
assert np.allclose(np.round(avg, 2), [26.35, 19.86, 10.88, 3.78, 1.22])               # Section 4.3 table
assert np.allclose(np.round(L[0], 2), [13.54, 21.29, 30.43, 40.12])
cols = ["student 1", "student 2", "student 3", "student 4", "epoch average"]
rows = [f"epoch {e}" for e in range(1, 6)]


def frame(n):                                      # n cells of the inner loop done
    z = np.full((5, 5), np.nan)
    txt = [[""] * 5 for _ in range(5)]
    for k in range(n):
        e, i = divmod(k, 4)
        z[e, i] = L[e, i]
        txt[e][i] = f"{L[e, i]:.2f}"
        if i == 3:
            z[e, 4], txt[e][4] = avg[e], f"<b>{avg[e]:.2f}</b>"
    fig = go.Figure(go.Heatmap(z=np.log10(z), x=cols, y=rows, text=txt, texttemplate="%{text}", textfont=dict(size=22),
                               colorscale="Reds", zmin=-0.5, zmax=1.7, showscale=False, xgap=4, ygap=4))
    if n < 20:
        e, i = divmod(n, 4)
        fig.add_shape(type="rect", x0=i - 0.5, x1=i + 0.5, y0=e - 0.5, y1=e + 0.5, line=dict(color="black", width=4))
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(template="simple_white", width=1000, height=520, font=dict(FONT, size=20),
                      title=dict(text="outer loop: epochs (down)   inner loop: students (across)", x=0.5),
                      margin=dict(l=110, r=20, t=80, b=40))
    return fig


if __name__ == "__main__":
    save_gif([frame(n) for n in range(21)], "loss_grid", [20], here, fps=3, cols=1)
