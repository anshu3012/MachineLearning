"""Still figures from the Note's own runs (Plotly):
weights_path.png (section 4.3), keras_gap.png (section 5), stuck.png (section 8)."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, GREEN, RED, PURPLE, GREY, FONT

here = Path(__file__).parent
F = dict(FONT, size=20)
X = np.array([[8, 8], [7, 9], [6, 10], [5, 12]], float)

# Section 4.3: the weights after every update, regression, 5 epochs
Y = np.array([4, 5, 6, 7], float)
W1, b1, W2, b2, lr = np.full((2, 2), 0.1), np.zeros(2), np.full(2, 0.1), 0.0, 0.001
hist = [(W1[0, 0], W1[1, 0], W2[0], W1[0, 1], W2[1])]
for ep in range(5):
    for x, y in zip(X, Y):
        O1 = W1.T @ x + b1
        g = -2 * (y - (W2 @ O1 + b2))
        W1, b1, W2, b2 = W1 - lr * np.outer(x, g * W2), b1 - lr * g * W2, W2 - lr * g * O1, b2 - lr * g
        hist.append((W1[0, 0], W1[1, 0], W2[0], W1[0, 1], W2[1]))
H = np.array(hist)
assert np.allclose(np.round(H[-1, :3], 3), [0.272, 0.393, 0.469])                    # Section 4.3
assert np.allclose(H[:, 0], H[:, 3]) and np.allclose(H[:, 2], H[:, 4])              # the twin weights stay equal
assert np.round(b1[0], 3) == 0.028 and np.round(b2, 3) == 0.122
fig = go.Figure()
for j, (name, c) in enumerate((("W¹₁₁ = W¹₁₂ (CGPA weights)", BLUE), ("W¹₂₁ = W¹₂₂ (profile weights)", ORANGE),
                               ("W²₁₁ = W²₂₁ (output weights)", GREEN))):
    fig.add_trace(go.Scatter(x=np.arange(21), y=H[:, j], mode="lines+markers", name=f"{name}: {H[-1, j]:.3f}",
                             line=dict(color=c, width=4), marker=dict(size=7)))
for e in range(1, 5):
    fig.add_vline(x=4 * e, line=dict(color=GREY, width=1, dash="dot"))
fig.update_layout(template="simple_white", width=1000, height=480, font=F,
                  xaxis=dict(title="update number (4 per epoch)", tickvals=[0, 4, 8, 12, 16, 20]),
                  yaxis=dict(title="weight value"), legend=dict(x=0.02, y=0.98), margin=dict(l=80, r=30, t=30, b=60))
fig.write_image(here / "weights_path.png", scale=2)

# Section 5: how far apart our code and Keras are, every epoch
reg = pd.read_csv(here.parent / "data" / "regression_loss.csv")
cls = pd.read_csv(here.parent / "data" / "classification_loss.csv")
gap_r, gap_c = (reg.ours - reg.keras).abs(), (cls.ours - cls.keras).abs()
assert round(gap_r.max(), 7) == 1.3e-6 and round(gap_c.max(), 8) == 7e-8   # Section 5 text
fig = go.Figure()
fig.add_trace(go.Scatter(x=reg.epoch, y=gap_r, mode="lines+markers", name="regression", line=dict(color=BLUE, width=3)))
fig.add_trace(go.Scatter(x=cls.epoch, y=gap_c, mode="lines+markers", name="classification", line=dict(color=ORANGE, width=3)))
fig.add_hline(y=0.0005, line=dict(color=RED, width=3, dash="dash"))
fig.add_annotation(x=74, y=np.log10(0.0005), yshift=16, xanchor="right", showarrow=False, font=dict(color=RED, size=20),
                   text="half a unit in the 3rd decimal: the smallest gap a printed loss like 0.177 could show")
fig.update_layout(template="simple_white", width=1000, height=480, font=F,
                  xaxis=dict(title="epoch"), yaxis=dict(title="|our loss − Keras loss|", type="log", range=[-10, -2.5],
                                                         dtick=1, exponentformat="power"),
                  legend=dict(x=0.75, y=0.78), margin=dict(l=90, r=30, t=30, b=60))
fig.write_image(here / "keras_gap.png", scale=2)

# Section 8: the classifier's prediction for each student, 50 epochs, stuck near 0.54
s = lambda z: 1 / (1 + np.exp(-z))
Yc = np.array([1, 1, 0, 0], float)
Xc = np.array([[8, 8], [7, 9], [6, 10], [5, 5]], float)
W1, b1, W2, b2 = np.full((2, 2), 0.1), np.zeros(2), np.full(2, 0.1), 0.0
P, Ls = [[s(W2 @ s(W1.T @ x + b1) + b2) for x in Xc]], []
for ep in range(50):
    l = []
    for x, y in zip(Xc, Yc):
        a1 = s(W1.T @ x + b1)
        yh = s(W2 @ a1 + b2)
        l.append(-y * np.log(yh) - (1 - y) * np.log(1 - yh))
        d = -(y - yh)
        dh = d * W2 * a1 * (1 - a1)
        W1, b1, W2, b2 = W1 - lr * np.outer(x, dh), b1 - lr * dh, W2 - lr * d * a1, b2 - lr * d
    Ls.append(np.mean(l))
    P.append([s(W2 @ s(W1.T @ x + b1) + b2) for x in Xc])
P = np.array(P)
assert round(Ls[0], 4) == 0.6942 and round(Ls[-1], 4) == 0.6937 and np.allclose(W1[:, 0], W1[:, 1])   # Section 8
assert np.all(np.abs(P - 0.54) < 0.02)
fig = go.Figure()
for i, c in enumerate((BLUE, GREEN, ORANGE, PURPLE)):
    fig.add_trace(go.Scatter(x=np.arange(51), y=P[:, i], mode="lines", line=dict(color=c, width=4),
                             name=f"student {i + 1} ({'placed' if Yc[i] else 'not placed'})"))
fig.add_hrect(y0=0.95, y1=1.0, fillcolor=GREEN, opacity=0.15, line_width=0)
fig.add_hrect(y0=0.0, y1=0.05, fillcolor=RED, opacity=0.15, line_width=0)
fig.add_annotation(x=25, y=0.975, text="where placed students should end", showarrow=False, font=dict(size=18))
fig.add_annotation(x=25, y=0.025, text="where the others should end", showarrow=False, font=dict(size=18))
fig.update_layout(template="simple_white", width=1000, height=480, font=F,
                  xaxis=dict(title="epoch"), yaxis=dict(title="predicted probability ŷ", range=[0, 1]),
                  legend=dict(x=0.55, y=0.38, bgcolor="rgba(0,0,0,0)"), margin=dict(l=80, r=30, t=30, b=60))
fig.write_image(here / "stuck.png", scale=2)
