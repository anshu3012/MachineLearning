"""The perceptron loss on four points, one per case (Manim). Line 2x + 3y + 4 = 0, labels +1 and -1.
For each point the chain y -> f(x) -> -y f(x) -> max(0, .) fills in: correct points cost 0, the two mistakes cost 6 and 30.
Run: python four_cases.py -> four_cases.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image
import manimpango

for f in Path("/usr/share/texmf/fonts/opentype/public/lm").glob("lmroman10-*.otf"):   # pango on topgro misses LM
    manimpango.register_font(str(f))

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
W = np.array([2.0, 3.0, 4.0])
PTS = [((2, 2), 1), ((-4, -3), -1), ((-2, -2), 1), ((4, 6), -1)]        # the four cases of the Note's table
F = [W[0] * x + W[1] * y + W[2] for (x, y), _ in PTS]
LOSS = [max(0, -lab * f) for (_, lab), f in zip(PTS, F)]
assert F == [14, -13, -6, 30] and LOSS == [0, 0, 6, 30] and sum(LOSS) / 4 == 9
U, CX, CY, R = 0.38, -4.0, -0.4, 7


def P(x, y):
    return np.array([CX + x * U, CY + y * U, 0])


def num(v):
    return f"{v:+.0f}".replace("-", "−") if v else "0"


class Cases(Scene):
    def construct(self):
        snaps = []
        title = Text("Perceptron loss of one point: max(0, −y f(x))", font_size=34, weight=BOLD).to_edge(UP, buff=0.2)
        box = Square(side_length=2 * R * U, color=GREY_C, stroke_width=2).move_to(P(0, 0))
        # positive side of 2x + 3y + 4 = 0 inside the box: corners clipped by hand
        ends = [P(-R, (-4 + 2 * R) / 3), P(R, (-4 - 2 * R) / 3)]
        side = Polygon(ends[0], P(-R, R), P(R, R), ends[1], stroke_width=0, fill_color=GREEN_C, fill_opacity=0.15)
        line = Line(*ends, color=BLACK, stroke_width=6)
        lab = Text("f(x) = 2x₁ + 3x₂ + 4", font_size=26).next_to(box, DOWN, buff=0.15)
        sides = VGroup(Text("f > 0", font_size=28, color=GREEN_C).move_to(P(4.5, -3)), Text("f < 0", font_size=28, color=GREY_C).move_to(P(-5, -5.5)))
        dots = [Dot(P(*p), radius=0.14, color=BLUE_C if y > 0 else ORANGE_C) for p, y in PTS]
        legend = VGroup(Dot(color=BLUE_C, radius=0.12), Text("y = +1", font_size=26), Dot(color=ORANGE_C, radius=0.12),
                        Text("y = −1", font_size=26)).arrange(RIGHT, buff=0.2).next_to(box, UP, buff=0.12)
        self.add(title, side, box, line, lab, sides, *dots, legend)
        cols = [0.3, 1.9, 3.1, 4.5, 6.1]
        head = [Text(s, font_size=28, weight=BOLD).move_to([x, 2.0, 0]) for s, x in zip(("point", "y", "f(x)", "−y f(x)", "loss"), cols)]
        rule = Line([-0.6, 1.6, 0], [6.9, 1.6, 0], color=GREY_C, stroke_width=2)
        self.add(*head, rule)
        self.wait(0.6)
        for r, (((x, y), labl), f, ls) in enumerate(zip(PTS, F, LOSS)):
            yy = 1.0 - 0.85 * r
            ring = Circle(radius=0.3, color=RED_C if ls else GREEN_C, stroke_width=6).move_to(dots[r])
            cells = [Text(f"({x}, {y})".replace("-", "−"), font_size=28), Text(num(labl), font_size=28, color=BLUE_C if labl > 0 else ORANGE_C),
                     Text(num(f), font_size=28), Text(num(-labl * f), font_size=28),
                     Text(f"{ls:.0f}", font_size=30, weight=BOLD, color=RED_C if ls else GREEN_C)]
            for c, xx in zip(cells, cols):
                c.move_to([xx, yy, 0])
            self.play(Create(ring), FadeIn(cells[0], cells[1]), run_time=0.6)
            for c in cells[2:]:
                self.play(FadeIn(c, shift=RIGHT * 0.2), run_time=0.5)
            verdict = Text("correct side: costs nothing" if ls == 0 else "wrong side: costs |f(x)|", font_size=26,
                           color=GREEN_C if ls == 0 else RED_C).move_to([3.2, -2.6, 0])
            self.play(FadeIn(verdict), run_time=0.3)
            self.wait(0.9)
            if r in (0, 2):
                snaps.append(Image.fromarray(self.renderer.get_frame()))
            self.play(FadeOut(verdict), ring.animate.set_stroke(width=3), run_time=0.3)
        total = Text("L = (0 + 0 + 6 + 30) / 4 = 9", font_size=34).move_to([3.2, -2.6, 0])
        self.play(FadeIn(total), run_time=0.5)
        self.wait(2.0)
        snaps.append(Image.fromarray(self.renderer.get_frame()))
        self.snaps = snaps


if __name__ == "__main__":
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "frame_rate": 15, "background_color": WHITE, "media_dir": str(media),
                     "output_file": "four_cases", "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = Cases()
        scene.render()
    mp4 = HERE / "four_cases.mp4"
    shutil.copy(next(media.rglob("four_cases.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=10,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "four_cases.gif")], check=True)
    w, h = scene.snaps[0].size
    sheet = Image.new("RGB", (w, 3 * h + 32), "white")
    for i, f in enumerate(scene.snaps):
        sheet.paste(f.convert("RGB"), (0, i * (h + 16)))
    sheet.save(HERE / "four_cases_frames.png")
    shutil.rmtree(media)
