"""Adam (eta = 0.5, beta1 = 0.9, beta2 = 0.999) on the students data from (m, b) = (-4, -4), with and without bias
correction. Left: both paths. Right, for the bias b of the corrected run: the gradient, the raw EWMA m and the
corrected m-hat (top); the size of the gradient, sqrt(v) and sqrt(v-hat) (bottom).
Run: python adam_moments.py -> adam_moments.gif, adam_moments_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from common import ORANGE, RED, GREY, FONT
from shared import X, y, BEST, START, grad, run, steps_to

HERE = Path(__file__).parent
ETA, B1, B2, SHOW = 0.5, 0.9, 0.999, 45


def adam(correct, steps=300):
    p, m, v, P, rec = START.copy(), np.zeros(2), np.zeros(2), [START.copy()], []
    for t in range(1, steps + 1):
        g = grad(p)
        m = B1 * m + (1 - B1) * g
        v = B2 * v + (1 - B2) * g ** 2
        mh, vh = (m / (1 - B1 ** t), v / (1 - B2 ** t)) if correct else (m, v)
        p = p - ETA * mh / (np.sqrt(vh) + 1e-8)
        P.append(p.copy())
        rec.append((g[1], m[1], m[1] / (1 - B1 ** t), np.sqrt(v[1]), np.sqrt(v[1] / (1 - B2 ** t))))
    return np.array(P), np.array(rec)


P, REC = adam(True)
PU, _ = adam(False)
assert np.allclose(P, run("adam", ETA))                    # same run as the Note's Figure 1
DONE, DONE_U = steps_to(P), steps_to(PU)
FIRST, FIRST_U = np.linalg.norm(P[1] - P[0]), np.linalg.norm(PU[1] - PU[0])
print(DONE, DONE_U, round(FIRST, 2), round(FIRST_U, 2), "max b without correction:", PU[:10, 1].max().round(2))
mm, bb = np.linspace(-5, 10.5, 170), np.linspace(-5, 9, 160)
M, B = np.meshgrid(mm, bb)
Z = np.log10(((y[None, None, :] - M[..., None] * X[:, 0] - B[..., None]) ** 2).mean(-1))
t_all = np.arange(1, len(REC) + 1)


def frame(k):
    fig = make_subplots(rows=2, cols=2, column_widths=[0.52, 0.48], specs=[[{"rowspan": 2}, {}], [None, {}]],
                        subplot_titles=["", "gradient of b and its average", "size of b's gradient and √v"],
                        horizontal_spacing=0.12, vertical_spacing=0.2)
    fig.update_annotations(font_size=24)
    fig.add_trace(go.Contour(x=mm, y=bb, z=Z, colorscale="Greys", reversescale=True, showscale=False,
                             contours=dict(start=-0.6, end=2.4, size=0.2), line=dict(width=0.6), opacity=0.5), 1, 1)
    fig.add_trace(go.Scatter(x=PU[:k + 1, 0], y=PU[:k + 1, 1], mode="lines+markers", name="raw averages, no correction",
                             line=dict(color=ORANGE, width=3, dash="dot"), marker=dict(size=6)), 1, 1)
    fig.add_trace(go.Scatter(x=P[:k + 1, 0], y=P[:k + 1, 1], mode="lines+markers", name="corrected averages (Adam)",
                             line=dict(color=RED, width=3), marker=dict(size=6)), 1, 1)
    fig.add_trace(go.Scatter(x=[BEST[0]], y=[BEST[1]], mode="markers", showlegend=False,
                             marker=dict(symbol="star", size=18, color="black")), 1, 1)
    t, R = t_all[:k], REC[:k]
    for row, (raw, cor, gcol, top) in enumerate(((1, 2, R[:, 0], (-17, 5)), (3, 4, np.abs(R[:, 0]), (0, 17))), 1):
        fig.add_trace(go.Scatter(x=t, y=gcol, mode="markers", marker=dict(color=GREY, size=7), showlegend=row == 1,
                                 name="gradient (its size below)"), row, 2)
        fig.add_trace(go.Scatter(x=t, y=R[:, raw], mode="lines+markers", marker=dict(size=4), line=dict(color=ORANGE, width=3, dash="dot"),
                                 showlegend=False), row, 2)
        fig.add_trace(go.Scatter(x=t, y=R[:, cor], mode="lines+markers", marker=dict(size=4), line=dict(color=RED, width=3),
                                 showlegend=False), row, 2)
        fig.update_xaxes(range=[0, SHOW + 1], row=row, col=2)
        fig.update_yaxes(range=list(top), row=row, col=2)
    fig.update_xaxes(title_text="step t", row=2, col=2)
    fig.update_xaxes(title_text="m (weight of IIT)", range=[-5, 10.5], row=1, col=1)
    fig.update_yaxes(title_text="b (bias)", range=[-5, 9], row=1, col=1)
    fig.update_layout(template="simple_white", width=1150, height=700, font=dict(FONT, size=22),
                      title=dict(text=f"step {k}", x=0.5, y=0.98), margin=dict(l=80, r=20, t=150, b=60),
                      legend=dict(x=0, y=1.08, yanchor="bottom", orientation="h"))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".moments_frames"
    tmp.mkdir(exist_ok=True)
    for k in range(1, SHOW + 1):
        frame(k).write_image(tmp / f"{k - 1:03d}.png")
    for k in range(SHOW, SHOW + 10):                       # hold the last frame
        shutil.copy(tmp / f"{SHOW - 1:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "4", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=780:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "adam_moments.gif")], check=True)
    keys = [Image.open(tmp / f"{k - 1:03d}.png").convert("RGB") for k in (1, 3, 8, SHOW)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "adam_moments_frames.png")
    shutil.rmtree(tmp)
