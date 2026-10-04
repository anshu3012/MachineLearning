"""Adding base regressors one at a time on the noisy sine data of section 3 (same data and models as app.py):
linear regression alone, then + SVR, then + a depth-5 tree. After each addition the voting regressor's curve
(solid blue), the mean of the members' curves, is redrawn.
Run: python add_members.py -> add_members.gif, add_members_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import figure, run  # noqa: E402

STEPS = [(["linear regression"], "1 member: the vote is the line itself"),
         (["linear regression", "SVR"], "2 members: the vote runs halfway between line and SVR"),
         (["linear regression", "SVR", "decision tree"], "3 members: the vote follows the tree's jumps a third of the way")]

if __name__ == "__main__":
    tmp = HERE / ".add_members"
    tmp.mkdir(exist_ok=True)
    keys, n = [], 0
    for (names, title), hold in zip(STEPS, [3, 4, 6]):
        fig = figure(run(names))
        fig.update_layout(width=1100, height=760, font=dict(family="Latin Modern Roman", size=22, color="black"),
                          title=dict(text=f"<b>{title}</b>", x=0.5, y=0.97, font_size=27),
                          legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.16, font_size=20),
                          margin=dict(l=70, r=20, t=70, b=200), yaxis_range=[-1.9, 2.1])
        png = tmp / f"{n:03d}.png"
        fig.write_image(png)
        keys.append(Image.open(png).convert("RGB"))
        for k in range(1, hold):
            shutil.copy(png, tmp / f"{n + k:03d}.png")
        n += hold
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "%03d.png"), "-vf",
                    "fps=5,scale=800:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "add_members.gif")], check=True)
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, f in enumerate(keys):
        sheet.paste(f, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "add_members_frames.png")
    shutil.rmtree(tmp)
