"""PX4's attitude autotuner, one step per frame, drawn from px4_autotune.tex (the still): the step in use is drawn
thick, the others faint. The steps follow the state machine of mc_autotune_attitude_control.cpp: roll, pitch, yaw
(shake and fit), then the gain design (computePidGmvc with the rise time MC_AT_RISE_TIME, 0.14 s, 0.2 s for yaw, and
damping index 0, "critical damping" in pid_design.hpp), then apply and test.
Run: python px4_autotune_anim.py -> px4_autotune_anim.gif, px4_autotune_anim_frames.png"""
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

here = Path(__file__).parent
SRC = (here / "px4_autotune.tex").read_text()
BOXES = ["(test)", "(model)", "(spec)", "(gains)"]
ARROWS = [r"\draw[arrow] (test) -- (model);", r"\draw[arrow] (model) -- (spec);", r"\draw[arrow] (spec) -- (gains);"]
CAPTIONS = [
    "PX4 tunes each turn-rate loop of a drone in four steps.",
    r"1. \textbf{Shake:} small steps on roll, then pitch, then yaw.",
    r"2. \textbf{Model:} fit a second-order model of each turn rate to what the steps did.",
    r"3. \textbf{Requirement:} rise time 0.14~s (0.2~s for yaw), critical damping.",
    r"4. \textbf{Gains:} the PID gains for that response; apply them, then a test flight.",
    "All four steps: the requirement is written in step-response numbers.",
]


def tex(lit):
    """lit: the box numbers (0 to 3) drawn thick; the rest faint. Arrows into a lit box are drawn, the rest faint."""
    src = SRC
    for i, b in enumerate(BOXES):
        style = ", line width=2.6pt" if i in lit else ", opacity=0.3, text opacity=0.45"
        assert src.count(f"] {b} at") == 1
        src = src.replace(f"] {b} at", f"{style}] {b} at")
    for i, a in enumerate(ARROWS):
        src = src.replace(a, a if (i + 1) in lit else a.replace("[arrow]", "[arrow, opacity=0.25]"))
    return src


frames = [(set(), 0), ({0}, 1), ({1}, 2), ({2}, 3), ({3}, 4), ({0, 1, 2, 3}, 5)]
assert "0.14 s" in SRC and "0.2 s for yaw" in SRC and "critical damping" in SRC
PDFTOPPM = str(Path(sys.executable).parent / "pdftoppm") if (Path(sys.executable).parent / "pdftoppm").exists() \
    else "pdftoppm"
tmp = here / ".px4_autotune_anim_tex"
tmp.mkdir(exist_ok=True)
shutil.copy(here / "px4_autotune.tex", tmp / "px4_autotune.tex")
pngs = []
for k, (lit, c) in enumerate(frames):
    body = tex(lit).replace(r"\end{tikzpicture}",
                            rf"\node[font=\large, text width=11.5cm, align=center] at (3.1,-7.3) {{{CAPTIONS[c]}}};"
                            "\n" + r"\end{tikzpicture}")
    body = body.replace(r"\input{../../../../../tools/tikz-style.tex}", r"\input{../../../../../../tools/tikz-style.tex}")
    f = tmp / f"px4_{k:02d}.tex"
    f.write_text(body)
    subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", f.name], cwd=tmp, check=True,
                   stdout=subprocess.DEVNULL)
    subprocess.run([PDFTOPPM, "-png", "-r", "150", "-singlefile", f.with_suffix(".pdf").name, f.stem], cwd=tmp,
                   check=True)
    pngs.append(tmp / f"{f.stem}.png")

# One GIF frame per second; each step holds 3 s, the last frame 8 s. Same size for every frame (pad to the largest).
ims = [Image.open(p).convert("RGB") for p in pngs]
W, H = max(i.size[0] for i in ims), max(i.size[1] for i in ims)
seq = tmp / "seq"
seq.mkdir(exist_ok=True)
j = 0
for im, hold in zip(ims, [3, 3, 3, 3, 3, 8]):
    canvas = Image.new("RGB", (W, H), "white")
    canvas.paste(im, ((W - im.size[0]) // 2, 0))
    for _ in range(hold):
        canvas.save(seq / f"{j:04d}.png")
        j += 1
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(seq / "%04d.png"), "-vf",
                "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=96[p];[b][p]paletteuse",
                str(here / "px4_autotune_anim.gif")], check=True)
keys = [1, 2, 3, 4]
sheet = Image.new("RGB", (2 * W + 16, 2 * H + 16), "white")
for n, k in enumerate(keys):
    canvas = Image.new("RGB", (W, H), "white")
    canvas.paste(ims[k], ((W - ims[k].size[0]) // 2, 0))
    sheet.paste(canvas, ((n % 2) * (W + 16), (n // 2) * (H + 16)))
sheet.save(here / "px4_autotune_anim_frames.png")
shutil.rmtree(tmp)
assert (here / "px4_autotune_anim.gif").stat().st_size / 1e6 < 3.2
