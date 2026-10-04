"""Section 5.3's worked example as a step-by-step computation. Left: W_i, one row per word; the current word's
one-hot vector picks its row (black frame). Right: the row x_t W_i, the feedback h_(t-1) W_h, their sum and
h_t = tanh(sum). The hidden states are asserted against data/worked_example.csv (Notebook).
Plotly frames -> GIF, plus a key-frame grid for the PDF."""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import save_gif

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=20)
VOCAB = ["movie", "was", "good", "bad", "not"]
Wi = np.array([[0.2, -0.1, 0.0], [0.0, 0.1, 0.1], [0.8, 0.3, -0.5], [-0.8, -0.3, 0.5], [-0.6, 0.2, 0.4]])
Wh = np.array([[0.5, 0.0, 0.1], [0.2, 0.4, 0.0], [0.0, -0.3, 0.5]])
Wo = np.array([1.5, 0.5, -1.0])
WORDS = ["movie", "was", "good"]
ref = pd.read_csv(HERE.parent / "data" / "worked_example.csv")

h, H = np.zeros(3), []
for t, w in enumerate(WORDS):
    xw, hw = Wi[VOCAB.index(w)], h @ Wh
    h = np.tanh(xw + hw)
    H.append((xw, hw, xw + hw, h))
    assert np.allclose(h, ref.loc[t, ["h1", "h2", "h3"]].values.astype(float), atol=6e-4)
y = 1 / (1 + np.exp(-(h @ Wo)))
assert round(y, 2) == 0.83
ROWS = ["x<sub>t</sub> W<sub>i</sub>", "h<sub>t-1</sub> W<sub>h</sub>", "sum", "h<sub>t</sub> = tanh(sum)"]
SCALE = [[0, "#E45756"], [0.5, "#FFFFFF"], [1, "#4C78A8"]]


def frame(t, k):
    """Time step t (0-based), showing the first k+1 rows of the computation (k = 3: h_t complete)."""
    fig = make_subplots(rows=1, cols=2, column_widths=[0.36, 0.64], horizontal_spacing=0.16,
                        subplot_titles=("W<sub>i</sub>: one row per word", f"time step t = {t + 1}"))
    fig.add_trace(go.Heatmap(z=Wi[::-1], x=["node 1", "node 2", "node 3"], y=VOCAB[::-1], zmin=-1, zmax=1,
                             colorscale=SCALE, showscale=False, text=Wi[::-1], texttemplate="%{text:.1f}",
                             textfont=dict(size=20)), row=1, col=1)
    r = 4 - VOCAB.index(WORDS[t])
    fig.add_shape(type="rect", x0=-0.5, x1=2.5, y0=r - 0.5, y1=r + 0.5, fillcolor="rgba(0,0,0,0)", opacity=1, line=dict(color="black", width=5), row=1, col=1)
    vals = np.full((4, 3), np.nan)
    for j in range(k + 1):
        vals[j] = H[t][j]
    fig.add_trace(go.Heatmap(z=vals[::-1], x=["node 1", "node 2", "node 3"], y=ROWS[::-1], zmin=-1, zmax=1,
                             colorscale=SCALE, showscale=False, text=[["" if np.isnan(v) else f"{v:.3f}" for v in row] for row in vals[::-1]],
                             texttemplate="%{text}",
                             textfont=dict(size=20), xgap=3, ygap=3), row=1, col=2)
    prev = "zeros (h<sub>0</sub>)" if t == 0 else "[" + ", ".join(f"{v:.3f}" for v in H[t - 1][3]) + "]"
    note = [f'one-hot "{WORDS[t]}" picks its row of W<sub>i</sub>',
            f"previous hidden state {prev} times W<sub>h</sub>",
            "add the two rows (biases are 0)",
            "tanh squeezes each number into (-1, 1)"][k]
    if t == 2 and k == 3:
        note = f"after the last word: ŷ = sigmoid(h<sub>3</sub> W<sub>o</sub>) = sigmoid({h @ Wo:.3f}) = <b>{y:.2f}</b>"
    fig.update_layout(template="simple_white", width=1100, height=520, font=FONT,
                      title=dict(text=f'"movie was good": word {t + 1}, <b>{WORDS[t]}</b><br><span style="font-size:18px">{note}</span>',
                                 x=0.5, y=0.95), margin=dict(l=20, r=20, t=140, b=40))
    fig.update_xaxes(side="bottom")
    return fig


if __name__ == "__main__":
    figs = [frame(t, k) for t in range(3) for k in range(4)]
    save_gif(figs, "worked_steps", HERE, keys=[3, 5, 7, 11], fps=1, width=900,
             holds=[1, 1, 1, 2] * 2 + [1, 1, 1, 5], cols=2)
