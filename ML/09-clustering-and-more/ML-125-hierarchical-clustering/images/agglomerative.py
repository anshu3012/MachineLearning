"""Agglomerative clustering of 6 points, merge by merge, with the dendrogram growing beside the scatter plot.
Distances between clusters: single linkage (closest pair). Then a cut that leaves 2 clusters.
Run: python agglomerative.py  -> agglomerative.mp4, agglomerative.gif, agglomerative_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image, ImageOps
from scipy.cluster.hierarchy import dendrogram, linkage

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, PURPLE_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"
MERGE_COLOURS = [BLUE_C, ORANGE_C, GREEN_C, PURPLE_C, RED_C]
Text.set_default(color=BLACK, font="Latin Modern Roman")

P = np.array([[1, 4], [1.6, 4.4], [4.2, 2.0], [5, 2.8], [5.4, 2.5], [6.2, 4.2]])
Z = linkage(P, "single")
LEAVES = dendrogram(Z, no_plot=True)["leaves"]          # left-to-right order of the points under the tree


class Agglomerative(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, text):
        return Text(text, font_size=24, color=GREY_C).to_edge(DOWN, buff=0.35)

    def construct(self):
        self.snaps = []
        heading = Text("Agglomerative clustering: merge the closest pair, repeat", font_size=30,
                       weight=BOLD).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 7, 1], y_range=[1, 5, 1], x_length=5.6, y_length=4.2, tips=False,
                  axis_config={"color": GREY_C, "include_ticks": False}).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        dots = [Dot(ax.c2p(*p), radius=0.09, color=BLACK) for p in P]
        labels = [Text(str(i + 1), font_size=24).next_to(d, UR, buff=0.05) for i, d in enumerate(dots)]

        dg = Axes(x_range=[0, 6, 1], y_range=[0, 4, 1], x_length=5.4, y_length=4.2, tips=False,
                  axis_config={"color": GREY_C}, y_axis_config={"include_ticks": True, "include_numbers": True,
                                                                  "font_size": 30, "decimal_number_config":
                                                                  {"color": BLACK, "num_decimal_places": 0}}
                  ).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.2)
        dg.x_axis.set_opacity(0.0)
        ylab = Text("merge distance", font_size=20).rotate(PI / 2).next_to(dg.y_axis, LEFT, buff=0.45)
        xpos = {leaf: i + 0.5 for i, leaf in enumerate(LEAVES)}
        leaf_labels = VGroup(*[Text(str(leaf + 1), font_size=24).move_to(dg.c2p(xpos[leaf], 0) + DOWN * 0.3)
                               for leaf in LEAVES])
        self.play(FadeIn(heading), Create(ax), *[FadeIn(d) for d in dots], *[FadeIn(l) for l in labels],
                  Create(dg), FadeIn(ylab, leaf_labels),
                  FadeIn(cap := self.caption("start: every point is its own cluster (6 clusters)")))
        self.wait(0.8)

        n = len(P)
        height = {i: 0.0 for i in range(n)}
        members = {i: [i] for i in range(n)}
        for step, (a, b, d, _) in enumerate(Z):
            a, b, new = int(a), int(b), n + step
            col = MERGE_COLOURS[step]
            members[new] = members[a] + members[b]
            xpos[new] = (xpos[a] + xpos[b]) / 2
            height[new] = d
            group = VGroup(*[dots[i] for i in members[new]])
            ring = SurroundingRectangle(VGroup(group, *[labels[i] for i in members[new]]), color=col, buff=0.1 + 0.07 * len(members[new]), corner_radius=0.2, stroke_width=4)
            u = VMobject(color=col, stroke_width=5).set_points_as_corners([
                dg.c2p(xpos[a], height[a]), dg.c2p(xpos[a], d), dg.c2p(xpos[b], d), dg.c2p(xpos[b], height[b])])
            left = n - step - 1
            names = ", ".join(str(i + 1) for i in sorted(members[new]))
            self.play(Create(ring), Create(u), Transform(cap, self.caption(
                f"merge {step + 1}: {{{names}}} at distance {d:.2f}, so {left} cluster{'s' if left > 1 else ''} left")),
                run_time=1.2)
            self.wait(0.7)
            if step in (0, 2, 4):
                self.snap()

        cut = DashedLine(dg.c2p(0, 2.6), dg.c2p(6, 2.6), color=RED_C, stroke_width=5)
        self.play(Create(cut), Transform(cap, self.caption(
            "cut the tree at 2.6: it crosses 2 vertical lines, so 2 clusters: {1, 2} and {3, 4, 5, 6}")))
        self.wait(1.5)
        self.snap()


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
                     "output_file": "agglomerative", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = Agglomerative()
        scene.render()
    mp4 = HERE / "agglomerative.mp4"
    shutil.copy(next(media.rglob("agglomerative.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "agglomerative.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "agglomerative_frames.png")
    shutil.rmtree(media)
