"""Mean and variance are both lambda, watched on the Notebook's simulation (Plotly frames -> GIF): 100,000 days
drawn with rng.poisson(lam=4), seed 42. As more days are added, the histogram settles onto the Poisson PMF (dots)
and the running mean and variance both settle near 4 (3.994 and 3.987 at 100,000 days)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from gifkit import BLUE, FONT, GREEN, ORANGE, RED, make_gif

here = Path(__file__).parent
rng = np.random.default_rng(42)
days = rng.poisson(lam=4, size=100_000)
assert round(days.mean(), 3) == 3.994 and round(days.var(), 3) == 3.987
NS = [10, 30, 100, 300, 1000, 3000, 10_000, 30_000, 100_000]
grid = np.unique(np.logspace(1, 5, 120).astype(int))
run_mean = [days[:n].mean() for n in grid]
run_var = [days[:n].var() for n in grid]
y = np.arange(0, 15)


def frame(n):
    d = days[:n]
    fig = make_subplots(1, 2, horizontal_spacing=0.1, column_widths=[0.5, 0.5],
                        subplot_titles=[f"{n:,} simulated days", "running mean and variance"])
    fig.update_annotations(font_size=22)
    share = np.bincount(d, minlength=15)[:15] / n
    fig.add_trace(go.Bar(x=y, y=share, marker_color=BLUE, name="share of days"), 1, 1)
    fig.add_trace(go.Scatter(x=y, y=stats.poisson.pmf(y, 4), mode="markers", marker=dict(size=12, color=RED),
                             name="Poisson PMF, λ = 4"), 1, 1)
    k = grid <= n
    fig.add_trace(go.Scatter(x=grid[k], y=np.array(run_mean)[k], mode="lines", line=dict(color=ORANGE, width=4),
                             name=f"mean = {d.mean():.3f}"), 1, 2)
    fig.add_trace(go.Scatter(x=grid[k], y=np.array(run_var)[k], mode="lines", line=dict(color=GREEN, width=4),
                             name=f"variance = {d.var():.3f}"), 1, 2)
    fig.add_hline(y=4, line=dict(color="black", dash="dash"), row=1, col=2)
    fig.update_xaxes(title="questions in one day", row=1, col=1)
    fig.update_yaxes(title="share of days", range=[0, 0.36], row=1, col=1)
    fig.update_xaxes(title="days simulated (log scale)", type="log", range=[1, 5], row=1, col=2)
    fig.update_yaxes(range=[1.5, 6.5], row=1, col=2)
    fig.update_layout(template="simple_white", width=1200, height=560, font=FONT,
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2), margin=dict(l=70, r=30, t=60, b=130))
    return fig


if __name__ == "__main__":
    make_gif([frame(n) for n in NS], here / "mean_var_sim", fps=1, holds=[1] * (len(NS) - 1) + [4],
             keys=[len(NS) - 1], cols=1)
