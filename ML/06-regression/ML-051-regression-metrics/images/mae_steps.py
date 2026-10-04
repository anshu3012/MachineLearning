"""How MAE is computed, step by step on the 40 test errors (Plotly frames -> GIF). 1: the signed errors, some
positive, some negative. 2: their plain average is close to 0 because they cancel. 3: drop the sign: every bar
points up. 4: the average of the sizes is MAE = 0.288 LPA."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from common import pred, y
from gifkit import BLUE, FONT, GREEN, GREY, RED, make_gif

here = Path(__file__).parent
e = y - pred
order = np.argsort(-np.abs(e))                          # biggest errors first
e = e[order]
MAE, MEAN = np.abs(e).mean(), e.mean()
assert round(MAE, 3) == 0.288 and round(MEAN, 3) == -0.041
first = np.flatnonzero(order == 0)[0]                   # the first test student: error 4.10 - 3.89 = 0.21
assert round(e[first], 2) == 0.21


def frame(step, k=40):
    v = np.abs(e) if step >= 3 else e
    cols = [GREEN if step >= 3 else (BLUE if s > 0 else RED) for s in e]
    fig = go.Figure(go.Bar(x=np.arange(1, 41), y=v, marker_color=cols, width=0.8))
    title = {1: "step 1: the 40 errors, actual − predicted",
             2: f"step 2: their plain average is {MEAN:+.3f}: they cancel",
             3: "step 3: drop the sign: |actual − predicted|",
             4: f"step 4: average the sizes: MAE = {MAE:.3f} LPA"}[step]
    if step == 2:
        fig.add_hline(y=MEAN, line=dict(color="black", width=3, dash="dash"))
    if step == 4:
        fig.add_hline(y=MAE, line=dict(color="black", width=3, dash="dash"))
        fig.add_annotation(x=38, y=MAE, text=f"MAE = {MAE:.3f}", showarrow=False, yshift=18, font=dict(size=24))
    fig.add_annotation(x=first + 1, y=v[first], text="first test student<br>4.10 − 3.89 = 0.21", ax=70, ay=-70,
                       font=dict(size=18))
    fig.update_layout(template="simple_white", width=1000, height=560, font=FONT, title=dict(text=title, x=0.5),
                      xaxis=dict(title="test students, largest error first", showticklabels=False),
                      yaxis=dict(title="error (LPA)", range=[-1.05, 1.05], zeroline=True, zerolinewidth=2),
                      margin=dict(l=80, r=30, t=80, b=60))
    return fig


if __name__ == "__main__":
    assert np.abs(e).max() < 1.05
    make_gif([frame(s) for s in (1, 2, 3, 4)], here / "mae_steps", fps=1, holds=[3, 3, 3, 5], keys=[0, 1, 2, 3])
