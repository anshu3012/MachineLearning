"""The distance formula as a dot product (Manim): the points a = (1, 2) and b = (4, 5), the difference vector
b - a = (3, 3), its dot product with itself, 3*3 + 3*3 = 18, and the square root, 4.24. Then a third feature is
added, (1, 2, 3) and (4, 5, 6): one more term, 27, and the square root 5.196, from the same line of code.
Run: python distance_dot.py  -> distance_dot.gif, distance_dot_frames.png"""
import glob
import shutil
import subprocess
from pathlib import Path

import manimpango
import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
for f in glob.glob("/usr/share/texmf/fonts/opentype/public/lm/lmroman*.otf"):   # topgro: register Latin Modern
    manimpango.register_font(f)
BLUE_C, RED_C, GREEN_C, GREY_C = "#4C78A8", "#E45756", "#54A24B", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
a, b = np.array([1, 2]), np.array([4, 5])
assert np.isclose(np.sqrt(np.dot(b - a, b - a)), 4.2426, atol=1e-4)
assert np.isclose(np.sqrt(np.dot(np.array([3, 3, 3]), np.array([3, 3, 3]))), 5.196, atol=1e-3)


class DistanceDot(Scene):
    def snap(self):
        self.snaps.append(self.camera.get_image().convert("RGB"))

    def construct(self):
        self.snaps = []
        ax = Axes(x_range=[0, 5.5, 1], y_range=[0, 6, 1], x_length=4.4, y_length=5.4, tips=False,
                  axis_config=dict(color=BLACK, include_numbers=True, font_size=26,
                                   decimal_number_config=dict(color=BLACK, num_decimal_places=0))).to_edge(LEFT, buff=0.6)
        pa, pb, corner = ax.c2p(1, 2), ax.c2p(4, 5), ax.c2p(4, 2)
        da, db = Dot(pa, color=BLUE_C, radius=0.11), Dot(pb, color=BLUE_C, radius=0.11)
        la = Text("a = (1, 2)", font_size=28).next_to(da, DOWN, buff=0.15, aligned_edge=LEFT)
        lb = Text("b = (4, 5)", font_size=28).next_to(db, UP, buff=0.15)
        self.play(Create(ax), FadeIn(da, db, la, lb), run_time=1)
        arrow = Arrow(pa, pb, buff=0, color=RED_C, stroke_width=6)
        side1 = DashedLine(pa, corner, color=GREY_C)
        side2 = DashedLine(corner, pb, color=GREY_C)
        t1 = Text("4 − 1 = 3", font_size=26, color=GREY_C).next_to(side1, DOWN, buff=0.7).shift(RIGHT * 0.4)
        t2 = Text("5 − 2 = 3", font_size=26, color=GREY_C).next_to(side2, RIGHT, buff=0.12)
        self.play(Create(side1), FadeIn(t1), run_time=0.8)
        self.play(Create(side2), FadeIn(t2), run_time=0.8)
        self.play(GrowArrow(arrow), run_time=0.8)

        def line(s, size=28, col=BLACK):
            return Text(s, font_size=size, color=col)

        rows = VGroup(line("difference vector"), line("b − a = (3, 3)", col=RED_C),
                      line("dot product with itself"), line("(3, 3) · (3, 3) = 3×3 + 3×3 = 18"),
                      line("square root"), line("distance = √18 = 4.24", col=RED_C))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.3).shift(UP * 1.2)
        for i in (0, 2, 4):
            rows[i].set_color(GREY_C).scale(0.8, about_edge=LEFT)
        self.play(FadeIn(rows[0], rows[1]), run_time=0.7)
        self.wait(0.8)
        self.snap()
        self.play(FadeIn(rows[2], rows[3]), run_time=0.7)
        self.wait(1)
        self.play(FadeIn(rows[4], rows[5]), run_time=0.7)
        self.wait(1.5)
        self.snap()
        # a third feature: the same line of code, one more term
        new = VGroup(line("add a third feature", 24, GREY_C), line("a = (1, 2, 3),  b = (4, 5, 6)"),
                     line("b − a = (3, 3, 3)", col=RED_C), line("3×3 + 3×3 + 3×3 = 27"),
                     line("distance = √27 = 5.196", col=RED_C))
        new.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(rows, aligned_edge=UL)
        code = Text("np.sqrt(np.dot(b - a, b - a))", font="DejaVu Sans Mono", font_size=26, color=GREEN_C)
        note = Text("the same code for 2, 3 or 100 features", font_size=26, color=GREEN_C)
        foot = VGroup(code, note).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(new, DOWN, buff=0.5,
                                                                                    aligned_edge=LEFT)
        self.play(FadeOut(rows), run_time=0.5)
        for r in new:
            self.play(FadeIn(r), run_time=0.5)
            self.wait(0.5)
        self.play(FadeIn(foot), run_time=0.6)
        self.wait(2.5)
        self.snap()


if __name__ == "__main__":
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "distance_dot", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = DistanceDot()
        scene.render()
    mp4 = next(media.rglob("distance_dot.mp4"))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=10,scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "distance_dot.gif")], check=True)
    w, h = scene.snaps[0].size
    grid = Image.new("RGB", (w, 3 * h), "white")
    for i, im in enumerate(scene.snaps):
        grid.paste(im, (0, i * h))
    grid.save(HERE / "distance_dot_frames.png")
    shutil.rmtree(media)
