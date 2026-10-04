"""Exact probabilities for two dice (Plotly): P(die 2 = 6 | die 1 = k) is 1/6 for every k (independent);
P(sum >= 10 | die 1 = k) changes with k (dependent)."""
from pathlib import Path
from fractions import Fraction
from itertools import product
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
out = list(product(range(1, 7), repeat=2))
k = list(range(1, 7))
p6 = [Fraction(sum(1 for a, b in out if a == j and b == 6), sum(1 for a, b in out if a == j)) for j in k]
p10 = [Fraction(sum(1 for a, b in out if a == j and a + b >= 10), sum(1 for a, b in out if a == j)) for j in k]
base6 = Fraction(sum(1 for a, b in out if b == 6), 36)
base10 = Fraction(sum(1 for a, b in out if a + b >= 10), 36)
print(p6, base6, p10, base10)
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1,
                    subplot_titles=("Independent: P(die 2 = 6 | die 1 = k)", "Not independent: P(sum ≥ 10 | die 1 = k)"))
for col, vals, base, c in ((1, p6, base6, "#4C78A8"), (2, p10, base10, "#E45756")):
    fig.add_trace(go.Bar(x=k, y=[float(v) for v in vals], marker_color=c, text=[str(v) for v in vals], textposition="outside"), 1, col)
    fig.add_trace(go.Scatter(x=[0.5, 6.5], y=[float(base)] * 2, mode="lines", line=dict(color="black", dash="dash", width=2)), 1, col)
    fig.add_annotation(x=1.0, y=float(base) + 0.1, text=f"without the condition: {base}", showarrow=False, xanchor="left",
                       font=dict(size=13), row=1, col=col)
fig.update_xaxes(title="die 1 shows k", dtick=1)
fig.update_yaxes(range=[0, 0.6])
fig.update_yaxes(title="probability", row=1, col=1)
fig.update_layout(template="simple_white", width=1100, height=440, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=15), margin=dict(l=60, r=20, t=50, b=60))
fig.write_image(here / "independence.png", scale=2); fig.write_image(here / "independence.pdf")
