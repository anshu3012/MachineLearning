"""Where Student's t comes from, df by df: 20,000 samples of size n from the normal population of section 7
(mu = 50, sigma = 15), each standardized with its own s: T = (x̄ - mu) / (s / √n). The histogram of T follows the
t-curve (orange), not the standard normal (blue); its tails beyond ±1.96 hold more than 5% until n is large.
Run: python t_df_sweep.py  -> t_df_sweep.gif, t_df_sweep_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from scipy import stats

HERE = Path(__file__).parent
BLUE, ORANGE, RED, GREY = "#4C78A8", "#F58518", "#E45756", "#BDBDBD"
MU, SIGMA, REPS = 50, 15, 20000
DFS = [1, 2, 3, 4, 6, 9, 14, 19, 29, 49, 99]
x = np.linspace(-5, 5, 600)
edges = np.linspace(-5, 5, 51)
rng = np.random.default_rng(42)


def simulate(df):
    s = rng.normal(MU, SIGMA, size=(REPS, df + 1))
    return (s.mean(1) - MU) / (s.std(1, ddof=1) / np.sqrt(df + 1))


T = {df: simulate(df) for df in DFS}
for df, t in T.items():                                      # the simulated tails match the t-distribution
    assert abs((np.abs(t) > 1.96).mean() - 2 * stats.t.sf(1.96, df)) < 0.01, df


def frame(df):
    t = T[df]
    h, _ = np.histogram(t, bins=edges)
    h = h / (REPS * (edges[1] - edges[0]))                   # density over all samples, also those off-screen
    mid = (edges[:-1] + edges[1:]) / 2
    tail = np.abs(mid) > 1.96
    tc = stats.t.ppf(0.975, df)
    fig = go.Figure()
    fig.add_bar(x=mid, y=h, width=0.2, marker_color=np.where(tail, RED, GREY), opacity=0.8, name="simulated T")
    fig.add_scatter(x=x, y=stats.norm.pdf(x), mode="lines", line=dict(color=BLUE, width=4), name="standard normal")
    fig.add_scatter(x=x, y=stats.t.pdf(x, df), mode="lines", line=dict(color=ORANGE, width=4, dash="dash"),
                    name=f"t, df = {df}")
    for s in (-1, 1):
        fig.add_vline(x=s * 1.96, line=dict(color=BLUE, width=2, dash="dot"))
    share = (np.abs(t) > 1.96).mean() * 100
    fig.add_annotation(x=3.6, y=0.3, text=f"beyond ±1.96:<br><b>{share:.1f}%</b> of samples<br>(normal: 5%)",
                       showarrow=False, font=dict(size=24, color=RED))
    fig.add_annotation(x=-3.6, y=0.3, text=f"95% cut-off<br>t = ±{tc:.2f}<br>(z = ±1.96)", showarrow=False,
                       font=dict(size=24, color=ORANGE))
    fig.update_layout(template="simple_white", width=900, height=640, bargap=0,
                      font=dict(family="Latin Modern Roman", size=24),
                      title=dict(text=f"samples of n = {df + 1}  →  df = {df}", x=0.5, y=0.96),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.18),
                      xaxis=dict(title="T = (x̄ − μ) / (s / √n)", range=[-5, 5]),
                      yaxis=dict(showticklabels=False, range=[0, 0.43]), margin=dict(l=30, r=30, t=70, b=40))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".tdf_frames"
    tmp.mkdir(exist_ok=True)
    n, keys = 0, {}
    for i, df in enumerate(DFS):
        frame(df).write_image(tmp / f"{n:03d}.png")
        keys[df] = n
        for _ in range(9 if i == len(DFS) - 1 else 2):       # each df held 3 frames, the last one longer
            shutil.copy(tmp / f"{n:03d}.png", tmp / f"{n + 1:03d}.png")
            n += 1
        n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=640:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "t_df_sweep.gif")], check=True)
    ims = [Image.open(tmp / f"{keys[d]:03d}.png").convert("RGB") for d in (1, 4, 14, 99)]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "t_df_sweep_frames.png")
    shutil.rmtree(tmp)
