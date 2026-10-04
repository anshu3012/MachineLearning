"""Perceptron trained with the perceptron loss: one SGD pass over 100 points (make_classification, class_sep 15,
random_state 41, labels mapped to -1/+1), learning rate 0.1, starting from the deliberately poor line
-x1 + x2 + 0.5 = 0. Shows the line after every update and the average loss falling to 0.
Run: python loss_training.py  -> loss_training.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image
from sklearn.datasets import make_classification

HERE = Path(__file__).parent
BLUE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
X, Y01 = make_classification(n_samples=100, n_features=2, n_informative=1, n_redundant=0, n_classes=2,
                             n_clusters_per_class=1, random_state=41, hypercube=False, class_sep=15)
Y = np.where(Y01 == 1, 1, -1)
XR, YR = (-3.5, 2.5), (-3.2, 2.4)
W0 = np.array([-1.0, 1.0, 0.5])            # (w1, w2, b)


def loss(w):
    return np.maximum(0, -Y * (X @ w[:2] + w[2])).mean()


def run(w=W0, lr=0.1, epochs=5):
    w = w.copy()
    events = []                            # (epoch, row, new w, new loss) for every real update
    for e in range(1, epochs + 1):
        for i in range(len(Y)):
            if Y[i] * (X[i] @ w[:2] + w[2]) < 0:
                w = w + lr * Y[i] * np.r_[X[i], 1]
                events.append((e, i, w.copy(), loss(w)))
    return events


def clip(w):
    """End points of w1 x + w2 y + b = 0 inside the plotting box."""
    pts = []
    for x in XR:
        if w[1] != 0:
            y = -(w[2] + w[0] * x) / w[1]
            if YR[0] <= y <= YR[1]:
                pts.append((x, y))
    for y in YR:
        if w[0] != 0:
            x = -(w[2] + w[1] * y) / w[0]
            if XR[0] <= x <= XR[1]:
                pts.append((x, y))
    return pts[:2]


class LossTraining(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        events = run()
        ax = Axes(x_range=[*XR, 1], y_range=[*YR, 1], x_length=6.6, y_length=6.0, tips=False,
                  axis_config={"color": BLACK, "include_numbers": True, "font_size": 22,
                               "decimal_number_config": {"color": BLACK, "num_decimal_places": 0}}).shift(LEFT * 3.2 + DOWN * 0.3)
        dots = VGroup(*[Dot(ax.c2p(*p), radius=0.06, color=GREEN_C if c == 1 else BLUE_C) for p, c in zip(X, Y)])
        title = Text("Training with the perceptron loss: the line moves, the loss falls", font_size=28,
                     weight=BOLD).to_edge(UP, buff=0.2)
        n = len(events)
        lax = Axes(x_range=[0, n, 2], y_range=[0, 1.8, 0.5], x_length=4.6, y_length=3.0, tips=False,
                   axis_config={"color": BLACK, "include_numbers": True, "font_size": 20,
                                "decimal_number_config": {"color": BLACK, "num_decimal_places": 1}},
                   x_axis_config={"decimal_number_config": {"color": BLACK, "num_decimal_places": 0}}).shift(RIGHT * 4.1 + DOWN * 1.4)
        lax.get_x_axis().numbers.set_color(BLACK)
        xl = Text("update", font_size=20).next_to(lax.x_axis, DOWN, buff=0.35)
        yl = Text("average loss", font_size=20).next_to(lax, UP, buff=0.15)
        self.add(ax, dots, title, lax, xl, yl)

        def line_for(w):
            a, b = clip(w)
            return Line(ax.c2p(*a), ax.c2p(*b), color=RED_C, stroke_width=6)

        def info_for(k, w, L):
            head = "start" if k == 0 else f"epoch 1, update {k} of {n}"
            return VGroup(Text(head, font_size=24),
                          Text("(w1, w2, b) = (" + ", ".join(f"{v:.2f}" for v in w) + ")", font_size=22),
                          Text(f"loss = {L:.3f}", font_size=24, color=RED_C)).arrange(DOWN, aligned_edge=LEFT).move_to([1.8, 2.6, 0], aligned_edge=UL)

        line = line_for(W0)
        info = info_for(0, W0, loss(W0))
        legend = VGroup(Text("green: y = +1", font_size=20, color=GREEN_C), Text("blue: y = -1", font_size=20, color=BLUE_C),
                        Text("ring: misclassified row", font_size=20, color=RED_C)).arrange(RIGHT, buff=0.4).to_edge(DOWN, buff=0.12).shift(LEFT * 3.0)
        prev = Dot(lax.c2p(0, loss(W0)), radius=0.06, color=RED_C)
        self.add(line, info, legend, prev)
        self.wait(0.6)
        self.snap()
        for k, (_, i, w, L) in enumerate(events, start=1):
            ring = Circle(radius=0.18, color=RED_C, stroke_width=5).move_to(ax.c2p(*X[i]))
            dot = Dot(lax.c2p(k, L), radius=0.06, color=RED_C)
            seg = Line(prev.get_center(), dot.get_center(), color=RED_C, stroke_width=3)
            self.play(Create(ring), run_time=0.3)
            self.play(Transform(line, line_for(w)), Transform(info, info_for(k, w, L)), Create(seg), FadeIn(dot), run_time=0.9)
            self.play(FadeOut(ring), run_time=0.2)
            prev = dot
            if k in (4, 8):
                self.snap()
        done = Text("loss 0: no row is misclassified, so later epochs change nothing", font_size=22,
                    color=RED_C).next_to(title, DOWN, buff=0.15)
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
    print("start loss", round(loss(W0), 4))
    for e, i, w, L in run():
        print(e, i, Y[i], w.round(3), round(L, 4))
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "loss_training", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = LossTraining()
        scene.render()
    mp4 = HERE / "loss_training.mp4"
    shutil.copy(next(media.rglob("loss_training.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "loss_training.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "loss_training_frames.png")
    shutil.rmtree(media)
