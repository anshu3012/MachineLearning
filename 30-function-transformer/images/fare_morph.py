"""The training-set Titanic fares sliding from raw values to log(1 + x): the histogram's long right tail is pulled in
(left) while the Q-Q plot straightens (right). Each fare moves along (1 - t) * raw + t * log1p, both rescaled to 0-1 so
one axis fits every frame; skewness and the Q-Q shape do not depend on that rescaling. Our own design.
Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from sklearn.model_selection import train_test_split
from anim import save_gif, FONT, BLUE, GREEN, RED

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "titanic_train.csv", usecols=["Age", "Fare", "Survived"])
X_train, _ = train_test_split(df[["Age", "Fare"]], test_size=0.2, random_state=42)
raw = X_train["Fare"].to_numpy()
logged = np.log1p(raw)
assert len(raw) == 712 and round(stats.skew(raw, bias=False), 2) == 4.88 and round(stats.skew(logged, bias=False), 2) == 0.40
a, b = raw / raw.max(), logged / logged.max()


def frame(t, head):
    u = (1 - t) * a + t * b
    col = GREEN if t == 1 else BLUE
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12, subplot_titles=["Histogram", "Q-Q plot"])
    fig.add_histogram(x=u, xbins=dict(start=0, end=1.0001, size=0.025), marker_color=col, opacity=0.7, row=1, col=1)
    (osm, osr), (slope, intercept, _) = stats.probplot(u, dist="norm")
    fig.add_scatter(x=osm, y=osr, mode="markers", marker=dict(color=col, size=6, opacity=0.6), row=1, col=2)
    fig.add_scatter(x=osm[[0, -1]], y=slope * osm[[0, -1]] + intercept, mode="lines", line=dict(color=RED, width=3), row=1, col=2)
    fig.update_xaxes(title="fare (rescaled to 0-1)", range=[-0.02, 1.02], row=1, col=1)
    fig.update_yaxes(title="passengers", range=[0, 330], row=1, col=1)
    fig.update_xaxes(title="normal quantiles", row=1, col=2)
    fig.update_yaxes(title="fare quantiles", range=[-0.35, 1.05], row=1, col=2)
    fig.update_annotations(font_size=22)
    fig.update_layout(template="simple_white", width=1200, height=560, font=FONT, showlegend=False, bargap=0.03,
                      title=dict(text=f"<b>{head}</b>   skewness {stats.skew(u, bias=False):.2f}", x=0.5),
                      margin=dict(l=80, r=30, t=110, b=70))
    return fig


if __name__ == "__main__":
    ts = np.linspace(0, 1, 9)
    figs = [frame(0, "Raw fare")] + [frame(t, "Towards log(1 + x)") for t in ts[1:-1]] + [frame(1, "log(1 + fare)")]
    save_gif(figs, "fare_morph", here, keys=[0, 4, 8], fps=2, holds=[4] + [1] * 7 + [10], cols=1, width=900)
