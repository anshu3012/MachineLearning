"""What one leaf output minimises, animated (Plotly frames). The leaf of the XGBoost regression Note holding students 1
and 3 (residuals -2.875 and -1.375): its loss 1/2 * sum (r - w)^2 against the leaf output w (blue), the penalty
1/2 * lambda * w^2 (green) and their sum (black). As lambda grows from 0 to 10 the minimum of the sum slides from the
mean residual, -2.125, towards 0; it always sits at sum(r) / (n + lambda).
Run: python leaf_lambda.py  -> leaf_lambda.gif, leaf_lambda_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
BLUE, GREEN, RED = "#4C78A8", "#54A24B", "#E45756"
r = np.array([-2.875, -1.375])
w = np.linspace(-4, 1.5, 551)
loss = 0.5 * ((r[None, :] - w[:, None]) ** 2).sum(axis=1)
LAMBDAS = [0, 0.25, 0.5, 0.75, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 7, 8, 9, 10]


def frame(lam):
    pen = 0.5 * lam * w ** 2
    best = r.sum() / (len(r) + lam)
    assert abs(w[(loss + pen).argmin()] - best) < 0.011     # the formula is the minimum of the curve
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=w, y=loss, mode="lines", line=dict(color=BLUE, width=3), name="loss ½ Σ (r − w)²"))
    fig.add_trace(go.Scatter(x=w, y=pen, mode="lines", line=dict(color=GREEN, width=3), name="penalty ½ λ w²"))
    fig.add_trace(go.Scatter(x=w, y=loss + pen, mode="lines", line=dict(color="black", width=5), name="loss + penalty"))
    fig.add_trace(go.Scatter(x=[best], y=[0.5 * ((r - best) ** 2).sum() + 0.5 * lam * best ** 2], mode="markers",
                             marker=dict(color=RED, size=20), name="lowest point: the leaf output"))
    fig.add_vline(x=0, line=dict(color="grey", dash="dot", width=2))
    fig.update_xaxes(title_text="leaf output w", range=[-4, 1.5])
    fig.update_yaxes(title_text="value", range=[0, 15])
    fig.update_layout(template="simple_white", width=1100, height=640, font=dict(family="Latin Modern Roman", size=21),
                      title=dict(text=f"λ = {lam:g}:   w = Σr / (n + λ) = −4.25 / {2 + lam:g} = −{abs(best):.3f}", x=0.5, y=0.96,
                                 font_size=26),
                      margin=dict(l=80, r=30, t=80, b=130), legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".leaf_lambda_frames"
    tmp.mkdir(exist_ok=True)
    n, keys = 0, []
    for lam in LAMBDAS:
        rep = 5 if lam == 0 else 8 if lam == 10 else 3 if lam == 1 else 1
        frame(lam).write_image(tmp / f"{n:03d}.png")
        if lam in (0, 1, 4, 10):
            keys.append(Image.open(tmp / f"{n:03d}.png").convert("RGB"))
        for k in range(1, rep):
            shutil.copy(tmp / f"{n:03d}.png", tmp / f"{n + k:03d}.png")
        n += rep
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "4", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=800:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "leaf_lambda.gif")], check=True)
    wd, h = keys[0].size
    grid = Image.new("RGB", (2 * wd, 2 * h), "white")
    for i, im in enumerate(keys):
        grid.paste(im, ((i % 2) * wd, (i // 2) * h))
    grid.save(HERE / "leaf_lambda_frames.png")
    shutil.rmtree(tmp)
