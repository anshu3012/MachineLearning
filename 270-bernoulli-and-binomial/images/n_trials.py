"""From Bernoulli to binomial: the PMF of the number of heads in n fair-coin tosses for n = 1 (the Bernoulli PMF),
2, 3, 5 and 10. Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy import stats
from anim import save_gif, FONT, BLUE, ORANGE

here = Path(__file__).parent
assert np.allclose(stats.binom(3, 0.5).pmf(range(4)), [1 / 8, 3 / 8, 3 / 8, 1 / 8])


def frame(n):
    k = np.arange(n + 1)
    pm = stats.binom(n, 0.5).pmf(k)
    fig = go.Figure(go.Bar(x=k, y=pm, marker_color=ORANGE if n == 1 else BLUE, width=0.6,
                           text=[f"{v:.3f}" for v in pm], textposition="outside", textfont=dict(size=16)))
    head = "<b>n = 1</b>: one toss, the Bernoulli PMF" if n == 1 else f"<b>n = {n}</b> tosses: Binomial({n}, 0.5)"
    fig.update_layout(template="simple_white", width=1000, height=540, font=dict(family="Latin Modern Roman", size=28), title=dict(text=head, x=0.5),
                      xaxis=dict(title="number of heads x", range=[-0.6, 10.6], dtick=1),
                      yaxis=dict(title="P(X = x)", range=[0, 0.6]), margin=dict(l=90, r=30, t=80, b=70))
    return fig


if __name__ == "__main__":
    save_gif([frame(n) for n in (1, 2, 3, 5, 10)], "n_trials", here, keys=[0, 2, 4], fps=1, holds=[3, 2, 3, 2, 5], cols=3)
