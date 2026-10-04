"""Variance around a point v: slide v along five Titanic ages and trace the average squared distance.
The curve is a U whose bottom sits at the sample mean, so the population mean always gives a larger value.
A second sample shows the same; the average absolute distance gives a V with a sharp corner instead.
Run: python variance_around_v.py -> variance_around_v.mp4, .gif, _frames.png (Manim; render on topgro)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MathTex.set_default(color=BLACK)
AGES = pd.read_csv(HERE.parent / "data" / "titanic_train.csv")["Age"].dropna().to_numpy()
MU = AGES.mean()                                                   # 29.70: all 714 known ages
SAMPLES = [np.random.default_rng(s).choice(AGES, 5, replace=False) for s in (0, 1)]
V0, V1 = 12, 56
sq = lambda x, v: ((x - v) ** 2).mean()                            # variance around v, dividing by n
ab = lambda x, v: np.abs(x - v).mean()
for x in SAMPLES:                                                  # the bottom of the U is the sample mean
    grid = np.linspace(V0, V1, 4401)
    assert abs(grid[np.argmin([sq(x, v) for v in grid])] - x.mean()) < 0.02
    assert sq(x, MU) > sq(x, x.mean())
print({f"sample {i}": (x.tolist(), round(x.mean(), 1), round(sq(x, x.mean()), 1), round(sq(x, MU), 1))
       for i, x in enumerate(SAMPLES)}, "mu", round(MU, 2))


class VarianceAroundV(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, title, detail):
        return VGroup(Text(title, font_size=34, weight=BOLD), Text(detail, font_size=26, color=GREY_C)
                      ).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.25)

    @staticmethod
    def grey_numbers(ax):
        for n in list(ax.x_axis.numbers) + list(ax.y_axis.numbers):
            n.set_color(GREY_C)

    def dots(self, line, x):
        rows = np.linspace(1.75, 0.55, 5)
        return VGroup(*[Dot(line.n2p(a) * RIGHT + r * UP, radius=0.11, color=BLUE_C) for a, r in zip(x, rows)])

    def construct(self):
        self.snaps = []
        line = NumberLine(x_range=[V0, V1, 4], length=10.6, color=GREY_C, include_numbers=True, font_size=26,
                          include_tip=False).move_to(UP * 0.3 + LEFT * 0.3)
        for n in line.numbers:
            n.set_color(GREY_C)
        lab = Text("age", font_size=26, color=GREY_C).next_to(line, RIGHT, buff=0.2)
        ax = Axes(x_range=[V0, V1, 4], y_range=[0, 800, 200], x_length=10.6, y_length=2.6,
                  axis_config={"color": GREY_C, "include_tip": False, "font_size": 24},
                  x_axis_config={"numbers_to_include": range(V0, V1 + 1, 4)},
                  y_axis_config={"numbers_to_include": [0, 200, 400, 600, 800]}).move_to(DOWN * 2.1 + LEFT * 0.3)
        self.grey_numbers(ax)
        ylab = Text("average of (x − v)²", font_size=22, color=GREY_C).rotate(PI / 2).next_to(ax.y_axis, LEFT, 0.5)
        xlab = MathTex("v", font_size=34, color=GREY_C).next_to(ax.x_axis, RIGHT, buff=0.15)
        x = SAMPLES[0]
        pts = self.dots(line, x)
        mu_line = DashedLine(line.n2p(MU) + UP * 2.0, line.n2p(MU), color=RED_C, stroke_width=3)
        mu_lab = MathTex(r"\mu = 29.7", font_size=30, color=RED_C).next_to(mu_line, UP, buff=0.05).shift(LEFT * 0.6)
        cap = self.caption("Five Titanic ages: one sample", "sample mean 34.2; the mean of all 714 ages is 29.7")
        self.play(FadeIn(cap), Create(line), FadeIn(lab), FadeIn(pts, lag_ratio=0.2), run_time=1.5)
        self.play(Create(mu_line), FadeIn(mu_lab))
        self.wait(1)
        self.snap()

        v = ValueTracker(V0)
        vline = always_redraw(lambda: Line(line.n2p(v.get_value()) + UP * 2.0, line.n2p(v.get_value()),
                                           color=ORANGE_C, stroke_width=5))
        gaps = always_redraw(lambda: VGroup(*[Line(d.get_center(), [line.n2p(v.get_value())[0], d.get_y(), 0],
                                                   color=ORANGE_C, stroke_width=3, stroke_opacity=0.7) for d in pts]))
        ball = always_redraw(lambda: Dot(ax.c2p(v.get_value(), sq(x, v.get_value())), radius=0.09, color=ORANGE_C))
        trace = TracedPath(ball.get_center, stroke_color=ORANGE_C, stroke_width=5)
        self.play(Transform(cap, self.caption("Variance around a point v",
                                              "square each distance to v, then average (divide by n)")),
                  Create(ax), FadeIn(ylab, xlab), FadeIn(vline, gaps, ball))
        self.add(trace)
        self.play(v.animate.set_value(V1), run_time=6, rate_func=linear)
        self.wait(0.3)
        u_curve = ax.plot(lambda t: sq(x, t), x_range=[V0, V1, 0.1], color=ORANGE_C, stroke_width=5)
        self.add(u_curve)
        self.remove(trace)
        self.play(v.animate.set_value(x.mean()), run_time=2)
        bottom = Dot(ax.c2p(x.mean(), sq(x, x.mean())), radius=0.12, color=BLUE_C)
        at_mu = Dot(ax.c2p(MU, sq(x, MU)), radius=0.12, color=RED_C)
        b_lab = MathTex(r"v=\bar{x}:\ 137", font_size=32, color=BLUE_C).next_to(bottom, UP, buff=0.55).shift(RIGHT * 1.3)
        m_lab = MathTex(r"v=\mu:\ 158", font_size=32, color=RED_C).next_to(at_mu, UP, buff=0.55).shift(LEFT * 1.3)
        self.play(FadeIn(bottom, at_mu, b_lab, m_lab),
                  Transform(cap, self.caption("The bottom of the U is the sample mean",
                                              "around the true mean the average is larger: 158 > 137")))
        self.wait(2)
        self.snap()

        x = SAMPLES[1]
        new_pts = self.dots(line, x)
        u2 = ax.plot(lambda t: sq(x, t), x_range=[V0, V1, 0.1], color=ORANGE_C, stroke_width=5)
        bottom2 = Dot(ax.c2p(x.mean(), sq(x, x.mean())), radius=0.12, color=BLUE_C)
        at_mu2 = Dot(ax.c2p(MU, sq(x, MU)), radius=0.12, color=RED_C)
        b2 = MathTex(r"\bar{x} = 32.8:\ 20", font_size=32, color=BLUE_C).next_to(bottom2, UP, buff=0.55).shift(RIGHT * 1.6)
        m2 = MathTex(r"\mu:\ 30", font_size=32, color=RED_C).next_to(at_mu2, UP, buff=0.55).shift(LEFT * 1.3)
        self.play(Transform(pts, new_pts), Transform(u_curve, u2), FadeOut(bottom, at_mu, b_lab, m_lab),
                  v.animate.set_value(x.mean()),
                  Transform(cap, self.caption("A second sample of five ages",
                                              "a new U; its bottom is again at its own sample mean")), run_time=2)
        self.play(FadeIn(bottom2, at_mu2, b2, m2))
        self.wait(2)
        self.snap()

        ax2 = Axes(x_range=[V0, V1, 4], y_range=[0, 25, 5], x_length=10.6, y_length=2.6,
                   axis_config={"color": GREY_C, "include_tip": False, "font_size": 24},
                   x_axis_config={"numbers_to_include": range(V0, V1 + 1, 4)},
                   y_axis_config={"numbers_to_include": [0, 5, 10, 15, 20, 25]}).move_to(ax)
        self.grey_numbers(ax2)
        ylab2 = Text("average of |x − v|", font_size=22, color=GREY_C).rotate(PI / 2).next_to(ax2.y_axis, LEFT, 0.5)
        vee = ax2.plot(lambda t: ab(x, t), x_range=[V0, V1, 0.05], color=GREEN_C, stroke_width=5)
        corner = Dot(ax2.c2p(np.median(x), ab(x, np.median(x))), radius=0.12, color=GREEN_C)
        c_lab = Text("sharp corner:\nno slope here", font_size=26, color=GREEN_C).move_to(ax2.c2p(48, 4))
        c_arrow = Arrow(c_lab.get_left(), corner.get_center(), buff=0.15, color=GREEN_C, stroke_width=4)
        self.remove(ball, vline, gaps)
        self.play(FadeOut(u_curve, bottom2, at_mu2, b2, m2, ylab), ReplacementTransform(ax, ax2), FadeIn(ylab2),
                  Transform(cap, self.caption("Absolute distances instead of squares",
                                              "the curve becomes a V with corners at the data")), run_time=1.5)
        self.play(Create(vee), run_time=2.5)
        self.play(FadeIn(corner, c_lab, c_arrow))
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
                     "output_file": "variance_around_v", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = VarianceAroundV()
        scene.render()
    mp4 = HERE / "variance_around_v.mp4"
    shutil.copy(next(media.rglob("variance_around_v.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "variance_around_v.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "variance_around_v_frames.png")
    shutil.rmtree(media)
