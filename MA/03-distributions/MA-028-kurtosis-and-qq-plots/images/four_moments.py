"""Runs per match in two seasons: each panel keeps the earlier summary numbers equal and changes one more.
Left: same mean, different spread. Middle: same mean and spread, opposite skew. Right: same mean, spread
and skew, different tails (kurtosis)."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
BLUE, ORANGE = "#4C78A8", "#F58518"
x = np.linspace(0, 100, 800)


def same_mean_sd(dist, mean=40, sd=15):
    """Shift and scale a frozen distribution so it has the given mean and standard deviation."""
    m, s = dist.mean(), dist.std()
    return lambda v: dist.pdf((v - mean) / sd * s + m) * s / sd


panels = [
    ("Same mean, different spread", stats.norm(40, 15).pdf, stats.norm(40, 8).pdf, "sd 15", "sd 8"),
    ("Same mean and spread, opposite skew", same_mean_sd(stats.skewnorm(6)), same_mean_sd(stats.skewnorm(-6)),
     "right skew", "left skew"),
    ("Same mean, spread and skew, different tails", stats.norm(40, 15).pdf, same_mean_sd(stats.laplace()),
     "normal tails", "fat tails"),
]
fig = make_subplots(rows=1, cols=3, subplot_titles=[p[0] for p in panels], horizontal_spacing=0.06)
for col, (_, f1, f2, n1, n2) in enumerate(panels, start=1):
    for f, name, colour, dash in ((f1, n1, BLUE, "solid"), (f2, n2, ORANGE, "dash")):
        y = f(x)
        fig.add_scatter(x=x, y=y, mode="lines", line=dict(color=colour, width=3.5, dash=dash), row=1, col=col)
        i = int(np.argmax(y))
        shift = {"right skew": -14, "left skew": 16}.get(name, 0)      # keep the two skew labels apart
        fig.add_annotation(x=x[i] + shift, y=y[i], text=name, showarrow=False, yshift=14,
                           font=dict(size=17, color=colour), row=1, col=col)
    fig.add_vline(x=40, line=dict(color="#6B6B6B", width=1.5, dash="dot"), row=1, col=col)
# inset in the right panel: zoom on the right tail, where the fat-tailed curve lies above the normal one
tail = np.linspace(75, 100, 200)
dom = fig.layout.xaxis3.domain
fig.update_layout(xaxis4=dict(domain=[dom[0] + 0.19, dom[1]], anchor="y4", range=[75, 100], dtick=5,
                              tickfont=dict(size=13)),
                  yaxis4=dict(domain=[0.5, 0.88], anchor="x4", showticklabels=False, range=[0, 0.0021]))
for f, colour, dash in ((panels[2][1], BLUE, "solid"), (panels[2][2], ORANGE, "dash")):
    fig.add_scatter(x=tail, y=f(tail), mode="lines", line=dict(color=colour, width=3, dash=dash), xaxis="x4", yaxis="y4")
fig.add_annotation(x=87.5, y=0.0021, xref="x4", yref="y4", text="zoom: right tail", showarrow=False, yshift=12,
                   font=dict(size=14, color="#6B6B6B"))
for c in (1, 2, 3):
    fig.update_xaxes(title_text="runs in a match", range=[0, 100], dtick=20, row=1, col=c)
for c in (1, 2, 3):
    fig.update_yaxes(showticklabels=False, range=[0, 0.062], row=1, col=c)
fig.update_yaxes(title_text="density", row=1, col=1)
fig.update_annotations(selector=dict(xref="paper"), font_size=19)
fig.update_layout(template="simple_white", width=1250, height=430, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=50, r=20, t=50, b=50))
fig.write_image(here / "four_moments.png", scale=2)
fig.write_image(here / "four_moments.pdf")
