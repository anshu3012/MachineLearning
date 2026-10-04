"""Why s in place of sigma changes the curve. We draw 400 samples of n = 5 (df = 4, as in the five-lessons example)
from a normal population whose true mean equals mu0, and compute two statistics per sample: z with the true sigma,
and t with the sample's own s. The z values pile up under the standard normal; the t values spread wider and
follow Student's t with 4 degrees of freedom: about 12 percent land beyond +-1.96 instead of 5 percent.
Run: python s_for_sigma.py  -> s_for_sigma.gif, s_for_sigma_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from plotly.subplots import make_subplots
from PIL import Image
from scipy import stats

HERE = Path(__file__).parent
BLUE, ORANGE, RED, GREY = "#4C78A8", "#F58518", "#E45756", "#6B6B6B"
MU, SIGMA, N, REPS, BW, LIM = 50, 1.2, 5, 400, 0.3, 5.0
rng = np.random.default_rng(1)
X = rng.normal(MU, SIGMA, size=(REPS, N))
zs = (X.mean(1) - MU) / (SIGMA / np.sqrt(N))
ts = (X.mean(1) - MU) / (X.std(1, ddof=1) / np.sqrt(N))
P_T = 2 * stats.t.sf(1.96, N - 1)
assert round(P_T, 2) == 0.12
for v, p in ((zs, 0.05), (ts, P_T)):                          # observed share within 3 binomial SEs of theory
    assert abs((np.abs(v) > 1.96).mean() - p) < 3 * np.sqrt(p * (1 - p) / REPS)
x = np.linspace(-LIM, LIM, 500)


def pile(v):
    v = np.clip(v, -LIM + 0.05, LIM - 0.05)                   # the few t values past +-5 sit at the edge
    b = np.floor(v / BW)
    return v, np.array([(b[:i] == b[i]).sum() + 0.5 for i in range(len(v))]) / (REPS * BW)


ZX, ZY = pile(zs)
TX, TY = pile(ts)


def frame(k, show_t_curve):
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.06,
                        subplot_titles=["z = (x̄ − μ) / (σ/√5)", "t = (x̄ − μ) / (s/√5)"])
    for col, (vx, vy, raw) in enumerate(((ZX, ZY, zs), (TX, TY, ts)), start=1):
        out = np.abs(raw[:k]) > 1.96
        fig.add_scatter(x=x, y=stats.norm.pdf(x), mode="lines", line=dict(color="black", width=3), row=1, col=col)
        if col == 2 and show_t_curve:
            fig.add_scatter(x=x, y=stats.t.pdf(x, N - 1), mode="lines", line=dict(color=ORANGE, width=4),
                            row=1, col=col)
        fig.add_scatter(x=vx[:k], y=vy[:k], mode="markers", row=1, col=col,
                        marker=dict(size=8, color=np.where(out, RED, BLUE), line=dict(width=0.5, color="white")))
        for s in (-1.96, 1.96):
            fig.add_vline(x=s, line=dict(color=RED, width=2, dash="dash"), opacity=1, row=1, col=col)
        if k:
            fig.add_annotation(x=0, y=0.52, showarrow=False, bgcolor="white", row=1, col=col,
                               text=f"beyond ±1.96: <b>{100 * out.mean():.0f}%</b>", font=dict(size=24, color=RED))
    if show_t_curve:
        fig.add_annotation(x=3.4, y=0.16, text="t, df = 4", showarrow=False, font=dict(size=22, color=ORANGE),
                           row=1, col=2)
        fig.add_annotation(x=3.4, y=0.16, text="standard<br>normal", showarrow=False, font=dict(size=22),
                           bgcolor="white", row=1, col=1)
    fig.update_xaxes(range=[-LIM, LIM], title_text="statistic")
    fig.update_yaxes(range=[0, 0.58], showticklabels=False)
    fig.update_layout(template="simple_white", width=1100, height=520, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=22),
                      title=dict(text=f"{k} samples of 5 values, H₀ true", x=0.5, y=0.97),
                      margin=dict(l=20, r=20, t=100, b=60))
    for a in fig.layout.annotations[:2]:
        a.font.size = 24
    return fig


PLAN = [(k, False, 1) for k in (5, 15, 30, 60, 100, 150, 200, 260, 330)] + [(400, False, 5), (400, True, 14)]

if __name__ == "__main__":
    tmp = HERE / ".sigma_frames"
    tmp.mkdir(exist_ok=True)
    n, keys = 0, []
    for i, (k, tc, hold) in enumerate(PLAN):
        frame(k, tc).write_image(tmp / f"{n:03d}.png")
        if i in (2, 5, 9, 10):
            keys.append(n)
        for _ in range(hold - 1):
            shutil.copy(tmp / f"{n:03d}.png", tmp / f"{n + 1:03d}.png")
            n += 1
        n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "s_for_sigma.gif")], check=True)
    ims = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in keys[1::2]]   # 150 samples, final frame
    w, h = ims[0].size
    sheet = Image.new("RGB", (w, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, (0, i * (h + 16)))
    sheet.save(HERE / "s_for_sigma_frames.png")
    shutil.rmtree(tmp)
