"""k-means on 18 students (standardized CGPA and IQ), k = 3, step by step: start centroids, assign each point
to its nearest centroid, move each centroid to the mean of its points, repeat until the centroids stop moving.
Run: python kmeans_2d.py  -> kmeans_2d.mp4, kmeans_2d.gif, kmeans_2d_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image, ImageOps

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#6B6B6B"
COLOURS = [BLUE_C, ORANGE_C, GREEN_C]
Text.set_default(color=BLACK, font="Latin Modern Roman")

X = np.array([[-0.49, -1.89], [-1.05, -1.2], [-1.36, -1.08], [-1.91, -1.08], [-1.5, 0.16], [-1.12, -1.12],
              [1.2, -0.83], [0.93, -0.74], [1.47, -0.68], [1.64, -0.67], [1.31, -0.06], [1.49, -0.78],
              [0.04, 1.49], [0.78, 1.21], [0.01, 1.65], [-0.21, 1.2], [0.41, 1.5], [0.13, 1.53]])
START = X[[3, 4, 5]].copy()          # three students picked "at random" as the first centroids


class KMeans2D(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, title, sub):
        g = VGroup(Paragraph(*title.split("|"), font_size=26, weight=BOLD, color=BLACK, font="Latin Modern Roman"),
                   Paragraph(*sub.split("|"), font_size=20, color=GREY_C, font="Latin Modern Roman"))
        return g.arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(self.heading, DOWN, buff=0.5, aligned_edge=LEFT)

    def construct(self):
        self.snaps = []
        ax = Axes(x_range=[0, 4.4, 1], y_range=[0, 4.0, 1], x_length=6.4, y_length=5.8, tips=False,
                  axis_config={"color": GREY_C, "include_ticks": False}).to_edge(LEFT, buff=0.9).shift(DOWN * 0.2)
        OFF = np.array([2.3, 2.1])        # shift the standardized values so the axes sit at the bottom left
        xl = Text("CGPA (standardized)", font_size=20).next_to(ax.x_axis, DOWN, buff=0.2)
        yl = Text("IQ (standardized)", font_size=20).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.2)
        dots = VGroup(*[Dot(ax.c2p(*(p + OFF)), radius=0.08, color=GREY_C) for p in X])
        heading = Text("k-means, k = 3", font_size=34, weight=BOLD).next_to(ax, RIGHT, buff=0.6).align_to(ax, UP)
        self.heading = heading

        def marks(cs):
            return VGroup(*[Cross(scale_factor=0.17, stroke_color=c, stroke_width=9).move_to(ax.c2p(*(p + OFF)))
                            for p, c in zip(cs, COLOURS)])

        c = START.copy()
        cm = marks(c)
        cap = self.caption("2. Pick 3 starting centroids", "three students chosen|at random (crosses)")
        self.play(Create(ax), FadeIn(xl, yl, dots, heading))
        self.play(FadeIn(cm), FadeIn(cap))
        self.wait(0.8)
        self.snap()

        it = 1
        while True:
            lab = ((X[:, None] - c) ** 2).sum(2).argmin(1)
            if it == 1:
                # Show the three distances for one student
                p = X[0]
                lines = VGroup(*[DashedLine(ax.c2p(*(p + OFF)), ax.c2p(*(q + OFF)), color=col, stroke_width=4)
                                 for q, col in zip(c, COLOURS)])
                self.play(Create(lines), Transform(cap, self.caption(
                    "3. Assign: measure distances", "from each student to every|centroid (Euclidean distance)")))
                self.wait(0.6)
                self.play(FadeOut(lines))
            changed = [d.animate.set_color(COLOURS[k]) for d, k in zip(dots, lab)]
            self.play(*changed, Transform(cap, self.caption(
                "3. Assign each student to|its nearest centroid", f"round {it}: colour = nearest centroid")))
            self.wait(0.6)
            if it == 1:
                self.snap()
            new = np.array([X[lab == k].mean(0) for k in range(3)])
            if np.allclose(new, c):
                self.play(Transform(cap, self.caption("5. Centroids did not move:|stop",
                                                      f"finished after {it} rounds:|three clusters")))
                self.wait(1.5)
                self.snap()
                break
            self.play(Transform(cm, marks(new)), Transform(cap, self.caption(
                "4. Move each centroid to|the mean of its points", "new centroid = (mean CGPA,|mean IQ) of each colour")),
                run_time=1.4)
            self.wait(0.6)
            if it in (1, 2):
                self.snap()
            c, it = new, it + 1
        self.snaps = [self.snaps[0], self.snaps[1], self.snaps[2], self.snaps[-1]]


def key_frames_grid(frames, out, gap=16, pad=20):
    boxes = [ImageOps.invert(f.convert("RGB")).getbbox() for f in frames[:4]]
    l, t = min(b[0] for b in boxes) - pad, min(b[1] for b in boxes) - pad
    r, b_ = max(b[2] for b in boxes) + pad, max(b[3] for b in boxes) + pad
    frames = [f.crop((max(l, 0), max(t, 0), r, b_)) for f in frames]
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "kmeans_2d", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = KMeans2D()
        scene.render()
    mp4 = HERE / "kmeans_2d.mp4"
    shutil.copy(next(media.rglob("kmeans_2d.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "kmeans_2d.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "kmeans_2d_frames.png")
    shutil.rmtree(media)
