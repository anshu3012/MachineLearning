"""How alpha sets inequality: the share of the total held by each fifth of a Pareto population, p^(1 - 1/alpha)
differences, as alpha grows from 1.16 (the 80-20 rule) to 3 (top fifth holds 34 percent). Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from anim import save_gif, FONT, BLUE, RED

here = Path(__file__).parent
ALPHAS = [np.log(5) / np.log(4), 1.5, 2, 3]
top = lambda p, a: p ** (1 - 1 / a)                       # share held by the richest fraction p
assert round(top(0.2, ALPHAS[0]), 3) == 0.8 and round(top(0.2, 3), 2) == 0.34


def frame(a):
    cum = np.array([top(p, a) for p in (0.2, 0.4, 0.6, 0.8, 1.0)])
    shares = np.diff(np.r_[0, cum])                          # richest fifth first
    names = ["richest fifth", "2nd fifth", "3rd fifth", "4th fifth", "poorest fifth"]
    fig = go.Figure(go.Bar(x=names, y=100 * shares, marker_color=[RED] + [BLUE] * 4,
                           text=[f"{100 * s:.0f}%" for s in shares], textposition="outside", textfont=dict(size=22)))
    fig.update_layout(template="simple_white", width=1000, height=560, font=FONT,
                      title=dict(text=f"<b>α = {a:.2f}</b>: the richest fifth holds {100 * shares[0]:.0f} percent of the total", x=0.5),
                      yaxis=dict(title="share of the total", range=[0, 92], ticksuffix="%"),
                      margin=dict(l=90, r=30, t=80, b=70))
    return fig


if __name__ == "__main__":
    save_gif([frame(a) for a in ALPHAS], "alpha_share", here, keys=[0, 1, 2, 3], fps=1, holds=[4, 3, 3, 6])
