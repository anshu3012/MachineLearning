"""The worked examples of sections 5.2 and 6.2 as one process: scores -> exp -> divide by the sum (softmax) ->
weights, then the weighted states added up into the context vector c_i. Numbers from the text (asserted).
Plotly frames -> GIF, plus a key-frame grid for the PDF."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, GREEN, FONT
from gifkit import save_gif

HERE = Path(__file__).parent
e = np.array([0.5, 0.2, 1.8])
ex = np.exp(e)
a = ex / ex.sum()
H = np.array([[1.0, 0.5, 0.6, 0.3], [0.2, 0.9, 0.1, 0.4], [0.7, 0.1, 0.8, 0.5]])
c = a.round(3) @ H                                     # the text uses the rounded weights
assert np.allclose(ex.round(2), [1.65, 1.22, 6.05]) and round(ex.sum(), 2) == 8.92
assert np.allclose(a.round(3), [0.185, 0.137, 0.678]) and np.allclose(c.round(3), [0.687, 0.284, 0.667, 0.449])
COL = [BLUE, ORANGE, GREEN]
STAGES = [("scores e<sub>ij</sub> from the alignment model", e, "{:.1f}"),
          (f"exp(e): all positive; their sum is {ex.sum():.2f}", ex, "{:.2f}"),
          ("divide by the sum: weights α<sub>ij</sub>, adding up to 1", a, "{:.3f}")]


def frame(k):
    """k = 0, 1, 2: softmax stages; k = 3, 4, 5: states 1 to k - 2 added into c."""
    fig = make_subplots(rows=1, cols=2, column_widths=[0.42, 0.58], horizontal_spacing=0.12,
                        subplot_titles=("one number per encoder state",
                                        "context vector c<sub>i</sub> = Σ α<sub>ij</sub> h<sub>j</sub>"))
    title, vals, fmt = STAGES[min(k, 2)]
    fig.add_bar(x=["h<sub>1</sub>", "h<sub>2</sub>", "h<sub>3</sub>"], y=vals, marker_color=COL, showlegend=False,
                text=[fmt.format(v) for v in vals], textposition="outside", row=1, col=1)
    fig.update_yaxes(range=[0, 7], row=1, col=1)
    n = max(k - 2, 0)
    for j in range(n):
        fig.add_bar(x=["1", "2", "3", "4"], y=a[j] * H[j], marker_color=COL[j], row=1, col=2,
                    name=f"{a[j]:.3f} x h<sub>{j + 1}</sub>")
    if n == 3:
        fig.add_scatter(x=["1", "2", "3", "4"], y=c + 0.06, mode="text", text=[f"{v:.3f}" for v in c],
                        textfont=dict(size=19), showlegend=False, row=1, col=2)
    fig.update_yaxes(range=[0, 0.85], row=1, col=2)
    fig.update_xaxes(title="position in the vector", row=1, col=2)
    if k >= 3:
        title = (f"add each state times its weight: {n} of 3 added" if n < 3
                 else "c<sub>i</sub> is dominated by h<sub>3</sub>, the state with the largest weight")
    fig.update_layout(template="simple_white", width=1100, height=480, font=dict(FONT, size=19), barmode="stack",
                      title=dict(text=title, x=0.5, y=0.97), legend=dict(x=0.62, y=0.98),
                      margin=dict(l=50, r=20, t=100, b=60))
    return fig


if __name__ == "__main__":
    save_gif([frame(k) for k in range(6)], "softmax_sum", HERE, keys=[0, 2, 3, 5], fps=0.8, holds=[1, 1, 2, 1, 1, 4])
