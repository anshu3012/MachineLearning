"""Section 3: the sums of squares on the nine marks (4, 5, 6), (6, 7, 8), (8, 9, 10), drawn as sticks.
SST: each mark to the grand mean 7 (total 30). SSW: each mark to its own group mean (total 6). SSB: each mark's group
mean to the grand mean (total 24). The bar on the right stacks the squared sticks: 30 = 24 + 6, and df 8 = 2 + 6.
Run: python ss_split.py  -> ss_split.gif, ss_split_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, GREY, PURPLE = "#4C78A8", "#F58518", "#54A24B", "#6B6B6B", "#B279A2"
COLOURS = [BLUE, ORANGE, GREEN]
GROUPS = [np.array([4, 5, 6]), np.array([6, 7, 8]), np.array([8, 9, 10])]
GRAND = 7
XS = [np.array([0.7, 1.0, 1.3]) + 1.6 * i for i in range(3)]          # x positions of the nine dots
SST = sum(((g - GRAND) ** 2).sum() for g in GROUPS)
SSW = sum(((g - g.mean()) ** 2).sum() for g in GROUPS)
SSB = sum(len(g) * (g.mean() - GRAND) ** 2 for g in GROUPS)
assert (SST, SSW, SSB) == (30, 6, 24)

TITLES = ["Nine marks, three sections; grand mean 7",
          "SST: each mark to the grand mean",
          "SSW: each mark to its own section mean",
          "SSB: each section mean to the grand mean",
          "The split: SST = SSB + SSW",
          "F = (SSB / 2) / (SSW / 6) = 12 / 1 = 12"]


def frame(step):
    fig = make_subplots(rows=1, cols=2, column_widths=[0.66, 0.34], horizontal_spacing=0.1)
    fig.add_scatter(x=[0.2, 5.0], y=[GRAND, GRAND], mode="lines", line=dict(color=GREY, dash="dash", width=2),
                    row=1, col=1)
    fig.add_annotation(x=1.45, y=GRAND, text="grand<br>mean 7", showarrow=False, yshift=-26, xanchor="left",
                       font=dict(color=GREY, size=18), row=1, col=1)
    for g, xs, c in zip(GROUPS, XS, COLOURS):
        if step >= 2:
            fig.add_scatter(x=[xs[0] - 0.2, xs[-1] + 0.2], y=[g.mean()] * 2, mode="lines",
                            line=dict(color=c, width=4), row=1, col=1)
        for x, v in zip(xs, g):
            ends = {1: (v, GRAND, PURPLE), 2: (v, g.mean(), c), 3: (g.mean(), GRAND, "black")}.get(step)
            if ends and ends[0] != ends[1]:
                fig.add_scatter(x=[x, x], y=ends[:2], mode="lines", line=dict(color=ends[2], width=5), row=1, col=1)
        fig.add_scatter(x=xs, y=g, mode="markers", marker=dict(size=20, color=c, line=dict(width=2, color="black")),
                        row=1, col=1)
    # right panel: stacked bars of the sums of squares found so far
    bars = []
    if step >= 1:
        bars.append(("SST", [("", SST, PURPLE)]))
    if step >= 2:
        bars.append(("split", [("SSW 6", SSW, BLUE)] + ([("SSB 24", SSB, "black")] if step >= 3 else [])))
    for name, parts in bars:
        base = 0
        for label, h, col in parts:
            fig.add_bar(x=[name], y=[h], base=[base], marker_color=col, width=0.6, row=1, col=2)
            if label:
                fig.add_annotation(x=name, y=base + h / 2, text=label, showarrow=False,
                                   font=dict(color="white", size=20), row=1, col=2)
            base += h
        fig.add_annotation(x=name, y=base, text=f"<b>{base:g}</b>", showarrow=False, yshift=16, row=1, col=2)
    if step >= 4:
        fig.add_annotation(x=0.5, y=-6, xref="x2 domain", yref="y2", text="df: 8 = 2 + 6", showarrow=False,
                           font=dict(size=22), row=1, col=2)
    if step >= 5:
        fig.add_annotation(x=0.5, y=40, xref="x2 domain", yref="y2", text="MSB = 24/2 = 12<br>MSW = 6/6 = 1",
                           showarrow=False, font=dict(size=22), row=1, col=2)
    fig.update_xaxes(tickvals=[1.0, 2.6, 4.2], ticktext=["A", "B", "C"], range=[0.2, 5.0], row=1, col=1)
    fig.update_yaxes(title_text="mark", range=[3, 11], dtick=1, row=1, col=1)
    fig.update_xaxes(categoryorder="array", categoryarray=["SST", "split"], range=[-0.6, 1.6], row=1, col=2)
    fig.update_yaxes(title_text="sum of squares", range=[-9, 48], tickvals=[0, 10, 20, 30], row=1, col=2)
    fig.update_layout(template="simple_white", width=1000, height=540, showlegend=False, barmode="overlay",
                      font=dict(family="Latin Modern Roman", size=22),
                      title=dict(text=TITLES[step], x=0.5, y=0.96), margin=dict(l=70, r=30, t=70, b=60))
    return fig


PLAN = [(0, 5), (1, 9), (2, 9), (3, 9), (4, 9), (5, 14)]

if __name__ == "__main__":
    tmp = HERE / ".ss_frames"
    tmp.mkdir(exist_ok=True)
    n, keys = 0, {}
    for step, hold in PLAN:
        frame(step).write_image(tmp / f"{n:03d}.png")
        keys[step] = n
        for _ in range(hold - 1):
            shutil.copy(tmp / f"{n:03d}.png", tmp / f"{n + 1:03d}.png")
            n += 1
        n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=700:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "ss_split.gif")], check=True)
    ims = [Image.open(tmp / f"{keys[k]:03d}.png").convert("RGB") for k in (1, 2, 3, 5)]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "ss_split_frames.png")
    shutil.rmtree(tmp)
