"""XOR in one dimension: a drug works only at a medium dose (low 0, medium 1, high 0). A straight line is turned
through every slope; at each slope it takes the height that gets the most patients right (it predicts "works" where it
is at 0.5 or above). The best is always 2 of the 3 groups. Toy data (nine patients, three per dose group), because the
point is the shape 0-1-0. Idea after StatQuest, "The Essential Main Ideas of Neural Networks".
Plotly frames (a line over data changing) -> ffmpeg GIF, plus a grid of key frames for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=22)
GREEN, RED, BLUE = "#54A24B", "#E45756", "#4C78A8"
DOSE = np.array([0.05, 0.10, 0.15, 0.45, 0.50, 0.55, 0.85, 0.90, 0.95])
WORKS = np.array([0, 0, 0, 1, 1, 1, 0, 0, 0])
GROUP = np.repeat([0, 1, 2], 3)
ANGLES = list(range(-80, 81, 10))


def best_line(angle):
    """Slope from the angle; intercept that gets the most patients right (ties: the line nearest the middle)."""
    m = np.tan(np.radians(angle))
    best = (-1, 9.0, 0.0)
    for c in np.linspace(-8, 8, 3201):
        right = ((m * DOSE + c >= 0.5).astype(int) == WORKS).sum()
        off = abs(m * 0.5 + c - 0.5)                  # ties: keep the line nearest the middle of the plot
        if (right, -off) > (best[0], -best[1]):
            best = (right, off, c)
    return m, best[2]


def frame(angle):
    m, c = best_line(angle)
    pred = (m * DOSE + c >= 0.5).astype(int)
    ok = pred == WORKS
    groups = sum(ok[GROUP == g].all() for g in range(3))
    fig = go.Figure()
    xs = np.array([-0.05, 1.05])
    fig.add_scatter(x=xs, y=m * xs + c, mode="lines", line=dict(color=BLUE, width=5), name="the line")
    fig.add_hline(y=0.5, line=dict(color="grey", dash="dot", width=2))
    for lab, col, name in ((1, GREEN, "drug works (1)"), (0, RED, "drug does not work (0)")):
        k = WORKS == lab
        fig.add_scatter(x=DOSE[k], y=WORKS[k], mode="markers", name=name, marker=dict(size=18, color=col))
    fig.add_scatter(x=DOSE[~ok], y=WORKS[~ok], mode="markers", name="predicted wrong",
                    marker=dict(size=30, color="rgba(0,0,0,0)", line=dict(color="black", width=3)))
    fig.update_layout(template="simple_white", width=1000, height=700, font=FONT,
                      title=dict(text=f"Best straight line at this slope: <b>{groups} of 3</b> dose groups right",
                                 x=0.5, y=0.95, font=dict(size=24)),
                      xaxis=dict(title="dose", tickvals=[0.1, 0.5, 0.9], ticktext=["low", "medium", "high"],
                                 range=[-0.05, 1.05]),
                      yaxis=dict(title="does the drug work?", tickvals=[0, 0.5, 1], range=[-0.6, 1.6]),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.18),
                      margin=dict(l=90, r=30, t=90, b=130))
    return fig, groups


if __name__ == "__main__":
    tmp = HERE / ".dl_frames"
    tmp.mkdir(exist_ok=True)
    keys, got = [], []
    for a in ANGLES:
        keys.append(tmp / f"a{a}.png")
        fig, g = frame(a)
        got.append(g)
        fig.write_image(keys[-1])
    print(dict(zip(ANGLES, got)))
    assert max(got) == 2, got                          # no straight line gets all three groups
    for j, i in enumerate(list(range(len(ANGLES))) + [len(ANGLES) - 1] * 4):
        shutil.copy(keys[i], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "dosage_line.gif")], check=True)
    ims = [Image.open(keys[ANGLES.index(a)]).convert("RGB") for a in (-60, 0, 60)]
    w, h = ims[0].size
    sheet = Image.new("RGB", (3 * w + 32, h), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, (i * (w + 16), 0))
    sheet.save(HERE / "dosage_line_frames.png")
    shutil.rmtree(tmp)
