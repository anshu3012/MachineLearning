"""The correct reading of p = 0.309, by repetition: 10,000 experiments of 100 tosses of a fair coin. As experiments
pile up, the share with 53 or more heads (red) settles near the p-value 0.309. Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy import stats
from anim import save_gif, FONT, BLUE, RED

here = Path(__file__).parent
heads = np.random.default_rng(0).binomial(100, 0.5, 10_000)
p = stats.binom(100, 0.5).sf(52)
assert round(p, 3) == 0.309 and abs(np.mean(heads >= 53) - p) < 0.015
K = np.arange(30, 71)


def frame(n):
    h = heads[:n]
    c = np.bincount(h, minlength=101)[K]
    share = np.mean(h >= 53)
    fig = go.Figure(go.Bar(x=K, y=c, marker_color=[RED if k >= 53 else BLUE for k in K], width=0.85))
    fig.update_layout(template="simple_white", width=1000, height=560, font=FONT,
                      title=dict(text=f"<b>{n:,}</b> fair-coin experiments: {share:.1%} gave 53 or more heads"
                                      f"<br>(the p-value is {p:.1%})", x=0.5, y=0.94),
                      xaxis=dict(title="heads in 100 tosses", range=[29.5, 70.5]), yaxis=dict(title="experiments"),
                      margin=dict(l=90, r=30, t=110, b=70))
    return fig


if __name__ == "__main__":
    ns = [10, 30, 100, 300, 1000, 3000, 10_000]
    save_gif([frame(n) for n in ns], "repeat_coin", here, keys=[0, 2, 4, 6], fps=1, holds=[2, 2, 2, 2, 2, 2, 6])
