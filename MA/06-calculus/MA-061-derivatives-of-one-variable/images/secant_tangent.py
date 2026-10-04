"""The secant line turning into the tangent line as h shrinks, for f(x) = x^2 at x0 = 1.
Difference quotient ((1 + h)^2 - 1) / h = 2 + h: 3 at h = 1, 2.5 at h = 0.5, 2.1 at h = 0.1, and 2 in the limit.
Run: python secant_tangent.py  -> secant_tangent.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
X0 = 1.0
f = lambda x: x ** 2


def boxed(mob, buff=0.08):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


class SecantTangent(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        h = ValueTracker(1.0)
        ax = Axes(x_range=[-0.5, 2.6, 0.5], y_range=[-1, 6.5, 1], x_length=7.2, y_length=6.2, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": True, "font_size": 26,
                               "decimal_number_config": {"color": BLACK, "num_decimal_places": 1}},
                  y_axis_config={"decimal_number_config": {"color": BLACK, "num_decimal_places": 0}})
        ax.to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        curve = ax.plot(f, x_range=[-0.5, 2.5], color=BLUE_C, stroke_width=5)
        flab = MathTex(r"f(x) = x^2", color=BLUE_C, font_size=38).move_to(ax.c2p(0.55, 5.6))
        p0 = Dot(ax.c2p(X0, f(X0)), color=BLACK, radius=0.09)

        def secant():
            hv = h.get_value()
            m = (f(X0 + hv) - f(X0)) / hv
            line = lambda x: f(X0) + m * (x - X0)
            colour = GREEN_C if hv < 0.02 else ORANGE_C
            seg = ax.plot(line, x_range=[-0.3, 2.45], color=colour, stroke_width=4)
            q = Dot(ax.c2p(X0 + hv, f(X0 + hv)), color=colour, radius=0.09)
            return VGroup(seg, q) if hv >= 0.02 else VGroup(seg)

        def brace():
            hv = h.get_value()
            if hv < 0.15:
                return VGroup()
            a, b, c = ax.c2p(X0, f(X0)), ax.c2p(X0 + hv, f(X0)), ax.c2p(X0 + hv, f(X0 + hv))
            run = DashedLine(a, b, color=GREY_C, stroke_width=3)
            rise = DashedLine(b, c, color=GREY_C, stroke_width=3)
            hl = MathTex("h", color=BLACK, font_size=32).next_to(run, DOWN, buff=0.1)
            return VGroup(run, rise, hl)

        sec = always_redraw(secant)
        br = always_redraw(brace)
        formula = boxed(MathTex(r"\text{slope} = \frac{f(1 + h) - f(1)}{h} = 2 + h", color=BLACK, font_size=40), 0.12)
        formula.move_to([3.9, 2.4, 0])
        readout = always_redraw(lambda: boxed(MathTex(
            rf"h = {h.get_value():.2f} \qquad \text{{slope}} = {2 + h.get_value():.2f}",
            color=BLACK, font_size=40), 0.1).move_to([3.9, 0.9, 0]))
        self.add(ax, curve, flab, sec, br, p0, formula, readout)
        self.wait(0.6)
        self.snap()
        self.play(h.animate.set_value(0.5), run_time=2)
        self.wait(0.4)
        self.snap()
        self.play(h.animate.set_value(0.1), run_time=2)
        self.wait(0.4)
        self.snap()
        self.play(h.animate.set_value(0.0001), run_time=1.5)
        tan = boxed(Tex(r"$h \to 0$: the secant becomes\\ the tangent, slope $f'(1) = 2$", font_size=38,
                        color=GREEN_C), 0.12).move_to([3.9, -0.7, 0])
        self.play(FadeIn(tan))
        self.wait(1.2)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, hgt = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * hgt + gap), "white")
    for i, fr in enumerate(frames[:4]):
        sheet.paste(fr.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (hgt + gap)))
    sheet.save(out)


if __name__ == "__main__":
    assert abs((f(1.1) - f(1)) / 0.1 - 2.1) < 1e-9
    name = "secant_tangent"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = SecantTangent()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
