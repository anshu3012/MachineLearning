"""The same correlation r = 0.30, more and more pairs (Plotly frames -> GIF). For each sample size n, the
correlation test's t = r sqrt(n - 2) / sqrt(1 - r^2) is placed on the t-distribution with n - 2 degrees of freedom.
At n = 30 it sits inside the 5% boundaries (p = 0.11); from n = 44 on it lands in the rejection region; at n = 100,
t = 3.11 and p = 0.002."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from gifkit import BLUE, FONT, GREEN, ORANGE, RED, make_gif

here = Path(__file__).parent
R = 0.30
tstat = lambda n: R * np.sqrt(n - 2) / np.sqrt(1 - R ** 2)
pval = lambda n: 2 * stats.t.sf(tstat(n), n - 2)
assert (round(tstat(30), 2), round(pval(30), 2), round(tstat(100), 2), round(pval(100), 3)) == (1.66, 0.11, 3.11, 0.002)
first = next(n for n in range(5, 200) if pval(n) <= 0.05)
assert first == 44, first
NS = [10, 20, 30, 40, 44, 60, 80, 100]
xs = np.linspace(-4.5, 4.5, 601)
ns_all = np.arange(5, 121)


def frame(n):
    t, p, crit = tstat(n), pval(n), stats.t.ppf(0.975, n - 2)
    sig = p <= 0.05
    fig = make_subplots(1, 2, column_widths=[0.55, 0.45], horizontal_spacing=0.1,
                        subplot_titles=[f"n = {n} pairs: t = {t:.2f} on t({n - 2})", "p-value against n (r = 0.30)"])
    fig.update_annotations(font_size=22)
    fig.add_trace(go.Scatter(x=xs, y=stats.t.pdf(xs, n - 2), mode="lines", line=dict(color=BLUE, width=4)), 1, 1)
    for side in (-1, 1):
        tail = xs[side * xs >= crit]
        fig.add_trace(go.Scatter(x=tail, y=stats.t.pdf(tail, n - 2), fill="tozeroy", mode="none",
                                 fillcolor="rgba(228,87,86,0.35)"), 1, 1)
    fig.add_trace(go.Scatter(x=[t, t], y=[0, 0.42], mode="lines", line=dict(color=GREEN if sig else ORANGE, width=5)), 1, 1)
    fig.add_annotation(x=t, y=0.42, text=f"p = {p:.3f}<br>{'reject H₀' if sig else 'fail to reject H₀'}",
                       showarrow=False, yanchor="bottom", font=dict(size=20, color=GREEN if sig else ORANGE), row=1, col=1)
    fig.add_trace(go.Scatter(x=ns_all, y=[pval(k) for k in ns_all], mode="lines", line=dict(color=BLUE, width=3)), 1, 2)
    fig.add_trace(go.Scatter(x=[0, 122], y=[0.05, 0.05], mode="lines", line=dict(color=RED, dash="dash", width=2)), 1, 2)
    fig.add_trace(go.Scatter(x=[n], y=[p], mode="markers", marker=dict(size=16, color=GREEN if sig else ORANGE)), 1, 2)
    fig.add_annotation(x=118, y=0.05, text="α = 0.05", showarrow=False, yshift=14, xanchor="right",
                       font=dict(size=18, color=RED), row=1, col=2)
    fig.update_xaxes(title="t", range=[-4.5, 4.5], row=1, col=1)
    fig.update_yaxes(title="density", range=[0, 0.52], row=1, col=1)
    fig.update_xaxes(title="number of pairs n", range=[0, 122], row=1, col=2)
    fig.update_yaxes(title="p-value", range=[0, 0.45], row=1, col=2)
    fig.update_layout(template="simple_white", width=1200, height=560, font=FONT, showlegend=False,
                      margin=dict(l=80, r=30, t=60, b=70))
    return fig


if __name__ == "__main__":
    make_gif([frame(n) for n in NS], here / "r_vs_n", fps=1, holds=[2, 1, 3, 1, 3, 1, 1, 5], keys=[2, len(NS) - 1], cols=1)
