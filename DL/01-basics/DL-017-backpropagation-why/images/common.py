"""Shared colours and font for the Plotly figures (no output when run)."""
BLUE, ORANGE, GREEN, RED, PURPLE, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=16)


def save_gif(figs, name, keys, here, fps=3, hold=6, width=720, cols=2):
    """Write Plotly figures as frames -> <name>.gif (ffmpeg palette) and a grid (`cols` wide) of frames `keys` -> <name>_frames.png."""
    import shutil, subprocess
    from PIL import Image
    tmp = here / f".{name}_tmp"
    tmp.mkdir(exist_ok=True)
    for k, fig in enumerate(figs):
        fig.write_image(tmp / f"{k:03d}.png")
    last = len(figs) - 1
    for k in range(len(figs), len(figs) + hold):                       # hold the final frame
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", str(tmp / "%03d.png"), "-vf",
                    f"scale={width}:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(here / f"{name}.gif")], check=True)
    ims = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in keys]
    w, h = ims[0].size
    rows = -(-len(ims) // cols)
    sheet = Image.new("RGB", (cols * (w + 16) - 16, rows * (h + 16) - 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % cols) * (w + 16), (i // cols) * (h + 16)))
    sheet.save(here / f"{name}_frames.png")
    shutil.rmtree(tmp)
