"""Masked self-attention in a trained transformer, as a grid of dots (rows: the word being computed, columns: the
word it takes from). Head 1 of the first decoder block of the transformer inference Note's model, on the decoder
input "<start> comment ça va ?". Four stages: raw scores q.k (dot area = size, blue positive, red negative),
divided by sqrt(d_k), the causal mask (-inf above the diagonal), and the softmax of each row.
Data: data/trained_grid.csv (exported by the transformer inference Note's Notebook, section 8).
Dot grid after Sanderson (3Blue1Brown), "Attention in transformers, step-by-step", 2024 (8:30-12:42).
Run: python trained_grid.py -> trained_grid.mp4, trained_grid.gif, trained_grid_frames.png (Manim)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, PURPLE_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MarkupText.set_default(color=BLACK, font="Latin Modern Roman")
HEAD = 1
g = pd.read_csv(HERE.parent / "data" / "trained_grid.csv")
g = g[g["head"] == HEAD]
WORDS = list(dict.fromkeys(g["query"]))
N = len(WORDS)
M = {k: g.pivot(index="i", columns="j", values=k).values for k in ("raw", "scaled", "weight")}
DK = round(float((M["raw"] / M["scaled"])[0, 0]) ** 2)
VMAX = np.abs(np.tril(M["raw"])).max()
STEP, R = 1.3, 0.5
ORIGIN = np.array([-5.3, 2.0, 0])


def pos(i, j):
    return ORIGIN + np.array([j * STEP, -i * STEP, 0])


def dot(v, i, j, kind):
    if kind == "weight":
        r, col = R * np.sqrt(v), BLUE_C
    else:
        r, col = R * np.sqrt(min(abs(v) / VMAX, 1)), BLUE_C if v >= 0 else RED_C
    c = Circle(radius=max(r, 0.025), color=col, fill_color=col, fill_opacity=0.85, stroke_width=0).move_to(pos(i, j))
    t = Text(f"{v:.2f}" if kind == "weight" else f"{v:.1f}", font_size=17, color=GREY_C).move_to(pos(i, j) + DOWN * 0.6)
    return VGroup(c, t)


def grid(kind, masked=False):
    out = VGroup()
    for i in range(N):
        for j in range(N):
            if masked and j > i:
                out.add(VGroup(Text("-∞", font_size=22, color=GREY_C).move_to(pos(i, j)), Dot(radius=0.01).move_to(pos(i, j))))
            else:
                out.add(dot(M[kind][i, j], i, j, kind))
    return out


class TrainedGrid(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        title = Text("Masked self-attention in a trained decoder", font_size=32).to_edge(UP, buff=0.25)
        cols = VGroup(*[Text(w, font_size=22).move_to(pos(0, j) + UP * 0.7) for j, w in enumerate(WORDS)])
        rows = VGroup(*[Text(w, font_size=22).move_to(pos(i, 0) + LEFT * 1.0) for i, w in enumerate(WORDS)])
        side = Text("row: the word being computed", font_size=20, color=GREY_C).next_to(cols, UP, buff=0.15)
        self.play(FadeIn(title), FadeIn(cols), FadeIn(rows), FadeIn(side))
        px = 1.3
        info = [
            ("1. raw scores q·k", "dot area = size of the score;\nblue positive, red negative"),
            (f"2. divide by √{DK} = {np.sqrt(DK):.2f}", "every score shrinks by the same factor"),
            ("3. causal mask", "-∞ above the diagonal:\nno word may take from later words"),
            ("4. softmax of each row", "weights; each row sums to 1,\nfuture weights are exactly 0"),
        ]

        def caption(k):
            head, body = info[k]
            return VGroup(Text(head, font_size=30, color=PURPLE_C), Text(body, font_size=24, line_spacing=0.9)
                          ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([px, 0.9, 0], aligned_edge=LEFT)

        cur, cap = grid("raw"), caption(0)
        self.play(FadeIn(cur, lag_ratio=0.03), FadeIn(cap), run_time=1.6)
        self.wait(1.2)
        self.snap()
        for k, (kind, masked) in enumerate((("scaled", False), ("scaled", True), ("weight", True)), start=1):
            new, ncap = grid(kind, masked), caption(k)
            self.play(Transform(cur, new), ReplacementTransform(cap, ncap), run_time=1.5)
            cap = ncap
            self.wait(1.3)
            if k >= 2:
                self.snap()
            if k == 1:
                self.snap()
        note = Text(f"head {HEAD} of 4, first decoder block\nof the trained English-to-French model",
                    font_size=20, color=GREY_C).move_to([px, -1.6, 0], aligned_edge=LEFT)
        self.play(FadeIn(note))
        self.wait(2.5)
        self.snaps[-1] = Image.fromarray(self.renderer.get_frame())


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "trained_grid", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = TrainedGrid()
        scene.render()
    mp4 = HERE / "trained_grid.mp4"
    shutil.copy(next(media.rglob("trained_grid.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "trained_grid.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "trained_grid_frames.png")
    shutil.rmtree(media)
