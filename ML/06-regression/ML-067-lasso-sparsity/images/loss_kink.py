"""The one-feature loss against the slope m while λ grows from 0 to 150, for S = 100 and D = 50 (the Note's numbers).
Left: Lasso, D m^2 - 2 S m + 2 λ |m|. Right: Ridge, D m^2 - 2 S m + λ m^2. Both without the constant that does not
depend on m. The Lasso curve grows a corner at m = 0 and its lowest point lands on the corner at λ = 100 and stays;
the Ridge curve stays a smooth parabola and its lowest point S / (D + λ) never reaches 0.
Run: python loss_kink.py  -> loss_kink.gif, loss_kink_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image

HERE = Path(__file__).parent
BLUE, RED, GREY = "#4C78A8", "#E45756", "#BBBBBB"
S, D = 100.0, 50.0
m = np.linspace(-2, 4, 601)
lasso = lambda lam: D * m ** 2 - 2 * S * m + 2 * lam * np.abs(m)
ridge = lambda lam: D * m ** 2 - 2 * S * m + lam * m ** 2
lasso_min = lambda lam: max(0.0, (S - lam) / D)
ridge_min = lambda lam: S / (D + lam)
lams = np.arange(0, 151, 5)
for lam in lams:                                   # the formulas really are the lowest points of the drawn curves
    assert abs(m[lasso(lam).argmin()] - lasso_min(lam)) < 0.011
    assert abs(m[ridge(lam).argmin()] - ridge_min(lam)) < 0.011
assert lasso_min(100) == 0 and lasso_min(150) == 0 and ridge_min(150) == 0.5
GHOSTS = (0, 50, 100)


def frame(lam):
    lm, rm = lasso_min(lam), ridge_min(lam)
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.09,
                        subplot_titles=(f"Lasso: lowest point at m = {lm:.2f}".replace("0.00", "0 (the corner)"),
                                        f"Ridge: lowest point at m = {rm:.2f}"))
    for c, f, mn, col in ((1, lasso, lm, RED), (2, ridge, rm, BLUE)):
        for g in GHOSTS:
            if g < lam:
                fig.add_trace(go.Scatter(x=m, y=f(g), mode="lines", line=dict(color=GREY, width=2)), 1, c)
        y = f(lam)
        fig.add_trace(go.Scatter(x=m, y=y, mode="lines", line=dict(color=col, width=5)), 1, c)
        ym = D * mn ** 2 - 2 * S * mn + (2 * lam * abs(mn) if c == 1 else lam * mn ** 2)
        fig.add_trace(go.Scatter(x=[mn], y=[ym], mode="markers",
                                 marker=dict(size=18, color="black", line=dict(color="white", width=2))), 1, c)
        fig.add_vline(x=0, line=dict(color="black", width=1, dash="dot"), row=1, col=c)
        fig.update_xaxes(title="slope m", range=[-2, 4], dtick=1, row=1, col=c)
        fig.update_yaxes(range=[-260, 620], row=1, col=c)
    fig.update_yaxes(title_text="loss (constant left out)", row=1, col=1)
    fig.update_layout(template="simple_white", width=1100, height=600, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=22), margin=dict(l=90, r=20, t=120, b=70),
                      title=dict(text=f"λ = {lam:.0f}", x=0.5, y=0.97, font_size=30))
    fig.update_annotations(font_size=24)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".kink_frames"
    tmp.mkdir(exist_ok=True)
    n = 0
    key = {}
    for lam in lams:
        frame(lam).write_image(tmp / f"{n:03d}.png")
        key[int(lam)] = n
        hold = 6 if lam in (0, 50, 100) else 1         # pause on the worked values
        for _ in range(hold - 1):
            shutil.copy(tmp / f"{n:03d}.png", tmp / f"{n + 1:03d}.png")
            n += 1
        n += 1
    for _ in range(12):                                # hold the last frame
        shutil.copy(tmp / f"{n - 1:03d}.png", tmp / f"{n:03d}.png")
        n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "6", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=880:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "loss_kink.gif")], check=True)
    keys = [Image.open(tmp / f"{key[k]:03d}.png").convert("RGB") for k in (0, 50, 100, 150)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "loss_kink_frames.png")
    shutil.rmtree(tmp)
