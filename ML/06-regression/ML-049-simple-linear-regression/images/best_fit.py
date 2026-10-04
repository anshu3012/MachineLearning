"""Searching for the best-fit line: the vertical gaps (errors) from each student to the line, and their squared sum,
for a flat line at the average, a too-steep line, and the best-fit line found by LinearRegression.
Run: python best_fit.py  -> best_fit.mp4, best_fit.gif, best_fit_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image
from common import X_train, y_train, M, B

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
x, y = X_train["cgpa"].to_numpy(), y_train.to_numpy()
sse = lambda m, b: float(((y - (m * x + b)) ** 2).sum())
MEAN = float(y.mean())
STAGES = [(0.0, MEAN, "Average for everyone", RED_C),
          (1.0, -4.0, "A steeper line", RED_C),
          (M, B, "Best-fit line", ORANGE_C)]


class BestFit(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        axes = Axes(x_range=[4, 10, 1], y_range=[1, 5, 1], x_length=7.2, y_length=5.0, tips=False,
                    axis_config={"color": GREY_C, "include_numbers": True,
                                 "decimal_number_config": {"num_decimal_places": 0, "color": GREY_C}}
                    ).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        labels = VGroup(Text("CGPA", font_size=22, color=GREY_C).next_to(axes.x_axis, DOWN, buff=0.45),
                        Text("package (LPA)", font_size=22, color=GREY_C).rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.45))
        dots = VGroup(*[Dot(axes.c2p(a, b), radius=0.045, color=BLUE_C) for a, b in zip(x, y)])
        m_t, b_t = ValueTracker(STAGES[0][0]), ValueTracker(STAGES[0][1])

        def line():
            m, b = m_t.get_value(), b_t.get_value()
            lo, hi = 4.0, 10.0
            if abs(m) > 1e-9:                        # keep the line inside the box y = 1..5
                ends = sorted([(1 - b) / m, (5 - b) / m])
                lo, hi = max(lo, ends[0]), min(hi, ends[1])
            return Line(axes.c2p(lo, m * lo + b), axes.c2p(hi, m * hi + b), color=ORANGE_C, stroke_width=5)

        def gaps():
            m, b = m_t.get_value(), b_t.get_value()
            return VGroup(*[Line(axes.c2p(a, c), axes.c2p(a, m * a + b), color=RED_C, stroke_width=1.5,
                                 stroke_opacity=0.6) for a, c in zip(x, y)])

        title = Text("Which line makes the smallest total error?", font_size=30, weight=BOLD).to_edge(UP, buff=0.3)
        px = 3.9
        eq = always_redraw(lambda: Text(f"package = {m_t.get_value():.2f} × CGPA "
                                        f"{'+' if b_t.get_value() >= 0 else '−'} {abs(b_t.get_value()):.2f}",
                                        font_size=24).move_to([px, 1.6, 0]))
        err = always_redraw(lambda: Text(f"sum of squared errors: {sse(m_t.get_value(), b_t.get_value()):.1f}",
                                         font_size=26, color=RED_C, weight=BOLD).move_to([px, 0.9, 0]))
        self.play(Create(axes), FadeIn(labels, title), FadeIn(dots, lag_ratio=0.01))
        self.add(always_redraw(gaps), always_redraw(line), eq, err)
        name = None
        for i, (m, b, text, colour) in enumerate(STAGES):
            if i:
                self.play(FadeOut(name), m_t.animate.set_value(m), b_t.animate.set_value(b), run_time=2.5)
            name = Text(text, font_size=26, color=colour, weight=BOLD).move_to([px, 0.2, 0])
            self.play(FadeIn(name))
            self.wait(0.8)
            self.snap()
        rule = VGroup(Text("error = actual − predicted", font_size=22),
                      Text("square each error, add them up", font_size=22),
                      Text("best-fit line: the smallest total", font_size=22, color=ORANGE_C, weight=BOLD)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([px, -1.3, 0])
        self.play(FadeIn(rule, lag_ratio=0.3))
        self.wait(1.5)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    for m, b, text, _ in STAGES:
        print(f"{text:40s} m={m:.3f} b={b:.3f} SSE={sse(m, b):.2f}")
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "best_fit", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = BestFit()
        scene.render()
    mp4 = HERE / "best_fit.mp4"
    shutil.copy(next(media.rglob("best_fit.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "best_fit.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "best_fit_frames.png")
    shutil.rmtree(media)
