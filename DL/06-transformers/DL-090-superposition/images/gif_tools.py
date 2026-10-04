"""Shared helper: write Plotly figures as a GIF plus a 2x2 key-frame grid (no output when run)."""
import shutil
import subprocess

from PIL import Image


def save_gif(figs, keys, out, here, fps=4, width=720):
    tmp = here / f".{out}_frames"
    tmp.mkdir(exist_ok=True)
    for i, f in enumerate(figs):
        f.write_image(tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", str(tmp / "%03d.png"), "-vf",
                    f"scale={width}:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(here / f"{out}.gif")], check=True)
    ims = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in keys]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(here / f"{out}_frames.png")
    shutil.rmtree(tmp)
