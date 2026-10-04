"""Sample size and width: 20 simulated 95% intervals for mu = 50 (sigma = 15) at n = 10, 30, 50, 120, 500 and 1000.
The margin of error falls as 1 / sqrt(n): 9.30, 5.37, 4.16, 2.68, 1.31, 0.93. Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy import stats
from anim import save_gif, FONT, BLUE, ORANGE

here = Path(__file__).parent
NS = [10, 30, 50, 120, 500, 1000]
E = {n: 1.96 * 15 / np.sqrt(n) for n in NS}
assert [round(E[n], 2) for n in NS] == [9.30, 5.37, 4.16, 2.68, 1.31, 0.93]
Z = np.random.default_rng(3).standard_normal(20)        # the same 20 standardized sample means in every frame


def frame(n):
    se = 15 / np.sqrt(n)
    means = 50 + Z * se
    lo, hi = means - 1.96 * se, means + 1.96 * se
    hit = (lo <= 50) & (50 <= hi)
    fig = go.Figure()
    for i in range(20):
        fig.add_scatter(x=[i, i], y=[lo[i], hi[i]], mode="lines", line=dict(color=BLUE if hit[i] else ORANGE, width=6))
    fig.add_scatter(x=np.arange(20), y=means, mode="markers", marker=dict(color="black", size=9))
    fig.add_hline(y=50, line=dict(color="red", width=2))
    fig.update_layout(template="simple_white", width=1000, height=600, font=FONT, showlegend=False,
                      title=dict(text=f"<b>n = {n}</b>: margin of error 1.96 × 15 / √{n} = <b>{E[n]:.2f}</b>", x=0.5),
                      xaxis=dict(title="sample", showticklabels=False), yaxis=dict(title="interval for μ", range=[32, 68]),
                      margin=dict(l=90, r=30, t=80, b=60))
    return fig


if __name__ == "__main__":
    save_gif([frame(n) for n in NS], "n_shrink", here, keys=[0, 2, 4, 5], fps=1, holds=[3, 2, 2, 2, 2, 6])
