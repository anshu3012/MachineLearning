"""Wisdom of the crowd with numbers (section 2): simulated guesses of an ox's weight. The true weight is
1,198 lb (Galton 1907); each simulated guess is the truth plus a random error with standard deviation 75 lb
(our choice, for illustration). The crowd grows 1 -> 5 -> 25 -> 100 -> 800 guessers; the mean of the guesses
closes in on the true weight. The typical error printed in each frame is the mean absolute error of the crowd's
mean over 2,000 simulated crowds of that size, so it does not depend on one lucky draw.
Run: python crowd_guess.py -> crowd_guess.gif, crowd_guess_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
TRUE, SD, SIZES = 1198, 75, [1, 5, 25, 100, 800]
BLUE, RED = "#4C78A8", "#E45756"
rng = np.random.default_rng(0)
guesses = TRUE + rng.normal(0, SD, SIZES[-1])                       # one crowd, revealed a few at a time
typical = {n: np.abs(rng.normal(0, SD, (2000, n)).mean(axis=1)).mean() for n in SIZES}
assert typical[1] > typical[5] > typical[25] > typical[100] > typical[800]
print({n: round(v, 1) for n, v in typical.items()})


def frame(n):
    g = guesses[:n]
    counts, edges = np.histogram(g, bins=np.arange(948, 1449, 20))
    fig = go.Figure(go.Bar(x=(edges[:-1] + edges[1:]) / 2, y=counts, width=18, marker_color=BLUE, opacity=0.75,
                           showlegend=False))
    top = max(counts.max() * 1.45, 2)
    fig.add_trace(go.Scatter(x=[TRUE, TRUE], y=[0, top], mode="lines", line=dict(color=RED, width=4, dash="dash"),
                             name=f"true weight {TRUE:,} lb"))
    fig.add_trace(go.Scatter(x=[g.mean()] * 2, y=[0, top], mode="lines", line=dict(color="black", width=4),
                             name=f"mean of the guesses {g.mean():,.0f} lb"))
    who = "one guesser" if n == 1 else f"a crowd of {n}"
    fig.add_annotation(xref="paper", yref="paper", x=0.5, y=-0.3, showarrow=False, font=dict(size=28),
                       text=f"typical error of {who}: <b>{typical[n]:.0f} lb</b>")
    fig.update_xaxes(title="guessed weight (lb)", range=[940, 1456])
    fig.update_yaxes(title="number of guesses", range=[0, top])
    fig.update_layout(template="simple_white", width=1100, height=700, barmode="overlay",
                      font=dict(family="Latin Modern Roman", size=24, color="black"),
                      legend=dict(x=0.01, y=0.99, font_size=24),
                      title=dict(text=f"<b>{n} guess{'es' if n > 1 else ''}</b>", x=0.5, y=0.96, font_size=32),
                      margin=dict(l=90, r=20, t=80, b=170))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".crowd_guess"
    tmp.mkdir(exist_ok=True)
    keys, i = [], 0
    for n, hold in zip(SIZES, [3, 3, 3, 3, 7]):
        png = tmp / f"{i:03d}.png"
        frame(n).write_image(png)
        if n != 5:
            keys.append(Image.open(png).convert("RGB"))
        for k in range(1, hold):
            shutil.copy(png, tmp / f"{i + k:03d}.png")
        i += hold
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "%03d.png"), "-vf",
                    "fps=5,scale=800:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "crowd_guess.gif")], check=True)
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for j, f in enumerate(keys):
        sheet.paste(f, ((j % 2) * (w + 16), (j // 2) * (h + 16)))
    sheet.save(HERE / "crowd_guess_frames.png")
    shutil.rmtree(tmp)
