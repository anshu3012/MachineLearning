"""What standardizing does to the 320 training users, drawn with one unit the same length on both axes (Plotly frames).
Raw, the salary spread is about 3,300 times the age spread, so the cloud is a thin vertical line. Step by step each
feature has its mean removed and is divided by its standard deviation; the cloud becomes round, with spread 1 both ways.
Run: python rescale.py -> rescale.gif, rescale_frames.png"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from common import BLUE, RED, save_gif

HERE = Path(__file__).parent
df = pd.read_csv(HERE.parent / "data" / "Social_Network_Ads.csv")
X, y = df[["Age", "EstimatedSalary"]].to_numpy(float), df["Purchased"].to_numpy()
X, _, y, _ = train_test_split(X, y, test_size=0.2, random_state=42)          # the Notebook's split
MU, SD = X.mean(0), X.std(0)
RATIO = SD[1] / SD[0]
assert len(X) == 320 and 3000 < RATIO < 3500
TS = np.linspace(0, 1, 21)


def at(t):
    return (X - t * MU) / SD ** t                                             # t = 0 raw, t = 1 standardized


def num(v):
    return f"{v:,.0f}" if v >= 100 else f"{v:.1f}"


def frame(t):
    D = at(t)
    c, half = (D.max(0) + D.min(0)) / 2, 1.15 * (D.max(0) - D.min(0)).max() / 2
    fig = go.Figure()
    for v, name, col, sym in ((0, "did not buy", BLUE, "circle"), (1, "bought", RED, "x")):
        m = y == v
        fig.add_trace(go.Scatter(x=D[m, 0], y=D[m, 1], mode="markers", name=name, marker=dict(color=col, symbol=sym, size=9, opacity=0.8)))
    s = D.std(0)
    step = "raw numbers" if t == 0 else ("standardized" if t == 1 else "rescaling each feature")
    fig.update_layout(template="simple_white", width=760, height=760, font=dict(family="Latin Modern Roman", size=22),
                      title=dict(text=f"{step}<br>spread of age <b>{num(s[0])}</b>,  spread of salary <b>{num(s[1])}</b>", x=0.5),
                      xaxis=dict(title="age", range=[c[0] - half, c[0] + half]),
                      yaxis=dict(title="salary", range=[c[1] - half, c[1] + half], scaleanchor="x", scaleratio=1),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.14), margin=dict(l=90, r=20, t=100, b=90))
    return fig


if __name__ == "__main__":
    figs = [frame(0)] * 4 + [frame(t) for t in TS[1:]]
    save_gif(figs, "rescale", [0, 12, 18, len(figs) - 1], HERE, fps=4, hold=10)
    print("spreads raw", SD.round(1), "ratio", round(RATIO))
