"""Twelve random versions of the same photo, as the network might see it in twelve epochs: Plotly frames turned into
a GIF with ffmpeg, plus a still sheet of four frames for the PDF."""
import shutil
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image
import plotly.graph_objects as go
from common import FONT

HERE = Path(__file__).parent
aug = HERE.parent / "data" / "aug"


def frame(k):
    img = np.array(Image.open(aug / f"combined_{k:02d}.jpg"))
    fig = go.Figure(go.Image(z=img))
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(template="simple_white", width=420, height=470, font=FONT,
                      title=dict(text=f"epoch {k + 1}: a new random version", x=0.5, y=0.97),
                      margin=dict(l=10, r=10, t=50, b=10))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".aug_frames"
    tmp.mkdir(exist_ok=True)
    for k in range(12):
        frame(k).write_image(tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1.5", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=420:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "aug_animation.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (0, 1, 2, 3)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (4 * w + 48, h), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, (i * (w + 16), 0))
    sheet.save(HERE / "aug_animation_frames.png")
    shutil.rmtree(tmp)
