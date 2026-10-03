"""The same 20 points spread over 5 cells (1 column), 25 cells (2 columns), 125 cells (3 columns: 5 floors).
Run: python sparsity.py  -> sparsity.mp4, sparsity.gif, sparsity_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
N, K = 20, 5                                          # 20 points, 5 bins per column
pts = np.random.default_rng(0).uniform(0, 1, (N, 3))
cells = np.floor(pts * K).astype(int)


def empty(d):
    return K ** d - len({tuple(c[:d]) for c in cells})


def grid(rows, cols, size):
    return VGroup(*[Square(size, color=GREY_C, stroke_width=2).move_to([(c - (cols - 1) / 2) * size,
                                                                      ((rows - 1) / 2 - r) * size, 0])
                    for r in range(rows) for c in range(cols)])


class Sparsity(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, title, d):
        filled = K ** d - empty(d)
        return VGroup(Text(title, font_size=30, weight=BOLD),
                      Text(f"{K ** d} cells, {N} points: {filled} cells have a point, {empty(d)} empty",
                           font_size=24, color=RED_C if empty(d) else BLACK)
                      ).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.4)

    def construct(self):
        self.snaps = []
        # 1 column: a road split into 5 stretches
        s1 = 1.6
        road = grid(1, K, s1)
        dots1 = VGroup(*[Dot([(p[0] - 0.5) * K * s1, (p[1] - 0.5) * 0.8 * s1, 0], radius=0.07, color=BLUE_C) for p in pts])
        cap = self.caption("1 column: a road in 5 stretches", 1)
        self.play(Create(road), FadeIn(cap))
        self.play(FadeIn(dots1, lag_ratio=0.1))
        self.wait(1)
        self.snap()
        # 2 columns: a campus, 5 x 5 blocks
        s2 = 1.0
        campus = grid(K, K, s2).shift(DOWN * 0.6)
        dots2 = VGroup(*[Dot(campus.get_center() + [(p[0] - 0.5) * K * s2, (p[1] - 0.5) * K * s2, 0], radius=0.07,
                             color=BLUE_C) for p in pts])
        cap2 = self.caption("2 columns: a campus in 5 × 5 blocks", 2)
        self.play(ReplacementTransform(road, campus), ReplacementTransform(dots1, dots2), FadeTransform(cap, cap2),
                  run_time=1.8)
        self.wait(1)
        self.snap()
        # 3 columns: a building with 5 floors, each floor 5 x 5 rooms
        s3 = 0.45
        floors = VGroup(*[grid(K, K, s3) for _ in range(K)]).arrange(RIGHT, buff=0.35).shift(DOWN * 0.7)
        labels = VGroup(*[Text(f"floor {i + 1}", font_size=20).next_to(f, DOWN, buff=0.15) for i, f in enumerate(floors)])
        dots3 = VGroup(*[Dot(floors[c[2]].get_center() + [(p[0] - 0.5) * K * s3, (p[1] - 0.5) * K * s3, 0], radius=0.05,
                             color=BLUE_C) for p, c in zip(pts, cells)])
        cap3 = self.caption("3 columns: a building, 5 floors of 5 × 5 rooms", 3)
        self.play(ReplacementTransform(campus, floors), ReplacementTransform(dots2, dots3), FadeIn(labels),
                  FadeTransform(cap2, cap3), run_time=2)
        self.wait(1)
        self.snap()
        # summary: share of empty cells
        bars = VGroup()
        for d in (1, 2, 3):
            share = empty(d) / K ** d
            bars.add(Text(f"{d} column{'s' if d > 1 else ''}: {share:.0%} of cells empty", font_size=26,
                          color=RED_C if share > 0.5 else BLACK))
        head = Text("Same 20 points, more columns:", font_size=34, weight=BOLD)
        tail = Text("each extra column multiplies the cells by 5; the points stay 20", font_size=24, color=GREY_C)
        summary = VGroup(head, bars.arrange(DOWN, aligned_edge=LEFT, buff=0.3), tail).arrange(DOWN, buff=0.5)
        for b in bars: b.scale(1.3)
        summary.arrange(DOWN, buff=0.5)
        self.play(FadeOut(VGroup(floors, dots3, labels, cap3)))
        self.play(FadeIn(summary, lag_ratio=0.3))
        self.wait(1.5)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    for d in (1, 2, 3):
        print(d, "columns:", K ** d, "cells,", empty(d), "empty")
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "sparsity", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = Sparsity()
        scene.render()
    mp4 = HERE / "sparsity.mp4"
    shutil.copy(next(media.rglob("sparsity.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "sparsity.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "sparsity_frames.png")
    shutil.rmtree(media)
