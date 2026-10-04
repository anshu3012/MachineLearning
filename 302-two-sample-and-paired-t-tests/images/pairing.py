"""Why pairing helps, on the weight-loss table with every "after" weight 2 kg lower (a real mean loss of 1.53 kg).
Left: the 15 before and 15 after weights as two groups; between-person spread (67 to 93 kg) gives an independent
standard error of 2.75 kg. Then each person's two weights are joined, and their own change d drops into the right
panel, drawn on the same 40 kg scale: the d values huddle together, standard error 0.63 kg.
Run: python pairing.py  -> pairing.gif, pairing_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
from PIL import Image
from scipy import stats

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
w = pd.read_csv(HERE.parent / "data" / "weight_loss.csv")
before, after = w.before.to_numpy(float), w.after.to_numpy(float) - 2
d = before - after
n = len(d)
se_pair = d.std(ddof=1) / np.sqrt(n)
se_ind = np.sqrt(before.var(ddof=1) / n + after.var(ddof=1) / n)
tp = stats.ttest_rel(before, after, alternative="greater")
ti = stats.ttest_ind(before, after, alternative="greater")
assert (d.min(), d.max()) == (-4, 5) and max(before.max(), after.max()) - min(before.min(), after.min()) == 27
assert round(d.mean(), 2) == 1.53 and round(se_pair, 2) == 0.63 and round(se_ind, 2) == 2.75
assert (round(tp.statistic, 2), round(tp.pvalue, 3)) == (2.43, 0.015)
assert (round(ti.statistic, 2), round(ti.pvalue, 2)) == (0.56, 0.29)
order = np.argsort(before)
jit = np.linspace(-0.12, 0.12, n)[np.argsort(order)]           # small fixed spread so dots do not hide each other


def frame(k_lines, k_d, final=False):
    fig = make_subplots(rows=1, cols=2, column_widths=[0.55, 0.45], horizontal_spacing=0.12,
                        subplot_titles=["as two groups", "each person's change d"])
    for i in range(n):
        on = i < k_lines
        fig.add_scatter(x=[0 + jit[i], 1 + jit[i]], y=[before[i], after[i]], mode="lines",
                        line=dict(color=GREY if on else "rgba(0,0,0,0)", width=1.5), row=1, col=1)
    fig.add_scatter(x=0 + jit, y=before, mode="markers", marker=dict(size=12, color=BLUE), row=1, col=1)
    fig.add_scatter(x=1 + jit, y=after, mode="markers", marker=dict(size=12, color=ORANGE), row=1, col=1)
    fig.add_annotation(x=0.5, y=99, text=f"independent SE = {se_ind:.2f} kg", showarrow=False,
                       font=dict(size=22, color=GREY), row=1, col=1)
    if k_d:
        fig.add_scatter(x=np.zeros(k_d) + jit[:k_d] * 2, y=d[:k_d], mode="markers",
                        marker=dict(size=12, color=GREEN), row=1, col=2)
        fig.add_annotation(x=0, y=19, text=f"paired SE = {se_pair:.2f} kg", showarrow=False,
                           font=dict(size=22, color=GREEN), row=1, col=2)
    fig.add_hline(y=0, line=dict(color=GREY, width=1.5, dash="dot"), opacity=1, row=1, col=2)
    if final:
        fig.add_scatter(x=[-0.45, 0.45], y=[d.mean()] * 2, mode="lines", line=dict(color="black", width=3),
                        row=1, col=2)
        fig.add_annotation(x=0.5, y=56, showarrow=False, bgcolor="white", row=1, col=1, align="left",
                           text=f"t = {ti.statistic:.2f}, p = {ti.pvalue:.2f}", font=dict(size=24, color=GREY))
        fig.add_annotation(x=0, y=-17, showarrow=False, bgcolor="white", row=1, col=2,
                           text=f"t = {tp.statistic:.2f}, <b>p = {tp.pvalue:.3f}</b>", font=dict(size=24, color=GREEN))
    fig.update_xaxes(tickvals=[0, 1], ticktext=["before", "after − 2 kg"], range=[-0.4, 1.4], row=1, col=1)
    fig.update_xaxes(tickvals=[0], ticktext=["before − after"], range=[-0.6, 0.6], row=1, col=2)
    fig.update_yaxes(title_text="weight (kg)", range=[53, 102], row=1, col=1)     # both panels span 49 kg
    fig.update_yaxes(title_text="d (kg)", range=[-21, 28], row=1, col=2)
    fig.update_layout(template="simple_white", width=1000, height=600, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=22), margin=dict(l=80, r=20, t=60, b=60))
    for a in fig.layout.annotations[:2]:
        a.font.size = 24
    return fig


PLAN = [(0, 0, False, 6)] + [(i, i, False, 1) for i in range(1, n + 1)] + [(n, n, True, 14)]

if __name__ == "__main__":
    tmp = HERE / ".pair_frames"
    tmp.mkdir(exist_ok=True)
    m, keys = 0, []
    for i, (kl, kd, fin, hold) in enumerate(PLAN):
        frame(kl, kd, fin).write_image(tmp / f"{m:03d}.png")
        if i in (0, len(PLAN) - 1):
            keys.append(m)
        for _ in range(hold - 1):
            shutil.copy(tmp / f"{m:03d}.png", tmp / f"{m + 1:03d}.png")
            m += 1
        m += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "pairing.gif")], check=True)
    Image.open(tmp / f"{keys[-1]:03d}.png").convert("RGB").save(HERE / "pairing_frames.png")   # last frame holds it all
    shutil.rmtree(tmp)
