"""Why the gradients must be parallel (idea: Sanderson's Khan Academy lessons on Lagrange multipliers; our own code).
Minimise f = x^2 + 2y^2 on x + y = 3. A point slides along the line. Its gradient grad f = (2x, 4y) splits into a
part across the line and a part along it (red). While the part along the line is not zero, stepping against it
lowers f without leaving the line. It vanishes only at (2, 1), where grad f = 4 * (1, 1): lambda = 4.
Then the line moves to x + y = c: the best value f*(c) = 2c^2/3 rises at the rate lambda = 4c/3.
Run: python slide_along.py  -> slide_along.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
G = 0.17                                            # arrow length per unit of gradient
U = np.array([1.0, -1.0]) / np.sqrt(2)              # direction of the line


def f(x, y):
    return x ** 2 + 2 * y ** 2


def boxed(mob, buff=0.08):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


class SlideAlong(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        s = ValueTracker(1.2)                       # point (s, c - s)
        c = ValueTracker(3.0)
        ax = Axes(x_range=[-3.2, 4.4, 1], y_range=[-2, 3.6, 1], x_length=7.4, y_length=5.9, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": True, "font_size": 26,
                               "decimal_number_config": {"color": BLACK, "num_decimal_places": 0}})
        ax.to_edge(LEFT, buff=0.4).shift(DOWN * 0.3)
        xl = MathTex("x", color=BLACK, font_size=34).next_to(ax.x_axis, RIGHT, buff=0.1)
        yl = MathTex("y", color=BLACK, font_size=34).next_to(ax.y_axis, UP, buff=0.1)
        line = always_redraw(lambda: ax.plot(lambda x: c.get_value() - x, x_range=[c.get_value() - 3.5, 4.2],
                                             color=ORANGE_C, stroke_width=5))
        pt = lambda: np.array([s.get_value(), c.get_value() - s.get_value()])

        def level():                                # the ellipse through the current point
            k = f(*pt())
            return DashedVMobject(ax.plot_parametric_curve(
                lambda t: np.array([np.sqrt(k) * np.cos(t), np.sqrt(k / 2) * np.sin(t), 0]), t_range=[0, TAU],
                color=BLUE_C, stroke_width=3), num_dashes=50)

        def arrows():
            p = pt()
            g = np.array([2 * p[0], 4 * p[1]])
            along = (g @ U) * U
            grp = VGroup(Arrow(ax.c2p(*p), ax.c2p(*(p + G * g)), buff=0, color=BLUE_C, stroke_width=6,
                               max_tip_length_to_length_ratio=0.18))
            if np.linalg.norm(along) * G > 0.08:
                grp.add(Arrow(ax.c2p(*p), ax.c2p(*(p - G * along)), buff=0, color=RED_C, stroke_width=7,
                              max_tip_length_to_length_ratio=0.3))
            grp.add(Dot(ax.c2p(*p), color=BLACK, radius=0.08))
            return grp

        def readout():
            p = pt()
            g = np.array([2 * p[0], 4 * p[1]])
            a = g @ U
            rows = VGroup(MathTex(rf"(x, y) = ({p[0]:.1f},\ {p[1]:.1f})", color=BLACK, font_size=38),
                          MathTex(rf"f = {f(*p):.2f}", color=BLACK, font_size=38),
                          MathTex(rf"\nabla f = ({g[0]:.1f},\ {g[1]:.1f})", color=BLUE_C, font_size=38),
                          MathTex(rf"\text{{part along the line}} = {abs(a):.1f}", color=RED_C, font_size=36))
            return boxed(rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22), 0.1).move_to([4.0, 1.6, 0])

        legend = boxed(VGroup(MathTex(r"\text{blue: } \nabla f", color=BLUE_C, font_size=32),
                              Tex(r"red: downhill along the line", color=RED_C, font_size=32)).arrange(DOWN, aligned_edge=LEFT, buff=0.1), 0.08)
        legend.move_to([4.0, -0.4, 0])
        self.add(ax, xl, yl, line, always_redraw(level), always_redraw(arrows), always_redraw(readout), legend)
        self.wait(1.0)
        self.snap()                                 # (1.2, 1.8): red part points right, f can still drop
        self.play(s.animate.set_value(3.0), run_time=2.5, rate_func=linear)
        self.wait(0.6)
        self.snap()                                 # (3, 0): red part points left
        self.play(s.animate.set_value(2.0), run_time=2.2, rate_func=smooth)
        msg = boxed(Tex(r"red part gone at $(2, 1)$:\\ $\nabla f = (4, 4) = 4\,(1, 1)$,\\ so $\lambda = 4$",
                        color=GREEN_C, font_size=36), 0.1).move_to([4.0, -2.2, 0])
        self.play(FadeIn(msg))
        self.wait(1.4)
        self.snap()                                 # tangency: parallel gradients, lambda = 4
        self.play(FadeOut(msg))

        # the multiplier as a price: move the line, the best point moves with it
        price = always_redraw(lambda: boxed(VGroup(
            MathTex(rf"x + y = c = {c.get_value():.2f}", color=ORANGE_C, font_size=36),
            MathTex(rf"f^\ast = 2c^2/3 = {2 * c.get_value() ** 2 / 3:.2f}", color=BLACK, font_size=36),
            MathTex(rf"6 + 4\,(c - 3) = {6 + 4 * (c.get_value() - 3):.2f}", color=GREEN_C, font_size=36)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15), 0.1).move_to([4.0, -2.2, 0]))
        self.add(price)
        self.wait(0.8)
        self.play(c.animate.set_value(3.3), s.animate.set_value(2.2), run_time=2.5)
        self.wait(1.0)
        tag = boxed(Tex(r"$\lambda = 4$: each unit of $c$ costs about 4", color=GREEN_C, font_size=34), 0.08)
        tag.to_edge(UP, buff=0.15)
        self.play(FadeIn(tag))
        self.wait(1.8)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, hgt = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * hgt + gap), "white")
    for i, fr in enumerate(frames[:4]):
        sheet.paste(fr.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (hgt + gap)))
    sheet.save(out)


if __name__ == "__main__":
    xs = np.linspace(0, 3, 3001)                    # the best point on x + y = 3 is (2, 1), f = 6
    assert abs(xs[np.argmin(f(xs, 3 - xs))] - 2) < 1e-9
    assert abs(np.array([4, 4]) @ U) < 1e-12        # grad f has no part along the line there
    cc = 3.3                                        # the best point on x + y = c is (2c/3, c/3)
    assert abs(f(2 * cc / 3, cc / 3) - 2 * cc ** 2 / 3) < 1e-12
    name = "slide_along"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = SlideAlong()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
