"""The puzzle of section 3, answered (Plotly): three independent models of accuracy 0.7, 0.6 and 0.55 vote to 0.673;
three independent models of accuracy 0.7 vote to 0.784. Exact sums over the 8 right/wrong combinations."""
from itertools import product
from pathlib import Path

import plotly.graph_objects as go

HERE = Path(__file__).parent


def vote(ps):
    """P(majority right) for independent models with accuracies ps: sum over all right/wrong combinations."""
    tot = 0.0
    for r in product((0, 1), repeat=len(ps)):
        pr = 1.0
        for p, ok in zip(ps, r):
            pr *= p if ok else 1 - p
        tot += pr * (sum(r) > len(ps) / 2)
    return tot


a, b = vote([0.7, 0.6, 0.55]), vote([0.7] * 3)
assert round(a, 3) == 0.673 and round(b, 3) == 0.784
x = ["M1", "M2", "M3", "vote of<br>M1, M2, M3", "vote of three<br>0.7 models"]
y = [0.7, 0.6, 0.55, a, b]
col = ["#4C78A8"] * 3 + ["#E45756", "#54A24B"]
fig = go.Figure(go.Bar(x=x, y=y, marker_color=col, text=[f"{v:.3f}".rstrip("0") if i < 3 else f"{v:.3f}" for i, v in enumerate(y)],
                       textposition="outside"))
fig.add_hline(y=0.7, line=dict(color="black", dash="dash", width=2))
fig.add_annotation(x=1.5, y=0.72, text="best single model: 0.7", showarrow=False, yanchor="bottom")
fig.update_layout(template="simple_white", width=1000, height=520, font=dict(family="Latin Modern Roman", size=24),
                  yaxis=dict(title="accuracy", range=[0, 0.92]), margin=dict(l=90, r=20, t=30, b=100), bargap=0.35)
fig.write_image(HERE / "puzzle_bars.png", scale=2); fig.write_image(HERE / "puzzle_bars.pdf")
