"""The second derivative as the change in the change (Plotly), for f(x) = x^3 from x = 1. Two equal steps dx = 0.5
(drawn large to be visible) raise f by df1 = 2.375 and then df2 = 4.625. The second rise is bigger by
ddf = df2 - df1 = 2.25: the slope itself is growing, so the curve bends upward.
Idea after 3Blue1Brown, "Higher order derivatives"; our own function."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, RED

here = Path(__file__).parent
f = lambda x: x ** 3
dx = 0.5
x0, x1, x2 = 1, 1 + dx, 1 + 2 * dx
df1, df2 = f(x1) - f(x0), f(x2) - f(x1)
assert (df1, df2, df2 - df1) == (2.375, 4.625, 2.25)
small = (f(1.02) - f(1.01)) - (f(1.01) - f(1))            # the same with dx = 0.01
assert abs(small / 0.01 ** 2 - 6) < 0.1                   # ddf / dx^2 is close to f''(1) = 6
x = np.linspace(0.8, 2.15, 200)
fig = go.Figure(go.Scatter(x=x, y=f(x), line=dict(color=BLUE, width=4)))
for a, b, d, col, name in ((x0, x1, df1, ORANGE, "df₁"), (x1, x2, df2, GREEN, "df₂")):
    fig.add_trace(go.Scatter(x=[a, b], y=[f(a), f(a)], mode="lines", line=dict(color=GREY, width=2, dash="dot")))
    fig.add_trace(go.Scatter(x=[b, b], y=[f(a), f(b)], mode="lines", line=dict(color=col, width=7)))
    fig.add_annotation(x=b, y=(f(a) + f(b)) / 2, text=f"{name} = {d}", showarrow=False, xanchor="left", xshift=10,
                       font=dict(size=22, color=col))
    fig.add_annotation(x=(a + b) / 2, y=f(a), text="dx", showarrow=False, yshift=-16, font=dict(size=20, color=GREY))
fig.add_trace(go.Scatter(x=[x0, x1, x2], y=[f(x0), f(x1), f(x2)], mode="markers", marker=dict(size=13, color="black")))
fig.add_annotation(x=0.85, y=7.2, xanchor="left", showarrow=False, align="left", font=dict(size=22, color=RED),
                   text="change in the change:<br>ddf = df₂ − df₁ = 2.25 > 0<br>the curve bends upward")
fig.update_xaxes(title="x", range=[0.8, 2.45], tickvals=[1, 1.5, 2])
fig.update_yaxes(title="f(x) = x³", range=[0, 9])
fig.update_layout(template="simple_white", width=900, height=520, font=FONT, showlegend=False, margin=dict(l=70, r=20, t=20, b=65))
fig.write_image(here / "second_diff.png", scale=2)
