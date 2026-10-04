"""PC1 as the line with the largest sum of squared projections, and the singular values as square roots of those sums
(idea after StatQuest, "Principal Component Analysis (PCA), Step-by-Step"; our own code, on the Note's 30 flats).
A line through the centre turns from 0 to 180 degrees; each flat's projection foot slides along it; the right panel
traces SS(angle) = sum of squared projected distances. Its peak is sigma1^2 = 78.2 at 45 degrees, its trough sigma2^2
at 135 degrees. Plotly frames -> ffmpeg GIF, plus a key-frame strip for the PDF.  Run: python pca_ss_sweep.py"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
BLUE, RED, GREY, GREEN = "#4C78A8", "#E45756", "#9A9A9A", "#54A24B"
FONT = dict(family="Latin Modern Roman", size=24)

rng = np.random.default_rng(7)                       # the flats exactly as in the notebook and the PCA Notes
N = 30
rooms = rng.uniform(1, 5, N)
rng.normal(0, 0.35, N)
wash = 0.8 * rooms + rng.normal(0, 0.35, N) + 0.4
wash = wash * rooms.std() / wash.std()
wash += 3 - wash.mean()
Xc = np.c_[rooms, wash] - np.c_[rooms, wash].mean(axis=0)
s = np.linalg.svd(Xc, compute_uv=False)
ANG = np.arange(0, 181, 5)
ss = lambda a: float(np.sum((Xc @ [np.cos(np.radians(a)), np.sin(np.radians(a))]) ** 2))
SS = np.array([ss(a) for a in ANG])
FINE = np.linspace(0, 180, 361)
SS_FINE = np.array([ss(a) for a in FINE])
assert abs(SS_FINE.max() - s[0] ** 2) < 0.05 and abs(SS_FINE.min() - s[1] ** 2) < 0.05
assert abs(FINE[SS_FINE.argmax()] - 45) <= 1 and abs(np.sqrt(ss(45)) - 8.843) < 0.01


def frame(k, final=False):
    a = ANG[k]
    u = np.array([np.cos(np.radians(a)), np.sin(np.radians(a))])
    t = Xc @ u
    feet = np.outer(t, u)
    fig = make_subplots(1, 2, horizontal_spacing=0.13, column_widths=[0.45, 0.55],
                        subplot_titles=(f"line at {a}°", "SS = sum of squared projected distances"))
    for p, q in zip(Xc, feet):
        fig.add_trace(go.Scatter(x=[p[0], q[0]], y=[p[1], q[1]], mode="lines", line=dict(color=GREY, width=1.5)), 1, 1)
    fig.add_trace(go.Scatter(x=[-4 * u[0], 4 * u[0]], y=[-4 * u[1], 4 * u[1]], mode="lines",
                             line=dict(color=RED, width=4)), 1, 1)
    fig.add_trace(go.Scatter(x=Xc[:, 0], y=Xc[:, 1], mode="markers", marker=dict(size=10, color=BLUE)), 1, 1)
    fig.add_trace(go.Scatter(x=feet[:, 0], y=feet[:, 1], mode="markers", marker=dict(size=8, color=RED)), 1, 1)
    upto = FINE <= (180 if final else a)
    fig.add_trace(go.Scatter(x=FINE[upto], y=SS_FINE[upto], mode="lines", line=dict(color=RED, width=4)), 1, 2)
    fig.add_trace(go.Scatter(x=[a], y=[SS[k]], mode="markers", marker=dict(size=14, color=RED)), 1, 2)
    if final:
        fig.add_trace(go.Scatter(x=[135], y=[s[1] ** 2], mode="markers", marker=dict(size=14, color=GREEN)), 1, 2)
        fig.add_annotation(x=135, y=s[1] ** 2, xref="x2", yref="y2", text=f"σ₂² = {s[1]**2:.2f}", showarrow=False,
                           yshift=22, font=dict(color=GREEN, size=24))
    fig.add_hline(y=s[0] ** 2, line=dict(color=GREEN, dash="dash"), row=1, col=2)
    fig.add_annotation(x=180, y=s[0] ** 2, xref="x2", yref="y2", text=f"σ₁² = {s[0]**2:.1f}", showarrow=False,
                       xanchor="right", yshift=18, font=dict(color=GREEN, size=24))
    title = f"SS = {SS[k]:.1f},   √SS = {np.sqrt(SS[k]):.2f}"
    if final:
        title = f"PC1 at 45°: √SS = {s[0]:.3f} = σ₁;   at 135°: √SS = {s[1]:.3f} = σ₂"
    fig.update_xaxes(title="rooms (centred)", range=[-3.4, 3.4], row=1, col=1)
    fig.update_yaxes(title="washrooms (centred)", range=[-3.4, 3.4], scaleanchor="x", row=1, col=1)
    fig.update_xaxes(title="angle of the line (degrees)", range=[0, 180], dtick=45, row=1, col=2)
    fig.update_yaxes(title="SS", range=[0, 90], row=1, col=2)
    fig.update_layout(template="simple_white", width=1300, height=620, showlegend=False, font=FONT,
                      margin=dict(l=90, r=30, t=120, b=70), title=dict(text=title, x=0.5, y=0.96))
    fig.update_annotations(selector=dict(xref="paper"), font_size=24)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".ss_frames"
    tmp.mkdir(exist_ok=True)
    n = len(ANG)
    for k in range(n):
        frame(k).write_image(tmp / f"{k:03d}.png")
    i45 = int(np.where(ANG == 45)[0][0])
    final = frame(i45, final=True)
    final.write_image(tmp / "final.png")
    for j in range(6):                                # hold the result
        shutil.copy(tmp / "final.png", tmp / f"{n + j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "4", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "pca_ss_sweep.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (18,)] + [Image.open(tmp / "final.png").convert("RGB")]
    w, h = keys[0].size
    sheet = Image.new("RGB", (w, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, (0, i * (h + 16)))
    sheet.save(HERE / "pca_ss_sweep_frames.png")
    shutil.rmtree(tmp)
