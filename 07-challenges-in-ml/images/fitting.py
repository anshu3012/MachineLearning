"""Underfitting, a good fit and overfitting on the same 12 points, with real polynomial fits.
Run: python fitting.py  -> fitting.mp4, fitting.gif, fitting_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")

rng = np.random.default_rng(31)
truth = lambda x: np.sin(2 * np.pi * x)
x_train = np.sort(rng.uniform(0, 1, 12))
y_train = truth(x_train) + rng.normal(0, 0.25, x_train.size)
LO, HI = x_train.min(), x_train.max()
x_new = rng.uniform(LO, HI, 300)                     # new data the model has never seen, same range
y_new = truth(x_new) + rng.normal(0, 0.25, x_new.size)

STAGES = [(1, "Underfitting", "too simple: misses the pattern", RED_C),
          (3, "Good fit", "follows the pattern, ignores the noise", GREEN_C),
          (11, "Overfitting", "memorises every point, including the noise", RED_C)]


def fit(degree):
    coefs = np.polyfit(x_train, y_train, degree)
    err = lambda x, y: float(np.sqrt(np.mean((np.polyval(coefs, x) - y) ** 2)))
    return coefs, err(x_train, y_train), err(x_new, y_new)


class Fitting(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        axes = Axes(x_range=[0, 1, 0.25], y_range=[-2, 2, 1], x_length=7.4, y_length=5.0, tips=False,
                    axis_config={"color": GREY_C}).shift(LEFT * 2.6 + DOWN * 0.3)
        dots = VGroup(*[Dot(axes.c2p(x, y), radius=0.08, color=BLUE_C) for x, y in zip(x_train, y_train)])
        title = Text("Training data: 12 points", font_size=28, weight=BOLD).to_edge(UP, buff=0.35).shift(LEFT * 2.6)
        self.play(Create(axes), FadeIn(dots, lag_ratio=0.05), FadeIn(title))
        self.wait(0.4)
        self.snap()

        curve = panel = None
        for degree, name, note, colour in STAGES:
            coefs, train_err, new_err = fit(degree)
            new_curve = axes.plot(lambda x: float(np.clip(np.polyval(coefs, x), -2, 2)),
                                  x_range=[LO, HI, 0.002], color=colour, stroke_width=5)
            new_panel = VGroup(
                Text(name, font_size=34, weight=BOLD, color=colour),
                Text(note, font_size=20),
                Text(f"error on training data: {train_err:.2f}", font_size=22),
                Text(f"error on new data: {new_err:.2f}", font_size=22, weight=BOLD),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35).shift(UP * 0.4)
            if curve is None:
                self.play(Create(new_curve), FadeIn(new_panel), run_time=1.5)
            else:
                self.play(Transform(curve, new_curve), FadeTransform(panel, new_panel), run_time=1.8)
                new_curve = curve
            curve, panel = new_curve, new_panel
            self.wait(1.2)
            self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    for d, name, *_ in STAGES:
        _, tr, nw = fit(d)
        print(f"{name:12s} degree {d:2d}: train {tr:.2f}  new {nw:.2f}")
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "fitting", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = Fitting()
        scene.render()
    mp4 = HERE / "fitting.mp4"
    shutil.copy(next(media.rglob("fitting.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "fitting.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "fitting_frames.png")
    shutil.rmtree(media)
