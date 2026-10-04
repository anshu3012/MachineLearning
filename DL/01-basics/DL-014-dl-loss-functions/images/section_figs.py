"""Three still figures with the Note's own numbers (Plotly):
loss_vs_cost.png (section 4), bce_curves.png (section 8), cce_bars.png (section 9)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, GREEN, RED, GREY, FONT

here = Path(__file__).parent
F = dict(FONT, size=20)

# Section 4: four losses, one cost
y, yh = np.array([6.3, 4.1, 3.5, 7.2]), np.array([6.1, 4.0, 3.7, 7.0])
L = (y - yh) ** 2
J = L.mean()
assert np.allclose(L, [0.04, 0.01, 0.04, 0.04]) and np.isclose(J, 0.0325)
fig = go.Figure(go.Bar(x=[f"student {i}" for i in range(1, 5)], y=L, marker_color=BLUE, width=0.55,
                       text=[f"loss {v:.2f}" for v in L], textposition="outside", name="loss of one student"))
fig.add_hline(y=J, line=dict(color=RED, width=4, dash="dash"), layer="above")
fig.add_annotation(x=1, y=J, yshift=-30, text=f"cost J = average = {J:.4f}", showarrow=False,
                   font=dict(color=RED, size=22), bgcolor="white")
fig.update_layout(template="simple_white", width=900, height=460, font=F, yaxis=dict(title="(y − ŷ)²", range=[0, 0.05]),
                  margin=dict(l=80, r=30, t=30, b=50), showlegend=False)
fig.write_image(here / "loss_vs_cost.png", scale=2)

# Section 8: binary cross-entropy for each label
p = np.linspace(0.005, 0.995, 400)
s1, s2 = -np.log(0.73), -np.log(1 - 0.25)
assert round(s1, 3) == 0.315 and round(s2, 3) == 0.288
fig = go.Figure()
fig.add_trace(go.Scatter(x=p, y=-np.log(p), name="y = 1 (placed):  −log ŷ", line=dict(color=BLUE, width=4)))
fig.add_trace(go.Scatter(x=p, y=-np.log(1 - p), name="y = 0 (not placed):  −log(1 − ŷ)", line=dict(color=ORANGE, width=4)))
fig.add_trace(go.Scatter(x=[0.73, 0.25], y=[s1, s2], mode="markers", marker=dict(size=14, color=[BLUE, ORANGE]),
                         showlegend=False))
for px, py, txt, c, ax in ((0.73, s1, f"student 1 (y = 1)<br>ŷ = 0.73, L = {s1:.3f}", BLUE, 0),
                           (0.25, s2, f"student 2 (y = 0)<br>ŷ = 0.25, L = {s2:.3f}", ORANGE, 0)):
    fig.add_annotation(x=px, y=py, ax=ax, ay=-90, text=txt, font=dict(color=c, size=19), arrowcolor=c, arrowwidth=2,
                       bgcolor="white")
fig.update_layout(template="simple_white", width=950, height=520, font=F,
                  xaxis=dict(title="predicted probability ŷ of class 1", range=[0, 1]),
                  yaxis=dict(title="loss", range=[0, 4]), legend=dict(x=0.25, y=0.98),
                  margin=dict(l=70, r=30, t=30, b=60))
fig.write_image(here / "bce_curves.png", scale=2)

# Section 9: categorical cross-entropy, only the true class counts
cls = ["yes", "no", "maybe"]
studs = [("student 1: true class yes", np.array([0.2, 0.3, 0.5]), 0),
         ("student 2: true class no", np.array([0.3, 0.6, 0.1]), 1)]
losses = [-np.log(q[c]) for _, q, c in studs]
assert np.allclose(np.round(losses, 3), [1.609, 0.511]) and round(np.mean(losses), 3) == 1.060
fig = make_subplots(rows=1, cols=2, subplot_titles=[s[0] for s in studs], horizontal_spacing=0.12)
for i, ((_, q, c), l) in enumerate(zip(studs, losses), start=1):
    fig.add_trace(go.Bar(x=cls, y=q, marker_color=[GREEN if j == c else "#D0D0D0" for j in range(3)], width=0.6,
                         text=[f"{v:.1f}" for v in q], textposition="outside", showlegend=False), 1, i)
    fig.add_annotation(x=cls[c], y=q[c] + 0.13, text=f"L = −log {q[c]:.1f} = {l:.3f}", showarrow=False,
                       font=dict(color=GREEN, size=20), row=1, col=i)
    fig.update_yaxes(range=[0, 0.85], title_text="softmax output ŷ" if i == 1 else None, row=1, col=i)
fig.update_layout(template="simple_white", width=1100, height=460, font=F, margin=dict(l=80, r=30, t=60, b=50))
fig.update_annotations(font_size=20)
fig.write_image(here / "cce_bars.png", scale=2)
