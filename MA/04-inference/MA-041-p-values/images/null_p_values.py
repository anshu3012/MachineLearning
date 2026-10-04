"""What alpha = 0.05 promises. The Note's training-program z-test (H0: mu = 50, sigma = 5, n = 30, right-tailed)
is run on 100, 1,000 and 10,000 samples drawn with H0 TRUE. The p-values spread evenly from 0 to 1, so about
5 percent of them fall at or below 0.05 (red bar): the false positives.
Plotly frames (a histogram filling up) -> null_p_values.gif, _frames.png"""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy import stats
from anim import save_gif, FONT, BLUE, RED

here = Path(__file__).parent
rng = np.random.default_rng(42)
means = rng.normal(50, 5, (10_000, 30)).mean(axis=1)             # H0 true in every sample
P = stats.norm.sf((means - 50) / (5 / np.sqrt(30)))
NS = [100, 1_000, 10_000]
SHARE = [float(np.mean(P[:n] <= 0.05)) for n in NS]
assert abs(SHARE[-1] - 0.05) < 0.01


def frame(i):
    n = NS[i]
    h = np.histogram(P[:n], bins=20, range=(0, 1))[0] / n
    fig = go.Figure(go.Bar(x=np.arange(0.025, 1, 0.05), y=h, width=0.046, marker_color=[RED] + [BLUE] * 19))
    fig.add_hline(y=0.05, line=dict(color="black", dash="dash", width=2))
    fig.update_layout(template="simple_white", width=1000, height=600, font=FONT,
                      title=dict(text=f"<b>{n:,} tests with H0 true</b><br><sup>p ≤ 0.05 (red) in "
                                      f"{100 * SHARE[i]:.1f} percent of them</sup>", x=0.5),
                      xaxis=dict(title="p-value", dtick=0.1, range=[0, 1]),
                      yaxis=dict(title="share of tests", range=[0, 0.12]), margin=dict(l=90, r=30, t=110, b=80))
    return fig


if __name__ == "__main__":
    save_gif([frame(i) for i in range(3)], "null_p_values", here, keys=[0, 2], fps=1, holds=[3, 3, 6], cols=2)
    print(SHARE)
