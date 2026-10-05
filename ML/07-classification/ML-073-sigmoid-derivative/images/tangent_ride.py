"""A tangent line rides the sigmoid; its slope is traced below and equals sigma(z) * (1 - sigma(z)).
At each z the vertical bar from 0 to 1 is split into sigma (blue) and 1 - sigma (orange); their product is the slope.
Run: python tangent_ride.py  -> tangent_ride.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")


def sig(z):
    return 1 / (1 + np.exp(-z))


def dsig(z):
    return sig(z) * (1 - sig(z))


def boxed(mob, buff=0.08):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


class TangentRide(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        z = ValueTracker(-6.0)
        ax_cfg = {"color": GREY_C, "include_numbers": True, "font_size": 28,
                  "decimal_number_config": {"color": BLACK, "num_decimal_places": 0}}
        top = Axes(x_range=[-6, 6, 2], y_range=[0, 1, 1], x_length=7.6, y_length=3.0, tips=False,
                   axis_config=ax_cfg).move_to([-1.4, 1.6, 0])
        bot = Axes(x_range=[-6, 6, 2], y_range=[0, 0.3, 0.1], x_length=7.6, y_length=2.4, tips=False,
                   x_axis_config={"include_numbers": True, "font_size": 28,
                                  "decimal_number_config": {"color": BLACK, "num_decimal_places": 0}},
                   y_axis_config={"include_numbers": True, "font_size": 24,
                                  "decimal_number_config": {"color": BLACK, "num_decimal_places": 1}},
                   axis_config={"color": GREY_C}).move_to([-1.4, -2.3, 0])
        curve = top.plot(sig, x_range=[-6, 6], color=BLUE_C, stroke_width=5)
        top_lab = MathTex(r"\sigma(z)", color=BLUE_C, font_size=40).next_to(top, LEFT, buff=0.2).shift(UP * 0.6)
        bot_lab = MathTex(r"\sigma'(z)", color=RED_C, font_size=40).next_to(bot, LEFT, buff=0.2).shift(UP * 0.5)
        zl = [MathTex("z", color=BLACK, font_size=36).next_to(a.x_axis, RIGHT, buff=0.15) for a in (top, bot)]
        ghost = DashedVMobject(bot.plot(dsig, x_range=[-6, 6], color="#CCCCCC", stroke_width=3), num_dashes=60)

        def tangent():
            v = z.get_value()
            s, m = sig(v), dsig(v)
            a, b = max(v - 1.6, -6) - v, min(v + 1.6, 6) - v   # keep the tangent inside the axes
            p0 = top.c2p(v + a, s + a * m)
            p1 = top.c2p(v + b, s + b * m)
            return Line(p0, p1, color=RED_C, stroke_width=6)

        def bars():
            v = z.get_value()
            s = sig(v)
            return VGroup(Line(top.c2p(v, 0), top.c2p(v, s), color=BLUE_C, stroke_width=9),
                          Line(top.c2p(v, s), top.c2p(v, 1), color=ORANGE_C, stroke_width=9))

        dot_top = always_redraw(lambda: Dot(top.c2p(z.get_value(), sig(z.get_value())), color=RED_C, radius=0.09))
        dot_bot = always_redraw(lambda: Dot(bot.c2p(z.get_value(), dsig(z.get_value())), color=RED_C, radius=0.09))
        trace = TracedPath(dot_bot.get_center, stroke_color=RED_C, stroke_width=5)

        def readout():
            v = z.get_value()
            s = sig(v)
            g = VGroup(MathTex(rf"z = {v:+.1f}", color=BLACK, font_size=38),
                       MathTex(rf"\sigma = {s:.3f}", color=BLUE_C, font_size=38),
                       MathTex(rf"1 - \sigma = {1 - s:.3f}", color=ORANGE_C, font_size=38),
                       MathTex(rf"\text{{slope}} = {s:.3f} \times {1 - s:.3f}", color=RED_C, font_size=34),
                       MathTex(rf"= {s * (1 - s):.3f}", color=RED_C, font_size=40))
            g.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.95, 0.9, 0])
            return g

        head = boxed(MathTex(r"\sigma'(z) = \sigma(z)\,\bigl(1 - \sigma(z)\bigr)", color=BLACK, font_size=36), 0.1)
        head.move_to([4.95, 3.3, 0])
        rd = always_redraw(readout)
        self.add(top, bot, curve, top_lab, bot_lab, *zl, ghost, trace, always_redraw(bars),
                 always_redraw(tangent), dot_top, dot_bot, rd, head)
        self.wait(0.6)
        self.play(z.animate.set_value(-4.0), run_time=1.2, rate_func=linear)
        self.wait(0.6)
        self.snap()                                   # z = -4: flat tangent, tiny slope
        self.play(z.animate.set_value(0.0), run_time=3, rate_func=linear)
        peak = boxed(Text("steepest: 0.5 × 0.5 = 0.25", font_size=30, color=RED_C), 0.08)
        peak.next_to(bot.c2p(0, 0.25), UP, buff=0.12)
        self.play(FadeIn(peak))
        self.wait(1.0)
        self.snap()                                   # z = 0: peak 0.25
        self.play(FadeOut(peak))
        self.play(z.animate.set_value(2.0), run_time=1.6, rate_func=linear)
        self.wait(1.0)
        self.snap()                                   # z = 2: 0.88 x 0.12
        self.play(z.animate.set_value(6.0), run_time=2.4, rate_func=linear)
        flat = boxed(Text("far from 0:\nslope near 0", font_size=32, color=RED_C), 0.08)
        flat.move_to([4.95, -2.4, 0])
        self.play(FadeIn(flat))
        self.wait(1.6)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    h = 1e-5
    for v in (-4.0, 0.0, 2.0):                    # the formula matches the numerical slope
        assert abs((sig(v + h) - sig(v - h)) / (2 * h) - dsig(v)) < 1e-8
    assert abs(dsig(0) - 0.25) < 1e-12
    name = "tangent_ride"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = TangentRide()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
