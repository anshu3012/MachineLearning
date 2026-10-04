"""Conditioning shrinks the sample space (two dice, sections 3-4). The 36 outcomes, then A = (die 1 = 5) and
B = (sum <= 10); knowing B rules out 3 cells, and the 33 left are re-laid as the whole world (same total area),
where A covers 5 cells: P(A | B) = 5/33. Then the roles swap: given A, only its 6 cells remain and 5 lie in B,
so P(B | A) = 5/6. Geometric idea after Sanderson (3Blue1Brown), "Bayes theorem, the geometry of changing beliefs".
Run: python shrink_space.py -> shrink_space.mp4, shrink_space.gif, shrink_space_frames.png (Manim + ffmpeg)"""
import shutil
import subprocess
from fractions import Fraction
from itertools import product
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, RED_C, GREY_C, PALE = "#4C78A8", "#F58518", "#E45756", "#9A9A9A", "#DCE6F2"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MathTex.set_default(color=BLACK)
S = 0.72                                                     # cell side of the 6 x 6 grid
OUT = list(product(range(1, 7), repeat=2))
IN_A = {o: o[0] == 5 for o in OUT}
IN_B = {o: sum(o) <= 10 for o in OUT}
assert Fraction(sum(IN_A[o] and IN_B[o] for o in OUT), sum(IN_B.values())) == Fraction(5, 33)
assert Fraction(sum(IN_A[o] and IN_B[o] for o in OUT), sum(IN_A.values())) == Fraction(5, 6)


def cell(o, side):
    sq = Square(side, stroke_color=WHITE, stroke_width=3, fill_color=PALE, fill_opacity=1)
    return VGroup(sq, Text(str(sum(o)), font_size=int(40 * side)).move_to(sq))


class ShrinkSpace(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def say(self, old, *lines):
        new = VGroup(*[t if isinstance(t, Mobject) else Text(t, font_size=30) for t in lines]
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, 0, 0])
        self.play(FadeOut(old), FadeIn(new), run_time=0.6) if old else self.play(FadeIn(new), run_time=0.6)
        return new

    def construct(self):
        self.snaps = []
        cells = {o: cell(o, S) for o in OUT}
        grid = VGroup(*cells.values()).arrange_in_grid(6, 6, buff=0).move_to([-3.1, -0.2, 0])
        lab1 = VGroup(*[Text(str(i), font_size=26, color=GREY_C).next_to(cells[(i, 1)], LEFT, buff=0.15)
                        for i in range(1, 7)])
        lab2 = VGroup(*[Text(str(j), font_size=26, color=GREY_C).next_to(cells[(1, j)], UP, buff=0.12)
                        for j in range(1, 7)])
        axes_lab = VGroup(Text("die 1", font_size=26).next_to(lab1, LEFT, buff=0.2).rotate(PI / 2),
                          Text("die 2", font_size=26).next_to(lab2, UP, buff=0.15))
        title = Text("Two dice: 36 equally likely outcomes", font_size=34).to_edge(UP, buff=0.3)
        self.play(FadeIn(title), FadeIn(grid, lag_ratio=0.02), FadeIn(lab1), FadeIn(lab2), FadeIn(axes_lab),
                  run_time=1.5)
        side = self.say(None, "numbers = sum of the dice")
        self.wait(0.5)

        # A: the die-1 = 5 row; B: sum <= 10
        a_box = SurroundingRectangle(VGroup(*[cells[(5, j)] for j in range(1, 7)]), color=ORANGE_C, buff=0.03,
                                     stroke_width=6)
        side = self.say(side, Text("A: die 1 = 5", font_size=32, color=ORANGE_C), MathTex(r"P(A) = 6/36", font_size=40))
        self.play(Create(a_box))
        self.wait(0.5)
        outB = [o for o in OUT if not IN_B[o]]
        side = self.say(side, Text("A: die 1 = 5", font_size=32, color=ORANGE_C),
                        Text("B: sum at most 10", font_size=32, color=BLUE_C),
                        MathTex(r"P(A) = 6/36", font_size=40), MathTex(r"P(B) = 33/36", font_size=40))
        self.play(*[cells[o][0].animate.set_fill(BLUE_C, 0.55) for o in OUT if IN_B[o]],
                  *[cells[o][0].animate.set_fill("#EEEEEE") for o in outB], run_time=1)
        self.wait(0.6)
        self.snap()

        # Condition on B: rule out the rest, mark A inside B
        side = self.say(side, Text("We learn: B happened", font_size=32, color=BLUE_C),
                        Text("the 3 outcomes outside B\nare ruled out", font_size=28))
        crosses = VGroup(*[Cross(cells[o], stroke_color=RED_C, stroke_width=5, scale_factor=0.6) for o in outB])
        self.play(Create(crosses))
        self.wait(0.4)
        self.snap()
        self.play(FadeOut(crosses), *[FadeOut(cells[o]) for o in outB], FadeOut(a_box), run_time=0.8)
        inAB = [o for o in OUT if IN_A[o] and IN_B[o]]
        self.play(*[cells[o][0].animate.set_fill(RED_C, 0.9) for o in inAB], run_time=0.8)
        self.wait(0.4)

        # Re-normalise: the 33 cells become the whole world (3 x 11, same total area as the 36)
        keep = [o for o in OUT if IN_B[o]]
        s2 = S * np.sqrt(36 / 33)
        target = VGroup(*[cell(o, s2) for o in keep]).arrange_in_grid(3, 11, buff=0).move_to([0, 1.0, 0])
        for t, o in zip(target, keep):
            t[0].set_fill(RED_C if o in inAB else BLUE_C, 0.9 if o in inAB else 0.55)
        world = SurroundingRectangle(target, color=BLACK, buff=0.02, stroke_width=4)
        self.play(FadeOut(side), FadeOut(lab1), FadeOut(lab2), FadeOut(axes_lab),
                  Transform(VGroup(*[cells[o] for o in keep]), target), run_time=1.6)
        self.play(Create(world), title.animate.become(
            Text("Given B: the 33 outcomes are the whole world", font_size=34).to_edge(UP, buff=0.3)))
        res = VGroup(Text("A takes 5 of the 33 cells", font_size=32, color=RED_C),
                     MathTex(r"P(A \mid B) = \frac{5}{33} \approx 0.152", font_size=52)
                     ).arrange(DOWN, buff=0.35).move_to([0, -2.2, 0])
        self.play(FadeIn(res[0]))
        self.play(Write(res[1]))
        self.wait(1.2)
        self.snap()

        # Swap the roles: condition on A instead
        self.play(*[FadeOut(m) for m in self.mobjects if m is not title])
        self.play(title.animate.become(Text("Swap the roles: given A, only die 1 = 5 is left",
                                            font_size=34).to_edge(UP, buff=0.3)))
        rowA = [(5, j) for j in range(1, 7)]
        start = VGroup(*[cell(o, S) for o in rowA]).arrange(RIGHT, buff=0).move_to([0, 2.0 - 4 * S, 0])
        for c, o in zip(start, rowA):
            c[0].set_fill(BLUE_C if IN_B[o] else "#EEEEEE", 0.55 if IN_B[o] else 1)
        big = VGroup(*[cell(o, 1.5) for o in rowA]).arrange(RIGHT, buff=0).move_to([0, 0.9, 0])
        for c, o in zip(big, rowA):
            c[0].set_fill(BLUE_C if IN_B[o] else "#EEEEEE", 0.55 if IN_B[o] else 1)
        self.play(FadeIn(start))
        self.play(Transform(start, big), run_time=1.2)
        self.play(Create(SurroundingRectangle(big, color=BLACK, buff=0.02, stroke_width=4)))
        res2 = VGroup(Text("B takes 5 of the 6 cells", font_size=32, color=BLUE_C),
                      MathTex(r"P(B \mid A) = \frac{5}{6} \quad \neq \quad P(A \mid B) = \frac{5}{33}", font_size=50)
                      ).arrange(DOWN, buff=0.35).move_to([0, -1.9, 0])
        self.play(FadeIn(res2[0]))
        self.play(Write(res2[1]))
        self.wait(2.5)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "shrink_space", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = ShrinkSpace()
        scene.render()
    mp4 = HERE / "shrink_space.mp4"
    shutil.copy(next(media.rglob("shrink_space.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=10,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "shrink_space.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "shrink_space_frames.png")
    shutil.rmtree(media)
