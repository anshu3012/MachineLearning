"""Perceptron trick on 100 points (make_classification, class_sep 10, random_state 41), learning rate 0.1, seed 0.
Only misclassified picks move the line; the animation shows every update and skips the loops with no change.
Run: python perceptron_anim.py  -> perceptron_anim.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image
from sklearn.datasets import make_classification

HERE = Path(__file__).parent
BLUE_C, GREEN_C, RED_C = "#4C78A8", "#54A24B", "#E45756"
Text.set_default(color=BLACK, font="Latin Modern Roman")
X, Y = make_classification(n_samples=100, n_features=2, n_informative=1, n_redundant=0, n_classes=2,
                           n_clusters_per_class=1, random_state=41, hypercube=False, class_sep=10)
XR, YR = (-2.6, 2.6), (-3.2, 2.4)


def run(lr=0.1, loops=1000, seed=0):
    rng = np.random.default_rng(seed)
    Xb = np.insert(X, 0, 1, axis=1)
    w = np.ones(3)
    events = []                      # (loop, picked row, new w) for every real update
    for i in range(loops):
        j = rng.integers(0, len(Y))
        y_hat = 1 if Xb[j] @ w > 0 else 0
        if Y[j] != y_hat:
            w = w + lr * (Y[j] - y_hat) * Xb[j]
            events.append((i + 1, j, w.copy()))
    return events


def clip(w):
    """End points of w0 + w1 x + w2 y = 0 inside the plotting box."""
    pts = []
    for x in XR:
        y = -(w[0] + w[1] * x) / w[2]
        if YR[0] <= y <= YR[1]:
            pts.append((x, y))
    for y in YR:
        x = -(w[0] + w[2] * y) / w[1]
        if XR[0] <= x <= XR[1]:
            pts.append((x, y))
    return pts[:2]


class Perceptron(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        ax = Axes(x_range=[*XR, 1], y_range=[*YR, 1], x_length=8.5, y_length=6.2, tips=False,
                  axis_config={"color": BLACK, "include_numbers": True, "font_size": 22,
                               "decimal_number_config": {"color": BLACK, "num_decimal_places": 0}}).shift(LEFT * 2.4 + DOWN * 0.2)
        dots = VGroup(*[Dot(ax.c2p(*p), radius=0.07, color=GREEN_C if c == 1 else BLUE_C) for p, c in zip(X, Y)])
        title = Text("Perceptron trick: only misclassified points move the line", font_size=28, weight=BOLD).to_edge(UP, buff=0.2)
        self.add(ax, dots, title)
        w = np.ones(3)

        def line_for(w):
            a, b = clip(w)
            return Line(ax.c2p(*a), ax.c2p(*b), color=RED_C, stroke_width=6)

        line = line_for(w)
        info = VGroup(Text("loop 0", font_size=24), Text("w = (1, 1, 1)", font_size=22)).arrange(DOWN, aligned_edge=LEFT)
        info.move_to([2.6, 2.3, 0], aligned_edge=UL)
        legend = VGroup(Text("green: class 1", font_size=22, color=GREEN_C), Text("blue: class 0", font_size=22, color=BLUE_C),
                        Text("ring: the picked point", font_size=22, color=RED_C)).arrange(DOWN, aligned_edge=LEFT)
        legend.next_to(info, DOWN, buff=0.6, aligned_edge=LEFT)
        self.add(line, info, legend)
        self.wait(0.6)
        self.snap()
        events = run()
        for k, (loop, j, w_new) in enumerate(events):
            ring = Circle(radius=0.2, color=RED_C, stroke_width=5).move_to(ax.c2p(*X[j]))
            new_info = VGroup(Text(f"loop {loop}, update {k + 1} of {len(events)}", font_size=24),
                              Text("w = (" + ", ".join(f"{v:.2f}" for v in w_new) + ")", font_size=22)).arrange(DOWN, aligned_edge=LEFT)
            new_info.move_to(info, aligned_edge=UL)
            self.play(Create(ring), run_time=0.4)
            self.play(Transform(line, line_for(w_new)), Transform(info, new_info), run_time=1.2)
            self.play(FadeOut(ring), run_time=0.3)
            if k + 1 in (2, 4):
                self.snap()
        done = VGroup(Text(f"loops {events[-1][0] + 1} to 1000:", font_size=22, color=RED_C),
                      Text("no point misclassified,", font_size=22, color=RED_C),
                      Text("so the line never moves again", font_size=22, color=RED_C)).arrange(DOWN, aligned_edge=LEFT)
        done.next_to(legend, DOWN, buff=0.6, aligned_edge=LEFT)
        self.play(FadeIn(done))
        self.wait(1.2)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    for loop, j, w in run():
        print(loop, j, Y[j], w.round(3))
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "perceptron_anim", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = Perceptron()
        scene.render()
    mp4 = HERE / "perceptron_anim.mp4"
    shutil.copy(next(media.rglob("perceptron_anim.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "perceptron_anim.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "perceptron_anim_frames.png")
    shutil.rmtree(media)
