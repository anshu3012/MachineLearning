"""Lagrange multipliers as a picture: minimise f(x, y) = x^2 + 2y^2 on the line x + y = 3.
The level curve f = c is an ellipse; we grow c until the ellipse first touches the line. That happens at c = 6,
at the point (2, 1), where the ellipse is tangent to the line and the two gradients are parallel:
grad f = (4, 4), grad of the constraint x + y = (1, 1), so grad f = 4 * (1, 1) and lambda = 4.
Run: python tangency.py  -> tangency.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")


def boxed(mob, buff=0.08):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


class Tangency(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        c = ValueTracker(0.5)
        ax = Axes(x_range=[-2.6, 4, 1], y_range=[-2, 3.5, 1], x_length=7.2, y_length=6.0, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": True, "font_size": 26,
                               "decimal_number_config": {"color": BLACK, "num_decimal_places": 0}})
        ax.to_edge(LEFT, buff=0.5)
        xl = MathTex("x", color=BLACK, font_size=34).next_to(ax.x_axis, RIGHT, buff=0.1)
        yl = MathTex("y", color=BLACK, font_size=34).next_to(ax.y_axis, UP, buff=0.1)
        line = ax.plot(lambda x: 3 - x, x_range=[-0.5, 4], color=ORANGE_C, stroke_width=5)
        llab = boxed(MathTex("x + y = 3", color=ORANGE_C, font_size=36)).move_to(ax.c2p(3.3, 1.0))

        def ellipse():
            cv = c.get_value()
            col = GREEN_C if cv > 5.99 else BLUE_C
            return ax.plot_parametric_curve(lambda t: np.array([np.sqrt(cv) * np.cos(t),
                                                                np.sqrt(cv / 2) * np.sin(t), 0]),
                                            t_range=[0, TAU], color=col, stroke_width=5)

        ell = always_redraw(ellipse)
        readout = always_redraw(lambda: boxed(MathTex(rf"x^2 + 2y^2 = c = {c.get_value():.1f}", color=BLACK,
                                                      font_size=40), 0.1).move_to([3.6, 2.6, 0]))
        self.add(ax, xl, yl, line, llab, ell, readout)
        self.wait(0.6)
        self.snap()
        self.play(c.animate.set_value(3.0), run_time=2, rate_func=linear)
        miss = boxed(Tex(r"too small: no point\\ of the line on it", color=BLUE_C, font_size=36)).move_to([3.6, 1.2, 0])
        self.play(FadeIn(miss), run_time=0.4)
        self.wait(0.6)
        self.snap()
        self.play(FadeOut(miss), run_time=0.3)
        self.play(c.animate.set_value(6.0), run_time=2, rate_func=linear)
        p = Dot(ax.c2p(2, 1), color=BLACK, radius=0.09)
        touch = boxed(Tex(r"first touch at $(2, 1)$:\\ tangent to the line", color=GREEN_C, font_size=36))
        touch.move_to([3.6, 1.2, 0])
        self.play(FadeIn(p), FadeIn(touch))
        self.wait(0.6)
        self.snap()
        gf = Arrow(ax.c2p(2, 1), ax.c2p(2 + 1.25, 1 + 1.25), buff=0, color=BLUE_C, stroke_width=6,
                   max_tip_length_to_length_ratio=0.2)
        gh = Arrow(ax.c2p(2, 1), ax.c2p(2 + 0.55, 1 + 0.55), buff=0, color=ORANGE_C, stroke_width=7,
                   max_tip_length_to_length_ratio=0.35)
        gfl = MathTex(r"\nabla f", color=BLUE_C, font_size=36).next_to(gf.get_end(), UP, buff=0.1)
        ghl = MathTex(r"\nabla(x + y)", color=ORANGE_C, font_size=32).next_to(gh.get_end(), RIGHT, buff=0.15).shift(DOWN * 0.15)
        eq = boxed(Tex(r"$\nabla f = (4, 4)$, \ $\nabla(x + y) = (1, 1)$\\ parallel: $\nabla f = 4\,(1, 1)$,"
                       r" so $\lambda = 4$", color=BLACK, font_size=36)).move_to([3.6, -0.4, 0])
        self.play(GrowArrow(gf), GrowArrow(gh), FadeIn(gfl), FadeIn(ghl), FadeIn(eq))
        self.wait(1.5)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, hgt = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * hgt + gap), "white")
    for i, fr in enumerate(frames[:4]):
        sheet.paste(fr.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (hgt + gap)))
    sheet.save(out)


if __name__ == "__main__":
    assert 2 ** 2 + 2 * 1 ** 2 == 6 and 2 + 1 == 3
    name = "tangency"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = Tangency()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
