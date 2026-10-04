"""A threshold sweeping from 1 down to 0: patients above it are predicted 'diabetes'; the ROC point moves along the curve.
Logistic regression on the Pima diabetes test set (154 patients). Run: python threshold_anim.py -> .mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, RED_C, ORANGE_C, GREY_C = "#4C78A8", "#E45756", "#F58518", "#9A9A9A"
Text.set_default(color=BLACK, font="Latin Modern Roman")
data = np.loadtxt(HERE / "lr_probs.csv", delimiter=",", skiprows=1)
Y, P = data[:, 0].astype(int), data[:, 1]
NPOS, NNEG = (Y == 1).sum(), (Y == 0).sum()


def rates(t):
    pred = P >= t
    return (pred & (Y == 0)).sum() / NNEG, (pred & (Y == 1)).sum() / NPOS


class Threshold(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        rng = np.random.default_rng(0)
        line = NumberLine(x_range=[0, 1, 0.1], length=6, color=BLACK, include_numbers=True, font_size=20,
                          decimal_number_config={"color": BLACK, "num_decimal_places": 1}).shift(LEFT * 3.4 + DOWN * 1.2)
        lab = Text("predicted probability of diabetes", font_size=20).next_to(line, DOWN, buff=0.45)
        dots = VGroup()
        for yi, pi in zip(Y, P):
            yoff = (0.4 + rng.random() * 1.0) if yi == 0 else (1.7 + rng.random() * 1.0)
            dots.add(Dot(line.n2p(pi) + UP * yoff, radius=0.045, color=BLUE_C if yi == 0 else RED_C))
        key = VGroup(Text("red: has diabetes", font_size=20, color=RED_C), Text("blue: no diabetes", font_size=20, color=BLUE_C)
                     ).arrange(DOWN, aligned_edge=LEFT).next_to(line, UP, buff=3.0).align_to(line, LEFT)
        ax = Axes(x_range=[0, 1, 0.2], y_range=[0, 1, 0.2], x_length=4.6, y_length=4.6, tips=False,
                  axis_config={"color": BLACK, "include_numbers": True, "font_size": 18,
                               "decimal_number_config": {"color": BLACK, "num_decimal_places": 1}}).shift(RIGHT * 3.8 + DOWN * 0.3)
        xl = Text("false positive rate", font_size=20).next_to(ax.x_axis, DOWN, buff=0.4)
        yl = Text("true positive rate", font_size=20).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.45)
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(1, 1), color=GREY_C)
        title = Text("Lower the threshold: more patients flagged, the ROC point climbs", font_size=26, weight=BOLD).to_edge(UP, buff=0.25)
        self.add(line, lab, dots, key, ax, xl, yl, diag, title)
        t = ValueTracker(1.0)
        bar = always_redraw(lambda: DashedLine(line.n2p(t.get_value()) + DOWN * 0.1, line.n2p(t.get_value()) + UP * 2.9,
                                               color=ORANGE_C, stroke_width=5))
        shade = always_redraw(lambda: Rectangle(width=max(line.n2p(1)[0] - line.n2p(t.get_value())[0], 0.001), height=2.6,
                                                fill_color=ORANGE_C, fill_opacity=0.12, stroke_width=0)
                              .move_to(line.n2p((t.get_value() + 1) / 2) + UP * 1.55))
        flagged = always_redraw(lambda: Text("flagged as diabetes →", font_size=18, color=ORANGE_C)
                                .next_to(line.n2p(t.get_value()) + UP * 2.9, RIGHT, buff=0.1))
        path = VMobject(color=BLUE_C, stroke_width=5)
        path.set_points_as_corners([ax.c2p(*rates(1.0)), ax.c2p(*rates(1.0))])

        def grow(m):
            f, r = rates(t.get_value())
            m.add_points_as_corners([ax.c2p(f, r)])
        path.add_updater(grow)
        pt = always_redraw(lambda: Dot(ax.c2p(*rates(t.get_value())), color=ORANGE_C, radius=0.09))
        readout = always_redraw(lambda: VGroup(
            Text(f"threshold t = {t.get_value():.2f}", font_size=22, color=ORANGE_C),
            Text(f"TPR = {rates(t.get_value())[1]:.2f}   FPR = {rates(t.get_value())[0]:.2f}", font_size=20)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(ax, UP, buff=0.2))
        self.add(shade, bar, flagged, path, pt, readout)
        self.wait(0.5)
        self.snap()
        for target in (0.7, 0.3, 0.0):
            self.play(t.animate.set_value(target), run_time=3, rate_func=linear)
            self.wait(0.6)
            self.snap()
        path.clear_updaters()
        self.wait(1)


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    for tt in (1.0, 0.7, 0.3, 0.0):
        print(tt, rates(tt))
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "threshold_anim", "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = Threshold()
        scene.render()
    mp4 = HERE / "threshold_anim.mp4"
    shutil.copy(next(media.rglob("threshold_anim.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "threshold_anim.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "threshold_anim_frames.png")
    shutil.rmtree(media)
