"""How Box-Cox picks lambda: each lambda tried gets a score, the log-likelihood (how well a normal curve explains the
transformed values); the learned lambda is the peak of that score curve.
Left: histogram of the concrete Age column (training set) after Box-Cox with the current lambda, standardised, with the
normal curve. Right: the log-likelihood (scipy.stats.boxcox_llf) of every lambda tried so far, and a marker at the current one.
Plotly frames -> ffmpeg GIF + _frames.png grid. Run: python likelihood_peak.py -> likelihood_peak.gif, likelihood_peak_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from scipy import stats
from sklearn.model_selection import train_test_split

HERE = Path(__file__).parent
BLUE, GREEN, RED, GREY = "#4C78A8", "#54A24B", "#E45756", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=22)

df = pd.read_csv(HERE.parent / "data" / "concrete_data.csv")
X_train, *_ = train_test_split(df.drop(columns=["Strength"]), df["Strength"], test_size=0.2, random_state=42)
AGE = X_train["Age"].values.astype(float)
LEARNED = stats.boxcox(AGE)[1]
assert round(LEARNED, 3) == 0.067
LAMS = np.round(np.arange(1.0, -0.81, -0.1), 2)                 # the lambdas tried, from 1 down to -0.8
LLF = np.array([stats.boxcox_llf(l, AGE) for l in LAMS])
BEST = stats.boxcox_llf(LEARNED, AGE)
assert BEST > LLF.max() - 1e-9                                  # the learned lambda is the peak
EDGES = np.arange(-5, 5.51, 0.5)
zgrid = np.linspace(-4, 4, 200)


def frame(k, final=False):                                      # k lambdas tried so far
    lam = LEARNED if final else LAMS[k - 1]
    t = stats.boxcox(AGE, lam)
    z = np.clip((t - t.mean()) / t.std(), -4.99, 5.49)
    share = np.histogram(z, EDGES)[0] / len(z)
    colour = GREEN if final else BLUE
    fig = make_subplots(1, 2, horizontal_spacing=0.14, subplot_titles=[
        "Age after Box-Cox (standardised)", "Score of each lambda tried"])
    fig.add_trace(go.Bar(x=EDGES[:-1] + 0.25, y=share, width=0.46, marker_color=colour, opacity=0.65), 1, 1)
    fig.add_trace(go.Scatter(x=zgrid, y=0.5 * stats.norm.pdf(zgrid), mode="lines", line=dict(color=RED, width=3)), 1, 1)
    fig.add_trace(go.Scatter(x=LAMS[:k], y=LLF[:k], mode="lines+markers", line=dict(color=GREY, width=3),
                             marker=dict(size=8, color=GREY)), 1, 2)
    fig.add_trace(go.Scatter(x=[lam], y=[BEST if final else LLF[k - 1]], mode="markers",
                             marker=dict(size=20, color=colour, line=dict(color="black", width=2))), 1, 2)
    if final:
        fig.add_annotation(x=lam, y=BEST, text=f"<b>peak: lambda = {LEARNED:.3f}</b>", showarrow=True, ax=0, ay=-45,
                           font=dict(color=GREEN, size=24), row=1, col=2)
    fig.update_xaxes(title="standardised value (red: normal curve)", range=[-5, 5.5], row=1, col=1)
    fig.update_yaxes(title="share of values", range=[0, 0.5], row=1, col=1)
    fig.update_xaxes(title="lambda", range=[-0.95, 1.1], row=1, col=2)
    fig.update_yaxes(title="log-likelihood (higher = more normal)", range=[LLF.min() - 150, BEST + 400], row=1, col=2)
    fig.update_annotations(font_size=23)
    head = (f"lambda = {LEARNED:.3f}: the highest score, the value PowerTransformer keeps" if final
            else f"Trying lambda = {lam:.1f}")
    fig.update_layout(template="simple_white", width=1300, height=600, font=FONT, showlegend=False, bargap=0,
                      title=dict(text=head, x=0.5, y=0.97), margin=dict(l=80, r=30, t=110, b=80))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".llf_frames"
    tmp.mkdir(exist_ok=True)
    n = len(LAMS)
    for k in range(1, n + 1):
        frame(k).write_image(tmp / f"{k - 1:03d}.png")
    frame(n, final=True).write_image(tmp / f"{n:03d}.png")
    for j in range(n + 1, n + 10):                              # hold the final frame
        shutil.copy(tmp / f"{n:03d}.png", tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "likelihood_peak.gif")], check=True)
    keys = [Image.open(tmp / f"{j:03d}.png").convert("RGB") for j in (0, 5, n - 4, n)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for j, im in enumerate(keys):
        sheet.paste(im, ((j % 2) * (w + 16), (j // 2) * (h + 16)))
    sheet.save(HERE / "likelihood_peak_frames.png")
    shutil.rmtree(tmp)
