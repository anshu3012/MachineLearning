"""The EWMA update, day by day, on the first 21 days of Delhi's 2013 temperatures (data/delhi_climate.csv): each day
the average V moves (1 - beta) = 10 percent of the way from yesterday's V towards today's value. beta = 0.9,
V_0 = theta_1. Plotly frames -> ffmpeg GIF, plus the final frame for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go

HERE = Path(__file__).parent
d = pd.read_csv(HERE.parent / "data" / "delhi_climate.csv")
theta = d.meantemp.values[:21]
BETA = 0.9
V = [theta[0]]
for x in theta[1:]:
    V.append(BETA * V[-1] + (1 - BETA) * x)
V = np.array(V)
ref = d.meantemp.ewm(alpha=0.1, adjust=False).mean().values[:21]
assert np.allclose(V, ref) and np.allclose(V[:5].round(2), [10.00, 9.74, 9.48, 9.40, 9.06])
days = np.arange(1, 22)


def frame(t):
    fig = go.Figure()
    fig.add_scatter(x=days[:t + 1], y=theta[:t + 1], mode="markers", name="daily temperature θ",
                    marker=dict(size=11, color="#F58518"))
    fig.add_scatter(x=days[:t + 1], y=V[:t + 1], mode="lines+markers", name="EWMA V (β = 0.9)",
                    line=dict(color="#4C78A8", width=4), marker=dict(size=8))
    if t > 0:
        fig.add_annotation(x=days[t], y=V[t], ax=days[t] - 1, ay=V[t - 1], xref="x", yref="y", axref="x", ayref="y",
                           showarrow=True, arrowhead=3, arrowwidth=2.5, arrowcolor="#4C78A8")
        fig.add_shape(type="line", x0=days[t], x1=days[t], y0=V[t - 1], y1=theta[t],
                      line=dict(color="#888", width=2, dash="dot"))
        gap, move = theta[t] - V[t - 1], V[t] - V[t - 1]
        title = (f"Day {t + 1}: today {theta[t]:.2f}, yesterday's average {V[t - 1]:.2f}<br>"
                 f"gap {gap:+.2f} °C, the average moves 10% of it: {move:+.2f} → V = <b>{V[t]:.2f}</b>")
    else:
        title = f"Day 1: start the average at the first value, V = {V[0]:.2f}<br> "
    fig.update_layout(template="simple_white", width=1050, height=620, font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text=title, x=0.5, y=0.95, font=dict(size=20)),
                      xaxis=dict(title="day of 2013", range=[0.3, 21.7], dtick=2),
                      yaxis=dict(title="temperature (°C)", range=[5, 19]),
                      legend=dict(x=0.02, y=0.98), margin=dict(l=80, r=30, t=110, b=70))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".es_frames"
    tmp.mkdir(exist_ok=True)
    keys = []
    for t in range(21):
        keys.append(tmp / f"t{t}.png")
        frame(t).write_image(keys[-1])
    seq = [0] * 2 + [t for t in range(1, 21) for _ in range(2 if t < 6 else 1)] + [20] * 5
    for j, t in enumerate(seq):
        shutil.copy(keys[t], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=820:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "ewma_steps.gif")], check=True)
    shutil.copy(keys[20], HERE / "ewma_steps_frames.png")
    shutil.rmtree(tmp)
    print(theta[:5].round(2), V[:5].round(2))
