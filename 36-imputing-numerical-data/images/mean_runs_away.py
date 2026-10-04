"""Why the median for a skewed column: nine real training fares (every eighth quantile, from the smallest to the largest
fare) on a number line. The largest fare is then raised from 512 to 5,000: the mean runs after it, the median does not
move. Idea after Khan Academy, "Mean and standard deviation versus median and IQR" (nine salaries, the top one raised),
on our own data. Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from anim import save_gif, FONT, BLUE, RED, GREEN

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "titanic_toy.csv")
Xtr, _, _, _ = train_test_split(df.drop(columns="Survived"), df["Survived"], test_size=0.2, random_state=2)
f = Xtr.Fare.dropna().sort_values().to_numpy()
nine = f[np.linspace(0, len(f) - 1, 9).round().astype(int)]
assert np.allclose(nine, [0, 7.75, 7.8958, 10.5, 14.4583, 25.4667, 31.275, 69.55, 512.3292])
assert round(nine.mean(), 1) == 75.5 and round(np.median(nine), 2) == 14.46
EDGE = 600  # the axis stops here; a larger top fare is drawn at the edge with its value printed


def frame(top):
    v = np.r_[nine[:8], top]
    mean, med = v.mean(), np.median(v)
    fig = go.Figure()
    fig.add_scatter(x=v[:8], y=[0] * 8, mode="markers", marker=dict(size=20, color=BLUE, opacity=0.75))
    fig.add_scatter(x=[min(top, EDGE)], y=[0], mode="markers+text", marker=dict(size=20, color=RED),
                    text=[f"top fare {top:,.0f}" + (" →" if top > EDGE else "")], textposition="bottom left",
                    textfont=dict(size=21, color=RED))
    for x, col, lab, y in ((med, GREEN, f"median {med:.2f}", 0.95), (mean, RED, f"mean {mean:.1f}", 0.7)):
        fig.add_shape(type="line", x0=x, x1=x, y0=-0.04, y1=y - 0.1, line=dict(color=col, width=4), opacity=1)
        fig.add_annotation(x=x, y=y, text=f"<b>{lab}</b>", showarrow=False,
                           xanchor="left" if x < 400 else "right", font=dict(size=22, color=col))
    fig.update_layout(template="simple_white", width=1100, height=430, font=FONT, showlegend=False,
                      title=dict(text=f"<b>Nine fares; the largest is {top:,.0f}</b>", x=0.5),
                      xaxis=dict(title="Fare", range=[-15, EDGE + 15]), yaxis=dict(visible=False, range=[-0.4, 1.15]),
                      margin=dict(l=30, r=30, t=80, b=70))
    return fig


if __name__ == "__main__":
    tops = [nine[8], 1000, 2000, 3000, 5000]
    save_gif([frame(t) for t in tops], "mean_runs_away", here, keys=[0, 4], fps=1, holds=[4, 2, 2, 2, 6], cols=1, width=860)
