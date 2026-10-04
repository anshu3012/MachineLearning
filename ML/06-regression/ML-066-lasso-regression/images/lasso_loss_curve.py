"""The Lasso loss as a function of the slope m (intercept held at -2.29) while lambda grows from 0 to 8000.
The curve rises and narrows, and its lowest point slides to m = 0 and then stays there exactly.
Run: python lasso_loss_curve.py  -> lasso_loss_curve.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image
from sklearn.datasets import make_regression

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#E45756", "#9A9A9A"
Text.set_default(color=BLACK, font="Latin Modern Roman")
X, Y = make_regression(n_samples=100, n_features=1, n_informative=1, noise=20, random_state=13)
x = X.ravel()
SXY, SXX = float((x * (Y + 2.29)).sum()), float((x * x).sum())


def loss(m, lam):          # in thousands
    return (((Y - m * x + 2.29) ** 2).sum() + lam * abs(m)) / 1000


def best_m(lam):
    return max(0.0, (SXY - lam / 2) / SXX)


class LassoLossCurve(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        ax = Axes(x_range=[-20, 40, 10], y_range=[0, 400, 100], x_length=10.5, y_length=5.0, tips=False,
                  axis_config={"color": BLACK, "include_numbers": True, "font_size": 24,
                               "decimal_number_config": {"color": BLACK, "num_decimal_places": 0}}).shift(DOWN * 0.15 + RIGHT * 0.4)
        xl = Text("slope m", font_size=26).next_to(ax.x_axis, DOWN, buff=0.4)
        yl = Text("loss (thousands)", font_size=26).rotate(PI / 2).next_to(ax, LEFT, buff=0.3)
        title = Text("Lasso loss for different λ (intercept held at −2.29)", font_size=30, weight=BOLD).to_edge(UP, buff=0.25)
        self.add(ax, xl, yl, title)
        lam = ValueTracker(0)
        curve = always_redraw(lambda: ax.plot(lambda m: loss(m, lam.get_value()), x_range=[-20, 40, 0.1],
                                              color=BLUE_C, stroke_width=6))
        dot = always_redraw(lambda: Dot(ax.c2p(best_m(lam.get_value()), loss(best_m(lam.get_value()), lam.get_value())),
                                        color=RED_C, radius=0.11))
        readout = always_redraw(lambda: VGroup(
            Text(f"λ = {lam.get_value():.0f}", font_size=30, color=BLUE_C, weight=BOLD),
            Text(f"lowest point at m = {best_m(lam.get_value()):.1f}", font_size=28, color=RED_C)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(ax.c2p(2, 390), DR, buff=0))
        self.add(curve, dot, readout)
        self.wait(0.8)
        self.snap()
        ghosts = VGroup()
        for target in (2000, 5000, 8000):
            ghosts.add(ax.plot(lambda m: loss(m, lam.get_value()), x_range=[-20, 40, 0.1], color=GREY_C,
                               stroke_width=2, stroke_opacity=0.6))
            self.add(ghosts)
            self.play(lam.animate.set_value(target), run_time=2)
            self.wait(0.6)
            self.snap()
        self.wait(1)


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    for l in (0, 2000, 4852, 5000, 8000):
        print(l, round(best_m(l), 2), round(loss(best_m(l), l), 1))
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "lasso_loss_curve", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = LassoLossCurve()
        scene.render()
    mp4 = HERE / "lasso_loss_curve.mp4"
    shutil.copy(next(media.rglob("lasso_loss_curve.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "lasso_loss_curve.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "lasso_loss_curve_frames.png")
    shutil.rmtree(media)
