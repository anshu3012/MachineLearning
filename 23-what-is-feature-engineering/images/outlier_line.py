"""A few outliers pull a linear regression line away from the main pattern: the three outliers are added one at a
time and the least-squares line is refitted after each. Example data (25 points on y = 2x + 3 plus noise).
Plotly frames -> GIF (replaces an earlier seaborn still)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from anim import save_gif, FONT, BLUE, RED, GREEN

here = Path(__file__).parent
rng = np.random.default_rng(3)
x = rng.uniform(1, 10, 25)
y = 2 * x + 3 + rng.normal(0, 1.2, 25)
xo, yo = np.array([8.5, 9.2, 9.8]), np.array([2.0, 1.0, 3.0])   # three outliers
grid = np.array([0, 10.5])
clean = np.polyfit(x, y, 1)


def frame(k):
    """k outliers added so far."""
    ax, ay = np.r_[x, xo[:k]], np.r_[y, yo[:k]]
    slope, icpt = np.polyfit(ax, ay, 1)
    fig = go.Figure()
    fig.add_scatter(x=grid, y=np.polyval(clean, grid), mode="lines", line=dict(color=GREEN, width=4, dash="dash"),
                    name="line fitted without outliers")
    if k:
        fig.add_scatter(x=grid, y=slope * grid + icpt, mode="lines", line=dict(color=RED, width=5),
                        name=f"line fitted with {k} outlier{'s' if k > 1 else ''}")
    fig.add_scatter(x=x, y=y, mode="markers", marker=dict(color=BLUE, size=13), name="25 normal points")
    if k:
        fig.add_scatter(x=xo[:k], y=yo[:k], mode="markers", name="outlier",
                        marker=dict(color=RED, size=20, symbol="x"))
    fig.update_layout(template="simple_white", width=1000, height=680, font=FONT,
                      title=dict(text=f"<b>{k} outlier{'s' if k != 1 else ''}</b>: slope {slope:.2f}"
                                      f" (without outliers: {clean[0]:.2f})", x=0.5),
                      xaxis=dict(title="input feature", range=[0, 10.5]),
                      yaxis=dict(title="target", range=[-1, 26]),
                      legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.8)"),
                      margin=dict(l=80, r=30, t=80, b=80))
    return fig, slope


if __name__ == "__main__":
    frames = [frame(k) for k in range(4)]
    s = [f[1] for f in frames]
    assert s[0] > s[1] > s[2] > s[3]                      # each outlier tilts the line further
    save_gif([f[0] for f in frames], "outlier_line", here, keys=[0, 1, 2, 3], fps=1, holds=[3, 3, 3, 6])
