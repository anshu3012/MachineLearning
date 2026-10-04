"""Section 7: how the KDE curve is built. Every passenger's age gets one small bell-shaped bump centred on that age;
the curve is the sum of the bumps (scipy.stats.gaussian_kde: a kernel-density estimate using Gaussian kernels).
Frames: 5 ages (the first five passengers with a known age), then 50, then all 714. Every bump has the width
gaussian_kde picks for the 714 ages, and the last frame is checked against gaussian_kde itself.
Plotly frames (bumps adding up) -> GIF, plus a key-frame grid for the PDF."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import gaussian_kde, norm
from gifkit import save_gif

HERE = Path(__file__).parent
BLUE, ORANGE = "#4C78A8", "#F58518"
age = pd.read_csv(HERE.parent / "data" / "titanic_train.csv")["Age"].dropna().to_numpy()
kde = gaussian_kde(age)
H = kde.factor * age.std(ddof=1)                 # the bump width (standard deviation) gaussian_kde uses
grid = np.linspace(-5, 85, 400)


def bumps(a):
    return norm.pdf(grid[None, :], a[:, None], H) / len(a)     # one row per passenger; rows add up to the curve


assert np.allclose(bumps(age).sum(0), kde(grid))


def frame(n, title, show_bumps=True, show_sum=True):
    a = age[:n]
    b = bumps(a)
    fig = go.Figure()
    if show_bumps:
        for row in b[:50]:
            fig.add_scatter(x=grid, y=row, mode="lines", line=dict(color=BLUE, width=1.5), opacity=0.7)
    if show_sum:
        fig.add_scatter(x=grid, y=b.sum(0), mode="lines", line=dict(color=ORANGE, width=4))
    fig.add_scatter(x=a, y=np.zeros(n), mode="markers", marker=dict(color=BLUE, size=11 if n <= 50 else 6, opacity=0.6))
    fig.update_layout(template="simple_white", width=1000, height=560, showlegend=False, font=dict(family="Latin Modern Roman", size=19),
                      title=dict(text=title, x=0.5), xaxis=dict(title="Age (years)", range=[-5, 85], dtick=10),
                      yaxis=dict(title="Density", rangemode="tozero"), margin=dict(l=90, r=20, t=90, b=70))
    return fig


if __name__ == "__main__":
    figs = [frame(5, "Five passengers: ages 22, 38, 26, 35 and 35", False, False),
            frame(5, "One small bump on each age (blue)", True, False),
            frame(5, "Add the bumps: the orange curve", True, True),
            frame(50, "50 passengers: 50 bumps, one sum", True, True),
            frame(len(age), "All 714 passengers: the KDE curve of Figure 7", False, True)]
    save_gif(figs, "kde_bumps", HERE, keys=[1, 2, 3, 4], fps=0.7)
    print("bump width", round(H, 2), age[:5])
