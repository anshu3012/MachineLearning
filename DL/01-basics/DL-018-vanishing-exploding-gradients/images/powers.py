"""One number multiplied by itself k times, k = 1 to 50 (Plotly frames): 2^k explodes, 1^k stays, 0.5^k vanishes.
The marked values: 2^4 = 16, 2^50 = 1.1e15, 0.5^50 = 8.9e-16.
Run: python powers.py -> powers.gif, powers_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from common import BLUE, RED, GREY, save_gif

HERE = Path(__file__).parent
assert 2 ** 4 == 16 and f"{2.0 ** 50:.1e}" == "1.1e+15" and f"{0.5 ** 50:.1e}" == "8.9e-16"
k = np.arange(0, 51)


def sci(v):
    if 0.01 <= v <= 1000:
        return f"{v:g}"
    m, e = f"{v:.1e}".split("e")
    return f"{m} × 10<sup>{int(e)}</sup>".replace("-", "−")


def frame(n):
    fig = go.Figure()
    for w, col, name in ((2.0, BLUE, "2"), (1.0, GREY, "1"), (0.5, RED, "0.5")):
        fig.add_trace(go.Scatter(x=k[:n + 1], y=w ** k[:n + 1], mode="lines", line=dict(color=col, width=5),
                                 name=f"{name} multiplied {n} times = {sci(w ** n)}"))
        fig.add_trace(go.Scatter(x=[n], y=[w ** n], mode="markers", marker=dict(color=col, size=14), showlegend=False))
    fig.update_layout(template="simple_white", width=1000, height=600, font=dict(family="Latin Modern Roman", size=24),
                      title=dict(text=f"the same factor used <b>{n}</b> times", x=0.5),
                      xaxis=dict(title="k, how many times the factor is used", range=[0, 51]),
                      yaxis=dict(title="product (log scale)", type="log", range=[-17, 17], dtick=4, exponentformat="power"),
                      legend=dict(x=0.02, y=0.02, yanchor="bottom", bgcolor="rgba(255,255,255,0.85)"), margin=dict(l=90, r=20, t=70, b=70))
    return fig


if __name__ == "__main__":
    ns = [1, 2, 3, 4] + list(range(6, 51, 2))
    save_gif([frame(n) for n in ns], "powers", [3, len(ns) - 1], HERE, fps=4, hold=10, cols=2)
