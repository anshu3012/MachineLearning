"""Section 6: drag one point away from the 30 points that follow y = 2x + 1 (Figure 3's data, outliers left out),
until its error is 42 (the 50-lakh student). Refit the line with MSE and with MAE each time. MSE chases the point;
MAE barely moves. Plotly frames -> outlier_drag.gif + _frames.png"""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import QuantileRegressor
from common import BLUE, ORANGE, RED, GREY, FONT, save_gif

here = Path(__file__).parent
d = np.load(here.parent / "data" / "outlier_fit.npz")
x0, y0 = d["x"][~d["is_out"]], d["y"][~d["is_out"]]
xo = 9.0                                                   # the dragged point sits at x = 9
LIFTS = [0, 3, 6, 10, 15, 20, 26, 32, 37, 42]
fits = []
for lift in LIFTS:
    x, y = np.append(x0, xo), np.append(y0, 2 * xo + 1 + lift)
    mse = np.polyfit(x, y, 1)
    q = QuantileRegressor(quantile=0.5, alpha=0, solver="highs").fit(x[:, None], y)
    fits.append((lift, mse, np.array([q.coef_[0], q.intercept_])))
at = lambda p: p[0] * xo + p[1]                            # each line's height at the dragged point
mse_move = at(fits[-1][1]) - at(fits[0][1])
mae_move = at(fits[-1][2]) - at(fits[0][2])
assert round(mse_move, 1) == 3.7 and abs(mae_move) < 0.01      # the numbers in the Note text
print(f"line height at x = 9 moved: MSE {mse_move:.2f}, MAE {mae_move:.2f}")


def frame(k):
    lift, mse, mae = fits[k]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x0, y=y0, mode="markers", marker=dict(color=GREY, size=9), name="30 normal points"))
    fig.add_trace(go.Scatter(x=[xo], y=[2 * xo + 1 + lift], mode="markers", marker=dict(color=RED, size=16, symbol="diamond"),
                             name=f"dragged point: {lift} above"))
    xs = np.array([0, 10])
    fig.add_trace(go.Scatter(x=xs, y=np.polyval(mse, xs), mode="lines", line=dict(color=BLUE, width=5),
                             name=f"MSE line: ŷ = {mse[0]:.2f}x {mse[1]:+.2f}"))
    fig.add_trace(go.Scatter(x=xs, y=np.polyval(mae, xs), mode="lines", line=dict(color=ORANGE, width=5, dash="dash"),
                             name=f"MAE line: ŷ = {mae[0]:.2f}x {mae[1]:+.2f}"))
    fig.update_layout(template="simple_white", width=950, height=620, font=dict(FONT, size=20),
                      title=dict(text=f"one point lifted {lift} above the pattern", x=0.5),
                      xaxis=dict(title="x", range=[0, 10.3]), yaxis=dict(title="y", range=[-1, 63]),
                      legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.85)"), margin=dict(l=70, r=30, t=70, b=60))
    return fig


if __name__ == "__main__":
    save_gif([frame(k) for k in range(len(fits))], "outlier_drag", [0, len(fits) - 1], here, fps=2)
