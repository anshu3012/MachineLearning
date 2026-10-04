"""All coefficients move at every step (Plotly frames -> GIF): batch gradient descent of Section 4 on the diabetes
data. Bars: the 10 coefficients after each epoch, all updated together from their start at 1; diamonds: the OLS
values. Title: the intercept, which starts at 0 and heads for about 152."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, ORANGE, make_gif
from run58 import HIST, NAMES, ols

here = Path(__file__).parent
EP = [0, 1, 2, 3, 5, 10, 20, 50, 100, 200, 500, 1000]


def frame(e):
    b, w, r2 = HIST[e]
    fig = go.Figure(go.Bar(x=NAMES, y=w, marker_color=BLUE, name="gradient descent"))
    fig.add_scatter(x=NAMES, y=ols.coef_, mode="markers", name="OLS (exact)",
                    marker=dict(symbol="diamond", size=16, color=ORANGE, line=dict(color="white", width=1.5)))
    fig.update_layout(template="simple_white", width=1100, height=560, font=FONT,
                      title=dict(text=f"epoch {e}: intercept β₀ = {b:.1f}, test R² = {r2:.3f}", x=0.5),
                      xaxis=dict(title="feature"), yaxis=dict(title="coefficient", range=[-1000, 1000]),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.18), margin=dict(l=80, r=30, t=70, b=120))
    return fig


if __name__ == "__main__":
    assert np.abs(ols.coef_).max() < 1000 and max(np.abs(h[1]).max() for h in HIST) < 1000
    make_gif([frame(e) for e in EP], here / "coef_steps", fps=2, holds=[3] + [1] * (len(EP) - 2) + [6], keys=[8, len(EP) - 1])
