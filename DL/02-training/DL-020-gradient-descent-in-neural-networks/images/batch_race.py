"""Race of the three variants over 100 epochs (training loss per epoch from the Notebook, data/epoch_loss.csv).
Left: the loss curves drawn epoch by epoch. Right: the updates each variant has made so far (log scale):
1, 10 and 320 per epoch on 320 training observations.
Run: python batch_race.py -> batch_race.gif, batch_race_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots

from common import BLUE, ORANGE, RED

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=22)
e = pd.read_csv(HERE.parent / "data" / "epoch_loss.csv")
RUNNERS = [("batch_size=320", "batch", 1, BLUE, 14), ("batch_size=32", "mini-batch", 10, ORANGE, -14),
           ("batch_size=1", "stochastic", 320, RED, 0)]   # last number: label nudge in pixels (curves start together)
EPOCHS = [1, 2, 3, 4, 5, 6, 8, 10] + list(range(12, 101, 4))
assert e.loc[99, "batch_size=320"] > e.loc[99, "batch_size=32"] > e.loc[99, "batch_size=1"]   # the Note's order


def frame(n):
    fig = make_subplots(rows=1, cols=2, column_widths=[0.6, 0.4], horizontal_spacing=0.16,
                        subplot_titles=("training loss", "updates made so far"))
    for col, name, per, c, dy in RUNNERS:
        fig.add_trace(go.Scatter(x=e.epoch[:n] + 1, y=e[col][:n], mode="lines", line=dict(color=c, width=5)), 1, 1)
        fig.add_trace(go.Scatter(x=[n], y=[e[col][n - 1]], mode="markers",
                                 marker=dict(size=14, color=c), cliponaxis=False), 1, 1)
        fig.add_annotation(x=n, y=e[col][n - 1], text=f"  {name}", showarrow=False, xanchor="left", yshift=dy,
                           font=dict(color=c, size=22), row=1, col=1)
        fig.add_trace(go.Bar(y=[name], x=[per * n], orientation="h", marker_color=c, text=[f"{per * n:,}"],
                             textposition="outside", textfont=dict(size=22), cliponaxis=False), 1, 2)
    fig.update_layout(template="simple_white", width=1150, height=560, font=FONT, showlegend=False,
                      title=dict(text=f"epoch {n}", x=0.5, y=0.97), margin=dict(l=80, r=40, t=110, b=70))
    fig.update_annotations(font_size=24, selector=dict(text="training loss"))
    fig.update_annotations(font_size=24, selector=dict(text="updates made so far"))
    fig.update_xaxes(title="epoch", range=[0, 135], row=1, col=1)
    fig.update_yaxes(range=[0.1, 0.75], row=1, col=1)
    fig.update_xaxes(type="log", range=[0, 5.7], title="updates (log scale)", row=1, col=2)
    fig.update_yaxes(autorange="reversed", row=1, col=2)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".race_frames"
    tmp.mkdir(exist_ok=True)
    for i, n in enumerate(EPOCHS):
        frame(n).write_image(tmp / f"{i:03d}.png")
    for i in range(len(EPOCHS), len(EPOCHS) + 12):            # hold the last frame
        shutil.copy(tmp / f"{len(EPOCHS) - 1:03d}.png", tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "5", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "batch_race.gif")], check=True)
    keys = [Image.open(tmp / f"{EPOCHS.index(n):03d}.png").convert("RGB") for n in (1, 10, 40, 100)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "batch_race_frames.png")
    shutil.rmtree(tmp)
