"""The line 2x + 3y + 5 = 0: what C, A and B do to it, then one update of the perceptron trick (Manim).
A negative point (4, 5) sits on the positive (green) side; subtracting (4, 5, 1) from (2, 3, 5) gives (-2, -2, 4)
and the point lands on the negative side.
Run: python abc_update.py -> abc_update.mp4, .gif, _frames.png"""
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
U, CX, CY, R = 0.36, -3.5, -0.5, 8                      # plot unit, centre, half-range of the plane
PT = np.array([4.0, 5.0])
assert 2 * 4 + 3 * 5 + 5 == 28 and -2 * 4 - 2 * 5 + 4 == -14   # before: positive side; after: negative side


def P(x, y):
    return np.array([CX + x * U, CY + y * U, 0])


def term(v, name, first=False):
    sign = "−" if v < 0 else ("" if first else "+")
    return f"{sign} {abs(v):.1f}{name}".strip()


class ABC(Scene):
    def construct(self):
        self.snaps = []
        A, B, C = ValueTracker(2), ValueTracker(3), ValueTracker(5)

        def geom():
            a, b, c = A.get_value(), B.get_value(), C.get_value()
            n = np.array([a, b]) / np.hypot(a, b)
            p0 = -c * np.array([a, b]) / (a * a + b * b)
            d = np.array([-n[1], n[0]])
            return p0, d, n

        def side():
            p0, d, n = geom()
            q = [p0 - 40 * d, p0 + 40 * d, p0 + 40 * d + 40 * n, p0 - 40 * d + 40 * n]
            return Polygon(*[P(*v) for v in q], stroke_width=0, fill_color=GREEN_C, fill_opacity=0.18)

        def line():
            p0, d, _ = geom()
            return Line(P(*(p0 - 40 * d)), P(*(p0 + 40 * d)), color=BLACK, stroke_width=6)

        def eq():
            a, b, c = A.get_value(), B.get_value(), C.get_value()
            return Text(f"{term(a, 'x', True)} {term(b, 'y')} {term(c, '')} = 0", font_size=40).move_to([3.3, 1.6, 0])

        box = Square(side_length=2 * R * U, color=GREY_C, stroke_width=2).move_to(P(0, 0))
        axes = VGroup(Line(P(-R, 0), P(R, 0), color=GREY_C, stroke_width=2), Line(P(0, -R), P(0, R), color=GREY_C, stroke_width=2))
        # white masks hide whatever falls outside the plot box
        masks = VGroup(*[Rectangle(width=w, height=h, stroke_width=0, fill_color=WHITE, fill_opacity=1).move_to(c) for w, h, c in
                         ((30, 10, box.get_top() + UP * 5), (30, 10, box.get_bottom() + DOWN * 5),
                          (20, 30, box.get_left() + LEFT * 10), (20, 30, box.get_right() + RIGHT * 10))]).set_z_index(5)
        title = Text("What A, B and C do to the line Ax + By + C = 0", font_size=32, weight=BOLD).to_edge(UP, buff=0.2).set_z_index(10)
        plus = Text("green: positive side, Ax + By + C > 0", font_size=26, color=GREEN_C).move_to([3.3, 2.5, 0]).set_z_index(10)
        self.add(always_redraw(side), axes, always_redraw(line), masks, box.set_z_index(6), title, plus,
                 always_redraw(lambda: eq().set_z_index(10)))

        def say(s, color=BLUE_C):
            t = Text(s, font_size=27, color=color, line_spacing=0.9).move_to([3.3, 0.2, 0]).set_z_index(10)
            if hasattr(self, "cap"):
                self.remove(self.cap)
            self.cap = t
            self.add(t)

        def snap():
            self.snaps.append(Image.fromarray(self.renderer.get_frame()))

        self.wait(0.8)
        say("Change C:\nthe line slides, staying parallel")
        self.play(C.animate.set_value(10), run_time=1.2)
        snap()
        self.play(C.animate.set_value(0), run_time=1.4)
        self.play(C.animate.set_value(5), run_time=0.8)
        say("Change A or B:\nthe line turns")
        self.play(A.animate.set_value(4), run_time=1.0)
        self.play(A.animate.set_value(1), run_time=1.2)
        snap()
        self.play(A.animate.set_value(2), run_time=0.6)
        self.play(B.animate.set_value(6), run_time=1.0)
        self.play(B.animate.set_value(1), run_time=1.2)
        self.play(B.animate.set_value(3), run_time=0.8)
        # one update
        dot = Dot(P(*PT), radius=0.13, color=RED_C).set_z_index(7)
        dl = Text("(4, 5)", font_size=28, color=RED_C).next_to(dot, DOWN, buff=0.12).set_z_index(7)
        say("A negative point on the positive side:\n2(4) + 3(5) + 5 = 28 > 0, misclassified", RED_C)
        self.play(FadeIn(dot, dl), run_time=0.6)
        self.wait(1.6)
        snap()
        work = Text("(2, 3, 5) − (4, 5, 1) = (−2, −2, 4)", font_size=30).move_to([3.3, -1.5, 0]).set_z_index(10)
        say("Subtract the point, with a 1 appended,\nfrom the coefficients", BLUE_C)
        self.play(FadeIn(work), run_time=0.6)
        self.wait(0.8)
        self.play(A.animate.set_value(-2), B.animate.set_value(-2), C.animate.set_value(4), run_time=2.5)
        say("Now −2(4) − 2(5) + 4 = −14 < 0:\nthe point is on the negative side", GREEN_C)
        self.wait(2.2)
        snap()


if __name__ == "__main__":
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "frame_rate": 15, "background_color": WHITE, "media_dir": str(media),
                     "output_file": "abc_update", "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = ABC()
        scene.render()
    mp4 = HERE / "abc_update.mp4"
    shutil.copy(next(media.rglob("abc_update.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=10,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "abc_update.gif")], check=True)
    w, h = scene.snaps[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, f in enumerate(scene.snaps[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "abc_update_frames.png")
    shutil.rmtree(media)
