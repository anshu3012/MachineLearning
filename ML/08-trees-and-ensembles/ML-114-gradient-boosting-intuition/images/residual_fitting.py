"""Gradient boosting, stage by stage, on the noisy quadratic data: start at the mean, show the residuals, fit a tree
to them, add half of it (learning rate 0.5), repeat for three trees.
Run: python residual_fitting.py  -> residual_fitting.mp4, residual_fitting.gif, residual_fitting_frames.png"""
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import X, boost, y  # noqa: E402  (the 100 training points and the boosting loop of the app)

BLUE_C, RED_C, GREEN_C, GREY_C = "#4C78A8", "#E45756", "#54A24B", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
LR, TREES = 0.5, 3
f0, trees = boost(TREES, LR, 8)
GRID = np.linspace(-0.5, 0.5, 800)


def model_at(m, x):
    """Prediction after m trees."""
    return f0 + LR * sum((t.predict(x.reshape(-1, 1)) for t in trees[:m]), np.zeros(len(x)))


class ResidualFitting(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, text):
        return Text(text, font_size=30).to_edge(UP, buff=0.3)

    def curve(self, ax, values, colour, width=5):
        pts = [ax.c2p(a, b) for a, b in zip(GRID, values)]
        return VMobject(stroke_color=colour, stroke_width=width).set_points_as_corners(pts)

    def construct(self):
        self.snaps = []
        top = Axes(x_range=[-0.5, 0.5, 0.25], y_range=[-0.2, 0.9, 0.2], x_length=11, y_length=3.3,
                   axis_config={"color": GREY_C, "include_ticks": False, "tip_width": 0.15, "tip_height": 0.15}).shift(UP * 1.05)
        bottom = Axes(x_range=[-0.5, 0.5, 0.25], y_range=[-0.45, 0.45, 0.2], x_length=11, y_length=2.2,
                      axis_config={"color": GREY_C, "include_ticks": False, "tip_width": 0.15, "tip_height": 0.15}).shift(DOWN * 2.55)
        top_lab = Text("data and model", font_size=22, color=GREY_C).next_to(top, LEFT, buff=0.1).rotate(PI / 2)
        bot_lab = Text("residuals", font_size=22, color=GREY_C).next_to(bottom, LEFT, buff=0.1).rotate(PI / 2)
        dots = VGroup(*[Dot(top.c2p(a, b), radius=0.045, color=BLUE_C) for a, b in zip(X[:, 0], y)])
        cap = self.caption("stage 1: predict the mean of y for everyone")
        model = self.curve(top, model_at(0, GRID), RED_C)
        self.play(Create(top), Create(bottom), FadeIn(top_lab), FadeIn(bot_lab), FadeIn(dots), FadeIn(cap))
        self.play(Create(model), run_time=1)
        self.wait(0.6)
        self.snap()

        for m in range(1, TREES + 1):
            pred = model_at(m - 1, X[:, 0])
            res = y - pred
            sticks = VGroup(*[Line(top.c2p(a, p), top.c2p(a, b), stroke_width=2, color=GREY_C)
                              for a, b, p in zip(X[:, 0], y, pred)])
            rdots = VGroup(*[Dot(bottom.c2p(a, r), radius=0.04, color=GREY_C) for a, r in zip(X[:, 0], res)])
            self.play(Transform(cap, self.caption(f"residuals of the current model: actual minus predicted")),
                      Create(sticks), run_time=1)
            self.play(TransformFromCopy(sticks, rdots), run_time=1)
            fit = self.curve(bottom, trees[m - 1].predict(GRID.reshape(-1, 1)), GREEN_C)
            self.play(Transform(cap, self.caption(f"tree {m} (8 leaves) is trained on the residuals")),
                      Create(fit), run_time=1.2)
            self.wait(0.4)
            if m == 1:
                self.snap()
            new_model = self.curve(top, model_at(m, GRID), RED_C)
            self.play(Transform(cap, self.caption(f"add 0.5 × tree {m}: the model after {m} tree{'s' * (m > 1)}")),
                      Transform(model, new_model), FadeOut(sticks), run_time=1.4)
            self.wait(0.5)
            if m in (1, TREES):
                self.snap()
            self.play(FadeOut(rdots), FadeOut(fit), run_time=0.5)
        self.wait(1)


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "residual_fitting", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = ResidualFitting()
        scene.render()
    mp4 = HERE / "residual_fitting.mp4"
    shutil.copy(next(media.rglob("residual_fitting.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "residual_fitting.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "residual_fitting_frames.png")
    shutil.rmtree(media)
