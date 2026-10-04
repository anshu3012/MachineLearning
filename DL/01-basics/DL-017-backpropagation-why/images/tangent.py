"""Section 5: a derivative is the slope of the tangent. Student 1, all parameters frozen at their start except
W^1_11: L(w) = (3.76 - 0.8 w)^2. The tangent slides along the curve; its slope's sign and size are printed.
At the start, w = 0.1, the slope is -5.888. Plotly frames -> tangent.gif + _frames.png"""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from common import BLUE, ORANGE, GREEN, RED, GREY, FONT, save_gif

here = Path(__file__).parent
L = lambda w: (4 - (0.1 * (8 * w + 0.1 * 8) + 0.1 * 1.6)) ** 2         # network forward pass, only W^1_11 free
dL = lambda w: -2 * (4 - (0.1 * (8 * w + 0.1 * 8) + 0.1 * 1.6)) * 0.1 * 8
assert np.isclose(L(0.1), (4 - 0.32) ** 2) and round(dL(0.1), 3) == -5.888                 # Section 5 numbers
assert abs(L(0.1 + 0.001) - L(0.1) + 0.006) < 0.0005                                        # +0.001 -> loss -0.006
assert abs(dL(4.7)) < 1e-9                                                                   # bottom at 4.7
W = [-3, -2, -1, 0.1, 1, 2, 3, 4, 4.7, 5.5, 6.5, 7.5, 8.5]
wg = np.linspace(-3.5, 9, 300)


def frame(w):
    s = dL(w) if abs(dL(w)) > 1e-9 else 0.0
    c = BLUE if s < -1e-9 else ORANGE if s > 1e-9 else GREEN
    word = "negative: raising W¹₁₁ lowers the loss" if s < -1e-9 else "positive: raising W¹₁₁ raises the loss" if s > 1e-9 else "zero: the bottom"
    t = np.array([w - 1.5, w + 1.5])
    fig = go.Figure(go.Scatter(x=wg, y=L(wg), line=dict(color=GREY, width=4), showlegend=False))
    fig.add_trace(go.Scatter(x=t, y=L(w) + s * (t - w), mode="lines", line=dict(color=c, width=5), showlegend=False))
    fig.add_trace(go.Scatter(x=[w], y=[L(w)], mode="markers", marker=dict(color=c, size=16), showlegend=False))
    tag = "   (the starting value)" if w == 0.1 else ""
    fig.update_layout(template="simple_white", width=950, height=560, font=dict(FONT, size=22),
                      title=dict(text=f"W¹₁₁ = {w}{tag}:  ∂L/∂W¹₁₁ = {s:.3f}<br><span style='color:{c}'>slope {word}</span>",
                                 x=0.5, y=0.95), xaxis=dict(title="W¹₁₁ (other 8 parameters frozen)", range=[-3.5, 9]),
                      yaxis=dict(title="loss of student 1", range=[-2, 45]), margin=dict(l=80, r=30, t=120, b=70))
    return fig


if __name__ == "__main__":
    save_gif([frame(w) for w in W], "tangent", [3, 8], here, fps=2)
