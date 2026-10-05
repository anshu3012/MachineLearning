"""Building the normal PDF term by term: e^x, e^-x, e^-|x|, e^(-x^2), shift by mu, widen by sigma, divide by sigma*sqrt(2 pi).
Run: python pdf_build.py -> pdf_build.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
ORANGE_C, BLUE_C, GREY_C = "#F58518", "#4C78A8", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MathTex.set_default(color=BLACK)
SIG = 1.5
MU = 2


class PdfBuild(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def header(self, formula, detail):
        return VGroup(MathTex(formula, font_size=46), Text(detail, font_size=26, color=GREY_C)
                      ).arrange(DOWN, buff=0.25).to_edge(UP, buff=0.35)

    def construct(self):
        self.snaps = []
        ax = Axes(x_range=[-5, 5, 1], y_range=[0, 1.2, 0.2], x_length=11, y_length=4.4,
                  axis_config={"color": GREY_C, "include_tip": False, "font_size": 26},
                  x_axis_config={"numbers_to_include": range(-5, 6)},
                  y_axis_config={"numbers_to_include": [0.2, 0.4, 0.6, 0.8, 1.0],
                                 "decimal_number_config": {"num_decimal_places": 1}}).shift(DOWN * 1.1)
        for n in list(ax.x_axis.numbers) + list(ax.y_axis.numbers):
            n.set_color(GREY_C)
        plot = lambda f, lo=-5, hi=5: ax.plot(f, x_range=[lo, hi, 0.02], color=ORANGE_C, stroke_width=6)

        head = self.header(r"y = e^{x}", "exponential growth")
        curve = plot(np.exp, -5, np.log(1.2))
        self.play(Create(ax), FadeIn(head), Create(curve), run_time=1.5)
        self.wait(0.5)
        self.play(Transform(head, self.header(r"y = e^{-x}", "a minus sign: exponential decay")),
                  Transform(curve, plot(lambda x: np.exp(-x), -np.log(1.2), 5)), run_time=1.3)
        self.wait(0.5)
        self.play(Transform(head, self.header(r"y = e^{-|x|}", "absolute value: it decays both ways, but has a sharp point")),
                  Transform(curve, plot(lambda x: np.exp(-abs(x)))), run_time=1.3)
        self.wait(0.6)
        self.snap()
        self.play(Transform(head, self.header(r"y = e^{-x^2}", "square x instead: a smooth bell")),
                  Transform(curve, plot(lambda x: np.exp(-x ** 2))), run_time=1.3)
        self.wait(0.6)
        self.snap()

        self.play(Transform(head, self.header(r"y = e^{-(x - \mu)^2}", "subtract the mean: the centre moves to mu = 2")),
                  Transform(curve, plot(lambda x: np.exp(-(x - 2) ** 2))), run_time=1.3)
        self.wait(0.5)
        self.snap()
        wide = lambda x: np.exp(-(x - MU) ** 2 / (2 * SIG ** 2))
        area_txt = MathTex(rf"\text{{area}} = \sigma\sqrt{{2\pi}} = {SIG * np.sqrt(2 * np.pi):.2f}", font_size=36,
                           color=BLUE_C).move_to(ax.c2p(-2.6, 1.0))
        fill = ax.get_area(plot(wide), x_range=[-5, 5], color=BLUE_C, opacity=0.25)
        self.play(Transform(head, self.header(r"y = e^{-\frac{(x - \mu)^2}{2\sigma^2}}",
                                              "divide by 2 sigma squared: sigma sets the width (here 1.5), mu stays 2")),
                  Transform(curve, plot(wide)), run_time=1.3)
        self.play(FadeIn(fill), FadeIn(area_txt), run_time=0.8)
        self.add(curve)                      # keep the curve drawn above the shaded area
        self.wait(0.6)
        self.snap()

        pdf = lambda x: wide(x) / (SIG * np.sqrt(2 * np.pi))
        self.play(Transform(head, self.header(r"f(x) = \frac{1}{\sigma\sqrt{2\pi}}\, e^{-\frac{(x - \mu)^2}{2\sigma^2}}",
                                              "divide by sigma times root 2 pi: area 1, the normal PDF")),
                  Transform(curve, plot(pdf)), Transform(fill, ax.get_area(plot(pdf), x_range=[-5, 5], color=BLUE_C,
                                                                            opacity=0.25)),
                  Transform(area_txt, MathTex(r"\text{area} = 1", font_size=36, color=BLUE_C).move_to(area_txt)),
                  run_time=1.6)
        self.add(curve)
        self.wait(1.5)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    rows = (len(frames) + 1) // 2
    sheet = Image.new("RGB", (2 * w + gap, rows * h + (rows - 1) * gap), "white")
    for i, f in enumerate(frames):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "pdf_build", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = PdfBuild()
        scene.render()
    mp4 = HERE / "pdf_build.mp4"
    shutil.copy(next(media.rglob("pdf_build.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "pdf_build.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "pdf_build_frames.png")
    shutil.rmtree(media)
