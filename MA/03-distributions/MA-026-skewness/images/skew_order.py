"""Mode, median and mean in three shapes: left skew (easy-exam marks, simulated), symmetric (simulated normal),
right skew (Titanic fares). In a skewed column the mean is pulled furthest towards the tail."""
from pathlib import Path
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED = "#4C78A8", "#F58518", "#54A24B", "#E45756"
rng = np.random.default_rng(42)
marks = np.round(100 * rng.beta(5, 1.5, 1000), 1)
sym = rng.normal(50, 10, 1000)
fare = pd.read_csv(here.parent / "data" / "titanic_train.csv")["Fare"].to_numpy()


def kde_mode(x, lo, hi):
    """Mode of a continuous column: the peak of its KDE."""
    g = np.linspace(lo, hi, 4001)
    return g[np.argmax(stats.gaussian_kde(x)(g))]


cases = [  # (title, data, mode, x range, bin size)
    ("Left skew: easy-exam marks", marks, kde_mode(marks, 0, 100), (20, 100), 2.5),
    ("Symmetric", sym, kde_mode(sym, 0, 100), (15, 85), 2.5),
    ("Right skew: Titanic fares", fare, pd.Series(fare).mode()[0], (0, 150), 5),
]
fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.06,
                    subplot_titles=[f"{t} (skew {pd.Series(d).skew():.2f})" for t, d, *_ in cases])
for col, (_, d, mode, (lo, hi), size) in enumerate(cases, start=1):
    fig.add_histogram(x=d[(d >= lo) & (d <= hi)], xbins=dict(start=lo, end=hi, size=size),
                      histnorm="probability density", marker=dict(color=BLUE, opacity=0.45), row=1, col=col)
    marks_ = [("mode", mode, GREEN, "dot"), ("median", np.median(d), ORANGE, "dash"), ("mean", d.mean(), RED, "solid")]
    for i, (name, v, colour, dash) in enumerate(marks_):
        fig.add_vline(x=v, line=dict(color=colour, width=3, dash=dash), layer="above", opacity=1, row=1, col=col)
        fig.add_annotation(x={1: 22, 2: 64, 3: 60}[col], y=1.0 - 0.09 * i, yref=f"y{'' if col == 1 else col} domain", text=f"{name} {v:.1f}",
                           showarrow=False, xanchor="left",
                           font=dict(size=15, color=colour), bgcolor="rgba(255,255,255,0.85)", row=1, col=col)
    fig.update_xaxes(range=[lo, hi], row=1, col=col)
    fig.update_yaxes(showticklabels=False, row=1, col=col)
fig.update_xaxes(title_text="marks", row=1, col=1)
fig.update_xaxes(title_text="value", row=1, col=2)
fig.update_xaxes(title_text="fare", row=1, col=3)
fig.update_yaxes(title_text="density", row=1, col=1)
fig.update_annotations(selector=dict(xref="paper"), font_size=18)
fig.update_layout(template="simple_white", width=1300, height=440, showlegend=False, bargap=0.03,
                  font=dict(family="Latin Modern Roman", size=16), margin=dict(l=60, r=20, t=50, b=50))
fig.write_image(here / "skew_order.png", scale=2)
fig.write_image(here / "skew_order.pdf")
