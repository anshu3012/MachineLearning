"""Momentum's step drawn head to tail on the valley L = (w1^2 + 100 w2^2)/2 from (-10, 0.4), eta = 0.01, beta = 0.9
(the run of Figure 1). Each step = old velocity times beta (orange) + minus eta times the gradient now (blue).
Across the valley the two arrows often point opposite ways and cancel; along it they agree and the steps grow.
Idea credited to Goh (2017), "Why Momentum Really Works", Distill; own data and code.
Run: python momentum_vectors.py -> momentum_vectors.gif, momentum_vectors_frames.png (Manim; render on topgro)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
K, START, ETA, BETA = 100, np.array([-10.0, 0.4]), 0.01, 0.9
SX, SY, X0 = 1.05, 3.4, -6.2                        # screen units per w1, per w2; screen x of w1 = -10.5 + ...
grad = lambda w: np.array([w[0], K * w[1]])
loss = lambda w: 0.5 * (w[0] ** 2 + K * w[1] ** 2)


def momentum_run(steps=80):
    """Points w_t, old pushes beta*v_{t-1} and gradient steps eta*grad(w_t), so w_{t+1} = w_t - push - gstep."""
    w, v, W, push, gstep = START.copy(), np.zeros(2), [START.copy()], [], []
    for _ in range(steps):
        push.append(BETA * v)
        gstep.append(ETA * grad(w))
        v = BETA * v + ETA * grad(w)
        w = w - v
        W.append(w.copy())
    return np.array(W), np.array(push), np.array(gstep)


W, PUSH, GSTEP = momentum_run()
DONE = int(np.argmax([loss(p) < 0.01 for p in W]))
assert DONE == 59 and np.allclose(W[1:], W[:-1] - PUSH - GSTEP)   # 59 steps, as in the Note's table


def pt(w):
    return np.array([X0 + SX * (w[0] + 10.5), SY * w[1] - 0.4, 0])


def arrow(a, b, colour, width=7):
    return Arrow(pt(a), pt(b), buff=0, color=colour, stroke_width=width, max_tip_length_to_length_ratio=0.25,
                 max_stroke_width_to_length_ratio=12)


class MomentumVectors(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        centre = pt([0, 0])
        rings = VGroup(*[Ellipse(width=2 * SX * np.sqrt(2 * c), height=2 * SY * np.sqrt(2 * c) / 10, color=GREY_C,
                                 stroke_width=1.5, stroke_opacity=0.5).move_to(centre) for c in (0.5, 3, 10, 22, 40, 60)])
        star = Star(5, outer_radius=0.2, color=RED_C, fill_opacity=1).move_to(centre)
        title = Text("momentum: each step = old push + slope now", font_size=34).to_edge(UP, buff=0.25)
        key = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.6, color=c, stroke_width=8), Text(s, font_size=26, color=c))
                       .arrange(RIGHT, buff=0.15) for c, s in ((ORANGE_C, "old velocity × β"),
                                                                (BLUE_C, "− η × gradient now"),
                                                                (GREEN_C, "the step: their sum"))])
        key.arrange(RIGHT, buff=0.6).next_to(title, DOWN, buff=0.25)
        counter = Text("step 1", font_size=30).to_corner(DL, buff=0.3)
        dot = Dot(pt(W[0]), radius=0.09, color=BLACK)
        self.add(rings, star, title, key, counter, dot)
        self.wait(0.5)
        trail = VGroup()
        for t in range(DONE):
            a, mid, b = W[t], W[t] - PUSH[t], W[t + 1]
            slow = t < 6
            o, g, s = arrow(a, mid, ORANGE_C), arrow(mid, b, BLUE_C), arrow(a, b, GREEN_C, 5)
            self.remove(counter)
            counter = Text(f"step {t + 1}", font_size=30).to_corner(DL, buff=0.3)
            self.add(counter)
            note = None
            if t == 2:
                note = Text("across the valley: here they point opposite ways and cancel", font_size=28,
                            color=GREY_C).next_to(key, DOWN, buff=0.3)
            if t == 9:
                note = Text("along the valley: the old push carries the speed", font_size=28,
                            color=GREY_C).next_to(key, DOWN, buff=0.3)
            if slow:
                if np.linalg.norm(PUSH[t]) > 0:
                    self.play(GrowArrow(o), run_time=0.6)
                self.play(GrowArrow(g), run_time=0.6)
                if note:
                    self.play(FadeIn(note), run_time=0.4)
                self.play(GrowArrow(s), run_time=0.5)
                self.wait(0.6 if note else 0.2)
            else:
                self.add(o, g, s)
                if note:
                    self.play(FadeIn(note), run_time=0.4)
                    self.wait(1.2)
                else:
                    self.wait(0.25 if t < 25 else 0.12)
            if t in (2, 9, 20):
                self.snap()
            seg = Line(pt(a), pt(b), color=GREEN_C, stroke_width=3, stroke_opacity=0.6)
            trail.add(seg)
            self.remove(o, g, s)
            if note:
                self.remove(note)
            self.add(trail)
            if slow:
                self.play(dot.animate.move_to(pt(b)), run_time=0.4)
            else:
                dot.move_to(pt(b))
        done = Text(f"loss < 0.01 after {DONE} steps", font_size=30, color=GREEN_C).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(done))
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
                     "output_file": "momentum_vectors", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = MomentumVectors()
        scene.render()
    mp4 = next(media.rglob("momentum_vectors.mp4"))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "momentum_vectors.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "momentum_vectors_frames.png")
    shutil.rmtree(media)
