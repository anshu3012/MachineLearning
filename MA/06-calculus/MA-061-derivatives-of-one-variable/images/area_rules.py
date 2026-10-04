"""Derivative rules as growing areas (idea: 3Blue1Brown, "Power Rule through geometry" and
"Visualizing the chain rule and product rule"; our own code and numbers).
square_area: a square of side x = 1 grows by h. New area = 2 strips (x h each) + a corner h^2,
  so the change divided by h is 2x + h: 3, 2.5, 2.1 for h = 1, 0.5, 0.1, and 2 in the limit.
product_area: a rectangle with sides f = x^2 and g = 3x + 1 at x = 1 (1 by 4). Nudging x by h widens it by
  df = (1 + h)^2 - 1 and raises it by dg = 3h; the change in area over h tends to f'g + fg' = 2*4 + 1*3 = 11.
Run: python area_rules.py  -> square_area.{mp4,gif}, square_area_frames.png, product_area.{mp4,gif}, product_area_frames.png"""
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


def rect(x0, y0, w, h, colour, op=0.55):
    """Rectangle with lower-left corner (x0, y0) in screen units."""
    return Rectangle(width=max(w, 1e-3), height=max(h, 1e-3), stroke_color=BLACK, stroke_width=2,
                     fill_color=colour, fill_opacity=op).move_to([x0 + w / 2, y0 + h / 2, 0])


class Snapper(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))


class SquareArea(Snapper):
    def construct(self):
        self.snaps = []
        S = 3.0                                    # screen units per unit of x
        O = np.array([-5.6, -3.0])                 # lower-left corner of the square
        h = ValueTracker(1.0)

        def shapes():
            d = h.get_value() * S
            return VGroup(rect(*O, S, S, BLUE_C, 0.45),
                          rect(O[0] + S, O[1], d, S, ORANGE_C),
                          rect(O[0], O[1] + S, S, d, ORANGE_C),
                          rect(O[0] + S, O[1] + S, d, d, GREEN_C, 0.75))

        lab_sq = MathTex("x^2", color=BLACK, font_size=56).move_to([O[0] + S / 2, O[1] + S / 2, 0])
        side_x = MathTex("x = 1", color=BLACK, font_size=38).next_to([O[0] + S / 2, O[1], 0], DOWN, buff=0.15)

        def labels():
            d = h.get_value() * S
            v = h.get_value()
            g = VGroup(MathTex(r"x\,h", color=ORANGE_C, font_size=40).next_to([O[0] + S + d, O[1] + S / 2, 0], RIGHT, buff=0.12),
                       MathTex(r"x\,h", color=ORANGE_C, font_size=40).next_to([O[0] + S / 2, O[1] + S + d, 0], UP, buff=0.1))
            if v > 0.3:
                g.add(MathTex("h^2", color=BLACK, font_size=36).move_to([O[0] + S + d / 2, O[1] + S + d / 2, 0]))
            g.add(MathTex(rf"h = {v:.2f}", color=BLACK, font_size=38).next_to([O[0] + S + d, O[1], 0], DR, buff=0.12))
            return g

        def readout():
            v = h.get_value()
            g = VGroup(MathTex(r"\text{new area} = x^2 + 2xh + h^2", color=BLACK, font_size=40),
                       MathTex(r"\frac{\text{change}}{h} = 2x + h", color=BLACK, font_size=44),
                       MathTex(rf"= 2 + {v:.2f} = {2 + v:.2f}", color=RED_C, font_size=48))
            return g.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.4, 0.6, 0])

        self.add(always_redraw(shapes), lab_sq, side_x, always_redraw(labels), always_redraw(readout))
        self.wait(1.0)
        self.snap()                                # h = 1: strips, corner, quotient 3
        self.play(h.animate.set_value(0.5), run_time=2)
        self.wait(0.8)
        self.snap()                                # h = 0.5: 2.5
        self.play(h.animate.set_value(0.1), run_time=2)
        self.wait(0.8)
        self.snap()                                # h = 0.1: corner nearly gone
        self.play(h.animate.set_value(0.02), run_time=1.5)
        end = boxed(VGroup(Text("the corner vanishes;", font_size=32, color=GREEN_C),
                           Text("two strips remain", font_size=32, color=ORANGE_C),
                           MathTex(r"\frac{d}{dx}\,x^2 = 2x", color=RED_C, font_size=56)).arrange(DOWN, buff=0.25), 0.12)
        end.move_to([3.4, -2.3, 0])
        self.play(FadeIn(end))
        self.wait(2.0)
        self.snap()


class ProductArea(Snapper):
    def construct(self):
        self.snaps = []
        S = 1.25
        O = np.array([-6.2, -3.4])
        h = ValueTracker(0.5)
        f0, g0 = 1.0, 4.0                          # f(1) = 1, g(1) = 4

        def parts():
            v = h.get_value()
            df, dg = (1 + v) ** 2 - 1, 3 * v
            return df, dg

        def shapes():
            df, dg = parts()
            return VGroup(rect(*O, f0 * S, g0 * S, BLUE_C, 0.45),
                          rect(O[0] + f0 * S, O[1], df * S, g0 * S, ORANGE_C),
                          rect(O[0], O[1] + g0 * S, f0 * S, dg * S, GREEN_C),
                          rect(O[0] + f0 * S, O[1] + g0 * S, df * S, dg * S, GREY_C, 0.7))

        fl = MathTex("f = x^2 = 1", color=BLACK, font_size=34).next_to([O[0] + 0.6, O[1], 0], DOWN, buff=0.15)
        gl = MathTex("g = 3x + 1 = 4", color=BLACK, font_size=34).rotate(PI / 2).next_to([O[0], O[1] + 2.5, 0], LEFT, buff=0.15)
        fg = MathTex("f g", color=BLACK, font_size=48).move_to([O[0] + f0 * S / 2, O[1] + 2.4, 0])

        def labels():
            df, dg = parts()
            g = VGroup(MathTex(r"g\,df", color=ORANGE_C, font_size=40).next_to([O[0] + (f0 + df) * S, O[1] + 2.4, 0], RIGHT, buff=0.15),
                       MathTex(r"f\,dg", color=GREEN_C, font_size=40).next_to([O[0] + f0 * S / 2, O[1] + (g0 + dg) * S, 0], UP, buff=0.1))
            return g

        def readout():
            v = h.get_value()
            df, dg = parts()
            g = VGroup(MathTex(rf"h = {v:.2f}", color=BLACK, font_size=40),
                       MathTex(rf"\text{{right strip }} g\,df = 4 \times {df:.3f}", color=ORANGE_C, font_size=38),
                       MathTex(rf"\text{{top strip }} f\,dg = 1 \times {dg:.3f}", color=GREEN_C, font_size=38),
                       MathTex(rf"\text{{corner }} df\,dg = {df * dg:.3f}", color=GREY_C, font_size=38),
                       MathTex(rf"\frac{{\text{{change}}}}{{h}} = {(g0 * df + f0 * dg + df * dg) / v:.2f}", color=RED_C, font_size=46))
            return g.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([2.6, 0.9, 0])

        head = boxed(MathTex(r"(f g)' = f' g + f g'", color=BLACK, font_size=48), 0.1).to_edge(UP, buff=0.2).shift(RIGHT * 2.6)
        self.add(always_redraw(shapes), fl, gl, fg, always_redraw(labels), always_redraw(readout), head)
        self.wait(1.0)
        self.snap()                                # h = 0.5
        self.play(h.animate.set_value(0.2), run_time=2)
        self.wait(0.8)
        self.snap()
        self.play(h.animate.set_value(0.05), run_time=1.5)
        self.wait(0.6)
        self.snap()                                # strips thin, change/h near 11
        self.play(h.animate.set_value(0.01), run_time=1.5)
        end = boxed(MathTex(r"f' g + f g' = 2 \times 4 + 1 \times 3 = 11", color=RED_C, font_size=46), 0.12)
        end.move_to([2.6, -2.9, 0])
        self.play(FadeIn(end))
        self.wait(2.0)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, hgt = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * hgt + gap), "white")
    for i, fr in enumerate(frames[:4]):
        sheet.paste(fr.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (hgt + gap)))
    sheet.save(out)


def render(cls, name):
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = cls()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)


if __name__ == "__main__":
    for v in (1.0, 0.5, 0.1):                      # square: change / h = 2 + h, the Note's table
        assert abs(((1 + v) ** 2 - 1) / v - (2 + v)) < 1e-12
    v = 1e-6                                       # rectangle: change / h -> 11
    assert abs(((1 + v) ** 2 * (3 * (1 + v) + 1) - 4) / v - 11) < 1e-4
    render(SquareArea, "square_area")
    render(ProductArea, "product_area")
