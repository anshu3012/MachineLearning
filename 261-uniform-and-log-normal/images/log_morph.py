"""Taking the log, smoothly: the Note's 1,000 simulated comment lengths transformed by (x^lam - 1) / lam, which is
the raw data (shifted) at lam = 1 and tends to ln x as lam -> 0. The right-skewed histogram turns into a bell; the
skewness falls from 4.4 to about 0. Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from anim import save_gif, FONT, BLUE

here = Path(__file__).parent
words = np.round(np.random.default_rng(42).lognormal(mean=3, sigma=1, size=1000)).clip(1)   # as lognormal_check.py
LAMS = [1, 0.6, 0.35, 0.2, 0.1, 0]


def t(x, lam):
    return np.log(x) if lam == 0 else (x ** lam - 1) / lam


sk = [pd.Series(t(words, l)).skew() for l in LAMS]
assert round(sk[0], 1) == 4.4 and abs(sk[-1]) < 0.1 and all(a > b for a, b in zip(sk, sk[1:]))


def frame(i):
    lam = LAMS[i]
    y = t(words, lam)
    z = (y - y.mean()) / y.std()                     # standardize so every frame fits one axis
    fig = go.Figure(go.Histogram(x=z, xbins=dict(start=-4, end=10, size=0.25), marker_color=BLUE))
    label = "raw lengths" if lam == 1 else ("ln x: the log" if lam == 0 else f"(x<sup>{lam}</sup> − 1) / {lam}")
    fig.update_layout(template="simple_white", width=1000, height=560, font=FONT, bargap=0.05,
                      title=dict(text=f"<b>{label}</b>: skewness {sk[i]:.2f}", x=0.5),
                      xaxis=dict(title="value, standardized", range=[-4, 10]), yaxis=dict(title="comments", range=[0, 260]),
                      margin=dict(l=90, r=30, t=80, b=80))
    return fig


if __name__ == "__main__":
    save_gif([frame(i) for i in range(len(LAMS))], "log_morph", here, keys=[0, 2, 3, 5], fps=1, holds=[4, 2, 2, 2, 2, 6])
