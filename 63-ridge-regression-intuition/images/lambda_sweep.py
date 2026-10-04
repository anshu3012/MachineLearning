"""Ridge on the two training points (1, 2) and (3, 5): as lambda grows, the best line pivots about the mean point
(2, 3.5) and flattens; the bars show the trade between squared errors and the penalty lambda * m^2
(Plotly frames + ffmpeg -> lambda_sweep.gif, lambda_sweep_frames.png).
With the intercept unpenalised the best slope is m = Sxy / (Sxx + lambda) = 3 / (2 + lambda).
Idea: Starmer, J. (StatQuest), "Regularization Part 1: Ridge (L2) Regression"."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from sklearn.linear_model import Ridge

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
xtr, ytr = np.array([1.0, 3.0]), np.array([2.0, 5.0])
LAMS = np.r_[np.zeros(4), np.linspace(0, 1, 6), np.geomspace(1.2, 30, 16), np.full(8, 30.0)]


def fit(lam):
    m = 3 / (2 + lam)
    b = 3.5 - 2 * m
    sse = float(((ytr - m * xtr - b) ** 2).sum())
    return m, b, sse, lam * m ** 2


for lam in (0.5, 1, 10):                                     # the closed form agrees with scikit-learn
    r = Ridge(alpha=lam).fit(xtr[:, None], ytr)
    assert np.isclose(r.coef_[0], fit(lam)[0]) and np.isclose(r.intercept_, fit(lam)[1])
assert np.isclose(sum(fit(1)[2:]), 1.5)                       # lambda = 1: best loss 1.5, below the slope-0.9 line's 1.53


def frame(lam):
    m, b, sse, pen = fit(lam)
    fig = make_subplots(1, 2, column_widths=[0.62, 0.38], horizontal_spacing=0.12,
                        subplot_titles=(f"λ = {lam:.1f}:  slope m = {m:.2f}", "Ridge loss = errors + λm²"))
    xs = np.array([0, 4])
    fig.add_trace(go.Scatter(x=xs, y=1.5 * xs + 0.5, mode="lines", line=dict(color=GREY, width=2, dash="dot")), 1, 1)
    for a, t in zip(xtr, ytr):                                  # error sticks
        fig.add_trace(go.Scatter(x=[a, a], y=[t, m * a + b], mode="lines", line=dict(color=RED, width=3)), 1, 1)
    fig.add_trace(go.Scatter(x=xs, y=m * xs + b, mode="lines", line=dict(color=GREEN, width=5)), 1, 1)
    fig.add_trace(go.Scatter(x=xtr, y=ytr, mode="markers", marker=dict(size=16, color=BLUE)), 1, 1)
    fig.add_trace(go.Scatter(x=[2], y=[3.5], mode="markers", marker=dict(size=10, color=GREY, symbol="x")), 1, 1)
    fig.add_trace(go.Bar(x=["errors", "λm²", "total"], y=[sse, pen, sse + pen], marker_color=[RED, ORANGE, GREEN],
                         width=0.6, text=[f"{v:.2f}" for v in (sse, pen, sse + pen)], textposition="outside",
                         textfont=dict(size=22)), 1, 2)
    fig.add_annotation(x=0.2, y=6.9, text="dotted: least squares, m = 1.5", showarrow=False, xanchor="left",
                       font=dict(size=18, color=GREY), row=1, col=1)
    fig.update_xaxes(title="x", range=[0, 4], row=1, col=1)
    fig.update_yaxes(title="y", range=[0, 7.5], row=1, col=1)
    fig.update_yaxes(range=[0, 5.4], row=1, col=2)
    fig.update_layout(template="simple_white", width=1100, height=540, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=20), margin=dict(l=70, r=30, t=70, b=60))
    fig.update_annotations(font_size=22)
    return fig


if __name__ == "__main__":
    for lam in (0, 1, 2, 10, 30):
        print(lam, [round(v, 3) for v in fit(lam)])
    tmp = HERE / ".lam_frames"
    tmp.mkdir(exist_ok=True)
    for k, lam in enumerate(LAMS):
        frame(lam).write_image(tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "5", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=880:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "lambda_sweep.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (0, 9, 16, len(LAMS) - 1)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "lambda_sweep_frames.png")
    shutil.rmtree(tmp)
