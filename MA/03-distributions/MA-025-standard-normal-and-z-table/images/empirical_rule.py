"""Deriving the 68-95-99.7 rule: shade mu +- 1, 2 and 3 standard deviations under the standard normal curve, one
step at a time, with the area Phi(k) - Phi(-k). Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy import stats
from anim import save_gif, FONT, BLUE, ORANGE

here = Path(__file__).parent
z = np.linspace(-4, 4, 500)
y = stats.norm.pdf(z)
AREA = {k: stats.norm.cdf(k) - stats.norm.cdf(-k) for k in (1, 2, 3)}
assert [round(100 * AREA[k], 2) for k in (1, 2, 3)] == [68.27, 95.45, 99.73]
SHADE = {1: "rgba(245,133,24,0.65)", 2: "rgba(245,133,24,0.4)", 3: "rgba(245,133,24,0.2)"}


def frame(k):
    fig = go.Figure()
    for j in range(k, 0, -1):
        m = np.abs(z) <= j
        fig.add_scatter(x=np.r_[-j, z[m], j], y=np.r_[0, y[m], 0], fill="toself", fillcolor=SHADE[j],
                        line=dict(width=0), mode="lines")
    fig.add_scatter(x=z, y=y, mode="lines", line=dict(color=BLUE, width=4))
    half = stats.norm.cdf(k) - 0.5
    fig.update_layout(template="simple_white", width=900, height=640, font=dict(family="Latin Modern Roman", size=28), showlegend=False,
                      title=dict(text=f"<b>μ ± {k}σ</b>: Φ({k}) − 0.5 = {half:.4f} per side<br>"
                                      f"both sides: 2 × {half:.4f} = <b>{100 * AREA[k]:.2f} percent</b>", x=0.5, y=0.94),
                      xaxis=dict(title="z", dtick=1),
                      yaxis=dict(title="density", range=[0, 0.45]), margin=dict(l=80, r=30, t=140, b=80))
    return fig


if __name__ == "__main__":
    save_gif([frame(k) for k in (1, 2, 3)], "empirical_rule", here, keys=[0, 1, 2], fps=1, holds=[4, 4, 6], cols=3)
