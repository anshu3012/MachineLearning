"""The medical test as a Bayes update (Plotly frames -> GIF). A test with sensitivity 0.9 and false positive rate 0.09
(Bayes factor 0.9 / 0.09 = 10) is given to 1000 women. The prevalence (the prior) rises from 1 in 1000 to 1 in 10.
Left: expected true positives and false positives. Right: P(cancer | positive) against the prevalence. The title
gives the same update in odds: prior odds x 10 = posterior odds."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import FONT, GREY, RED, make_gif

here = Path(__file__).parent
SENS, FPR, N = 0.9, 0.09, 1000


def ppv(p):
    return SENS * p / (SENS * p + FPR * (1 - p))


assert round(ppv(0.01), 3) == 0.092 and round(ppv(0.1), 2) == 0.53 and round(ppv(0.001), 2) == 0.01
assert abs(ppv(0.01) - 10 / (10 + 99)) < 1e-12          # odds form: 1 : 99 times 10 = 10 : 99
grid = np.logspace(-3, -1, 100)


def frame(k):                                            # prevalence = 1 in k
    p = 1 / k
    tp, fp = SENS * p * N, FPR * (1 - p) * N
    fig = make_subplots(1, 2, column_widths=[0.42, 0.58], horizontal_spacing=0.14,
                        subplot_titles=["positive tests among 1000 women", "P(cancer | positive test)"])
    fig.update_annotations(font_size=21)
    fig.add_trace(go.Bar(x=["true positives", "false positives"], y=[tp, fp], marker_color=[RED, GREY],
                         text=[f"{tp:.1f}".rstrip("0").rstrip("."), f"{fp:.0f}"], textposition="outside", showlegend=False), 1, 1)
    fig.add_trace(go.Scatter(x=grid, y=ppv(grid), mode="lines", line=dict(color=RED, width=4), showlegend=False), 1, 2)
    fig.add_trace(go.Scatter(x=[p], y=[ppv(p)], mode="markers+text", text=[f"{ppv(p):.3f}"], textposition="top left", textfont=dict(size=24),
                             marker=dict(size=18, color=RED, line=dict(color="black", width=2)), showlegend=False), 1, 2)
    fig.update_yaxes(range=[0, 105], row=1, col=1)
    fig.update_yaxes(range=[0, 0.62], row=1, col=2)
    fig.update_xaxes(type="log", range=[-3.03, -0.9], title="prevalence (the prior)", tickvals=[0.001, 0.01, 0.1], ticktext=["1 in 1000", "1 in 100", "1 in 10"], row=1, col=2)
    fig.update_layout(template="simple_white", width=1200, height=600, font=FONT, margin=dict(l=60, r=30, t=130, b=70),
                      title=dict(text=f"prior 1 in {k}: odds 1 : {k - 1}, times 10 gives 10 : {k - 1}, so 10 of {k + 9} = {ppv(p):.3f}", x=0.5, font=dict(size=25)))
    return fig


if __name__ == "__main__":
    ks = [1000, 500, 200, 100, 50, 20, 10]
    make_gif([frame(k) for k in ks], here / "medical", fps=1, holds=[2, 1, 1, 4, 1, 1, 4], keys=[3, 6], cols=1)
