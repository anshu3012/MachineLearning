"""The p-value on a case small enough to count: five tosses of a fair coin, 4 heads observed. The 32 equally
likely outcomes give bars 1, 5, 10, 10, 5, 1 (out of 32). Red = the observed bar, then the more extreme bar
(5 heads): p = 6/32. Last frame: with a two-sided H1 the equally rare other side (0 or 1 heads) is added: 12/32.
Plotly frames (bars being highlighted and summed) -> five_flips.gif, _frames.png"""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy import stats
from anim import save_gif, FONT, BLUE, RED, ORANGE

here = Path(__file__).parent
K = np.arange(6)
COUNT = np.array([1, 5, 10, 10, 5, 1])
assert np.allclose(stats.binom.pmf(K, 5, 0.5), COUNT / 32) and np.isclose(stats.binom.sf(3, 5, 0.5), 6 / 32)


def frame(title, red=(), orange=()):
    col = [RED if k in red else (ORANGE if k in orange else BLUE) for k in K]
    fig = go.Figure(go.Bar(x=K, y=COUNT / 32, marker_color=col, text=[f"{c}/32" for c in COUNT],
                           textposition="outside", textfont_size=24))
    fig.update_layout(template="simple_white", width=1000, height=620, font=FONT, title=dict(text=title, x=0.5),
                      xaxis=dict(title="heads in 5 tosses", dtick=1), yaxis=dict(title="probability if the coin is fair",
                      range=[0, 0.37]), margin=dict(l=90, r=30, t=110, b=80))
    return fig


if __name__ == "__main__":
    figs = [frame("<b>If the coin is fair</b>: 32 equally likely outcomes"),
            frame("<b>Our result</b>: 4 heads, 5/32", red=[4]),
            frame("<b>More extreme</b>: 5 heads, 1/32<br><sup>p-value = 5/32 + 1/32 = 6/32 = 0.19</sup>", red=[4, 5]),
            frame("<b>Two-sided H1</b>: add the equally rare other side<br><sup>p-value = 6/32 + 6/32 = 12/32 = 0.375</sup>",
                  red=[4, 5], orange=[0, 1])]
    save_gif(figs, "five_flips", here, keys=[0, 1, 2, 3], fps=1, holds=[3, 3, 5, 6], cols=2)
