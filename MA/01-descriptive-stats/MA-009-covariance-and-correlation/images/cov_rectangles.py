"""Covariance of the five employees, built point by point: each point draws the rectangle from the two mean lines to
itself, with area (x - xbar)(y - ybar); positive rectangles are blue, negative red, and the running sum reaches 86,
so s_xy = 86 / 4 = 21.5. Data: the Note's table. Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from anim import save_gif, FONT, BLUE, RED, GREY

here = Path(__file__).parent
x = np.array([2, 5, 8, 12, 13]); y = np.array([1, 2, 5, 12, 10])
mx, my = x.mean(), y.mean()
prod = (x - mx) * (y - my)
assert (mx, my) == (8, 6) and prod.tolist() == [30, 12, 0, 24, 20] and np.cov(x, y)[0, 1] == 21.5


def frame(k):
    fig = go.Figure()
    for i in range(k):
        c = BLUE if prod[i] >= 0 else RED
        fig.add_shape(type="rect", x0=mx, x1=x[i], y0=my, y1=y[i], fillcolor=c, opacity=0.25 if i < k - 1 else 0.45,
                      line=dict(color=c, width=2))
    fig.add_hline(y=my, line=dict(color=GREY, dash="dash", width=2))
    fig.add_vline(x=mx, line=dict(color=GREY, dash="dash", width=2))
    fig.add_annotation(x=13.6, y=my, text="mean ȳ = 6", showarrow=False, yshift=14, xanchor="right", font=dict(size=18))
    fig.add_annotation(x=mx, y=13.4, text="mean x̄ = 8", showarrow=False, xshift=8, xanchor="left", font=dict(size=18))
    fig.add_scatter(x=x[:k], y=y[:k], mode="markers+text", marker=dict(size=16, color="black"),
                    text=[f"{int(p)}" for p in prod[:k]], textposition="top left", textfont=dict(size=20))
    fig.add_scatter(x=x[k:], y=y[k:], mode="markers", marker=dict(size=14, color="#cccccc"))
    if k == 0:
        head = "Five employees: experience x and salary y"
    else:
        i = k - 1
        head = (f"Employee {k}: ({x[i] - mx:+g}) × ({y[i] - my:+g}) = {int(prod[i])}"
                f"<br>running sum = {int(prod[:k].sum())}" + (f"   →   s<sub>xy</sub> = 86 / 4 = <b>21.5</b>" if k == 5 else ""))
    fig.update_layout(template="simple_white", width=950, height=820, font=FONT, showlegend=False,
                      title=dict(text=head, x=0.5, y=0.95),
                      xaxis=dict(title="experience x (years)", range=[0, 14], constrain="domain"),
                      yaxis=dict(title="salary y (lakh rupees)", range=[0, 14], scaleanchor="x", constrain="domain"),
                      margin=dict(l=80, r=30, t=120, b=80))
    return fig


if __name__ == "__main__":
    save_gif([frame(k) for k in range(6)], "cov_rectangles", here, keys=[1, 2, 4, 5], fps=1, holds=[2, 2, 2, 2, 2, 6])
